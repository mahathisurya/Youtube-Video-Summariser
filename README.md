# YouTube Video Summarizer 🎥📝

A powerful Flask-based backend service for multi-language YouTube video transcription, translation, and summarization. This project implements a sophisticated NLP pipeline that processes videos up to 1+ hour across multiple languages, reducing transcript length by 60-70% while preserving key information.

## ✨ Features

- **Multi-Language Transcription**: Support for 10+ languages using AssemblyAI's speech-to-text API
- **Accurate Translation**: Powered by Google Translate for translation to multiple target languages
- **BERT-Based Summarization**: Extractive summarization using BERT embeddings with 60-70% text reduction
- **Robust Error Handling**: Built-in validation, retry mechanisms, and error recovery
- **Long-Form Content Support**: Process videos up to 1+ hour in various audio/video formats
- **RESTful API**: Clean, well-documented API endpoints
- **Production-Ready**: Comprehensive logging, environment configuration, and error handling

## 🏗️ Architecture

```
┌─────────────────┐
│  YouTube Video  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Video Download  │  (pytube)
│ Audio Extract   │  (moviepy)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Transcription  │  (AssemblyAI)
│   10+ Languages │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Translation   │  (Googletrans)
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
- AssemblyAI API key ([Get one free here](https://www.assemblyai.com/))

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

4. **Set up environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your AssemblyAI API key
# ASSEMBLYAI_API_KEY=your_api_key_here
```

5. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "success": true,
  "message": "YouTube Video Summarizer API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

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
    "word_count": 5000,
    "confidence": 0.95
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

The system supports 10+ languages including:

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

Create a `.env` file based on `.env.example`:

```env
# AssemblyAI API Key (Required)
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Optional: Set max video duration in seconds (default: 7200 = 2 hours)
MAX_VIDEO_DURATION=7200
```

### Configuration Options

- **MAX_VIDEO_DURATION**: Maximum allowed video duration in seconds (default: 7200)
- **PORT**: Server port (default: 5000)
- **FLASK_DEBUG**: Enable debug mode (default: True)

## 📁 Project Structure

```
xyz/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
│
├── services/                  # Core services
│   ├── __init__.py
│   ├── video_downloader.py    # YouTube download & audio extraction
│   ├── transcription.py       # AssemblyAI integration
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
- **Library**: pytube, moviepy
- **Process**: Downloads YouTube video, extracts audio, converts to WAV
- **Features**: Retry mechanism, format validation, duration limits

### 2. Speech-to-Text Transcription
- **Service**: AssemblyAI
- **Features**: Multi-language support, auto language detection, high accuracy
- **Error Handling**: Automatic retries, status monitoring

### 3. Translation
- **Library**: googletrans
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

- **Video Duration**: Supports videos up to 1+ hour (configurable)
- **Model Loading**: BERT model lazy-loaded on first summarization request
- **GPU Support**: Automatically uses GPU if available for faster summarization
- **File Cleanup**: Automatic cleanup of temporary files
- **Memory Management**: Efficient handling of large transcripts

## 🔒 Security Best Practices

1. **API Keys**: Store sensitive keys in `.env` file (never commit)
2. **Input Validation**: All inputs validated before processing
3. **File Size Limits**: 100MB max request size
4. **Temporary Files**: Automatic cleanup after processing
5. **Error Messages**: Generic error messages to prevent information leakage

## 🐛 Troubleshooting

### Common Issues

**1. "AssemblyAI API key not found"**
- Ensure `.env` file exists and contains `ASSEMBLYAI_API_KEY`
- Check that `.env` is in the project root directory

**2. "Video download failed"**
- Check if video is available and not restricted
- Verify internet connection
- Try a different video URL

**3. "BERT model loading error"**
- Ensure sufficient disk space (model ~400MB)
- Check internet connection for initial download
- Try running with `pip install --upgrade transformers`

**4. "Module not found" errors**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**5. Video too long**
- Adjust `MAX_VIDEO_DURATION` in `.env`
- Or process shorter videos

## 📈 Future Enhancements

- [ ] Support for subtitle/caption extraction
- [ ] Abstractive summarization using T5/GPT models
- [ ] Batch processing for multiple videos
- [ ] WebSocket support for real-time progress updates
- [ ] Database integration for caching results
- [ ] Frontend web interface
- [ ] Docker containerization
- [ ] API rate limiting and authentication

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions:
1. Check the Troubleshooting section
2. Review the API documentation
3. Check application logs in `app.log`

## 🎓 Credits

Built with:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [AssemblyAI](https://www.assemblyai.com/) - Speech-to-text API
- [Google Translate](https://pypi.org/project/googletrans/) - Translation
- [Transformers](https://huggingface.co/transformers/) - BERT models
- [pytube](https://pytube.io/) - YouTube video download
- [moviepy](https://zulko.github.io/moviepy/) - Audio extraction

---

**Built with ❤️ for efficient video content processing**
