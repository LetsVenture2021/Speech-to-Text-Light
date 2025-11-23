# Security Analysis and Risk Assessment

## Executive Summary

Your Speech-to-Text application has **several critical security vulnerabilities** that need immediate attention. This document explains what's wrong, the risks you face, and how to fix each issue.

---

## 🚨 CRITICAL ISSUES

### 1. **Incorrect OpenAI API Model Names** (Severity: CRITICAL)

**What's Happening:**
```python
TTS_MODEL = "gpt-4o-mini-tts"          # ❌ This model doesn't exist
STT_MODEL = "gpt-4o-mini-transcribe"   # ❌ This model doesn't exist
LLM_MODEL = "gpt-4o-mini"              # ✅ This one is correct
```

**The Risk:**
- Your application will **fail immediately** when trying to use text-to-speech or speech-to-text features
- Every API call to these non-existent models will return an error
- You're wasting API quota on failed requests
- Users will get error messages instead of functionality

**The Real OpenAI Models You Should Use:**
- For Text-to-Speech: `"tts-1"` or `"tts-1-hd"` (for higher quality)
- For Speech-to-Text: `"whisper-1"`
- For Chat/LLM: `"gpt-4o-mini"` (correct) or `"gpt-4o"` or `"gpt-3.5-turbo"`

**How to Fix:**
```python
TTS_MODEL = "tts-1"        # Correct TTS model
STT_MODEL = "whisper-1"    # Correct STT model
LLM_MODEL = "gpt-4o-mini"  # Already correct
```

---

### 2. **Incorrect OpenAI API Parameters** (Severity: CRITICAL)

**What's Happening:**

**Problem #1 - Wrong image parameter structure:**
```python
# ❌ INCORRECT (lines 117-119)
"type": "input_image",
"image": {
    "data": b64,
    "media_type": mime_type,
}
```

**The Risk:**
- OpenAI API will reject this request format
- Image analysis will fail every time
- No error handling means the app will crash

**How to Fix:**
```python
# ✅ CORRECT format
"type": "image_url",
"image_url": {
    "url": f"data:{mime_type};base64,{b64}"
}
```

**Problem #2 - Wrong TTS API parameters:**
```python
# ❌ INCORRECT (lines 184-190)
audio_bytes = client.audio.speech.create(
    model=TTS_MODEL,
    voice="coral",              # ❌ "coral" is not a valid voice
    input=narration_text,
    instructions=instructions,  # ❌ TTS doesn't accept "instructions" parameter
    response_format="mp3",
)
```

**The Risk:**
- Invalid voice name will cause API errors
- The "instructions" parameter doesn't exist for TTS API
- Your TTS calls will fail completely

**How to Fix:**
```python
# ✅ CORRECT format
response = client.audio.speech.create(
    model=TTS_MODEL,
    voice="alloy",  # Valid voices: alloy, echo, fable, onyx, nova, shimmer
    input=narration_text,
    response_format="mp3"
)
# Then read the response content:
audio_bytes = response.content
```

---

### 3. **SSRF (Server-Side Request Forgery) Vulnerability** (Severity: HIGH)

**What's Happening:**
```python
def fetch_url_text(url: str) -> str:
    try:
        resp = requests.get(url, timeout=10)  # ❌ No validation!
```

**The Risk:**
An attacker can:
1. **Scan your internal network** - They can make your server request internal URLs like:
   - `http://localhost:22` - Check what services are running locally
   - `http://192.168.1.1/admin` - Access internal admin panels
   - `http://169.254.169.254/latest/meta-data/` - Steal AWS credentials if you're on EC2
   
2. **Bypass firewall restrictions** - Use your server as a proxy to access:
   - Internal databases
   - Admin panels
   - Other services behind your firewall

3. **DOS (Denial of Service)** - Make your server:
   - Request huge files that fill up disk space
   - Request slow endpoints that tie up your workers
   - Make thousands of requests to attack other sites (using your IP)

**Real Attack Example:**
```
User submits: http://localhost:6379/  (Redis database)
Your server fetches it and potentially exposes sensitive data
```

**How to Fix:**
Add URL validation to block dangerous URLs:

```python
import ipaddress
from urllib.parse import urlparse

def is_safe_url(url: str) -> tuple[bool, str]:
    """Validate URL to prevent SSRF attacks."""
    try:
        parsed = urlparse(url)
        
        # Only allow http/https
        if parsed.scheme not in ('http', 'https'):
            return False, f"Invalid scheme: {parsed.scheme}"
        
        # Block if no hostname
        if not parsed.hostname:
            return False, "No hostname provided"
        
        # Block private/internal IP addresses
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                return False, f"Access to private IP addresses is not allowed"
        except ValueError:
            # It's a hostname (not an IP), need to resolve it
            import socket
            try:
                ip_str = socket.gethostbyname(parsed.hostname)
                ip = ipaddress.ip_address(ip_str)
                if ip.is_private or ip.is_loopback or ip.is_link_local:
                    return False, f"Hostname resolves to private IP address"
            except socket.gaierror:
                return False, f"Cannot resolve hostname"
        
        # Block common internal hostnames
        blocked_hosts = ['localhost', 'metadata.google.internal']
        if parsed.hostname.lower() in blocked_hosts:
            return False, f"Access to {parsed.hostname} is not allowed"
        
        return True, "OK"
    except Exception as e:
        return False, f"URL validation error: {e}"

def fetch_url_text(url: str) -> str:
    """Fetch URL with SSRF protection."""
    # Validate URL first
    is_safe, reason = is_safe_url(url)
    if not is_safe:
        return f"URL rejected for security reasons: {reason}"
    
    try:
        resp = requests.get(url, timeout=10, allow_redirects=False)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        return f"Failed to fetch URL {url}: {e}"
    
    # ... rest of the function
```

