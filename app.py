import os
import io
import base64
import mimetypes
import re
from pathlib import Path

from flask import Flask, request, make_response
from flask import render_template_string
from openai import OpenAI
import requests

from pypdf import PdfReader
from docx import Document
import pandas as pd

# ---------- CONFIG ----------

# Initialize OpenAI client - allows for missing key during import (for testing)
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

TTS_MODEL = "gpt-4o-mini-tts"          # text → speech :contentReference[oaicite:0]{index=0}
STT_MODEL = "gpt-4o-mini-transcribe"   # speech → text :contentReference[oaicite:1]{index=1}
LLM_MODEL = "gpt-4o-mini"              # text/image → “narration script” :contentReference[oaicite:2]{index=2}

# ---------- FLASK APP ----------

app = Flask(__name__)

# ---------- UTILITIES ----------

URL_REGEX = re.compile(r"^https?://", re.IGNORECASE)


def ensure_client():
    """Ensure OpenAI client is initialized with API key."""
    if client is None:
        raise RuntimeError(
            "OpenAI API key not configured. "
            "Please set the OPENAI_API_KEY environment variable."
        )


def looks_like_url(text: str) -> bool:
    return bool(URL_REGEX.match(text.strip()))


def fetch_url_text(url: str) -> str:
    """
    Fetch and convert URL content to text.
    Includes basic SSRF protection by blocking private/local addresses.
    """
    try:
        from urllib.parse import urlparse
        import socket

        # Parse and validate URL
        parsed = urlparse(url)
        if not parsed.scheme in ['http', 'https']:
            return f"Invalid URL scheme. Only http and https are allowed."

        # Get hostname and check if it's private/local
        hostname = parsed.hostname
        if not hostname:
            return f"Invalid URL: missing hostname."

        # Resolve hostname to IP and check if it's private
        try:
            ip_addr = socket.gethostbyname(hostname)
            # Block private IP ranges (10.x, 172.16-31.x, 192.168.x, 127.x, 169.254.x)
            octets = ip_addr.split('.')
            if (octets[0] == '10' or
                octets[0] == '127' or
                (octets[0] == '172' and 16 <= int(octets[1]) <= 31) or
                (octets[0] == '192' and octets[1] == '168') or
                (octets[0] == '169' and octets[1] == '254')):
                return f"Access to private/local addresses is not allowed."
        except socket.gaierror:
            return f"Failed to resolve hostname: {hostname}"

        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        return f"Failed to fetch URL {url}: {e}"

    # ultra-lightweight HTML stripping
    # (you can swap this for BeautifulSoup / readability if you want)
    text = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text_from_pdf(file_stream) -> str:
    reader = PdfReader(file_stream)
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n\n".join(pages)


def extract_text_from_docx(file_stream) -> str:
    # python-docx expects a path or file-like; BytesIO works.
    doc = Document(file_stream)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text_from_plain(file_stream) -> str:
    return file_stream.read().decode("utf-8", errors="ignore")


def summarize_table(df: pd.DataFrame) -> str:
    """Turn a dataframe into a compact textual description."""
    buf = []
    buf.append(f"Table shape: {df.shape[0]} rows x {df.shape[1]} columns.")
    buf.append(f"Columns: {', '.join(map(str, df.columns))}.")
    # Simple stats on numeric columns
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        desc = numeric.describe().to_dict()
        buf.append("Numeric summary (per column):")
        for col, stats in desc.items():
            buf.append(
                f"- {col}: mean={stats.get('mean'):.3g}, "
                f"min={stats.get('min'):.3g}, max={stats.get('max'):.3g}"
            )
    return "\n".join(buf)


def interpret_image_to_text(img_bytes: bytes, filename: str) -> str:
    """Send an image to gpt-4o-mini and ask for a descriptive, narration-ready text."""
    ensure_client()
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    mime_type = mimetypes.guess_type(filename)[0] or "image/png"

    res = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a 'vision adapter' for a voice reader. "
                    "Describe this image as if you are narrating it out loud: "
                    "clear, vivid, but concise. Highlight trends if it is a chart/diagram."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image for spoken narration.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{b64}",
                        },
                    },
                ],
            },
        ],
    )

    return res.choices[0].message.content


