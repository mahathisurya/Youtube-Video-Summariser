# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  (Web Browser, Mobile App, CLI, Python Client, cURL, etc.)     │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK APPLICATION                           │
│                         (app.py)                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Endpoints                                            │  │
│  │  • POST /api/process      (Complete Pipeline)            │  │
│  │  • POST /api/transcribe   (Transcription Only)           │  │
│  │  • POST /api/translate    (Translation Only)             │  │
│  │  • POST /api/summarize    (Summarization Only)           │  │
│  │  • GET  /api/languages    (Supported Languages)          │  │
│  │  • GET  /                 (Health Check)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Middleware                                               │  │
│  │  • Request Validation                                     │  │
│  │  • Error Handling                                         │  │
│  │  • CORS Support                                           │  │
│  │  • Logging                                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   UTILS      │  │  VALIDATORS  │  │    ERROR     │
│              │  │              │  │   HANDLERS   │
│ • Helpers    │  │ • URL        │  │ • Retries    │
│ • Config     │  │ • Language   │  │ • Logging    │
│ • Logging    │  │ • Parameters │  │ • Recovery   │
└──────────────┘  └──────────────┘  └──────────────┘
                         │
        ┌────────────────┼────────────────────────┐
        ▼                ▼                        ▼
┌──────────────┐  ┌──────────────┐  ┌───────────────────┐
│   SERVICE    │  │   SERVICE    │  │     SERVICE       │
│              │  │              │  │                   │
│    VIDEO     │  │ TRANSCRIBE   │  │   TRANSLATION    │
│  DOWNLOADER  │  │              │  │                   │
│              │  │              │  │                   │
│ • pytube     │  │ • AssemblyAI │  │ • Googletrans    │
│ • moviepy    │  │ • Multi-lang │  │ • 100+ langs     │
│ • Extract    │  │ • Auto-detect│  │ • Chunking       │
└──────────────┘  └──────────────┘  └───────────────────┘
        │
        ▼
┌──────────────┐
│   SERVICE    │
│              │
│     BERT     │
│  SUMMARIZER  │
│              │
│ • Embeddings │
│ • Extractive │
│ • 60-70% ↓   │
└──────────────┘
        │
        ▼
┌──────────────────────────────────┐
│     EXTERNAL SERVICES            │
│                                  │
│  • YouTube (Video Content)      │
│  • AssemblyAI API (Transcribe)  │
│  • Google Translate (Translate) │
│  • HuggingFace (BERT Model)     │
└──────────────────────────────────┘
```

## Request Flow - Complete Pipeline

```
1. CLIENT REQUEST
   │
   ├─► POST /api/process
   │   {
   │     "video_url": "https://youtube.com/...",
   │     "source_language": "en",
   │     "target_language": "es",
   │     "summary_ratio": 0.3,
   │     "include_translation": true
   │   }
   │
   ▼
2. VALIDATION
   │
   ├─► Validate YouTube URL
   ├─► Validate language codes
   ├─► Validate summary ratio
   │
   ▼
3. VIDEO DOWNLOAD (video_downloader.py)
   │
   ├─► Download video from YouTube (pytube)
   ├─► Extract audio stream
   ├─► Convert to WAV format (moviepy)
   ├─► Save to temp_audio/
   │
   ▼
4. TRANSCRIPTION (transcription.py)
   │
   ├─► Upload audio to AssemblyAI
   ├─► Wait for transcription
   ├─► Receive text transcript
   ├─► Get word count, confidence
   │
   ▼
5. TRANSLATION (translation.py) [OPTIONAL]
   │
   ├─► Split text into chunks
   ├─► Translate each chunk via Google Translate
   ├─► Combine translated chunks
   │
   ▼
6. SUMMARIZATION (summarizer.py)
   │
   ├─► Split text into sentences
   ├─► Generate BERT embeddings
   ├─► Calculate sentence scores
   ├─► Select top sentences
   ├─► Maintain original order
   │
   ▼
7. CLEANUP
   │
   ├─► Delete temporary audio files
   ├─► Free up resources
   │
   ▼
8. RESPONSE
   │
   └─► {
         "success": true,
         "video_id": "...",
         "metadata": {...},
         "transcription": {...},
         "translation": {...},
         "summary": {...}
       }
```

## Data Flow Diagram

```
┌──────────────┐
│ YouTube URL  │
└──────┬───────┘
       │
       ▼
┌──────────────┐      ┌────────────────┐
│ Video File   │─────►│ Audio File     │
│ (MP4)        │      │ (WAV)          │
└──────────────┘      └────────┬───────┘
                               │
                               ▼
                      ┌────────────────┐
                      │ AssemblyAI     │
                      │ Transcription  │
                      └────────┬───────┘
                               │
                               ▼
                      ┌────────────────┐
                      │ Raw Transcript │
                      │ (5000 words)   │
                      └────────┬───────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
           ┌────────────────┐    ┌────────────────┐
           │ Original Lang  │    │ Translation    │
           │ (English)      │    │ (Spanish)      │
           └────────┬───────┘    └────────┬───────┘
                    │                     │
                    └──────────┬──────────┘
                               │
                               ▼
                      ┌────────────────┐
                      │ BERT Summarizer│
                      └────────┬───────┘
                               │
                               ▼
                      ┌────────────────┐
                      │ Summary        │
                      │ (1500 words)   │
                      │ 70% reduction  │
                      └────────────────┘
