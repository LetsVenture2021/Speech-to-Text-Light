# Speech-to-Text Light

A lightweight hands-free listening companion that transforms incoming content into adaptive speech. It ingests links, files, pasted text, visuals, and real-time voice prompts, then routes each input through an emotion-aware processing loop to produce contextually aligned narration.

## Features

- **Link ingestion**: Fetch URLs and narrate content with tone-aware speech
- **Direct paste reading**: Process pasted text through the Inflective Emergence Loop
- **Document uploads**: Parse PDF, Word, or plain-text files
- **Image uploads**: Use vision to describe images for spoken narration
- **Data file uploads**: Summarize structured data (XLSX, CSV)
- **Real-time speech**: Transcribe live audio and respond with adaptive prosody

## Prerequisites

- Python 3.10+
- OpenAI API key with access to:
  - `gpt-4o-mini` (text/image processing)
  - `gpt-4o-mini-tts` (text-to-speech)
  - `gpt-4o-mini-transcribe` (speech-to-text)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `FLASK_DEBUG` | No | Set to `1` for debug mode (default: `0`) |
| `FLASK_HOST` | No | Host to bind to (default: `127.0.0.1`) |
| `FLASK_PORT` | No | Port to run on (default: `5000`) |

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/LetsVenture2021/Speech-to-Text-Light.git
   cd Speech-to-Text-Light
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser to `http://localhost:5000`

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t speech-to-text-light .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 -e OPENAI_API_KEY="your-api-key-here" speech-to-text-light
   ```

## Project Structure

```
Speech-to-Text-Light/
├── app.py              # Main Flask application with API endpoints
├── public/             # Static web client files
│   ├── index.html      # Main HTML page
│   ├── css/            # Stylesheets
│   │   ├── pv-brand.css
│   │   └── styles.css
│   └── js/
│       └── app.js      # Frontend JavaScript
├── docs/               # Documentation
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── environment.yaml    # Conda environment (alternative)
└── tests/              # Test suite
```

## API Endpoints

### `POST /api/process`
Process text, URLs, or file uploads and return narrated audio.

**Request**: `multipart/form-data`
- `text` (string): Text content or URL
- `file` (file): Optional file upload

**Response**: `audio/mpeg` (MP3 audio)

### `POST /api/voice`
Process recorded audio, transcribe, and return narrated response.

**Request**: `multipart/form-data`
- `audio` (file): Audio recording (webm/wav)

**Response**: `audio/mpeg` (MP3 audio)

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## Security

- URL fetching validates against SSRF attacks (blocks private/local IPs)
- No credentials are stored in code
- See [SECURITY.md](SECURITY.md) for vulnerability reporting

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
