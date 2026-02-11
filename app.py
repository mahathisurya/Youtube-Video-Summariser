"""
YouTube Video Summarizer - Flask Backend API
Multi-language transcription, translation, and BERT-based summarization
"""
import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from services.video_downloader import VideoDownloader
from services.transcription import TranscriptionService
from services.translation import TranslationService
from services.summarizer import BERTSummarizer
from utils.validators import VideoValidator
from utils.error_handlers import (
    handle_errors, 
    VideoProcessingError,
    logger as error_logger
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max request size
app.config['JSON_SORT_KEYS'] = False

# Initialize services (lazy loading for BERT model and Whisper)
video_downloader = VideoDownloader()
transcription_service = None  # Will be initialized on first use (Whisper model is large)
translation_service = TranslationService()
bert_summarizer = None  # Will be initialized on first use

def get_transcription_service():
    """Lazy initialization of Whisper transcription service"""
    global transcription_service
    if transcription_service is None:
        logger.info("Initializing Whisper transcription service...")
        model_size = os.getenv('WHISPER_MODEL_SIZE', 'base')
        transcription_service = TranscriptionService(model_size=model_size)
    return transcription_service

def get_summarizer():
    """Lazy initialization of BERT summarizer"""
    global bert_summarizer
    if bert_summarizer is None:
        logger.info("Initializing BERT summarizer...")
        bert_summarizer = BERTSummarizer()
    return bert_summarizer

@app.route('/')
def index():
    """Serve the web interface"""
    return render_template('index.html')

@app.route('/api')
@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'YouTube Video Summarizer API',
        'version': '1.0.0',
        'endpoints': {
            'process': '/api/process',
            'transcribe': '/api/transcribe',
            'translate': '/api/translate',
            'summarize': '/api/summarize',
            'languages': '/api/languages'
        }
    })

@app.route('/api/process', methods=['POST'])
@handle_errors
def process_video():
    """
    Complete pipeline: Download -> Transcribe -> Translate (optional) -> Summarize
    
    Request JSON:
    {
        "video_url": "YouTube URL",
        "source_language": "en" (optional, default: auto-detect),
        "target_language": "es" (optional, for translation),
        "summary_ratio": 0.3 (optional, 0.1-0.5, default: 0.3),
        "include_translation": true/false (optional, default: false)
    }
    """
    data = request.get_json()
    
    if not data:
        raise VideoProcessingError("Request body is required")
    
    video_url = data.get('video_url')
    source_language = data.get('source_language', 'en')
    target_language = data.get('target_language')
    summary_ratio = data.get('summary_ratio', 0.3)
    include_translation = data.get('include_translation', False)
    
    # Validate inputs
    is_valid, video_id, error_msg = VideoValidator.validate_youtube_url(video_url)
    if not is_valid:
        raise VideoProcessingError(error_msg)
    
    is_valid, error_msg = VideoValidator.validate_language_code(source_language)
    if not is_valid:
        raise VideoProcessingError(error_msg)
    
    if target_language:
        is_valid, error_msg = VideoValidator.validate_language_code(target_language)
        if not is_valid:
            raise VideoProcessingError(error_msg)
    
    is_valid, error_msg = VideoValidator.validate_summary_ratio(summary_ratio)
    if not is_valid:
        raise VideoProcessingError(error_msg)
    
    logger.info(f"Processing video: {video_id}")
    
    try:
        # Step 1: Download video and extract audio
        logger.info("Step 1: Downloading video and extracting audio...")
        audio_path, metadata = video_downloader.download_video(video_url, video_id)
        
        # Step 2: Transcribe audio
        logger.info("Step 2: Transcribing audio...")
        transcriber = get_transcription_service()
        transcription_result = transcriber.transcribe_audio(
            audio_path, 
            source_language
        )
        
        transcript_text = transcription_result['text']
        
        # Step 3: Translate (if requested)
        translation_result = None
        if include_translation and target_language and target_language != source_language:
            logger.info(f"Step 3: Translating to {target_language}...")
            translation_result = translation_service.translate_text(
                transcript_text,
                source_language,
                target_language
            )
            text_to_summarize = translation_result['translated_text']
        else:
            text_to_summarize = transcript_text
        
        # Step 4: Summarize
        logger.info("Step 4: Generating summary...")
        summarizer = get_summarizer()
        summary_result = summarizer.summarize(
            text_to_summarize,
            ratio=summary_ratio
        )
        
        # Cleanup temporary files
        video_downloader.cleanup(audio_path)
        
        # Prepare response
        response = {
            'success': True,
            'video_id': video_id,
            'metadata': metadata,
            'transcription': {
                'text': transcript_text,
                'language': transcription_result['language'],
                'word_count': transcription_result['word_count']
            },
            'summary': {
                'text': summary_result['summary'],
                'original_length': summary_result['original_length'],
                'summary_length': summary_result['summary_length'],
                'reduction_ratio': summary_result['reduction_ratio'],
                'compression_percentage': summary_result['compression_percentage']
            }
        }
        
        if translation_result:
            response['translation'] = {
                'text': translation_result['translated_text'],
                'source_language': translation_result['source_language'],
                'target_language': translation_result['target_language'],
                'word_count': translation_result['word_count']
            }
        
        logger.info(f"Processing complete for video {video_id}")
        return jsonify(response), 200
        
    except Exception as e:
        # Cleanup on error
        video_downloader.cleanup_all()
        raise

