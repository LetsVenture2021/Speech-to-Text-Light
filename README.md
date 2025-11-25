# Speech-to-Text Light

[![CI Status](https://github.com/LetsVenture2021/Speech-to-Text-Light/workflows/Python%20Package%20using%20Conda/badge.svg)](https://github.com/LetsVenture2021/Speech-to-Text-Light/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/LetsVenture2021/Speech-to-Text-Light)](LICENSE)

An intelligent, voice-first content reader that transforms any form of digital content—text, documents, images, data files, URLs, and spoken queries—into adaptive, emotionally-aligned audio narration.

## ✨ Features

- 🎤 **Voice Input**: Real-time speech recognition with auto-silence detection
- 📄 **Multi-Format Support**: PDF, Word, Excel, CSV, images, plain text
- 🌐 **URL Processing**: Fetch and narrate web content
- 🎨 **Image Description**: AI-powered visual content narration
- 🧠 **Smart Processing**: Emotion-aware content analysis with adaptive prosody
- 🔊 **High-Quality TTS**: Natural-sounding voice narration
- 🎯 **Zero Friction**: Hands-free, voice-first experience

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LetsVenture2021/Speech-to-Text-Light.git
   cd Speech-to-Text-Light
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Linux/Mac
   export OPENAI_API_KEY="your-api-key-here"
   
   # Windows
   set OPENAI_API_KEY=your-api-key-here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🐳 Docker Quick Start

```bash
# Build the image
docker build -t speech-to-text-light .

# Run the container
docker run -p 5000:5000 -e OPENAI_API_KEY=your-key speech-to-text-light
```

## 📖 Documentation

- **[Product Brief](docs/PRODUCT_BRIEF.md)** - Comprehensive product documentation
- **[Launch Readiness](docs/LAUNCH_READINESS.md)** - Deployment guide and assessment
- **[Automation Opportunities](docs/AUTOMATION_OPPORTUNITIES.md)** - CI/CD and automation guide
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute (includes Git tutorial)
- **[Security Policy](SECURITY.md)** - Security guidelines

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional)
pre-commit install

# Run tests
pytest tests/

# Run with code coverage
pytest --cov=. --cov-report=html
```

### Project Structure

```
Speech-to-Text-Light/
├── app.py                 # Main Flask application
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── Procfile              # Production server configuration
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_app.py       # Application tests
└── docs/                 # Documentation
    ├── README.md
    ├── PRODUCT_BRIEF.md
    ├── LAUNCH_READINESS.md
    └── AUTOMATION_OPPORTUNITIES.md
```

## 🚢 Deployment

### Heroku (Recommended for MVP)

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Open app
heroku open
```

### Other Platforms

See the [Launch Readiness Guide](docs/LAUNCH_READINESS.md) for deployment instructions for:
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service
- Docker
- Traditional VPS

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_app.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=term-missing
```

## 🔒 Security

- SSRF protection with DNS rebinding mitigation
- Input validation and sanitization
- Secure API key management
- See [SECURITY.md](SECURITY.md) for details

## 💰 Cost Considerations

- OpenAI API usage is pay-per-use
- Estimated cost: $0.001-0.02 per request
- See [Product Brief](docs/PRODUCT_BRIEF.md) for detailed cost analysis

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for:
- Git workflow and best practices
- Code style guidelines
- Pull request process
- Troubleshooting tips

## 📝 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- Built with [OpenAI API](https://openai.com/)
- Powered by [Flask](https://flask.palletsprojects.com/)
- UI inspired by modern minimalist design principles

## 📊 Status

✅ **Launch Ready** - Functionally complete and ready for deployment

See [Launch Readiness Assessment](docs/LAUNCH_READINESS.md) for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/LetsVenture2021/Speech-to-Text-Light/issues)
- **Discussions**: [GitHub Discussions](https://github.com/LetsVenture2021/Speech-to-Text-Light/discussions)

---

Made with ❤️ by the LetsVenture2021 team
