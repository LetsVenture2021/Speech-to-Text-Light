FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY public/ ./public/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Run application
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
CMD ["python", "app.py"]
