import * as poseDetection from '@tensorflow-models/pose-detection';
import * as tf from '@tensorflow/tfjs';
import React, { useRef, useState, useEffect, useCallback } from 'react';
import '@tensorflow/tfjs-backend-webgl';
import Webcam from 'react-webcam';
import { count } from '../../utils/music'; 
 
import Instructions from '../../components/Instrctions/Instructions';
import './Yoga.css';
 
import DropDown from '../../components/DropDown/DropDown';
import { poseImages } from '../../utils/pose_images';
import { POINTS, keypointConnections } from '../../utils/data';
import { drawPoint, drawSegment } from '../../utils/helper';

// Constants
const POSE_LIST = [
  'Tree', 'Chair', 'Cobra', 'Warrior', 'Dog',
  'Shoulderstand', 'Traingle'
];

const DETECTION_INTERVAL = 100; // ms
const POSE_CONFIDENCE_THRESHOLD = 0.97;
const KEYPOINT_CONFIDENCE_THRESHOLD = 0.4;
const MAX_UNDETECTED_KEYPOINTS = 4;

let skeletonColor = 'rgb(255,255,255)';
let interval;
let flag = false; // Tracks if pose is currently being held correctly


function Yoga() {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);

  const [startingTime, setStartingTime] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [poseTime, setPoseTime] = useState(0);
  const [bestPerform, setBestPerform] = useState(0);
  const [currentPose, setCurrentPose] = useState('Tree');
  const [isStartPose, setIsStartPose] = useState(false);

  
  useEffect(() => {
    const timeDiff = (currentTime - startingTime) / 1000;
    if (flag) {
      setPoseTime(timeDiff);
    }
    if (timeDiff > bestPerform) {
      setBestPerform(timeDiff);
    }
  }, [currentTime, startingTime, bestPerform]);

  useEffect(() => {
    setCurrentTime(0);
    setPoseTime(0);
    setBestPerform(0);
  }, [currentPose]);

  const CLASS_NO = {
    Chair: 0,
    Cobra: 1,
    Dog: 2,
    No_Pose: 3,
    Shoulderstand: 4,
    Traingle: 5,
    Tree: 6,
    Warrior: 7,
  }

  const getCenterPoint = useCallback((landmarks, leftBodypart, rightBodypart) => {
    const left = tf.gather(landmarks, leftBodypart, 1);
    const right = tf.gather(landmarks, rightBodypart, 1);
    const center = tf.add(tf.mul(left, 0.5), tf.mul(right, 0.5));
    return center;
  }, []);

  const getPoseSize = useCallback((landmarks, torsoSizeMultiplier = 2.5) => {
    const hipsCenter = getCenterPoint(landmarks, POINTS.LEFT_HIP, POINTS.RIGHT_HIP);
    const shouldersCenter = getCenterPoint(landmarks, POINTS.LEFT_SHOULDER, POINTS.RIGHT_SHOULDER);
    const torsoSize = tf.norm(tf.sub(shouldersCenter, hipsCenter));
    
    let poseCenterNew = getCenterPoint(landmarks, POINTS.LEFT_HIP, POINTS.RIGHT_HIP);
    poseCenterNew = tf.expandDims(poseCenterNew, 1);
    poseCenterNew = tf.broadcastTo(poseCenterNew, [1, 17, 2]);
    
    const d = tf.gather(tf.sub(landmarks, poseCenterNew), 0, 0);
    const maxDist = tf.max(tf.norm(d, 'euclidean', 0));
    
    const poseSize = tf.maximum(tf.mul(torsoSize, torsoSizeMultiplier), maxDist);
    return poseSize;
  }, [getCenterPoint]);

  const normalizePoseLandmarks = useCallback((landmarks) => {
    let poseCenter = getCenterPoint(landmarks, POINTS.LEFT_HIP, POINTS.RIGHT_HIP);
    poseCenter = tf.expandDims(poseCenter, 1);
    poseCenter = tf.broadcastTo(poseCenter, [1, 17, 2]);
    landmarks = tf.sub(landmarks, poseCenter);

    const poseSize = getPoseSize(landmarks);
    landmarks = tf.div(landmarks, poseSize);
    return landmarks;
  }, [getCenterPoint, getPoseSize]);

  const landmarksToEmbedding = useCallback((landmarks) => {
    const normalizedLandmarks = normalizePoseLandmarks(tf.expandDims(landmarks, 0));
    const embedding = tf.reshape(normalizedLandmarks, [1, 34]);
    return embedding;
  }, [normalizePoseLandmarks]);

  const runMovenet = useCallback(async () => {
    const detectorConfig = { 
      modelType: poseDetection.movenet.modelType.SINGLEPOSE_THUNDER 
    };
    const detector = await poseDetection.createDetector(
      poseDetection.SupportedModels.MoveNet, 
      detectorConfig
    );
    const poseClassifier = await tf.loadLayersModel(
      'https://models.s3.jp-tok.cloud-object-storage.appdomain.cloud/model.json'
    );
    const countAudio = new Audio(count);
    countAudio.loop = true;
    
    interval = setInterval(() => { 
      detectPose(detector, poseClassifier, countAudio);
    }, DETECTION_INTERVAL);
  }, []);

  const detectPose = useCallback(async (detector, poseClassifier, countAudio) => {
    if (
      typeof webcamRef.current !== "undefined" &&
      webcamRef.current !== null &&
      webcamRef.current.video.readyState === 4
    ) {
      let notDetected = 0;
      const video = webcamRef.current.video;
      const pose = await detector.estimatePoses(video);
      const ctx = canvasRef.current.getContext('2d');
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      
      try {
        const keypoints = pose[0].keypoints;
        const input = keypoints.map((keypoint) => {
          if (keypoint.score > KEYPOINT_CONFIDENCE_THRESHOLD) {
            if (!(keypoint.name === 'left_eye' || keypoint.name === 'right_eye')) {
              drawPoint(ctx, keypoint.x, keypoint.y, 8, 'rgb(255,255,255)');
              const connections = keypointConnections[keypoint.name];
              
              try {
                connections.forEach((connection) => {
                  const conName = connection.toUpperCase();
                  drawSegment(
                    ctx, 
                    [keypoint.x, keypoint.y],
                    [keypoints[POINTS[conName]].x, keypoints[POINTS[conName]].y],
                    skeletonColor
                  );
                });
              } catch (err) {
                console.error('Error drawing connections:', err);
              }
            }
          } else {
            notDetected += 1;
          }
          return [keypoint.x, keypoint.y];
        });
        
        if (notDetected > MAX_UNDETECTED_KEYPOINTS) {
          skeletonColor = 'rgb(255,255,255)';
          return;
        }
        
        const processedInput = landmarksToEmbedding(input);
        const classification = poseClassifier.predict(processedInput);

        classification.array().then((data) => {
          const classNo = CLASS_NO[currentPose];
          console.log(`${currentPose} confidence:`, data[0][classNo]);
          
          if (data[0][classNo] > POSE_CONFIDENCE_THRESHOLD) {
            if (!flag) {
              countAudio.play();
              setStartingTime(Date.now());
              flag = true;
            }
            setCurrentTime(Date.now());
            skeletonColor = 'rgb(0,255,0)';
          } else {
            flag = false;
            skeletonColor = 'rgb(255,255,255)';
            countAudio.pause();
            countAudio.currentTime = 0;
          }
        });
      } catch (err) {
        console.error('Error detecting pose:', err);
      }
    }
  }, [currentPose, landmarksToEmbedding]);

  const startYoga = useCallback(() => {
    setIsStartPose(true);
    runMovenet();
  }, [runMovenet]);

  const stopPose = useCallback(() => {
    setIsStartPose(false);
    clearInterval(interval);
  }, []);

  
  if (isStartPose) {
    return (
      <div className="yoga-container">
        <div className="performance-container">
          <div className="pose-performance">
            <h4>Pose Time: {poseTime.toFixed(1)} s</h4>
          </div>
          <div className="pose-performance">
            <h4>Best: {bestPerform.toFixed(1)} s</h4>
          </div>
        </div>
        <div>
          <Webcam 
            width='640px'
            height='480px'
            id="webcam"
            ref={webcamRef}
            style={{
              position: 'absolute',
              left: 120,
              top: 100,
              padding: '0px',
            }}
          />
          <canvas
            ref={canvasRef}
            id="my-canvas"
            width='640px'
            height='480px'
            style={{
              position: 'absolute',
              left: 120,
              top: 100,
              zIndex: 1
            }}
          />
          <div>
            <img 
              src={poseImages[currentPose]}
              className="pose-img"
              alt={`${currentPose} pose reference`}
            />
          </div>
        </div>
        <button
          onClick={stopPose}
          className="secondary-btn"    
        >
          Stop Pose
        </button>
      </div>
    );
  }

  return (
    <div className="yoga-container">
      <DropDown
        poseList={POSE_LIST}
        currentPose={currentPose}
        setCurrentPose={setCurrentPose}
      />
      <Instructions currentPose={currentPose} />
      <button
        onClick={startYoga}
        className="secondary-btn"    
      >
        Start Pose
      </button>
    </div>
  );
}

export default Yoga;