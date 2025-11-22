// Front-end app — attempts to call server /api/summarize when available,
// falls back to local heuristics when server is unavailable.

(function () {
  const inputText = document.getElementById('inputText');
  const sendBtn = document.getElementById('sendBtn');
  const micBtn = document.getElementById('micBtn');
  const fileInput = document.getElementById('fileInput');
  const uploadBtn = document.getElementById('uploadBtn');
  const status = document.getElementById('status');
  const memoryList = document.getElementById('memoryList');
  const log = document.getElementById('log');
  const ttsEnabled = document.getElementById('ttsEnabled');
  const autoPlay = document.getElementById('autoPlay');
  const voiceSelect = document.getElementById('voiceSelect');
  const prosodySelect = document.getElementById('prosodySelect');
  const clearMemoryBtn = document.getElementById('clearMemory');
  const downloadTranscript = document.getElementById('downloadTranscript');

  let transcripts = [];

  function loadMemory() { return JSON.parse(localStorage.getItem('sttl_memory') || '[]'); }
  function saveMemory(mem) { localStorage.setItem('sttl_memory', JSON.stringify(mem || [])); }

  function appendLog(msg) {
    const time = new Date().toISOString().split('T')[1].slice(0,8);
    log.textContent = `[${time}] ${msg}\n` + log.textContent;
  }
  function setStatus(s) { status.textContent = s; appendLog(s); }

  function renderMemory() {
    const mem = loadMemory();
    memoryList.innerHTML = '';
    mem.slice().reverse().forEach(entry => {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${entry.summary}</strong><div style="font-size:0.86rem;color:var(--pv-text-muted)">${entry.note || ''} • ${new Date(entry.ts).toLocaleString()}</div>`;
      memoryList.appendChild(li);
    });
  }

  // Local heuristics (fallback when server is not available)
  const positiveWords = ['good','great','happy','love','wonderful','excellent','amazing','positive'];
  const negativeWords = ['bad','sad','angry','hate','terrible','horrible','negative','upset'];
  function inferEmotionLocal(text) {
    if (!text) return {score:0,label:'neutral'};
    const t = text.toLowerCase();
    let score = 0;
    for (const w of positiveWords) if (t.includes(w)) score += 1;
    for (const w of negativeWords) if (t.includes(w)) score -= 1;
    let label = 'neutral';
    if (score > 0) label = 'positive';
    if (score < 0) label = 'negative';
    return {score, label};
  }
  function prosodyFor(emotion, preset) {
    let rate = 1.0, pitch = 1.0, volume = 1.0;
    if (emotion.label === 'positive') { rate += 0.08; pitch += 0.12; }
    if (emotion.label === 'negative') { rate -= 0.05; pitch -= 0.08; }
    switch(preset) {
      case 'warm': rate *= 0.9; pitch *= 0.9; break;
      case 'bright': rate *= 1.15; pitch *= 1.2; break;
      case 'empathetic': rate *= 0.95; pitch *= 1.02; break;
      default: break;
    }
    return {rate: clamp(rate,0.6,1.6), pitch: clamp(pitch,0.5,2), volume: clamp(volume,0.2,1)};
  }
  function clamp(v,a,b){ return Math.max(a,Math.min(b,v)); }

  function speakText(text, emotion) {
    if (!('speechSynthesis' in window)) {
      setStatus('No SpeechSynthesis available in this browser.');
      return;
    }
    const utter = new SpeechSynthesisUtterance(text);
    const preset = prosodySelect.value || 'neutral';
    const p = prosodyFor(emotion, preset);
    utter.rate = p.rate; utter.pitch = p.pitch; utter.volume = p.volume;
    const vname = voiceSelect.value;
    const voice = speechSynthesis.getVoices().find(v => v.name === vname);
    if (voice) utter.voice = voice;
    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
    setStatus(`Speaking (${emotion.label}) — rate:${utter.rate.toFixed(2)} pitch:${utter.pitch.toFixed(2)}`);
  }

  function generateNarrationLocal(inputText, emotion) {
    const opener = { positive: "Here's an upbeat take:", negative: "Here's a careful summary:", neutral: "Here's a brief read:" }[emotion.label || 'neutral'];
    const chopped = inputText.length > 800 ? inputText.slice(0,800) + '...' : inputText;
    return `${opener} ${chopped}`;
  }

  // Try server-side summarization; if fails, fallback local
  async function serverSummarize(text) {
    try {
      const res = await fetch('/api/summarize', {
        method: 'POST',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({ text })
      });
      if (!res.ok) throw new Error('Server responded ' + res.status);
      return await res.json();
    } catch (err) {
      appendLog('Server summarize failed: ' + err.message);
      return null;
    }
  }

  async function handleSubmit(raw, meta = {}) {
    setStatus('Processing input...');
    // try server
    const serverResult = await serverSummarize(raw).catch(()=>null);
    if (serverResult && serverResult.narration) {
      const { narration, emotion } = serverResult;
      // save memory
      const memory = loadMemory();
      memory.push({ ts: Date.now(), summary: narration.slice(0,120), note: `emo:${emotion.label} score:${emotion.score}` });
      if (memory.length > 40) memory.shift();
      saveMemory(memory); renderMemory();
      transcripts.push({ ts: Date.now(), raw, narration, emotion });
      if (autoPlay.checked && ttsEnabled.checked) speakText(narration, emotion);
      setStatus('Done — narration generated (server).');
      return { narration, emotion };
    }

    // fallback to local heuristics
    const emotion = inferEmotionLocal(raw);
    const narration = generateNarrationLocal(raw, emotion);
    const memory = loadMemory();
    memory.push({ ts: Date.now(), summary: narration.slice(0,120), note: `emo:${emotion.label} score:${emotion.score}` });
    if (memory.length > 40) memory.shift();
    saveMemory(memory); renderMemory();
    transcripts.push({ ts: Date.now(), raw, narration, emotion });
    if (autoPlay.checked && ttsEnabled.checked) speakText(narration, emotion);
    setStatus('Done — narration generated (local).');
    return { narration, emotion };
  }

  // File upload: prefer server extraction
  uploadBtn.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', async (ev) => {
    const f = ev.target.files[0];
    if (!f) return;
    setStatus('Uploading file: ' + f.name);
    try {
      const fd = new FormData();
      fd.append('file', f);
      const res = await fetch('/api/upload', { method:'POST', body: fd });
      if (!res.ok) throw new Error('Upload failed: ' + res.status);
      const data = await res.json();
      if (data && data.text) {
        inputText.value = data.text;
        setStatus('File extracted to input.');
      } else {
        inputText.value = `[Uploaded: ${f.name}]`;
        setStatus('Uploaded — no extracted text returned.');
      }
    } catch (err) {
      appendLog('Upload/extract failed: ' + err.message);
      inputText.value = `[Could not upload file locally: ${f.name}]`;
      setStatus('Upload failed — try local copy/paste.');
    }
  });

  sendBtn.addEventListener('click', async () => {
    let text = inputText.value.trim();
    if (!text) { setStatus('Nothing to send.'); return; }
    if (/^https?:\/\//i.test(text) && text.split(/\s+/).length === 1) {
      setStatus('Detected URL — requesting server to fetch...');
      try {
        const res = await fetch('/api/fetch-url', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ url: text }) });
        const body = await res.json();
        if (res.ok && body.text) { inputText.value = body.text; text = body.text; setStatus('Fetched remote content to input.'); }
        else { appendLog('Fetch-url failed'); }
      } catch (err) { appendLog('Fetch-url exception: ' + err.message); }
    }
    await handleSubmit(text);
  });

  // Microphone/recognition (client-side), same auto-send after silence approach
  let recognition, silenceTimer;
  async function initRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      appendLog('No SpeechRecognition available in this browser.');
      return null;
    }
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.continuous = true;
    let transcriptParts = [];
    recognition.onresult = (ev) => {
      let interim = '';
      for (let i = ev.resultIndex; i < ev.results.length; i++) {
        const res = ev.results[i];
        if (res.isFinal) transcriptParts.push(res[0].transcript);
        else interim += res[0].transcript;
      }
      inputText.value = (transcriptParts.join(' ') + ' ' + interim).trim();
      clearTimeout(silenceTimer);
      silenceTimer = setTimeout(() => recognition.stop(), 3000);
    };
    recognition.onerror = (ev) => appendLog('Recognition error: ' + ev.error);
    recognition.onend = async () => {
      appendLog('Recognition ended — auto-sending transcript.');
      const text = inputText.value.trim();
      if (text) await handleSubmit(text); else setStatus('No speech captured.');
    };
    return recognition;
  }

  micBtn.addEventListener('click', async () => {
    if (micBtn.dataset.recording === '1') {
      if (recognition) recognition.stop();
      micBtn.dataset.recording = '0';
      micBtn.textContent = '🎙️';
      setStatus('Stopped recording.');
    } else {
      if (!recognition) recognition = await initRecognition();
      if (!recognition) { setStatus('Speech recognition not supported in your browser.'); return; }
      transcripts = transcripts || [];
      recognition.start();
      micBtn.dataset.recording = '1';
      micBtn.textContent = '⏹️';
      setStatus('Recording — speak now. Auto-send after 3s of silence.');
    }
  });

  // Voice selection
  function populateVoices() {
    const voices = speechSynthesis.getVoices();
    voiceSelect.innerHTML = '';
    voices.forEach(v => {
      const o = document.createElement('option');
      o.value = v.name;
      o.textContent = `${v.name} — ${v.lang}${v.default ? ' (default)' : ''}`;
      voiceSelect.appendChild(o);
    });
  }
  if ('speechSynthesis' in window) {
    populateVoices();
    window.speechSynthesis.onvoiceschanged = populateVoices;
  } else {
    voiceSelect.innerHTML = '<option>SpeechSynthesis not available</option>';
  }

  (function init() { renderMemory(); setStatus('Ready'); })();

  clearMemoryBtn.addEventListener('click', () => {
    if (confirm('Clear stored conversation memory?')) { saveMemory([]); renderMemory(); setStatus('Memory cleared.'); }
  });

  downloadTranscript.addEventListener('click', () => {
    if (!transcripts.length) { setStatus('No transcripts to download yet.'); return; }
    const blob = new Blob([JSON.stringify(transcripts, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'transcripts.json'; a.click(); URL.revokeObjectURL(url);
    setStatus('Transcript downloaded.');
  });

  inputText.addEventListener('paste', (ev) => {
    setTimeout(() => {
      const val = inputText.value.trim();
      if (/^https?:\/\//i.test(val) && val.split(/\s+/).length === 1) appendLog('Pasted URL detected.');
    }, 50);
  });

  window.S2TL = { inferEmotionLocal: inferEmotionLocal, handleSubmit, loadMemory, saveMemory, transcripts };

})();