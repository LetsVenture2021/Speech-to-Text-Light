# Environment Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install flask openai requests pypdf python-docx pandas openpyxl
```

Or create a `requirements.txt`:
```bash
flask>=3.0.0
openai>=1.0.0
requests>=2.31.0
pypdf>=3.17.0
python-docx>=1.1.0
pandas>=2.1.0
openpyxl>=3.1.0
```

Then install:
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

**Option A: Using .env file (recommended for development)**

Create a file named `.env` in the project root:
```bash
# Required
OPENAI_API_KEY=sk-your-actual-key-here

# Optional (development settings)
FLASK_DEBUG=true
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

Then load it before running:
```bash
# On Linux/Mac
export $(cat .env | xargs)
python3 app.py

# Or use python-dotenv package
pip install python-dotenv
# Add to app.py: from dotenv import load_dotenv; load_dotenv()
```

**Option B: Export directly (Linux/Mac)**
```bash
export OPENAI_API_KEY="sk-your-actual-key-here"
export FLASK_DEBUG="false"
python3 app.py
```

**Option C: Windows Command Prompt**
```cmd
set OPENAI_API_KEY=sk-your-actual-key-here
set FLASK_DEBUG=false
python app.py
```

**Option D: Windows PowerShell**
```powershell
$env:OPENAI_API_KEY="sk-your-actual-key-here"
$env:FLASK_DEBUG="false"
python app.py
```

### 3. Run the Application

```bash
python3 app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

### 4. Test the Application

Open your browser and go to: http://127.0.0.1:5000

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key from platform.openai.com |
| `FLASK_DEBUG` | No | `false` | Enable Flask debug mode (`true`/`false`) |
| `FLASK_HOST` | No | `127.0.0.1` | Host to bind to (`0.0.0.0` for all interfaces) |
| `FLASK_PORT` | No | `5000` | Port number to listen on |

---

## Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **Important:** Never commit this key to git!

---

## Security Notes

### ⚠️ Never Commit Your API Key

Add `.env` to your `.gitignore`:
```bash
echo ".env" >> .gitignore
```

### ⚠️ Production Deployment

For production:
1. **Never set `FLASK_DEBUG=true`** in production
2. **Use a production WSGI server** like gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. **Use HTTPS** with a reverse proxy (nginx, Apache)
4. **Set up proper firewall rules**
5. **Use environment-specific configuration**

---

## Troubleshooting

### Error: "OPENAI_API_KEY environment variable is required"

**Problem:** The API key is not set.

**Solution:** Export the environment variable before running:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Error: "Module not found"

**Problem:** Dependencies not installed.

**Solution:**
```bash
pip install flask openai requests pypdf python-docx pandas openpyxl
```

### Error: "Address already in use"

**Problem:** Port 5000 is already in use by another application.

**Solution:** Use a different port:
```bash
export FLASK_PORT=8000
python3 app.py
```

### App starts but features don't work

**Problem:** Using incorrect OpenAI API models.

**Solution:** Make sure you're using the fixed version of `app.py` with:
- `TTS_MODEL = "tts-1"`
- `STT_MODEL = "whisper-1"`
- `LLM_MODEL = "gpt-4o-mini"`

---

## Testing the Security Fixes

### Test SSRF Protection

Try submitting these URLs (should be blocked):
- `http://localhost/admin`
- `http://127.0.0.1/`
- `http://192.168.1.1/`
- `http://169.254.169.254/latest/meta-data/`

Should see: "URL rejected for security reasons: ..."

### Test File Size Limits

Try uploading a file larger than 10MB.
Should see: "File too large (max 10MB)"

### Test File Type Validation

Try uploading an executable (.exe, .sh, .bin).
Should see: "File type .exe not allowed"

---

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Security Analysis](SECURITY_ANALYSIS.md) - Detailed vulnerability explanations
- [Fixes Applied](FIXES_APPLIED.md) - Summary of all security fixes
