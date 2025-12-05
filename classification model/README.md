# YogaVision AI - Machine Learning Model

Neural network for classifying yoga poses from body keypoints.

**Author:** Priyanshu Pattnaik

---

## Overview

This directory contains the machine learning pipeline for training a yoga pose classifier. The model uses MoveNet for pose detection and a custom neural network for classification.

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Dataset

Organize your images in this structure:
```
yoga_poses/
├── train/
│   ├── chair/
│   ├── cobra/
│   ├── dog/
│   ├── tree/
│   └── ...
└── test/
    ├── chair/
    ├── cobra/
    └── ...
```

### 3. Preprocess Data

```bash
python preprocessing.py
```

This will:
- Download MoveNet model (if needed)
- Extract keypoints from all images
- Save landmarks to CSV files
- Create `train_data.csv` and `test_data.csv`

### 4. Train Model

```bash
python training.py
```

This will:
- Load and preprocess the data
- Build the neural network
- Train for up to 200 epochs
- Save the best model weights
- Export to TensorFlow.js format

### 5. Deploy Model

Copy the trained model to the frontend:
```bash
cp model/model.json ../frontend/src/
cp model/group1-shard1of1.bin ../frontend/src/
```

---

## Model Architecture

### Input
- 34 features (17 keypoints × 2 coordinates)
- Normalized pose landmarks

### Network Layers
```
Input (34) 
    ↓
Dense (128, ReLU6) 
    ↓
Dropout (50%)
    ↓
Dense (64, ReLU6)
    ↓
Dropout (50%)
    ↓
Dense (8, Softmax)
```

### Output
- 8 classes (7 poses + no pose)
- Softmax probabilities

---

## Supported Poses

1. **Chair** (Utkatasana)
2. **Cobra** (Bhujangasana)
3. **Dog** (Adho Mukha Svanasana)
4. **Shoulder Stand** (Sarvangasana)
5. **Triangle** (Trikonasana)
6. **Tree** (Vrikshasana)
7. **Warrior** (Virabhadrasana)
8. **No Pose** (Background/Invalid)

---

## Files Description

### Core Scripts

- **`preprocessing.py`** - Extract keypoints from images
- **`training.py`** - Train the classification model
- **`data.py`** - Data structures and types (from TensorFlow)
- **`movenet.py`** - MoveNet wrapper (from TensorFlow)

### Data Files

- **`train_data.csv`** - Processed training data
- **`test_data.csv`** - Processed test data
- **`csv_per_pose/`** - Individual CSV files per pose class
- **`weights.best.hdf5`** - Best model checkpoint

### Model Files

- **`model/model.json`** - TensorFlow.js model architecture
- **`model/group1-shard1of1.bin`** - Model weights
- **`movenet_thunder.tflite`** - MoveNet pose detection model

---

## Training Configuration

Edit these constants in `training.py`:

```python
EPOCHS = 200              # Maximum training epochs
BATCH_SIZE = 16           # Batch size
TEST_SIZE = 0.15          # Validation split (15%)
RANDOM_STATE = 42         # Random seed
```

---

## Preprocessing Configuration

Edit these constants in `preprocessing.py`:

```python
DETECTION_THRESHOLD = 0.1  # Minimum keypoint confidence
INFERENCE_COUNT = 3        # Number of detection passes
```

---

## Adding New Poses

1. **Collect Images**
   - Gather 50-100 images per pose
   - Ensure variety in angles and people
   - Use good lighting and clear backgrounds

2. **Organize Dataset**
   ```
   yoga_poses/train/new_pose_name/
   yoga_poses/test/new_pose_name/
   ```

3. **Update Code**
   - Add pose to `CLASS_NO` dict in frontend
   - Update pose list in frontend components
   - Add reference image

4. **Retrain**
   ```bash
   python preprocessing.py
   python training.py
   ```

---

## Model Performance

### Metrics
- **Training Accuracy**: ~95%+
- **Validation Accuracy**: ~90%+
- **Test Accuracy**: ~85%+

### Optimization
- Early stopping (patience: 20 epochs)
- Dropout regularization (50%)
- Adam optimizer
- Categorical crossentropy loss

---

## Troubleshooting

### Low Accuracy
- Collect more training data
- Ensure image quality is good
- Check for class imbalance
- Adjust detection threshold

### Memory Issues
- Reduce batch size
- Process fewer images at once
- Use CPU instead of GPU

### Slow Training
- Use GPU if available
- Reduce number of epochs
- Increase batch size

---

## Technical Details

### Pose Normalization

The model normalizes poses by:
1. Centering at hip midpoint
2. Scaling to constant size
3. Removing translation/scale variance

This makes the model robust to:
- Different body sizes
- Camera distances
- Image resolutions

### Keypoint Detection

MoveNet Thunder detects 17 body keypoints:
- Nose, Eyes, Ears
- Shoulders, Elbows, Wrists
- Hips, Knees, Ankles

Each keypoint has:
- X coordinate
- Y coordinate
- Confidence score

---

## Dependencies

See `requirements.txt` for full list:
- TensorFlow >= 2.13.0
- Keras >= 2.13.0
- TensorFlow.js >= 4.11.0
- NumPy >= 1.24.0
- Pandas >= 2.0.0
- OpenCV >= 4.8.0
- scikit-learn >= 1.3.0

---

## References

- [MoveNet Documentation](https://www.tensorflow.org/hub/tutorials/movenet)
- [TensorFlow.js Converter](https://www.tensorflow.org/js/guide/conversion)
- [Pose Classification Guide](https://www.tensorflow.org/lite/tutorials/pose_classification)

---

For complete project documentation, see the main README in the root directory.