@app.route('/api/transcribe', methods=['POST'])
@handle_errors
def transcribe_video():
    """
    Transcribe video only
    
    Request JSON:
    {
        "video_url": "YouTube URL",
        "source_language": "en" (optional, default: auto-detect)
    }
    """
    data = request.get_json()
    
    if not data:
        raise VideoProcessingError("Request body is required")
    
    video_url = data.get('video_url')
    source_language = data.get('source_language', 'en')
    
    # Validate inputs
    is_valid, video_id, error_msg = VideoValidator.validate_youtube_url(video_url)
    if not is_valid:
        raise VideoProcessingError(error_msg)
    
    is_valid, error_msg = VideoValidator.validate_language_code(source_language)
    if not is_valid:
        raise VideoProcessingError(error_msg)
    
    try:
        # Download and transcribe
        audio_path, metadata = video_downloader.download_video(video_url, video_id)
        transcriber = get_transcription_service()
        transcription_result = transcriber.transcribe_audio(audio_path, source_language)
        
        # Cleanup
        video_downloader.cleanup(audio_path)
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'metadata': metadata,
            'transcription': transcription_result
        }), 200
        
    except Exception as e:
        video_downloader.cleanup_all()
        raise

@app.route('/api/translate', methods=['POST'])
@handle_errors
def translate_text():
    """
    Translate text
    
    Request JSON:
    {
        "text": "Text to translate",
        "source_language": "en" (optional, default: auto),
        "target_language": "es" (required)
    }
    """
    data = request.get_json()
    
    if not data:
        raise VideoProcessingError("Request body is required")
    
    text = data.get('text')
    source_language = data.get('source_language', 'auto')
    target_language = data.get('target_language')
    
    if not text:
        raise VideoProcessingError("Text is required")
    
    if not target_language:
        raise VideoProcessingError("Target language is required")
    
    # Translate
    result = translation_service.translate_text(text, source_language, target_language)
    
    return jsonify({
        'success': True,
        'translation': result
    }), 200

@app.route('/api/summarize', methods=['POST'])
@handle_errors
def summarize_text():
    """
    Summarize text using BERT
    
    Request JSON:
    {
        "text": "Text to summarize",
        "ratio": 0.3 (optional, 0.1-0.5, default: 0.3)
    }
    """
    data = request.get_json()
    
    if not data:
        raise VideoProcessingError("Request body is required")
    
    text = data.get('text')
    ratio = data.get('ratio', 0.3)
    
    if not text:
        raise VideoProcessingError("Text is required")
    
    is_valid, error_msg = VideoValidator.validate_summary_ratio(ratio)
    if not is_valid:
        raise VideoProcessingError(error_msg)
    
    # Summarize
    summarizer = get_summarizer()
    result = summarizer.summarize(text, ratio=ratio)
    
    return jsonify({
        'success': True,
        'summary': result
    }), 200

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    return jsonify({
        'success': True,
        'languages': {
            'transcription': VideoValidator.SUPPORTED_LANGUAGES,
            'translation': list(translation_service.get_supported_languages().keys())
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting YouTube Video Summarizer API on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
