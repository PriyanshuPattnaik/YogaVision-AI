# YogaVision AI - Quick Reference

Fast reference for common tasks and commands.

**Author:** Priyanshu Pattnaik

---

## 🚀 Quick Start

```bash
# Clone and run
git clone <repo-url>
cd yogavision-ai/frontend
npm install
npm start
```

---

## 📦 Installation

### Frontend
```bash
cd frontend
npm install
```

### Python/ML
```bash
cd "classification model"
pip install -r requirements.txt
```

---

## 🎯 Common Commands

### Development
```bash
npm start              # Start dev server
npm test               # Run tests
npm run build          # Build for production
```

### ML Training
```bash
python preprocessing.py    # Extract keypoints
python training.py         # Train model
```

---

## 🔧 Configuration

### Detection Settings (Yoga.js)
```javascript
const DETECTION_INTERVAL = 100;              // Detection frequency (ms)
const POSE_CONFIDENCE_THRESHOLD = 0.97;      // Pose accuracy needed
const KEYPOINT_CONFIDENCE_THRESHOLD = 0.4;   // Keypoint visibility
const MAX_UNDETECTED_KEYPOINTS = 4;          // Max missing points
```

### Training Settings (training.py)
```python
EPOCHS = 200           # Training iterations
BATCH_SIZE = 16        # Samples per batch
TEST_SIZE = 0.15       # Validation split
```

---

## 📁 Project Structure

```
yogavision-ai/
├── frontend/              # React app
│   ├── src/
│   │   ├── pages/        # App pages
│   │   ├── components/   # UI components
│   │   └── utils/        # Helpers
│   └── package.json
│
├── classification model/  # ML pipeline
│   ├── yoga_poses/       # Training data
│   ├── *.py              # Python scripts
│   └── requirements.txt
│
└── README.md             # Main docs
```

---

## 🎨 Supported Poses

1. Tree (Vrikshasana)
2. Chair (Utkatasana)
3. Cobra (Bhujangasana)
4. Warrior (Virabhadrasana)
5. Dog (Adho Mukha Svanasana)
6. Shoulder Stand (Sarvangasana)
7. Triangle (Trikonasana)

---

## 🐛 Quick Fixes

### Webcam not working
```bash
# Check permissions in browser settings
# Close other apps using camera
# Try different browser
```

### Dependencies issues
```bash
# Frontend
rm -rf node_modules package-lock.json
npm install

# Python
pip install --upgrade pip
pip install -r requirements.txt
```

### Model not loading
```bash
# Check internet connection
# Clear browser cache
# Verify model files exist
```

---

## 📊 File Locations

### Model Files
- `frontend/src/model.json`
- `frontend/src/group1-shard1of1.bin`

### Training Data
- `classification model/train_data.csv`
- `classification model/test_data.csv`

### Model Weights
- `classification model/weights.best.hdf5`

---

## 🔗 Important URLs

### Development
- Frontend: `http://localhost:3000`
- React DevTools: Chrome Extension

### Documentation
- Main README: `README.md`
- Setup Guide: `SETUP.md`
- Contributing: `CONTRIBUTING.md`

---

## 💡 Tips

### Performance
- Use Chrome for best performance
- Close unnecessary tabs
- Ensure good lighting
- Keep full body in frame

### Training
- Use 50-100 images per pose
- Ensure variety in angles
- Good lighting in images
- Clear backgrounds

### Development
- Use VS Code with ESLint
- Enable format on save
- Check console for errors
- Test on multiple browsers

---

## 🎓 Learning Resources

### React
- [React Docs](https://react.dev/)
- [React Hooks](https://react.dev/reference/react)

### TensorFlow.js
- [TF.js Guide](https://www.tensorflow.org/js)
- [Pose Detection](https://github.com/tensorflow/tfjs-models/tree/master/pose-detection)

### MoveNet
- [MoveNet Tutorial](https://www.tensorflow.org/hub/tutorials/movenet)

---

## 📝 Code Snippets

### Add New Pose (Frontend)
```javascript
// In Yoga.js
const CLASS_NO = {
  // ... existing poses
  NewPose: 8,
}

const POSE_LIST = [
  // ... existing poses
  'NewPose'
]
```

### Adjust Detection Speed
```javascript
// In Yoga.js
const DETECTION_INTERVAL = 200; // Slower (5 FPS)
const DETECTION_INTERVAL = 50;  // Faster (20 FPS)
```

### Change Confidence Threshold
```javascript
// In Yoga.js
const POSE_CONFIDENCE_THRESHOLD = 0.90; // More lenient
const POSE_CONFIDENCE_THRESHOLD = 0.99; // More strict
```

---

## 🚨 Troubleshooting Checklist

- [ ] Node.js installed? (`node --version`)
- [ ] Dependencies installed? (`npm install`)
- [ ] Webcam working? (Test at webcamtests.com)
- [ ] Browser permissions granted?
- [ ] Using HTTPS? (Required for camera)
- [ ] Model files present?
- [ ] Internet connection active?
- [ ] Console errors checked?

---

## 📞 Getting Help

1. Check documentation files
2. Search existing issues
3. Create new issue with:
   - Clear description
   - Steps to reproduce
   - Error messages
   - Environment details

---

## ⚡ Keyboard Shortcuts

### VS Code
- `Ctrl/Cmd + P` - Quick file open
- `Ctrl/Cmd + Shift + F` - Search in files
- `Ctrl/Cmd + /` - Toggle comment
- `Alt + Shift + F` - Format document

### Browser DevTools
- `F12` - Open DevTools
- `Ctrl/Cmd + Shift + C` - Inspect element
- `Ctrl/Cmd + Shift + J` - Console

---

## 📈 Version Info

- **Current Version:** 1.0.0
- **React:** 18.2.0
- **TensorFlow.js:** 4.15.0
- **Node.js Required:** 14+
- **Python Required:** 3.7+

---

## 🎯 Quick Links

- [Main README](README.md)
- [Setup Guide](SETUP.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE)

---

**Keep this file handy for quick reference!** 📌
