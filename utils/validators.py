"""
Input validation utilities for YouTube Video Summarizer
"""
import re
import validators
from typing import Tuple, Optional

class VideoValidator:
    """Validates YouTube video URLs and parameters"""
    
    SUPPORTED_LANGUAGES = [
        'en', 'es', 'fr', 'de', 'it', 'pt', 'nl', 'ru', 'zh', 'ja',
        'ko', 'ar', 'hi', 'tr', 'pl', 'vi', 'th', 'id', 'ro', 'uk'
    ]
    
    # YouTube URL patterns
    YOUTUBE_PATTERNS = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',
    ]
    
    @staticmethod
    def validate_youtube_url(url: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate YouTube URL and extract video ID
        
        Args:
            url: YouTube video URL
            
        Returns:
            Tuple of (is_valid, video_id, error_message)
        """
        if not url or not isinstance(url, str):
            return False, None, "URL is required and must be a string"
        
        # Check if it's a valid URL format
        if not validators.url(url) and not any(re.match(pattern, url) for pattern in VideoValidator.YOUTUBE_PATTERNS):
            return False, None, "Invalid URL format"
        
        # Extract video ID
        for pattern in VideoValidator.YOUTUBE_PATTERNS:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                return True, video_id, None
        
        return False, None, "Could not extract video ID from URL"
    
    @staticmethod
    def validate_language_code(lang_code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate language code
        
        Args:
            lang_code: ISO 639-1 language code
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not lang_code or not isinstance(lang_code, str):
            return False, "Language code is required and must be a string"
        
        if lang_code.lower() not in VideoValidator.SUPPORTED_LANGUAGES:
            return False, f"Unsupported language. Supported languages: {', '.join(VideoValidator.SUPPORTED_LANGUAGES)}"
        
        return True, None
    
    @staticmethod
    def validate_summary_ratio(ratio: float) -> Tuple[bool, Optional[str]]:
        """
        Validate summary reduction ratio
        
        Args:
            ratio: Ratio of summary length to original (0.0 to 1.0)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(ratio, (int, float)):
            return False, "Summary ratio must be a number"
        
        if not 0.1 <= ratio <= 0.5:
            return False, "Summary ratio must be between 0.1 and 0.5 (10% to 50% of original)"
        
        return True, None
