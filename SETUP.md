# YogaVision AI - Setup Guide

Complete setup instructions for getting YogaVision AI running on your machine.

**Author:** Priyanshu Pattnaik

---

## Prerequisites

Before you begin, ensure you have:

- **Node.js** (v14 or higher) - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Python 3.7+** (only for ML training) - [Download](https://www.python.org/)
- **Webcam** (for pose detection)
- **Modern browser** (Chrome, Firefox, Safari, or Edge)

---

## Quick Setup (Frontend Only)

If you just want to run the app without training models:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd yogavision-ai
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Start the Application

```bash
npm start
```

The app will open at `http://localhost:3000`

### 4. Allow Webcam Access

When prompted by your browser, click "Allow" to grant webcam access.

### 5. Start Practicing!

- Select a yoga pose from the dropdown
- Click "Start Pose"
- Follow the reference image
- Hold the pose until the skeleton turns green

---

## Full Setup (With ML Training)

If you want to train your own models:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd yogavision-ai
```

### 2. Setup Python Environment

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
cd "classification model"
pip install -r requirements.txt
```

### 3. Prepare Training Data

Organize your yoga pose images:

```
classification model/yoga_poses/
├── train/
│   ├── chair/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── cobra/
│   ├── dog/
│   └── ...
└── test/
    ├── chair/
    ├── cobra/
    └── ...
```

### 4. Preprocess Images

```bash
python preprocessing.py
```

This will:
- Download MoveNet model (~50MB)
- Extract keypoints from all images
- Create CSV files with landmark data
- Takes 5-10 minutes depending on dataset size

### 5. Train the Model

```bash
python training.py
```

This will:
- Train the neural network
- Save best weights
- Export to TensorFlow.js format
- Takes 10-30 minutes depending on hardware

### 6. Copy Model to Frontend

```bash
# From classification model directory
cp model/model.json ../frontend/src/
cp model/group1-shard1of1.bin ../frontend/src/
```

### 7. Setup Frontend

```bash
cd ../frontend
npm install
npm start
```

---

## Verification Steps

### Check Node.js Installation

```bash
node --version  # Should show v14 or higher
npm --version   # Should show 6 or higher
```

### Check Python Installation

```bash
python --version  # Should show 3.7 or higher
pip --version     # Should be available
```

### Check Webcam

- Open your browser
- Go to `https://webcamtests.com/`
- Verify your webcam works

---

## Common Issues

### Issue: "npm: command not found"

**Solution:** Install Node.js from [nodejs.org](https://nodejs.org/)

### Issue: "python: command not found"

**Solution:** Install Python from [python.org](https://www.python.org/)

### Issue: Webcam not working

**Solutions:**
- Check browser permissions (Settings → Privacy → Camera)
- Close other apps using the webcam
- Try a different browser
- Ensure you're using HTTPS (required for camera access)

### Issue: "Module not found" errors

**Solution:**
```bash
# For frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# For Python
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Model loading fails

**Solutions:**
- Check internet connection
- Verify model files exist in `frontend/src/`
- Clear browser cache
- Check browser console for errors

### Issue: Low FPS / Laggy detection

**Solutions:**
- Close unnecessary browser tabs
- Use Chrome (best performance)
- Reduce detection frequency in code
- Use a device with better GPU

---

## Development Setup

### Frontend Development

```bash
cd frontend
npm start          # Start dev server
npm test           # Run tests
npm run build      # Build for production
```

### Python Development

```bash
cd "classification model"
python preprocessing.py  # Preprocess data
python training.py       # Train model
```

---

## Environment Variables

Create `.env` file in frontend directory (optional):

```env
REACT_APP_MODEL_URL=https://your-model-url.com/model.json
REACT_APP_API_URL=https://your-api-url.com
```

---

## IDE Setup

### VS Code (Recommended)

Install these extensions:
- ESLint
- Prettier
- Python
- Pylance

### Settings

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

---

## Docker Setup (Optional)

### Frontend

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
EXPOSE 3000
CMD ["npm", "start"]
```

### Build and Run

```bash
docker build -t yogavision-ai .
docker run -p 3000:3000 yogavision-ai
```

---

## Testing

### Frontend Tests

```bash
cd frontend
npm test
```

### Manual Testing Checklist

- [ ] App loads without errors
- [ ] Webcam access works
- [ ] Can select different poses
- [ ] Pose detection works
- [ ] Timer updates correctly
- [ ] Skeleton overlay displays
- [ ] Audio feedback plays
- [ ] Navigation works

---

## Deployment

### Deploy to Netlify

```bash
cd frontend
npm run build
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

### Deploy to Vercel

```bash
cd frontend
npm run build
npm install -g vercel
vercel --prod
```

### Deploy to GitHub Pages

```bash
cd frontend
npm install --save-dev gh-pages

# Add to package.json:
# "homepage": "https://yourusername.github.io/yogavision-ai"
# "predeploy": "npm run build"
# "deploy": "gh-pages -d build"

npm run deploy
```

---

## Next Steps

1. Read the main [README.md](README.md) for project overview
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
3. Review [CHANGELOG.md](CHANGELOG.md) for version history
4. Explore the code and customize as needed

---

## Getting Help

- **Issues:** Open an issue on GitHub
- **Questions:** Check existing issues or create a new one
- **Documentation:** See README files in each directory

---

**Happy coding! 🚀**
