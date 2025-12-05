# YogaVision AI

An intelligent yoga pose detection and correction system powered by machine learning and computer vision. Using real-time pose estimation, this application helps users perfect their yoga practice with instant feedback and performance tracking.

**Developed by:** Priyanshu Pattnaik

---

## What Does This Do?

YogaVision AI watches you through your webcam as you practice yoga poses. It uses artificial intelligence to:
- Recognize which yoga pose you're attempting
- Tell you if you're doing it correctly
- Track how long you hold each pose
- Give you visual feedback with a skeleton overlay on your body

Think of it as having a yoga instructor who never gets tired and gives you instant feedback!

---

## Features

- **Real-Time Pose Detection**: Instant recognition of 7 different yoga poses
- **Live Feedback**: Visual skeleton overlay turns green when your pose is correct
- **Performance Tracking**: Monitor your pose hold time and personal best records
- **Audio Cues**: Sound feedback when you achieve the correct pose
- **Webcam Integration**: Works with any standard webcam
- **No Installation Required**: Runs entirely in your web browser

### Supported Yoga Poses

1. Tree Pose (Vrikshasana)
2. Chair Pose (Utkatasana)
3. Cobra Pose (Bhujangasana)
4. Warrior Pose (Virabhadrasana)
5. Downward Dog (Adho Mukha Svanasana)
6. Shoulder Stand (Sarvangasana)
7. Triangle Pose (Trikonasana)

---

## Tech Stack

### Frontend Technologies

- **React 17** - User interface framework
- **TensorFlow.js** - Machine learning in the browser
  - `@tensorflow/tfjs` (v3.10.0) - Core TensorFlow library
  - `@tensorflow-models/pose-detection` (v0.0.6) - Pose estimation models
  - `@tensorflow-models/posenet` (v2.2.2) - Human pose detection
- **React Webcam** (v6.0.0) - Camera access and video streaming
- **React Router DOM** (v6.0.0) - Navigation between pages
- **HTML5 Canvas** - Drawing pose skeleton overlays

### Backend/ML Technologies

- **Python 3.x** - Machine learning model training
- **TensorFlow** - Deep learning framework
- **Keras** - High-level neural network API
- **TensorFlow.js Converter** - Converting models for browser use
- **MoveNet** - Google's pose detection model (Thunder variant)
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation and CSV processing
- **scikit-learn** - Train/test data splitting
- **OpenCV (cv2)** - Image processing

### Model Architecture

- **Input**: 34 normalized pose landmark coordinates
- **Hidden Layers**: 
  - Dense layer (128 neurons, ReLU6 activation)
  - Dropout (50%)
  - Dense layer (64 neurons, ReLU6 activation)
  - Dropout (50%)
- **Output**: 8 classes (7 poses + no pose) with softmax activation
- **Optimizer**: Adam
- **Loss Function**: Categorical crossentropy

---

## Project Structure

```
yogavision-ai/
├── frontend/                      # React web application
│   ├── public/                    # Static assets
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   │   ├── DropDown/          # Pose selection dropdown
│   │   │   ├── Instructions/      # Pose instructions display
│   │   │   └── PoseStart/         # Pose session controls
│   │   ├── pages/                 # Application pages
│   │   │   ├── Home/              # Landing page
│   │   │   ├── Yoga/              # Main pose detection page
│   │   │   ├── About/             # About page
│   │   │   └── Tutorials/         # Tutorial page
│   │   ├── utils/                 # Utility functions
│   │   ├── App.js                 # Main app component
│   │   ├── model.json             # Trained ML model
│   │   └── group1-shard1of1.bin   # Model weights
│   └── package.json
│
├── classification model/          # ML model training pipeline
│   ├── yoga_poses/                # Training dataset
│   │   ├── train/                 # Training images by pose
│   │   └── test/                  # Testing images by pose
│   ├── csv_per_pose/              # Extracted pose landmarks
│   ├── model/                     # Exported TensorFlow.js model
│   ├── data.py                    # Data structures and types
│   ├── movenet.py                 # MoveNet pose detection wrapper
│   ├── preprocessing.py           # Dataset preprocessing
│   ├── training.py                # Model training script
│   ├── train_data.csv             # Processed training data
│   ├── test_data.csv              # Processed test data
│   └── movenet_thunder.tflite     # MoveNet model file
│
└── README.md                      # This file
```

---

## How It Works

### 1. Data Collection & Preprocessing
- Yoga pose images are collected and organized by pose type
- MoveNet Thunder model detects 17 body keypoints in each image
- Keypoints are normalized and saved to CSV files for training

