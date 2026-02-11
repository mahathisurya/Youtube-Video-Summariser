"""
Error handling utilities for YouTube Video Summarizer
"""
import logging
from functools import wraps
from flask import jsonify
from typing import Callable, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VideoProcessingError(Exception):
    """Base exception for video processing errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class VideoDownloadError(VideoProcessingError):
    """Exception raised when video download fails"""
    pass

class TranscriptionError(VideoProcessingError):
    """Exception raised when transcription fails"""
    pass

class TranslationError(VideoProcessingError):
    """Exception raised when translation fails"""
    pass

class SummarizationError(VideoProcessingError):
    """Exception raised when summarization fails"""
    pass

def handle_errors(func: Callable) -> Callable:
    """
    Decorator for handling errors in route functions
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except VideoProcessingError as e:
            logger.error(f"Video processing error: {e.message}")
            return jsonify({
                'success': False,
                'error': e.message,
                'error_type': type(e).__name__
            }), e.status_code
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'An unexpected error occurred. Please try again.',
                'error_type': 'InternalServerError'
            }), 500
    return wrapper

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator for retrying failed operations
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            import time
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
            
            # If all retries failed, raise the last exception
            logger.error(f"All {max_retries} attempts failed")
            raise last_exception
        return wrapper
    return decorator
