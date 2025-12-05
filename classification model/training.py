"""
YogaVision AI - Model Training Script
Author: Priyanshu Pattnaik
Description: Trains a neural network to classify yoga poses from body keypoints
"""

import csv
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from data import BodyPart 
import tensorflow as tf
import tensorflowjs as tfjs

# Configuration
TFJS_MODEL_DIR = 'model'
TRAIN_DATA_PATH = 'train_data.csv'
TEST_DATA_PATH = 'test_data.csv'
CHECKPOINT_PATH = "weights.best.hdf5"
EPOCHS = 200
BATCH_SIZE = 16
TEST_SIZE = 0.15
RANDOM_STATE = 42


def load_csv(csv_path):
    """
    Load and preprocess CSV data for training.
    
    Args:
        csv_path (str): Path to the CSV file containing pose landmarks
        
    Returns:
        tuple: (X, y, classes) - Features, labels, and class names
    """
    df = pd.read_csv(csv_path)
    df.drop(['filename'], axis=1, inplace=True)
    classes = df.pop('class_name').unique()
    y = df.pop('class_no')
    
    X = df.astype('float64')
    y = keras.utils.to_categorical(y)
    
    return X, y, classes


def get_center_point(landmarks, left_bodypart, right_bodypart):
    """
    Calculate the center point between two body landmarks.
    
    Args:
        landmarks: Tensor of body keypoints
        left_bodypart: Left body part enum
        right_bodypart: Right body part enum
        
    Returns:
        Tensor: Center point coordinates
    """
    left = tf.gather(landmarks, left_bodypart.value, axis=1)
    right = tf.gather(landmarks, right_bodypart.value, axis=1)
    center = left * 0.5 + right * 0.5
    return center