def run_inflective_emergence_loop(raw_text: str, modality: str) -> str:
    """
    Central brain:
    - semantic layer (understand content)
    - emotion inference
    - identity kernel + drift-aware memory
    - prosody-aware narration script
    Returns: text that is ready to be sent to TTS.
    """
    ensure_client()
    system_prompt = f"""
You are an 'Inflective Emergence Loop' driving a voice-only content reader.

Pipeline:
1. Semantic Layer: Quickly understand the source ({modality}) and extract the essential ideas.
2. Emotion Inference: Infer the emotional tone appropriate for the material 
   (neutral, upbeat, urgent, empathetic, etc.).
3. Identity Kernel: Maintain a consistent, calm, intelligent narrator persona with subtle drift 
   over time (slightly adapting tone to the content without becoming caricatured).
4. Prosody Plan: Shape sentences so they are easy to speak and easy to listen to: 
   short clauses, logical pauses, and clear emphasis.
5. Output: A narration SCRIPT — not bullets, not markdown — just clean, 
   spoken-style paragraphs.

Constraints:
- Be concise but complete enough that I’d understand the gist if I only listened once.
- No meta-commentary like "the following text says".
- Do not mention the pipeline or that you are an AI.
"""
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Source modality: {modality}\n\nRaw content:\n{raw_text}",
            },
        ],
        temperature=0.7,
        max_tokens=1200,
    )
    return resp.choices[0].message.content


def text_to_speech(narration_text: str) -> bytes:
    """
    Use the Audio API to turn text into speech.
    We rely on the fact that audio.speech.create returns raw audio bytes. :contentReference[oaicite:4]{index=4}
    """
    ensure_client()
    # optional: add extra style guidance
    instructions = (
        "Read as a calm, clear narrator. Vary intonation slightly to match emotion, "
        "but stay professional and easy to follow."
    )

    audio_bytes = client.audio.speech.create(
        model=TTS_MODEL,
        voice="coral",
        input=narration_text,
        instructions=instructions,
        response_format="mp3",
    )
    return audio_bytes


def transcribe_audio(file_obj) -> str:
    """Speech to text via gpt-4o-mini-transcribe."""
    ensure_client()
    transcript = client.audio.transcriptions.create(
        model=STT_MODEL,
        file=file_obj,
    )
    return transcript.text


# ---------- CORE PROCESSING ----------

def process_request_content(text_input: str | None, uploaded_file) -> tuple[str, str]:
    """
    Normalize all entry paths into:
    - normalized_text   (to feed into the Inflective loop)
    - modality label    (for the system prompt)
    """
    if uploaded_file:
        filename = uploaded_file.filename or ""
        ext = (Path(filename).suffix or "").lower()

        # Read bytes once
        data = uploaded_file.read()
        stream = io.BytesIO(data)

        if ext == ".pdf":
            return extract_text_from_pdf(stream), "pdf-document"
        elif ext in {".doc", ".docx"}:
            return extract_text_from_docx(stream), "word-document"
        elif ext in {".txt", ".md"}:
            return extract_text_from_plain(stream), "text-document"
        elif ext in {".xlsx", ".xls", ".csv"}:
            if ext == ".csv":
                df = pd.read_csv(stream)
            else:
                df = pd.read_excel(stream)
            summary = summarize_table(df)
            return summary, "structured-data"
        elif ext in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
            description = interpret_image_to_text(data, filename)
            return description, "image-visual"
        else:
            # Fallback: treat as text
            try:
                txt = data.decode("utf-8", errors="ignore")
            except Exception:
                txt = ""
            return txt or "Unable to parse file; it might be a binary format.", "unknown-file"

    # No file: see if it's a URL or plain text
    if text_input and looks_like_url(text_input):
        url_text = fetch_url_text(text_input.strip())
        return url_text, "remote-url"
    else:
        return (text_input or "").strip(), "direct-text"


# ---------- ROUTES ----------

@app.route("/", methods=["GET"])
def index():
    # Simple inline HTML/JS UI
    return render_template_string(
        HTML_TEMPLATE,
    )


@app.route("/api/process", methods=["POST"])
def api_process():
    """
    Handles:
    - typed/pasted text (including URLs)
    - file uploads (PDF/Word/text/image/xlsx/csv)
    Returns: MP3 audio only.
    """
    text_input = request.form.get("text", "")
    uploaded_file = request.files.get("file")

    normalized_text, modality = process_request_content(text_input, uploaded_file)

    if not normalized_text.strip():
        normalized_text = "The user provided empty content. Briefly explain that there was nothing to read."

    narration_script = run_inflective_emergence_loop(normalized_text, modality)
    audio_bytes = text_to_speech(narration_script)

    resp = make_response(audio_bytes)
    resp.headers["Content-Type"] = "audio/mpeg"
    return resp


