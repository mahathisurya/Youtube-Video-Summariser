# 🚀 Deployment Guide - YouTube Video Summarizer

This guide covers multiple deployment options from easiest to most advanced.

## 📋 Table of Contents

1. [Quick Local Deployment](#quick-local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Platform Deployment](#cloud-platform-deployment)
4. [Production Server Setup](#production-server-setup)
5. [Important Considerations](#important-considerations)

---

## 1️⃣ Quick Local Deployment (Development)

**Best for:** Testing, personal use

```bash
cd /Users/saimahathisuryadevara/Desktop/xyz

# Activate environment
source venv/bin/activate

# Run the server
python app.py
```

Access at: `http://localhost:5000`

**Pros:**
- ✅ Easiest setup
- ✅ Free
- ✅ Full control

**Cons:**
- ❌ Only accessible on your network
- ❌ Stops when you close terminal

---

## 2️⃣ Docker Deployment (Recommended)

**Best for:** Consistent deployment across any platform

### Option A: Local Docker

```bash
cd /Users/saimahathisuryadevara/Desktop/xyz

# Build the Docker image
docker build -t youtube-summarizer .

# Run the container
docker run -d -p 5000:5000 \
  --name youtube-summarizer \
  youtube-summarizer

# Check logs
docker logs -f youtube-summarizer

# Stop
docker stop youtube-summarizer

# Remove
docker rm youtube-summarizer
```

### Option B: Docker Compose (Easier)

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

**Pros:**
- ✅ Portable and consistent
- ✅ Easy to scale
- ✅ Works on any platform

**Cons:**
- ❌ Requires Docker installed

---

## 3️⃣ Cloud Platform Deployment

### A. **Railway.app** (Easiest Cloud Deployment) ⭐ RECOMMENDED

**Cost:** Free tier available, then ~$5/month

**Steps:**

1. **Push to GitHub:**
```bash
cd /Users/saimahathisuryadevara/Desktop/xyz

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect and deploy!

3. **Configure Environment:**
   - In Railway dashboard, go to Variables
   - Add: `PORT=5000`
   - Add: `MAX_VIDEO_DURATION=3600` (limit to 1 hour for free tier)

**Pros:**
- ✅ Extremely easy
- ✅ Auto HTTPS
- ✅ Auto deployments from GitHub
- ✅ Free tier available

---

### B. **Render.com** (Free Tier Available)

**Cost:** Free for web services (with limitations)

**Steps:**

1. Push code to GitHub (see above)

2. Go to [render.com](https://render.com)
   - Sign up → "New Web Service"
   - Connect GitHub repo
   - Configure:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn -w 2 -b 0.0.0.0:$PORT app:app`

3. Add `gunicorn` to requirements:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

**Pros:**
- ✅ Free tier
- ✅ Auto HTTPS
- ✅ Easy setup

**Cons:**
- ❌ Free tier spins down after inactivity
- ❌ Limited resources

---

### C. **Heroku** (Popular but Paid)

**Cost:** $5-7/month minimum

**Steps:**

1. Install Heroku CLI:
```bash
brew install heroku/brew/heroku
```

2. Create deployment files:

**Procfile:**
```bash
echo "web: gunicorn app:app" > Procfile
```

**runtime.txt:**
```bash
echo "python-3.11.0" > runtime.txt
```

3. Deploy:
```bash
heroku login
heroku create youtube-summarizer-app
git push heroku main
heroku open
```

---

### D. **AWS EC2** (Full Control)

**Cost:** ~$10-50/month depending on instance

**Steps:**

1. **Launch EC2 Instance:**
   - Go to AWS Console → EC2
   - Launch Ubuntu 22.04 instance (t2.medium recommended)
   - Configure security group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

2. **SSH into instance:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Setup on server:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3-pip python3-venv nginx ffmpeg

# Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

4. **Setup Nginx (Optional but recommended):**

Create `/etc/nginx/sites-available/youtube-summarizer`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/youtube-summarizer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

5. **Setup as systemd service:**

Create `/etc/systemd/system/youtube-summarizer.service`:
```ini
[Unit]
Description=YouTube Video Summarizer
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/YOUR_REPO
Environment="PATH=/home/ubuntu/YOUR_REPO/venv/bin"
ExecStart=/home/ubuntu/YOUR_REPO/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl enable youtube-summarizer
sudo systemctl start youtube-summarizer
sudo systemctl status youtube-summarizer
```

**Pros:**
- ✅ Full control
- ✅ Scalable
- ✅ Professional setup

**Cons:**
- ❌ More complex
- ❌ Higher cost
- ❌ Requires maintenance

---

### E. **Google Cloud Run** (Serverless)

**Cost:** Pay-per-use, very cheap for low traffic

**Steps:**

1. Install Google Cloud SDK:
```bash
brew install google-cloud-sdk
```

2. Initialize:
```bash
gcloud init
gcloud auth login
```

3. Build and deploy:
```bash
cd /Users/saimahathisuryadevara/Desktop/xyz

# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/youtube-summarizer

# Deploy
gcloud run deploy youtube-summarizer \
  --image gcr.io/YOUR_PROJECT_ID/youtube-summarizer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 300s
```

---

## 4️⃣ Production Server Setup (VPS)

**Best for:** Full control, any VPS provider (DigitalOcean, Linode, Vultr)

### DigitalOcean Droplet

**Cost:** $12-24/month

1. **Create Droplet:**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Create Droplet → Ubuntu 22.04 → 2GB RAM minimum

2. **Setup (same as AWS EC2 steps above)**

3. **Point domain:**
   - Add DNS A record pointing to your droplet IP
   - Follow Nginx setup above

---

## 5️⃣ Important Deployment Considerations

### System Requirements

**Minimum:**
- RAM: 2GB (4GB recommended)
- CPU: 2 cores
- Storage: 5GB (for models)
- Bandwidth: Depends on usage

**Why?**
- Whisper model: ~140MB (base), up to 3GB (large)
- BERT model: ~440MB
- Runtime memory: 1-2GB during processing

### Model Configuration

For production, consider model sizes:

```env
# .env file
WHISPER_MODEL_SIZE=tiny    # Fastest (39MB), less accurate
WHISPER_MODEL_SIZE=base    # Balanced (74MB) ✅ RECOMMENDED
WHISPER_MODEL_SIZE=small   # Better (244MB)
WHISPER_MODEL_SIZE=medium  # Best (769MB)
```

### Performance Optimization

1. **Use Gunicorn** (production WSGI server):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 300 app:app
```

2. **Use Nginx** as reverse proxy (handles static files, SSL)

3. **Enable GPU** (if available) for 10x faster transcription:
   - Whisper and BERT automatically use CUDA if available
   - On AWS, use g4dn instances

4. **Add Redis caching** for repeated requests

5. **Queue system** for handling multiple requests:
```bash
pip install celery redis
```

### Security Checklist

- [ ] Change default ports
- [ ] Enable HTTPS (use Let's Encrypt/Certbot)
- [ ] Add rate limiting
- [ ] Set up firewall (UFW on Ubuntu)
- [ ] Regular security updates
- [ ] Monitor logs
- [ ] Backup regularly

### Cost Estimates

| Platform | Cost | Best For |
|----------|------|----------|
| **Railway** | Free tier, then $5/mo | Quick deployment |
| **Render** | Free (limited) | Testing/demos |
| **Heroku** | $7+/mo | Easy management |
| **DigitalOcean** | $12-24/mo | Good balance |
| **AWS EC2** | $20-50/mo | Scalability |
| **Google Cloud Run** | Pay-per-use | Variable traffic |

---

## 🎯 Quick Decision Guide

**Choose based on your needs:**

1. **Just testing?** → Local deployment
2. **Quick demo/prototype?** → Railway or Render
3. **Professional deployment?** → AWS EC2 or DigitalOcean
4. **Variable traffic?** → Google Cloud Run
5. **Need full control?** → VPS with custom setup

---

## 🚀 Recommended Quick Deployment (5 minutes)

**For fastest public deployment:**

1. Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/your-repo.git
git push -u origin main
```

2. Deploy to Railway:
   - Go to railway.app
   - "New Project" → "Deploy from GitHub"
   - Done! 🎉

---

## 📝 Post-Deployment Checklist

- [ ] Test all endpoints
- [ ] Verify video processing works
- [ ] Check logs for errors
- [ ] Monitor resource usage
- [ ] Set up alerts
- [ ] Document your deployment
- [ ] Share the URL! 🎉

---

## 🆘 Troubleshooting

**Out of Memory?**
- Reduce `WHISPER_MODEL_SIZE` to `tiny` or `base`
- Limit video duration in `.env`

**Slow processing?**
- Use GPU instances
- Reduce model sizes
- Implement queue system

**Port issues?**
- Check firewall settings
- Ensure port 5000 is open
- Use `0.0.0.0` instead of `localhost`

---

Need help? Check the logs:
```bash
# Local
tail -f app.log

# Docker
docker logs -f youtube-summarizer

# Systemd
sudo journalctl -u youtube-summarizer -f
```

---

**You're ready to deploy! 🚀**