def get_pose_size(landmarks, torso_size_multiplier=2.5):
    """
    Calculate pose size for normalization.
    
    Returns the maximum of:
    - Torso size multiplied by torso_size_multiplier
    - Maximum distance from pose center to any landmark
    
    Args:
        landmarks: Tensor of body keypoints
        torso_size_multiplier: Scaling factor for torso size
        
    Returns:
        Tensor: Normalized pose size
    """
    hips_center = get_center_point(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP)
    shoulders_center = get_center_point(landmarks, BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER)
    
    torso_size = tf.linalg.norm(shoulders_center - hips_center)
    pose_center_new = get_center_point(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP)
    pose_center_new = tf.expand_dims(pose_center_new, axis=1)
    pose_center_new = tf.broadcast_to(pose_center_new, [tf.size(landmarks) // (17*2), 17, 2])

    d = tf.gather(landmarks - pose_center_new, 0, axis=0, name="dist_to_pose_center")
    max_dist = tf.reduce_max(tf.linalg.norm(d, axis=0))

    pose_size = tf.maximum(torso_size * torso_size_multiplier, max_dist)
    return pose_size


def normalize_pose_landmarks(landmarks):
    """
    Normalize landmarks by centering at (0,0) and scaling to constant size.
    
    Args:
        landmarks: Tensor of body keypoints
        
    Returns:
        Tensor: Normalized landmarks
    """
    pose_center = get_center_point(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP)
    pose_center = tf.expand_dims(pose_center, axis=1)
    pose_center = tf.broadcast_to(pose_center, [tf.size(landmarks) // (17*2), 17, 2])
    landmarks = landmarks - pose_center

    pose_size = get_pose_size(landmarks)
    landmarks /= pose_size
    return landmarks


def landmarks_to_embedding(landmarks_and_scores):
    """
    Convert input landmarks into a pose embedding vector.
    
    Args:
        landmarks_and_scores: Flat tensor of landmarks with scores
        
    Returns:
        Tensor: Flattened embedding vector (34 features)
    """
    reshaped_inputs = keras.layers.Reshape((17, 3))(landmarks_and_scores)
    landmarks = normalize_pose_landmarks(reshaped_inputs[:, :, :2])
    embedding = keras.layers.Flatten()(landmarks)
    return embedding


def preprocess_data(X_data):
    """
    Preprocess dataset by converting landmarks to embeddings.
    
    Args:
        X_data: DataFrame of raw landmark coordinates
        
    Returns:
        Tensor: Processed embeddings ready for training
    """
    processed_data = []
    for i in range(X_data.shape[0]):
        embedding = landmarks_to_embedding(
            tf.reshape(tf.convert_to_tensor(X_data.iloc[i]), (1, 51))
        )
        processed_data.append(tf.reshape(embedding, (34)))
    return tf.convert_to_tensor(processed_data)


def build_model(num_classes):
    """
    Build the neural network architecture for pose classification.
    
    Args:
        num_classes: Number of output classes
        
    Returns:
        keras.Model: Compiled model ready for training
    """
    inputs = tf.keras.Input(shape=(34,), name='pose_embedding')
    
    x = keras.layers.Dense(128, activation=tf.nn.relu6, name='dense_1')(inputs)
    x = keras.layers.Dropout(0.5, name='dropout_1')(x)
    x = keras.layers.Dense(64, activation=tf.nn.relu6, name='dense_2')(x)
    x = keras.layers.Dropout(0.5, name='dropout_2')(x)
    outputs = keras.layers.Dense(num_classes, activation='softmax', name='output')(x)
    
    model = keras.Model(inputs, outputs, name='yoga_pose_classifier')
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def main():
    """Main training pipeline."""
    print('=' * 60)
    print('YogaVision AI - Model Training')
    print('Author: Priyanshu Pattnaik')
    print('=' * 60)
    
    # Load data
    print('\n[1/5] Loading training data...')
    X, y, class_names = load_csv(TRAIN_DATA_PATH)
    print(f'Loaded {len(X)} training samples with {len(class_names)} classes')
    print(f'Classes: {", ".join(class_names)}')
    
    # Split data
    print('\n[2/5] Splitting data into train and validation sets...')
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    print(f'Training samples: {len(X_train)}')
    print(f'Validation samples: {len(X_val)}')
    
    # Load test data
    print('\n[3/5] Loading test data...')
    X_test, y_test, _ = load_csv(TEST_DATA_PATH)
    print(f'Test samples: {len(X_test)}')
    
    # Preprocess data
    print('\n[4/5] Preprocessing data (normalizing landmarks)...')
    processed_X_train = preprocess_data(X_train)
    processed_X_val = preprocess_data(X_val)
    processed_X_test = preprocess_data(X_test)
    print('Preprocessing complete!')
    
    # Build model
    print('\n[5/5] Building and training model...')
    model = build_model(len(class_names))
    model.summary()
    
    # Setup callbacks
    checkpoint = keras.callbacks.ModelCheckpoint(
        CHECKPOINT_PATH,
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        mode='max'
    )
    
    earlystopping = keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=20,
        verbose=1,
        restore_best_weights=True
    )
    
    # Train model
    print('\n' + '=' * 60)
    print('TRAINING STARTED')
    print('=' * 60)
    
    history = model.fit(
        processed_X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(processed_X_val, y_val),
        callbacks=[checkpoint, earlystopping],
        verbose=1
    )
    
    # Evaluate model
    print('\n' + '=' * 60)
    print('EVALUATION ON TEST SET')
    print('=' * 60)
    
    loss, accuracy = model.evaluate(processed_X_test, y_test, verbose=0)
    print(f'Test Loss: {loss:.4f}')
    print(f'Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)')
    
    # Save model for TensorFlow.js
    print('\n' + '=' * 60)
    print('SAVING MODEL')
    print('=' * 60)
    
    tfjs.converters.save_keras_model(model, TFJS_MODEL_DIR)
    print(f'TensorFlow.js model saved to: {TFJS_MODEL_DIR}')
    print('\nTraining complete! 🎉')
    print('=' * 60)


if __name__ == '__main__':
    main()
