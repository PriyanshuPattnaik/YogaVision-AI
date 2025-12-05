# Contributing to YogaVision AI

Thank you for your interest in contributing to YogaVision AI! This document provides guidelines for contributing to the project.

**Project Author:** Priyanshu Pattnaik

---

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Your environment (OS, browser, Node version)

### Suggesting Features

Feature suggestions are welcome! Please:
- Check if the feature has already been requested
- Clearly describe the feature and its benefits
- Provide examples of how it would work

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Ensure the app runs without errors
   - Test on different browsers if possible
   - Verify pose detection still works

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe what you changed and why
   - Reference any related issues

---

## Development Setup

### Frontend Development

```bash
cd frontend
npm install
npm start
```

### Python/ML Development

```bash
cd "classification model"
pip install -r requirements.txt
python preprocessing.py
python training.py
```

---

## Code Style Guidelines

### JavaScript/React
- Use functional components with hooks
- Use camelCase for variables and functions
- Add JSDoc comments for functions
- Keep components focused and reusable
- Use meaningful variable names

### Python
- Follow PEP 8 style guide
- Use snake_case for variables and functions
- Add docstrings for classes and functions
- Keep functions focused on single tasks
- Use type hints where appropriate

---

## Areas for Contribution

- **New Yoga Poses**: Add support for more poses
- **UI/UX Improvements**: Enhance the user interface
- **Performance Optimization**: Improve detection speed
- **Mobile Support**: Better mobile experience
- **Documentation**: Improve guides and tutorials
- **Testing**: Add unit and integration tests
- **Accessibility**: Improve accessibility features
- **Internationalization**: Add multi-language support

---

## Questions?

Feel free to open an issue for any questions about contributing!

---

**Thank you for helping make YogaVision AI better!** 🙏
