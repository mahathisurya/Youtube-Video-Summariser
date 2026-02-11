# 🚀 Quick Start Guide

Get up and running with YouTube Video Summarizer in 5 minutes!

## Prerequisites

- Python 3.8+
- AssemblyAI API Key ([Get free key](https://www.assemblyai.com/))

## Setup (3 Steps)

### 1️⃣ Run Setup Script

```bash
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies (~400MB BERT model)
- Create `.env` file
- Set up directories

### 2️⃣ Add API Key

Edit `.env` and add your AssemblyAI API key:

```bash
ASSEMBLYAI_API_KEY=your_actual_api_key_here
```

### 3️⃣ Start Server

```bash
source venv/bin/activate
python app.py
```

Server will start at `http://localhost:5000`

## First Test 🧪

Open a new terminal and run:

```bash
python test_api.py
```

## Quick API Examples

### Process a Video
```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "source_language": "en",
    "summary_ratio": 0.3
  }'
```

### Summarize Text
```bash
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long text here...",
    "ratio": 0.3
  }'
```

### Translate Text
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, world!",
    "target_language": "es"
  }'
```

## Using Python Client

```python
from example_usage import VideoSummarizerClient

client = VideoSummarizerClient()

# Process a video
result = client.process_video(
    video_url="https://www.youtube.com/watch?v=VIDEO_ID",
    source_language="en",
    summary_ratio=0.3
)

print(result['summary']['text'])
```

## Docker Deployment 🐳

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

## Key Features

✅ **Multi-Language**: 10+ languages supported  
✅ **Smart Summarization**: BERT-based, 60-70% reduction  
✅ **Translation**: 100+ languages via Google Translate  
✅ **Long Videos**: Up to 1+ hour supported  
✅ **Error Recovery**: Automatic retries and validation  

## Common Issues

**"Module not found"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"API key not found"**
- Check `.env` file exists
- Verify `ASSEMBLYAI_API_KEY` is set

**"Port already in use"**
- Change PORT in `.env`
- Or kill existing process: `lsof -ti:5000 | xargs kill`

## Next Steps

📖 Read full documentation: [README.md](README.md)  
🧪 Run tests: `python test_api.py`  
💻 Try examples: `python example_usage.py`  
🐳 Deploy with Docker: `docker-compose up`  

## Support

- Check logs: `tail -f app.log`
- Test endpoints: `python test_api.py`
- See examples: `python example_usage.py`

---

**Built with Flask, AssemblyAI, BERT, and Google Translate**