@app.route("/api/voice", methods=["POST"])
def api_voice():
    """
    Accepts recorded audio (e.g., webm/wav) from the browser.
    - Transcribes
    - Runs through inflective loop
    - Returns MP3 speech
    """
    audio_file = request.files.get("audio")
    if not audio_file:
        return "No audio provided", 400

    # Transcribe
    text = transcribe_audio(audio_file)
    if not text.strip():
        text = "The user spoke, but nothing intelligible was detected. Respond briefly."

    # Run through same loop, modality = 'real-time-speech'
    narration_script = run_inflective_emergence_loop(text, "real-time-speech")
    audio_bytes = text_to_speech(narration_script)

    resp = make_response(audio_bytes)
    resp.headers["Content-Type"] = "audio/mpeg"
    return resp


# ---------- INLINE FRONTEND ----------

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Inflective TTS</title>
  <style>
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #0b0c10;
      color: #e5e7eb;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }
    .app-container {
      width: 100%;
      max-width: 700px;
      background: #111827;
      padding: 16px 18px;
      border-radius: 18px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.45);
    }
    .header {
      font-size: 1rem;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #9ca3af;
    }
    .header span.title {
      font-weight: 600;
      color: #e5e7eb;
    }
    .input-wrapper {
      position: relative;
      display: flex;
      align-items: stretch;
      border-radius: 14px;
      background: #020617;
      border: 1px solid #1f2937;
      overflow: hidden;
    }
    textarea {
      flex: 1;
      resize: vertical;
      min-height: 80px;
      max-height: 200px;
      border: none;
      outline: none;
      background: transparent;
      color: #e5e7eb;
      padding: 10px 64px 10px 40px; /* leave room for icons left+right */
      font-size: 0.9rem;
    }
    textarea::placeholder {
      color: #4b5563;
    }
    .icon-button {
      border: none;
      background: transparent;
      cursor: pointer;
      font-size: 1rem;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 10px;
      color: #9ca3af;
      transition: background 0.12s ease, color 0.12s ease, transform 0.05s ease;
    }
    .icon-button:hover {
      background: #111827;
      color: #f9fafb;
    }
    .icon-button:active {
      transform: scale(0.96);
    }
    .file-label {
      position: absolute;
      left: 6px;
      top: 50%;
      transform: translateY(-50%);
      display: flex;
      align-items: center;
      justify-content: center;
      width: 28px;
      height: 28px;
      border-radius: 999px;
      cursor: pointer;
      color: #9ca3af;
      font-size: 1rem;
      transition: background 0.12s ease, color 0.12s ease;
    }
    .file-label:hover {
      background: #111827;
      color: #f9fafb;
    }
    #file-input {
      display: none;
    }
    .right-buttons {
      display: flex;
      align-items: center;
    }
    .icon-mic.recording {
      color: #f97373;
    }
    .status-bar {
      margin-top: 8px;
      font-size: 0.8rem;
      color: #9ca3af;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .pill {
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 0.7rem;
      border: 1px solid #374151;
      color: #9ca3af;
    }
  </style>
