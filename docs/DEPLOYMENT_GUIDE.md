# Deployment Guide

This guide provides step-by-step instructions for deploying Speech-to-Text Light to various platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Heroku Deployment](#heroku-deployment)
- [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
- [Google Cloud Run](#google-cloud-run)
- [Azure App Service](#azure-app-service)
- [Docker Deployment](#docker-deployment)
- [Traditional VPS](#traditional-vps)

## Prerequisites

Before deploying, ensure you have:

1. ✅ An OpenAI API key
2. ✅ Git installed
3. ✅ Account on your chosen platform
4. ✅ Platform CLI tools installed (if applicable)

## Heroku Deployment

**Best for:** Quick MVP launch, easy scaling, minimal configuration

### Step 1: Install Heroku CLI

```bash
# Mac
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login and Create App

```bash
# Login to Heroku
heroku login

# Create a new app
heroku create your-app-name

# Or create with specific region
heroku create your-app-name --region eu
```

### Step 3: Configure Environment

```bash
# Set OpenAI API key
heroku config:set OPENAI_API_KEY=your-api-key-here

# Set Flask environment to production
heroku config:set FLASK_ENV=production

# Verify config
heroku config
```

### Step 4: Deploy

```bash
# Push to Heroku
git push heroku main

# Or if on a different branch
git push heroku your-branch:main

# View logs
heroku logs --tail

# Open the app
heroku open
```

### Step 5: Scale (Optional)

```bash
# Scale to multiple dynos
heroku ps:scale web=2

# Use performance dynos
heroku ps:type performance-m
```

**Cost:** $0-$7/month (free tier), $25+/month (hobby/production)

---

## AWS Elastic Beanstalk

**Best for:** AWS ecosystem integration, production workloads

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize Application

```bash
# Initialize EB application
eb init -p python-3.10 speech-to-text-light --region us-east-1

# Create environment
eb create production-env
```

### Step 3: Configure Environment Variables

```bash
# Set environment variables
eb setenv OPENAI_API_KEY=your-api-key-here
eb setenv FLASK_ENV=production
```

### Step 4: Deploy

```bash
# Deploy application
eb deploy

# Open application
eb open

# View logs
eb logs
```

### Step 5: Configure (Optional)

Create `.ebextensions/python.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
  aws:elasticbeanstalk:environment:proxy:
    ProxyServer: nginx
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
```

**Cost:** ~$30-100/month (t3.small instance + load balancer)

---

## Google Cloud Run

**Best for:** Serverless deployment, automatic scaling, pay-per-use

### Step 1: Install Google Cloud SDK

```bash
# Mac
brew install google-cloud-sdk

# Linux
curl https://sdk.cloud.google.com | bash

# Windows: Download from https://cloud.google.com/sdk/docs/install
```

### Step 2: Authenticate and Configure

```bash
# Login
gcloud auth login

# Set project
gcloud config set project your-project-id
```

### Step 3: Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
```

### Step 4: Build and Deploy

```bash
# Build container
gcloud builds submit --tag gcr.io/your-project-id/speech-to-text-light

# Deploy to Cloud Run
gcloud run deploy speech-to-text-light \
  --image gcr.io/your-project-id/speech-to-text-light \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key,FLASK_ENV=production \
  --memory 1Gi \
  --timeout 60s

# Get URL
gcloud run services describe speech-to-text-light --region us-central1
```

**Cost:** ~$0.10-50/month (pay per request, free tier available)

---

## Azure App Service

**Best for:** Microsoft ecosystem, enterprise deployments

### Step 1: Install Azure CLI

```bash
# Mac
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Windows: Download from https://aka.ms/installazurecliwindows
```

### Step 2: Login and Create Resources

```bash
# Login
az login

# Create resource group
az group create --name speech-to-text-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name speech-to-text-plan \
  --resource-group speech-to-text-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --name your-app-name \
  --resource-group speech-to-text-rg \
  --plan speech-to-text-plan \
  --runtime "PYTHON:3.10"
```

### Step 3: Configure and Deploy

```bash
# Set environment variables
az webapp config appsettings set \
  --name your-app-name \
  --resource-group speech-to-text-rg \
  --settings OPENAI_API_KEY=your-key FLASK_ENV=production

# Deploy code
az webapp up \
  --name your-app-name \
  --resource-group speech-to-text-rg

# View logs
az webapp log tail --name your-app-name --resource-group speech-to-text-rg
```

**Cost:** ~$13-100/month (B1-P1v2 tiers)

---

## Docker Deployment

**Best for:** Containerized deployments, Kubernetes, self-hosting

### Step 1: Create Dockerfile

```dockerfile
# Multi-stage build for smaller image
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "60", "app:app"]
```

### Step 2: Build and Run

```bash
# Build image
docker build -t speech-to-text-light .

# Run container
docker run -d \
  -p 5000:5000 \
  -e OPENAI_API_KEY=your-key \
  -e FLASK_ENV=production \
  --name speech-to-text \
  speech-to-text-light

# View logs
docker logs -f speech-to-text

# Stop container
docker stop speech-to-text
```

### Step 3: Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - FLASK_ENV=production
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

**Cost:** Depends on hosting (VPS $5-50/month)

---

## Traditional VPS

**Best for:** Full control, custom configurations

### Step 1: Connect to Server

```bash
ssh user@your-server-ip
```

### Step 2: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install -y python3.10 python3-pip nginx supervisor git

# Install Gunicorn
pip3 install gunicorn
```

### Step 3: Clone and Setup Application

```bash
# Clone repository
cd /opt
sudo git clone https://github.com/LetsVenture2021/Speech-to-Text-Light.git
cd Speech-to-Text-Light

# Install dependencies
pip3 install -r requirements.txt

# Set environment variables
echo "export OPENAI_API_KEY='your-key'" | sudo tee -a /etc/environment
echo "export FLASK_ENV='production'" | sudo tee -a /etc/environment
source /etc/environment
```

### Step 4: Configure Supervisor

Create `/etc/supervisor/conf.d/speech-to-text.conf`:

```ini
[program:speech-to-text]
directory=/opt/Speech-to-Text-Light
command=/usr/local/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/speech-to-text.err.log
stdout_logfile=/var/log/speech-to-text.out.log
environment=OPENAI_API_KEY="your-key",FLASK_ENV="production"
```

```bash
# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start speech-to-text
```

### Step 5: Configure Nginx

Create `/etc/nginx/sites-available/speech-to-text`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/speech-to-text /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: SSL with Let's Encrypt (Optional)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

**Cost:** $5-50/month (VPS) + domain cost

---

## Post-Deployment Checklist

After deploying to any platform:

- [ ] Verify the app is accessible via browser
- [ ] Test all features (text input, file upload, voice input)
- [ ] Check health endpoint: `https://your-app/health`
- [ ] Monitor logs for errors
- [ ] Set up monitoring/alerting (optional but recommended)
- [ ] Configure domain name (if not using platform subdomain)
- [ ] Set up SSL/HTTPS
- [ ] Configure rate limiting (recommended)
- [ ] Set up backups (if using database in future)

## Troubleshooting

### Application won't start

```bash
# Check logs
heroku logs --tail  # Heroku
docker logs speech-to-text  # Docker
sudo journalctl -u nginx  # VPS

# Common issues:
# - Missing OPENAI_API_KEY environment variable
# - Port already in use
# - Missing dependencies
```

### 502 Bad Gateway

- Check if Gunicorn is running
- Verify port configuration
- Check Nginx/proxy configuration
- Increase timeout values

### High memory usage

- Reduce number of Gunicorn workers
- Increase instance size
- Add request queuing/rate limiting

## Support

For deployment issues, please open an issue on [GitHub](https://github.com/LetsVenture2021/Speech-to-Text-Light/issues).

---

*Last Updated: November 2024*
