# 🤝 Contributing to Multimodal Video Transcriber

Thank you for your interest in contributing to the Multimodal Video Transcriber! This project is open source and we welcome contributions from the community.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/your-username/multimodal-video-transcriber.git`
3. **Create a feature branch**: `git checkout -b feature/amazing-feature`
4. **Make your changes**
5. **Test your changes**: `python test_local.py`
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to your fork**: `git push origin feature/amazing-feature`
8. **Create a Pull Request**

## 🧪 Testing

Before submitting your changes, please ensure:

- [ ] All tests pass: `python test_local.py`
- [ ] Code follows PEP 8 style guidelines
- [ ] New features include appropriate tests
- [ ] Documentation is updated

## 📝 Code Style

We use:
- **Python 3.9+** with type hints
- **PEP 8** style guidelines
- **Black** for code formatting
- **Flake8** for linting

## 🏗️ Project Structure

```
multimodal-video-transcriber/
├── app.py                 # Streamlit web interface
├── config.py             # Configuration management
├── models.py             # Pydantic data models
├── transcriber.py        # Core transcription logic
├── visualizer.py         # Results visualization
├── main.py               # CLI interface
├── example.py            # Usage examples
├── test_local.py         # Local testing script
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── DEPLOYMENT.md         # Deployment guide
├── LOCAL_TESTING.md      # Local testing guide
└── .github/workflows/    # CI/CD workflows
```

## 🎯 Areas for Contribution

### High Priority
- [ ] **Performance optimization** for long videos
- [ ] **Additional language support** for speaker identification
- [ ] **Batch processing** for multiple videos
- [ ] **Advanced analytics** and insights

### Medium Priority
- [ ] **Additional export formats** (SRT, VTT, etc.)
- [ ] **Custom prompt templates**
- [ ] **Video preprocessing** options
- [ ] **Caching** for repeated transcriptions

### Low Priority
- [ ] **UI improvements** and themes
- [ ] **Additional deployment platforms**
- [ ] **Documentation** improvements
- [ ] **Example notebooks** for advanced usage

## 🔧 Development Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**:
   ```bash
   cp test_env.txt .env
   # Edit .env with your API key
   ```

3. **Run tests**:
   ```bash
   python test_local.py
   ```

4. **Start development server**:
   ```bash
   streamlit run app.py
   ```

## 🐛 Bug Reports

When reporting bugs, please include:

- **Environment**: OS, Python version, package versions
- **Steps to reproduce**: Clear, step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full error traceback
- **Sample video**: If applicable, a public video URL

## 💡 Feature Requests

When requesting features, please include:

- **Use case**: Why this feature is needed
- **Proposed solution**: How you envision it working
- **Alternatives considered**: Other approaches you've thought about
- **Mockups**: If applicable, UI mockups or examples

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] **Tests pass**: All existing and new tests
- [ ] **Code style**: Follows project conventions
- [ ] **Documentation**: Updated README, docstrings, etc.
- [ ] **No secrets**: No API keys or sensitive data
- [ ] **Descriptive title**: Clear, concise PR title
- [ ] **Detailed description**: Explains what and why
- [ ] **Screenshots**: If UI changes are involved

## 🎉 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

## 📞 Questions?

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: For private or sensitive matters

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to the Multimodal Video Transcriber! 🎬