</head>
<body>
  <div class="app-container">
    <div class="header">
      <span class="title">Inflective Audio Reader</span>
      <span class="pill">TTS + Files + Vision + Voice</span>
    </div>

    <div class="input-wrapper">
      <!-- Left paperclip -->
      <label for="file-input" class="file-label" title="Upload file">
        📎
      </label>
      <input id="file-input" type="file" />

      <!-- Main text area -->
      <textarea id="text-input" placeholder="Paste text, drop a URL, or just speak…"></textarea>

      <!-- Right side: mic + send -->
      <div class="right-buttons">
        <button id="mic-btn" class="icon-button icon-mic" title="Hold to speak / click to start & auto-stop on silence">
          🎤
        </button>
        <button id="send-btn" class="icon-button" title="Send text / file for narration">
          ⬆️
        </button>
      </div>
    </div>

    <div class="status-bar">
      <span id="status-text">Idle</span>
      <span class="pill">Output: audio only</span>
    </div>

    <audio id="audio-player" style="display:none;"></audio>
  </div>

  <script>
    const textInput = document.getElementById("text-input");
    const fileInput = document.getElementById("file-input");
    const sendBtn = document.getElementById("send-btn");
    const micBtn = document.getElementById("mic-btn");
    const statusText = document.getElementById("status-text");
    const audioPlayer = document.getElementById("audio-player");

    // ---------- TEXT / FILE SEND ----------

    async function sendForNarration() {
      const formData = new FormData();
      formData.append("text", textInput.value || "");

      if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
      }

      statusText.textContent = "Processing…";
      sendBtn.disabled = true;
      micBtn.disabled = true;

      try {
        const resp = await fetch("/api/process", {
          method: "POST",
          body: formData,
        });
        if (!resp.ok) {
          throw new Error("Server error: " + resp.status);
        }
        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        audioPlayer.src = url;
        audioPlayer.play();
        statusText.textContent = "Playing audio…";
      } catch (err) {
        console.error(err);
        statusText.textContent = "Error: " + err.message;
      } finally {
        // Do not clear text by default; user might want it.
        sendBtn.disabled = false;
        micBtn.disabled = false;
      }
    }

    sendBtn.addEventListener("click", () => {
      if (!textInput.value && fileInput.files.length === 0) {
        statusText.textContent = "Nothing to send.";
        return;
      }
      sendForNarration();
    });

    // ---------- VOICE INPUT WITH SILENCE DETECTION ----------

    let mediaStream = null;
    let mediaRecorder = null;
    let audioChunks = [];
    let audioContext = null;
    let analyser = null;
    let sourceNode = null;
    let silenceTimer = null;
    const SILENCE_MS = 3000;  // 3 seconds
    const SILENCE_THRESHOLD = 0.01; // tweak for environment

    async function startRecording() {
      if (mediaRecorder && mediaRecorder.state === "recording") {
        return;
      }
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (e) {
        console.error(e);
        statusText.textContent = "Mic access denied.";
        return;
      }

      statusText.textContent = "Listening… (auto-stop after 3s of silence)";
      micBtn.classList.add("recording");
      sendBtn.disabled = true;

      // Setup Web Audio for simple silence detection
      audioContext = new (window.AudioContext || window.webkitAudioContext)();
      sourceNode = audioContext.createMediaStreamSource(mediaStream);
      analyser = audioContext.createAnalyser();
      analyser.fftSize = 2048;
      sourceNode.connect(analyser);

      const dataArray = new Uint8Array(analyser.fftSize);
      let lastNonSilent = performance.now();

      function checkSilence() {
        analyser.getByteTimeDomainData(dataArray);
        // Compute RMS-ish magnitude
        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
          const v = (dataArray[i] - 128) / 128.0;
          sum += v * v;
        }
        const rms = Math.sqrt(sum / dataArray.length);
        const now = performance.now();
        if (rms > SILENCE_THRESHOLD) {
          lastNonSilent = now;
        }
        const silenceFor = now - lastNonSilent;
        if (silenceFor >= SILENCE_MS) {
          stopRecording(true);
        } else {
          silenceTimer = requestAnimationFrame(checkSilence);
        }
      }
      silenceTimer = requestAnimationFrame(checkSilence);

      // Set up MediaRecorder
      audioChunks = [];
      mediaRecorder = new MediaRecorder(mediaStream, { mimeType: "audio/webm" });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        if (!audioChunks.length) {
          statusText.textContent = "No audio captured.";
          cleanupRecording();
          return;
        }

        statusText.textContent = "Transcribing & narrating…";

        const blob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", blob, "speech.webm");

        try {
          const resp = await fetch("/api/voice", {
            method: "POST",
            body: formData,
          });
          if (!resp.ok) {
            throw new Error("Server error: " + resp.status);
          }
          const audioBlob = await resp.blob();
          const url = URL.createObjectURL(audioBlob);
          audioPlayer.src = url;
          audioPlayer.play();
          statusText.textContent = "Playing response…";
        } catch (err) {
          console.error(err);
          statusText.textContent = "Error: " + err.message;
        } finally {
          cleanupRecording();
        }
      };

      mediaRecorder.start();
    }

    function stopRecording(auto = false) {
      if (silenceTimer) {
        cancelAnimationFrame(silenceTimer);
        silenceTimer = null;
      }
      if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
      } else if (!auto) {
        statusText.textContent = "Not recording.";
      }
    }

    function cleanupRecording() {
      if (mediaStream) {
        mediaStream.getTracks().forEach(t => t.stop());
        mediaStream = null;
      }
      if (audioContext) {
        audioContext.close();
        audioContext = null;
      }
      micBtn.classList.remove("recording");
      sendBtn.disabled = false;
      micBtn.disabled = false;
    }

    micBtn.addEventListener("click", () => {
      if (mediaRecorder && mediaRecorder.state === "recording") {
        // manual stop if user clicks again
        stopRecording(false);
      } else {
        startRecording();
      }
    });

    // Optional: Enter key to send when not holding Shift
    textInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendBtn.click();
      }
    });
  </script>
</body>
</html>
"""

# ---------- ENTRY ----------

if __name__ == "__main__":
    app.run(debug=True)
