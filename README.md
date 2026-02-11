# YouTube Video Summarizer 🎥📝

A powerful Flask-based backend service for multi-language YouTube video transcription, translation, and summarization. This project implements a sophisticated NLP pipeline that processes videos up to 1+ hour across multiple languages, reducing transcript length by 60-70% while preserving key information.

## ✨ Features

- **Multi-Language Transcription**: Support for 99+ languages using OpenAI's Whisper (runs locally, completely FREE!)
- **No API Keys Required**: Whisper runs on your machine - no external API dependencies
- **Accurate Translation**: Powered by Google Translate for translation to multiple target languages
- **BERT-Based Summarization**: Extractive summarization using BERT embeddings with 60-70% text reduction
- **Robust Error Handling**: Built-in validation, retry mechanisms, and error recovery
- **Long-Form Content Support**: Process videos up to 1+ hour in various audio/video formats
- **RESTful API**: Clean, well-documented API endpoints
- **Beautiful Web Interface**: User-friendly UI for processing videos
- **Production-Ready**: Comprehensive logging, environment configuration, and error handling

## 🏗️ Architecture

```
┌─────────────────┐
│  YouTube Video  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Video Download  │  (yt-dlp)
│ Audio Extract   │  (moviepy)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Transcription  │  (Whisper - Local, FREE)
│   99+ Languages │  (No API Key Required!)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Translation   │  (Deep Translator)
│    (Optional)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ BERT Summary    │  (Transformers)
│  60-70% Reduce  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ JSON Response   │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- ffmpeg (for audio processing)

**That's it! No API keys needed!** 🎉

### Installation

1. **Clone or navigate to the project directory**
```bash
cd /Users/saimahathisuryadevara/Desktop/xyz
```

2. **Create a virtual environment**
```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

**Note:** First run will download Whisper model (~140MB for base model)

4. **Run the application**
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## 🌐 Using the Web Interface

1. Open your browser and go to `http://localhost:5000`
2. Paste any YouTube video URL
3. Select source language and options
4. Click "Process Video"
5. Get your summary! 🎉

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Web Interface
```http
GET /
```

Opens the beautiful web interface for easy video processing.

---

#### 2. Complete Pipeline (Process Video)
```http
POST /api/process
```

**Description:** Downloads video, transcribes, optionally translates, and summarizes.

**Request Body:**
```json
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "source_language": "en",
  "target_language": "es",
  "summary_ratio": 0.3,
  "include_translation": true
}
```

**Parameters:**
- `video_url` (required): YouTube video URL
- `source_language` (optional): Source language code (default: "en")
- `target_language` (optional): Target language for translation
- `summary_ratio` (optional): Compression ratio 0.1-0.5 (default: 0.3)
- `include_translation` (optional): Enable translation (default: false)