```

## Component Interaction Matrix

| Component | Depends On | Used By | Purpose |
|-----------|-----------|---------|---------|
| app.py | All services, utils | Client | API endpoints, routing |
| video_downloader | pytube, moviepy | app.py | Download & extract audio |
| transcription | AssemblyAI | app.py | Speech-to-text |
| translation | googletrans | app.py | Multi-language translation |
| summarizer | transformers, torch | app.py | Text summarization |
| validators | - | app.py | Input validation |
| error_handlers | - | All services | Error handling, retries |

## Technology Stack Layers

```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER              │
│  REST API (JSON) - Flask Routes         │
└─────────────────────────────────────────┘
              │
┌─────────────────────────────────────────┐
│         BUSINESS LOGIC LAYER            │
│  • Video Download Service               │
│  • Transcription Service                │
│  • Translation Service                  │
│  • Summarization Service                │
└─────────────────────────────────────────┘
              │
┌─────────────────────────────────────────┐
│         INFRASTRUCTURE LAYER            │
│  • Error Handling                       │
│  • Validation                           │
│  • Retry Logic                          │
│  • File Management                      │
│  • Logging                              │
└─────────────────────────────────────────┘
              │
┌─────────────────────────────────────────┐
│         EXTERNAL SERVICES               │
│  • YouTube API                          │
│  • AssemblyAI API                       │
│  • Google Translate API                 │
│  • HuggingFace Models                   │
└─────────────────────────────────────────┘
```

## Deployment Architecture

### Local Development
```
┌─────────────────┐
│   Developer     │
│    Machine      │
│                 │
│  ┌───────────┐  │
│  │  Python   │  │
│  │  venv     │  │
│  │           │  │
│  │  Flask    │  │
│  │  :5000    │  │
│  └───────────┘  │
└─────────────────┘
```

### Docker Deployment
```
┌─────────────────────────────────┐
│         Docker Host             │
│                                 │
│  ┌───────────────────────────┐  │
│  │    Docker Container       │  │
│  │                           │  │
│  │  ┌─────────────────────┐  │  │
│  │  │   Flask App         │  │  │
│  │  │   Port: 5000        │  │  │
│  │  └─────────────────────┘  │  │
│  │                           │  │
│  │  ┌─────────────────────┐  │  │
│  │  │   Volumes           │  │  │
│  │  │   • temp_videos     │  │  │
│  │  │   • temp_audio      │  │  │
│  │  │   • app.log         │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### Production Deployment (Kubernetes)
```
┌────────────────────────────────────────┐
│         Kubernetes Cluster             │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │        Load Balancer             │  │
│  └────────────┬─────────────────────┘  │
│               │                        │
│       ┌───────┼───────┐               │
│       ▼       ▼       ▼               │
│  ┌─────┐ ┌─────┐ ┌─────┐              │
│  │ Pod │ │ Pod │ │ Pod │              │
│  │ #1  │ │ #2  │ │ #3  │              │
│  └─────┘ └─────┘ └─────┘              │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │     Persistent Storage           │  │
│  │     (Shared temp files)          │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│         SECURITY LAYERS                 │
│                                         │
│  1. Input Validation Layer              │
│     • URL validation                    │
│     • Parameter sanitization            │
│     • Type checking                     │
│                                         │
│  2. Authentication Layer (Future)       │
│     • API keys                          │
│     • Rate limiting                     │
│                                         │
│  3. Environment Security                │
│     • .env for secrets                  │
│     • No hardcoded credentials          │
│                                         │
│  4. File System Security                │
│     • Temporary file cleanup            │
│     • Limited file access               │
│                                         │
│  5. Error Handling Security             │
│     • Generic error messages            │
│     • No sensitive data in logs         │
└─────────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- No session management
- Each request independent
- Load balancer ready

### Vertical Scaling
- GPU support for BERT
- Configurable resource limits
- Memory-efficient processing

### Caching Strategy (Future)
```
┌──────────┐
│  Redis   │◄──── Cache transcriptions
└──────────┘      Cache summaries
                  Cache translations
```

## Monitoring & Observability

```
┌─────────────────────────────────────────┐
│         LOGGING & MONITORING            │
│                                         │
│  1. Application Logs                    │
│     • app.log (rotating)                │
│     • ERROR, WARNING, INFO levels       │
│                                         │
│  2. Health Checks                       │
│     • GET / endpoint                    │
│     • Service availability              │
│                                         │
│  3. Performance Metrics (Future)        │
│     • Request duration                  │
│     • Error rates                       │
│     • API usage                         │
└─────────────────────────────────────────┘
```

---

**Architecture Status**: Production-Ready, Scalable, Maintainable