### 2. Model Training
- Pose landmarks are converted to embeddings (34 features)
- Neural network learns to classify poses from these embeddings
- Model achieves high accuracy through dropout regularization
- Trained model is converted to TensorFlow.js format for browser use

### 3. Real-Time Detection
- Webcam captures live video feed
- MoveNet detects body keypoints in each frame (10 FPS)
- Keypoints are normalized and fed to the classifier
- If confidence > 97%, the pose is marked as correct
- Visual and audio feedback provided to the user

---

## Getting Started

### Prerequisites

- **Node.js** (v14 or higher)
- **npm** or **yarn**
- **Python 3.7+** (only for model training)
- **Webcam** (for pose detection)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd yogavision-ai
   ```

2. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Install Python dependencies** (only if training models)
   ```bash
   cd "classification model"
   pip install tensorflow keras tensorflowjs pandas numpy opencv-python scikit-learn tqdm wget
   ```

### Running the Application

1. **Start the development server**
   ```bash
   cd frontend
   npm start
   ```

2. **Open your browser**
   - Navigate to `http://localhost:3000`
   - Allow webcam access when prompted

3. **Start practicing!**
   - Select a yoga pose from the dropdown
   - Click "Start Pose"
   - Follow the reference image and hold the pose
   - Watch the skeleton turn green when you nail it!

---

## Training Your Own Model

If you want to train the model with your own dataset:

1. **Prepare your dataset**
   - Organize images in `classification model/yoga_poses/train/` and `test/`
   - Create folders for each pose class

2. **Preprocess the data**
   ```bash
   cd "classification model"
   python preprocessing.py
   ```

3. **Train the model**
   ```bash
   python training.py
   ```

4. **Copy the model to frontend**
   ```bash
   cp model/model.json ../frontend/src/
   cp model/group1-shard1of1.bin ../frontend/src/
   ```

---

## Configuration

### Adjusting Detection Sensitivity

In `frontend/src/pages/Yoga/Yoga.js`, you can modify:

```javascript
// Confidence threshold for pose classification (default: 0.97)
if(data[0][classNo] > 0.97) {
  // Pose detected as correct
}

// Keypoint visibility threshold (default: 0.4)
if(keypoint.score > 0.4) {
  // Keypoint is visible enough to use
}
```

### Detection Frequency

```javascript
// Detection interval in milliseconds (default: 100ms = 10 FPS)
interval = setInterval(() => { 
    detectPose(detector, poseClassifier, countAudio)
}, 100)
```

---

## Browser Compatibility

- **Chrome** (recommended) - Full support
- **Firefox** - Full support
- **Safari** - Full support
- **Edge** - Full support

**Note**: Requires a modern browser with WebGL support for TensorFlow.js

---

## Performance Tips

- Use good lighting for better pose detection
- Ensure your full body is visible in the webcam frame
- Wear contrasting clothing against your background
- Maintain a stable internet connection for initial model loading
- Close other applications to free up system resources

---

## Known Limitations

- Requires webcam access
- Works best with single person in frame
- Needs clear view of full body
- Performance depends on device capabilities
- Initial model loading may take a few seconds

---

## Future Enhancements

- [ ] Add more yoga poses
- [ ] Multi-person pose detection
- [ ] Pose correction suggestions
- [ ] Progress tracking over time
- [ ] Mobile app version
- [ ] Offline mode support
- [ ] Custom workout routines
- [ ] Social sharing features

---

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

## License

This project is open source and available for educational purposes.

---

## Acknowledgments

- **TensorFlow Team** - For TensorFlow.js and pose detection models
- **Google Research** - For the MoveNet model
- **React Team** - For the React framework
- Yoga community for pose references and inspiration

---

## Contact

**Developer**: Priyanshu Pattnaik

For questions, suggestions, or collaboration opportunities, please open an issue on the repository.

---

## Troubleshooting

### Webcam not working
- Check browser permissions for camera access
- Ensure no other application is using the webcam
- Try refreshing the page

### Model not loading
- Check your internet connection
- Clear browser cache and reload
- Verify model files are in the correct location

### Poor detection accuracy
- Improve lighting conditions
- Ensure full body is visible
- Move closer or farther from camera
- Check that background is not too cluttered

### Performance issues
- Close unnecessary browser tabs
- Reduce detection frequency in code
- Use a device with better GPU support

---

**Made with ❤️ for the yoga community**