**Response:**
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "metadata": {
    "title": "Video Title",
    "author": "Channel Name",
    "duration": 1234,
    "views": 10000,
    "thumbnail": "https://...",
    "description": "..."
  },
  "transcription": {
    "text": "Full transcript...",
    "language": "en",
    "word_count": 5000
  },
  "translation": {
    "text": "Translated text...",
    "source_language": "en",
    "target_language": "es",
    "word_count": 5100
  },
  "summary": {
    "text": "Summary text...",
    "original_length": 25000,
    "summary_length": 7500,
    "reduction_ratio": 0.7,
    "compression_percentage": 70.0
  }
}
```

---

#### 3. Transcribe Only
```http
POST /api/transcribe
```

**Request Body:**
```json
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "source_language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "metadata": {...},
  "transcription": {
    "text": "Transcribed text...",
    "language": "en",
    "word_count": 5000
  }
}
```

---

#### 4. Translate Text
```http
POST /api/translate
```

**Request Body:**
```json
{
  "text": "Text to translate",
  "source_language": "en",
  "target_language": "es"
}
```

**Response:**
```json
{
  "success": true,
  "translation": {
    "original_text": "Text to translate",
    "translated_text": "Texto para traducir",
    "source_language": "en",
    "target_language": "es",
    "word_count": 3
  }
}
```

---

#### 5. Summarize Text
```http
POST /api/summarize
```

**Request Body:**
```json
{
  "text": "Long text to summarize...",
  "ratio": 0.3
}
```

**Response:**
```json
{
  "success": true,
  "summary": {
    "summary": "Summarized text...",
    "original_length": 10000,
    "summary_length": 3000,
    "reduction_ratio": 0.7,
    "compression_percentage": 70.0,
    "num_sentences": 50,
    "summary_sentences": 15
  }
}
```

---

#### 6. Get Supported Languages
```http
GET /api/languages
```

**Response:**
```json
{
  "success": true,
  "languages": {
    "transcription": ["en", "es", "fr", "de", "it", ...],
    "translation": ["en", "es", "fr", "de", "it", ...]
  }
}
```

## 🌍 Supported Languages

The system supports 99+ languages for transcription including:

**Popular Languages:**
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Dutch (nl)
- Russian (ru)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Hindi (hi)
- Turkish (tr)
- Polish (pl)
- Vietnamese (vi)
- Thai (th)
- Indonesian (id)
- Romanian (ro)
- Ukrainian (uk)

...and 79 more languages!

## 🧪 Testing Examples

### Example 1: Process English Video with Summary
```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "source_language": "en",
    "summary_ratio": 0.3
  }'
```

### Example 2: Transcribe and Translate to Spanish
```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "source_language": "en",
    "target_language": "es",
    "include_translation": true,
    "summary_ratio": 0.25
  }'
```

### Example 3: Just Transcribe a Video
```bash
curl -X POST http://localhost:5000/api/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "source_language": "en"
  }'
```

### Example 4: Summarize Existing Text
```bash
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long text here...",
    "ratio": 0.3
  }'
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file or edit the existing one:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Optional: Set max video duration in seconds (default: 7200 = 2 hours)
MAX_VIDEO_DURATION=7200

