"""
YogaVision AI - Data Preprocessing Script
Author: Priyanshu Pattnaik
Description: Extracts pose keypoints from images using MoveNet for model training
"""

import tensorflow as tf
import numpy as np
import pandas as pd 
import os
from movenet import Movenet
import wget
import csv
import tqdm 
from data import BodyPart

# Configuration
MOVENET_MODEL_URL = 'https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/float16/4?lite-format=tflite'
MOVENET_MODEL_NAME = 'movenet_thunder.tflite'
DETECTION_THRESHOLD = 0.1
INFERENCE_COUNT = 3

# Download MoveNet model if not present
if MOVENET_MODEL_NAME not in os.listdir():
    print(f'Downloading MoveNet model from TensorFlow Hub...')
    wget.download(MOVENET_MODEL_URL, MOVENET_MODEL_NAME)
    print('\nModel downloaded successfully!')

movenet = Movenet('movenet_thunder')

def detect(input_tensor, inference_count=INFERENCE_COUNT):
    """
    Detect pose keypoints in an image using MoveNet.
    
    Args:
        input_tensor: Image tensor
        inference_count: Number of inference iterations for better accuracy
        
    Returns:
        Person: Detected person with keypoints
    """
    movenet.detect(input_tensor.numpy(), reset_crop_region=True)
    
    for _ in range(inference_count - 1):
        detection = movenet.detect(input_tensor.numpy(), reset_crop_region=False)
    
    return detection

class Preprocessor:
    """
    Preprocesses yoga pose images by extracting keypoints and saving to CSV.
    
    This class processes images of yoga poses, detects body keypoints using MoveNet,
    and saves the landmark coordinates to CSV files for model training.
    """
    
    def __init__(self, images_in_folder, csvs_out_path):
        """
        Initialize the preprocessor.
        
        Args:
            images_in_folder (str): Path to folder containing pose class subfolders
            csvs_out_path (str): Path for the output CSV file
        """
        self._images_in_folder = images_in_folder
        self._csvs_out_path = csvs_out_path
        self._csvs_out_folder_per_class = 'csv_per_pose'
        self._messages = []
        
        if self._csvs_out_folder_per_class not in os.listdir():
            os.makedirs(self._csvs_out_folder_per_class)
        
        self._pose_class_names = sorted([n for n in os.listdir(images_in_folder)])
    

    
    def process(self, detection_threshold=DETECTION_THRESHOLD):
        """
        Process all images and extract pose keypoints.
        
        Args:
            detection_threshold (float): Minimum confidence score for keypoints
        """
        print('=' * 60)
        print('Starting preprocessing...')
        print('=' * 60)
        
        for pose_class_name in self._pose_class_names:
            print(f'\nProcessing class: {pose_class_name}')
            
            images_in_folder = os.path.join(self._images_in_folder, pose_class_name)
            csv_out_path = os.path.join(
                self._csvs_out_folder_per_class,
                f'{pose_class_name}.csv'
            )
            
            with open(csv_out_path, 'w', newline='') as csv_out_file:
                csv_out_writer = csv.writer(
                    csv_out_file,
                    delimiter=',',
                    quoting=csv.QUOTE_MINIMAL
                )
                
                image_names = sorted([n for n in os.listdir(images_in_folder)])
                valid_image_count = 0
                
                for image_name in tqdm.tqdm(image_names, desc=f'{pose_class_name}'):
                    image_path = os.path.join(images_in_folder, image_name)
                    
                    try:
                        image = tf.io.read_file(image_path)
                        image = tf.io.decode_jpeg(image)
                    except Exception as e:
                        self._messages.append(f'Skipped {image_path}: Invalid image - {str(e)}')
                        continue
                    
                    if image.shape[2] != 3:
                        self._messages.append(f'Skipped {image_path}: Not RGB format')
                        continue
                    
                    person = detect(image)
                    
                    min_landmark_score = min([kp.score for kp in person.keypoints])
                    if min_landmark_score < detection_threshold:
                        self._messages.append(
                            f'Skipped {image_path}: Low confidence ({min_landmark_score:.2f})'
                        )
                        continue
                    
                    valid_image_count += 1
                    
                    pose_landmarks = np.array(
                        [[kp.coordinate.x, kp.coordinate.y, kp.score]
                         for kp in person.keypoints],
                        dtype=np.float32
                    )
                    
                    coord = pose_landmarks.flatten().astype(str).tolist()
                    csv_out_writer.writerow([image_name] + coord)
                
                print(f'  Valid images: {valid_image_count}/{len(image_names)}')
        
        if self._messages:
            print('\nWarnings:')
            for msg in self._messages[:10]:  # Show first 10 warnings
                print(f'  - {msg}')
            if len(self._messages) > 10:
                print(f'  ... and {len(self._messages) - 10} more')
        
        print('\nCombining all CSV files...')
        all_landmarks_df = self.all_landmarks_as_dataframe()
        all_landmarks_df.to_csv(self._csvs_out_path, index=False)
        print(f'Saved combined data to: {self._csvs_out_path}')
        print('Preprocessing complete! ✓')

    
    def class_names(self):
        """Get list of pose class names."""
        return self._pose_class_names
    
    def all_landmarks_as_dataframe(self):
        """
        Merge all per-class CSV files into a single DataFrame.
        
        Returns:
            pd.DataFrame: Combined dataset with proper column names
        """
        total_df = None
        
        for class_index, class_name in enumerate(self._pose_class_names):
            csv_out_path = os.path.join(
                self._csvs_out_folder_per_class,
                f'{class_name}.csv'
            )
            per_class_df = pd.read_csv(csv_out_path, header=None)
            
            per_class_df['class_no'] = class_index
            per_class_df['class_name'] = class_name
            per_class_df[per_class_df.columns[0]] = f'{class_name}/' + per_class_df[per_class_df.columns[0]]
            
            if total_df is None:
                total_df = per_class_df
            else:
                total_df = pd.concat([total_df, per_class_df], axis=0)
        
        # Create proper column names
        header_name = ['filename']
        for bodypart in BodyPart:
            header_name.extend([
                f'{bodypart.name}_x',
                f'{bodypart.name}_y',
                f'{bodypart.name}_score'
            ])
        
        header_map = {total_df.columns[i]: header_name[i] for i in range(len(header_name))}
        total_df.rename(header_map, axis=1, inplace=True)
        
        return total_df


def main():
    """Main preprocessing pipeline."""
    print('=' * 60)
    print('YogaVision AI - Data Preprocessing')
    print('Author: Priyanshu Pattnaik')
    print('=' * 60)
    
    # Preprocess training data
    print('\n[1/2] Processing training data...')
    train_preprocessor = Preprocessor(
        images_in_folder=os.path.join('yoga_poses', 'train'),
        csvs_out_path='train_data.csv'
    )
    train_preprocessor.process()
    
    # Preprocess testing data
    print('\n[2/2] Processing test data...')
    test_preprocessor = Preprocessor(
        images_in_folder=os.path.join('yoga_poses', 'test'),
        csvs_out_path='test_data.csv'
    )
    test_preprocessor.process()
    
    print('\n' + '=' * 60)
    print('All preprocessing complete! 🎉')
    print('=' * 60)


if __name__ == '__main__':
    main()
            
            
                        