# Contributing to EEG Recorder App

Thank you for your interest in contributing! This project aims to make EEG recording accessible to everyone, and we welcome contributions from developers, neuroscientists, and enthusiasts alike.

## 🎯 Ways to Contribute

### 1. Report Bugs

- Open a [GitHub issue](https://github.com/itayinbarr/eeg-recorder-app/issues)
- Describe the problem clearly
- Include steps to reproduce
- Share your browser/OS/device information

### 2. Suggest Features

- Check existing issues first to avoid duplicates
- Explain the use case and benefits
- Be open to discussion and alternative approaches

### 3. Improve Documentation

- Fix typos or clarify confusing sections
- Add examples or tutorials
- Translate documentation to other languages

### 4. Submit Code

- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Make your changes
- Test thoroughly
- Commit with clear messages
- Push to your fork
- Open a Pull Request

## 🔧 Development Setup

### Web App

```bash
npm install
npm run dev
```

### Python Pipeline

```bash
cd post-recording
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📝 Code Style

### JavaScript/React

- Use ES6+ features
- Prefer functional components with hooks
- Keep components focused and reusable
- Add comments for complex logic

### Python

- Follow PEP 8 style guide
- Use type hints where helpful
- Add docstrings for functions
- Keep functions focused and testable

## 🧪 Testing

Before submitting:

- Test with actual Muse 2 hardware if possible
- Check browser console for errors
- Verify CSV export format
- Test post-processing pipeline with sample data

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome beginners and provide helpful feedback
- Focus on constructive criticism
- Celebrate each other's contributions

## 📚 Areas for Contribution

### High Priority

- Better error handling and user feedback
- Additional visualization options
- Real-time frequency band monitoring
- Mobile browser optimization

### Medium Priority

- Support for Muse S headset
- Additional analysis metrics
- Integration with other tools
- Performance optimizations

### Low Priority

- UI themes and customization
- Internationalization
- Additional export formats
- Advanced filtering options

## 🎓 Learning Resources

### Web Bluetooth

- [Web Bluetooth API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)
- [web-muse library](https://github.com/itayinbarr/web-muse)

### EEG Analysis

- [MNE-Python tutorials](https://mne.tools/stable/auto_tutorials/index.html)
- [AutoReject documentation](https://autoreject.github.io/)

### React

- [React documentation](https://react.dev/)
- [Hooks reference](https://react.dev/reference/react)

## 💬 Questions?

- Open a [GitHub Discussion](https://github.com/itayinbarr/eeg-recorder-app/discussions)
- Comment on existing issues
- Check the [README](README.md) and [QUICKSTART](QUICKSTART.md)

## 📄 License

By contributing, you agree that your contributions will be licensed under the ISC License.

---

Thank you for helping make EEG accessible to everyone! 🧠✨