# Whisper Model Size (tiny, base, small, medium, large)
# base is recommended for good balance of speed and accuracy
WHISPER_MODEL_SIZE=base
```

### Whisper Model Options

Choose based on your needs:

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| `tiny` | 39MB | Fastest | Basic | Quick testing |
| `base` | 74MB | Fast | Good | **Recommended** |
| `small` | 244MB | Medium | Better | Higher accuracy |
| `medium` | 769MB | Slow | Great | Professional |
| `large` | 1.5GB | Slowest | Best | Maximum quality |

## 📁 Project Structure

```
xyz/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
│
├── templates/                 # Web interface
│   └── index.html            # Beautiful UI
│
├── services/                  # Core services
│   ├── __init__.py
│   ├── video_downloader.py    # YouTube download & audio extraction
│   ├── transcription.py       # Whisper integration (LOCAL, FREE!)
│   ├── translation.py         # Google Translate integration
│   └── summarizer.py          # BERT-based summarization
│
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── validators.py          # Input validation
│   └── error_handlers.py      # Error handling & logging
│
├── temp_videos/               # Temporary video files (auto-created)
└── temp_audio/                # Temporary audio files (auto-created)
```

## 🛠️ Technical Implementation

### 1. Video Download & Audio Extraction
- **Library**: yt-dlp, moviepy
- **Process**: Downloads YouTube video, extracts audio, converts to WAV
- **Features**: Retry mechanism, format validation, duration limits

### 2. Speech-to-Text Transcription
- **Service**: OpenAI Whisper (runs locally)
- **Features**: 99+ languages, auto language detection, high accuracy
- **Advantages**: FREE, no API limits, works offline
- **Models**: Multiple sizes from tiny (39MB) to large (1.5GB)

### 3. Translation
- **Library**: deep-translator (Google Translate)
- **Features**: 100+ languages, auto-detection, text chunking for large inputs
- **Optimization**: Splits large texts to avoid API limits

### 4. BERT-Based Summarization
- **Model**: BERT (bert-base-uncased)
- **Method**: Extractive summarization using sentence embeddings
- **Algorithm**:
  1. Split text into sentences
  2. Generate BERT embeddings for each sentence
  3. Calculate similarity to document embedding
  4. Select top-scoring sentences
  5. Maintain original order
- **Performance**: 60-70% text reduction while preserving key information

## 🚨 Error Handling

The system includes comprehensive error handling:

- **Input Validation**: URL format, language codes, ratio values
- **Retry Mechanisms**: Automatic retries for transient failures
- **Error Recovery**: Graceful degradation and cleanup
- **Logging**: Detailed logs for debugging and monitoring
- **Custom Exceptions**: Specific error types for different failures

## 📊 Performance Considerations

- **Video Duration**: Supports videos up to 1+ hour (configurable to 2+ hours)
- **Model Loading**: Whisper and BERT models lazy-loaded on first use
- **GPU Support**: Automatically uses GPU if available for faster processing
- **File Cleanup**: Automatic cleanup of temporary files
- **Memory Management**: Efficient handling of large transcripts

### Processing Speed

| Model | Video Length | Processing Time |
|-------|-------------|-----------------|
| Whisper tiny | 10 min | ~30 seconds |
| Whisper base | 10 min | ~1 minute |
| Whisper small | 10 min | ~2 minutes |
| Whisper medium | 10 min | ~5 minutes |

*On CPU. With GPU, 5-10x faster!*

## 🔒 Security Best Practices

- ✅ No API keys stored (Whisper runs locally)
- ✅ Input validation and sanitization
- ✅ Request size limits (100MB max)
- ✅ Temporary file cleanup
- ✅ Generic error messages (no information leakage)
- ✅ .gitignore for sensitive files

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**2. Video download fails**
- Check if video is available and not restricted
- Verify internet connection
- Try a different video URL

**3. Out of memory during processing**
- Use smaller Whisper model: `WHISPER_MODEL_SIZE=tiny`
- Reduce video duration limit
- Close other applications

**4. Slow processing**
- Use smaller Whisper model
- Enable GPU if available
- Reduce video length

**5. Port already in use**
```bash
# Change PORT in .env
echo "PORT=5001" >> .env

# Or kill existing process
lsof -ti:5000 | xargs kill
```

## 📈 Future Enhancements

- [ ] Support for subtitle/caption extraction
- [ ] Abstractive summarization using T5/GPT models
- [ ] Batch processing for multiple videos
- [ ] WebSocket support for real-time progress updates
- [ ] Database integration for caching results
- [ ] API rate limiting and authentication
- [ ] Mobile app
- [ ] Multi-language UI

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

**Quick Deploy Options:**
- Railway (recommended - 5 minutes)
- Render (free tier)
- Docker (local/cloud)
- AWS/DigitalOcean (production)

Or use the deployment helper:
```bash
./deploy.sh
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions:
1. Check the Troubleshooting section
2. Review the API documentation
3. Check application logs in `app.log`
4. See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help

## 🎓 Credits

Built with:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech-to-text (LOCAL, FREE!)
- [Deep Translator](https://pypi.org/project/deep-translator/) - Translation
- [Transformers](https://huggingface.co/transformers/) - BERT models
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube video download
- [moviepy](https://zulko.github.io/moviepy/) - Audio extraction

## ⭐ Key Advantages

- ✅ **100% FREE** - No API costs, runs locally
- ✅ **No API Keys** - Whisper runs on your machine
- ✅ **99+ Languages** - More languages than most paid services
- ✅ **Offline Capable** - Works without internet (after first model download)
- ✅ **No Rate Limits** - Process as many videos as you want
- ✅ **Privacy** - All processing happens locally
- ✅ **High Accuracy** - State-of-the-art Whisper and BERT models

---

**Built with ❤️ for efficient video content processing**

**Now with FREE local transcription using OpenAI Whisper!** 🎉
