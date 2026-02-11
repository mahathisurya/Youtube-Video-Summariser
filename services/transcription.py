"""
Whisper transcription service (Local, Free, No API Key Required)
"""
import os
import logging
import whisper
from typing import Dict
from utils.error_handlers import TranscriptionError, retry_on_failure

logger = logging.getLogger(__name__)

class TranscriptionService:
    """Handles audio transcription using OpenAI's Whisper (runs locally)"""
    
    # Language mapping for Whisper
    LANGUAGE_MAP = {
        'en': 'english',
        'es': 'spanish',
        'fr': 'french',
        'de': 'german',
        'it': 'italian',
        'pt': 'portuguese',
        'nl': 'dutch',
        'ru': 'russian',
        'zh': 'chinese',
        'ja': 'japanese',
        'ko': 'korean',
        'ar': 'arabic',
        'hi': 'hindi',
        'tr': 'turkish',
        'pl': 'polish',
        'vi': 'vietnamese',
        'th': 'thai',
        'id': 'indonesian',
        'ro': 'romanian',
        'uk': 'ukrainian',
    }
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
                       - tiny: fastest, least accurate
                       - base: good balance (recommended)
                       - small: better accuracy
                       - medium/large: best accuracy but slower
        """
        try:
            logger.info(f"Loading Whisper model: {model_size}")
            self.model = whisper.load_model(model_size)
            logger.info(f"Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            raise TranscriptionError(f"Failed to initialize transcription service: {str(e)}")
    
    @retry_on_failure(max_retries=2, delay=3.0)
    def transcribe_audio(
        self, 
        audio_path: str, 
        source_language: str = 'en',
        include_timestamps: bool = False
    ) -> Dict:
        """
        Transcribe audio file using Whisper
        
        Args:
            audio_path: Path to audio file
            source_language: Source language code
            include_timestamps: Whether to include word-level timestamps
            
        Returns:
            Dictionary containing transcription results
        """
        try:
            logger.info(f"Starting transcription for {audio_path} in language {source_language}")
            
            # Validate language
            if source_language not in self.LANGUAGE_MAP:
                logger.warning(f"Language {source_language} not in map, using auto-detection")
                language = None
            else:
                language = self.LANGUAGE_MAP[source_language]
            
            # Transcribe audio file
            logger.info("Transcribing audio with Whisper...")
            result = self.model.transcribe(
                audio_path,
                language=language,
                verbose=False,
                word_timestamps=include_timestamps
            )
            
            # Extract text
            text = result['text'].strip()
            
            if not text:
                raise TranscriptionError("Transcription resulted in empty text")
            
            # Prepare result
            transcription_result = {
                'text': text,
                'language': result.get('language', source_language),
                'confidence': None,  # Whisper doesn't provide confidence scores
                'word_count': len(text.split()),
                'duration': None
            }
            
            # Add segments/timestamps if requested
            if include_timestamps and 'segments' in result:
                transcription_result['segments'] = [
                    {
                        'text': segment['text'],
                        'start': segment['start'],
                        'end': segment['end']
                    }
                    for segment in result['segments']
                ]
            
            logger.info(f"Transcription complete: {transcription_result['word_count']} words")
            return transcription_result
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            raise TranscriptionError(f"Error during transcription: {str(e)}")
    
    def transcribe_with_auto_detect(self, audio_path: str) -> Dict:
        """
        Transcribe audio with automatic language detection
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary containing transcription results
        """
        try:
            logger.info(f"Starting transcription with auto language detection for {audio_path}")
            
            # Transcribe without specifying language
            result = self.model.transcribe(
                audio_path,
                verbose=False
            )
            
            text = result['text'].strip()
            detected_language = result.get('language', 'en')
            
            transcription_result = {
                'text': text,
                'language': detected_language,
                'confidence': None,
                'word_count': len(text.split()),
                'auto_detected': True
            }
            
            logger.info(f"Transcription complete. Detected language: {detected_language}")
            return transcription_result
            
        except Exception as e:
            logger.error(f"Auto-detect transcription error: {str(e)}")
            raise TranscriptionError(f"Error during auto-detect transcription: {str(e)}")
