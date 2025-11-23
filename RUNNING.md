# Running the Inflective TTS Application

This guide will help you get the Speech-to-Text Light (Inflective TTS) application up and running.

## Prerequisites

- Python 3.10 or higher
- OpenAI API key

## Installation

### Option 1: Using pip

1. Clone the repository:
```bash
git clone https://github.com/LetsVenture2021/Speech-to-Text-Light.git
cd Speech-to-Text-Light
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Using Conda

1. Clone the repository:
```bash
git clone https://github.com/LetsVenture2021/Speech-to-Text-Light.git
cd Speech-to-Text-Light
```

2. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate speech-to-text-light
```

## Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

On Windows:
```cmd
set OPENAI_API_KEY=your-api-key-here
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. The application will be running in debug mode. You can now:
   - Type or paste text for narration
   - Upload files (PDF, Word, Excel, CSV, images)
   - Paste URLs to have web content read aloud
   - Use voice input (click the microphone icon)

## Testing

Run the test suite:
```bash
pytest test_app.py -v
```

## Production Deployment

For production deployment, use a production-grade WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### API Key Issues
If you get an error about missing API key:
- Ensure OPENAI_API_KEY is set in your environment
- Verify the key is valid and has sufficient credits

### Port Already in Use
If port 5000 is already in use, you can specify a different port:
```bash
python app.py
# Then modify the app.run() line in app.py to use a different port
```

### Microphone Access
For voice input to work, your browser needs microphone permissions. Grant access when prompted.

## Features Available

- **Text Input**: Type or paste any text for immediate narration
- **URL Processing**: Paste a URL to have the webpage content narrated
- **Document Upload**: Upload PDF, Word (.docx), or plain text files
- **Data Files**: Upload Excel (.xlsx) or CSV files for data summaries
- **Image Analysis**: Upload images for visual description and narration
- **Voice Input**: Use the microphone for hands-free interaction (auto-stops after 3 seconds of silence)

## Need Help?

Check the main [README.md](README.md) for more information about the project's features and architecture.
