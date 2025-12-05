# YogaVision AI - Frontend

React-based web application for real-time yoga pose detection and feedback.

**Author:** Priyanshu Pattnaik

---

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

The app will open at [http://localhost:3000](http://localhost:3000)

---

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── DropDown/       # Pose selection dropdown
│   ├── Instructions/   # Pose instructions
│   └── PoseStart/      # Session controls
├── pages/              # Application pages
│   ├── Home/           # Landing page
│   ├── Yoga/           # Main pose detection
│   ├── About/          # About page
│   └── Tutorials/      # Tutorials page
├── utils/              # Utility functions
├── App.js              # Root component
└── index.js            # Entry point
```

---

## Key Technologies

- **React 18** - UI framework
- **TensorFlow.js 4.15** - Machine learning
- **MoveNet** - Pose detection model
- **React Webcam** - Camera integration
- **React Router 6** - Navigation

---

## Available Scripts

### `npm start`
Runs the app in development mode at [http://localhost:3000](http://localhost:3000)

### `npm test`
Launches the test runner in interactive watch mode

### `npm run build`
Builds the app for production to the `build` folder

### `npm run eject`
**Warning:** This is a one-way operation. Ejects from Create React App.

---

## Configuration

### Model URL
Update the model URL in `src/pages/Yoga/Yoga.js`:
```javascript
const poseClassifier = await tf.loadLayersModel('YOUR_MODEL_URL');
```

### Detection Settings
Adjust thresholds in `src/pages/Yoga/Yoga.js`:
```javascript
const POSE_CONFIDENCE_THRESHOLD = 0.97;
const KEYPOINT_CONFIDENCE_THRESHOLD = 0.4;
const DETECTION_INTERVAL = 100; // ms
```

---

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

Requires WebGL support for TensorFlow.js

---

## Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel --prod
```

---

## Troubleshooting

### Webcam Not Working
- Check browser permissions
- Ensure HTTPS (required for camera access)
- Close other apps using the camera

### Model Loading Issues
- Check internet connection
- Verify model URL is accessible
- Clear browser cache

### Performance Issues
- Close unnecessary browser tabs
- Use a device with GPU support
- Reduce detection frequency

---

## Learn More

- [React Documentation](https://react.dev/)
- [TensorFlow.js Guide](https://www.tensorflow.org/js)
- [Create React App Docs](https://create-react-app.dev/)

---

For the complete project documentation, see the main README in the root directory.