---

### 4. **Missing Input Validation** (Severity: MEDIUM)

**What's Happening:**
- No file size limits - Users can upload gigantic files
- No content type validation - Users can upload executables
- No rate limiting - Users can spam your API

**The Risk:**
1. **Disk space exhaustion** - Someone uploads a 10GB file
2. **Memory exhaustion** - Large files loaded into memory
3. **CPU exhaustion** - Processing massive files
4. **Cost explosion** - Large files sent to expensive OpenAI APIs

**How to Fix:**
Add validation in your route handlers:

```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.route("/api/process", methods=["POST"])
def api_process():
    uploaded_file = request.files.get("file")
    
    if uploaded_file:
        # Check file size
        uploaded_file.seek(0, os.SEEK_END)
        size = uploaded_file.tell()
        uploaded_file.seek(0)
        
        if size > MAX_FILE_SIZE:
            return "File too large (max 10MB)", 400
        
        # Validate file extension
        allowed_extensions = {'.pdf', '.docx', '.txt', '.md', '.xlsx', 
                             '.csv', '.png', '.jpg', '.jpeg', '.gif', '.webp'}
        ext = Path(uploaded_file.filename).suffix.lower()
        if ext not in allowed_extensions:
            return f"File type {ext} not allowed", 400
    
    # ... rest of handler
```

---

### 5. **No Environment Variable Validation** (Severity: MEDIUM)

**What's Happening:**
```python
client = OpenAI()  # Expects OPENAI_API_KEY in environment
```

**The Risk:**
- If `OPENAI_API_KEY` is not set, the app crashes with a confusing error
- No clear error message for debugging
- Harder for contributors to set up the project

**How to Fix:**
```python
import os

# Validate API key at startup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY environment variable is required. "
        "Get your API key from https://platform.openai.com/api-keys"
    )

client = OpenAI(api_key=OPENAI_API_KEY)
```

---

### 6. **Debug Mode in Production** (Severity: LOW but important)

**What's Happening:**
```python
if __name__ == "__main__":
    app.run(debug=True)  # ❌ Debug mode enabled
```

**The Risk:**
- Stack traces exposed to users reveal code structure
- Debug console can be exploited if Werkzeug debugger PIN is weak
- Performance impact

**How to Fix:**
```python
if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", "5000"))
    )
```

---

## 📊 Risk Summary Table

| Issue | Severity | Impact | Fix Complexity |
|-------|----------|--------|----------------|
| Wrong OpenAI model names | CRITICAL | App doesn't work | Easy |
| Wrong API parameters | CRITICAL | API calls fail | Easy |
| SSRF vulnerability | HIGH | Network attacks | Medium |
| Missing input validation | MEDIUM | DOS, cost explosion | Medium |
| No env var validation | MEDIUM | Poor developer experience | Easy |
| Debug mode enabled | LOW | Info disclosure | Easy |

---

## 🎓 Learning Resources

### Understanding SSRF
- [OWASP SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [PortSwigger: What is SSRF](https://portswigger.net/web-security/ssrf)

### OpenAI API Documentation
- [Text-to-Speech API](https://platform.openai.com/docs/guides/text-to-speech)
- [Speech-to-Text (Whisper) API](https://platform.openai.com/docs/guides/speech-to-text)
- [Vision API](https://platform.openai.com/docs/guides/vision)

### Flask Security
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## ✅ Recommended Fix Priority

1. **Fix OpenAI API usage** (CRITICAL - app doesn't work without this)
2. **Add SSRF protection** (HIGH - prevents network attacks)
3. **Add input validation** (MEDIUM - prevents resource exhaustion)
4. **Add environment validation** (MEDIUM - improves developer experience)
5. **Disable debug mode** (LOW - security hardening)

---

## 🔒 Additional Security Recommendations

1. **Add rate limiting** - Prevent abuse using Flask-Limiter
2. **Add authentication** - Don't expose this API publicly without auth
3. **Use HTTPS only** - Set up TLS/SSL for production
4. **Add logging** - Monitor for suspicious activity
5. **Set up monitoring** - Alert on unusual patterns
6. **Regular dependency updates** - Keep libraries patched
7. **Content Security Policy** - Add CSP headers
8. **CORS configuration** - Restrict allowed origins

---

## 📝 Next Steps

1. Review this document carefully
2. Understand each vulnerability
3. Apply the fixes in order of priority
4. Test each fix thoroughly
5. Set up automated security scanning
6. Consider a security audit before production deployment

---

## Questions?

If you need clarification on any of these issues, please ask! Security is complex, and it's better to ask questions than to leave vulnerabilities in your code.
