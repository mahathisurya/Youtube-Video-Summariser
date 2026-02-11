"""
Translation service using Deep Translator
"""
import logging
from deep_translator import GoogleTranslator
from typing import Dict, List
from utils.error_handlers import TranslationError, retry_on_failure

logger = logging.getLogger(__name__)

class TranslationService:
    """Handles text translation using Google Translate via Deep Translator"""
    
    def __init__(self):
        """Initialize Google Translator"""
        # Deep Translator doesn't need initialization
        logger.info("Translation service initialized")
    
    @retry_on_failure(max_retries=3, delay=1.0)
    def translate_text(
        self, 
        text: str, 
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Dict:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code (use 'auto' for auto-detection)
            target_lang: Target language code
            
        Returns:
            Dictionary containing translation results
        """
        try:
            if not text or not text.strip():
                raise TranslationError("Text cannot be empty")
            
            # Validate target language
            supported_langs = GoogleTranslator().get_supported_languages(as_dict=True)
            if target_lang not in supported_langs.values():
                raise TranslationError(f"Unsupported target language: {target_lang}")
            
            logger.info(f"Translating text from {source_lang} to {target_lang}")
            
            # For large texts, split into chunks to avoid API limits
            chunks = self._split_text(text, max_length=4500)
            translated_chunks = []
            detected_lang = source_lang
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Translating chunk {i+1}/{len(chunks)}")
                
                # Create translator for this chunk
                translator = GoogleTranslator(
                    source=source_lang,
                    target=target_lang
                )
                
                translated_chunk = translator.translate(chunk)
                translated_chunks.append(translated_chunk)
            
            # Combine translated chunks
            translated_text = ' '.join(translated_chunks)
            
            result = {
                'original_text': text,
                'translated_text': translated_text,
                'source_language': source_lang if source_lang != 'auto' else 'auto-detected',
                'target_language': target_lang,
                'word_count': len(translated_text.split())
            }
            
            logger.info(f"Translation complete: {result['word_count']} words")
            return result
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise TranslationError(f"Error during translation: {str(e)}")
    
    def translate_to_multiple_languages(
        self, 
        text: str, 
        target_languages: List[str],
        source_lang: str = 'auto'
    ) -> Dict[str, Dict]:
        """
        Translate text to multiple target languages
        
        Args:
            text: Text to translate
            target_languages: List of target language codes
            source_lang: Source language code
            
        Returns:
            Dictionary mapping language codes to translation results
        """
        results = {}
        
        for lang in target_languages:
            try:
                result = self.translate_text(text, source_lang, lang)
                results[lang] = result
                logger.info(f"Successfully translated to {lang}")
            except Exception as e:
                logger.error(f"Failed to translate to {lang}: {str(e)}")
                results[lang] = {
                    'error': str(e),
                    'success': False
                }
        
        return results
    
    def detect_language(self, text: str) -> Dict:
        """
        Detect the language of given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing detected language information
        """
        try:
            if not text or not text.strip():
                raise TranslationError("Text cannot be empty")
            
            logger.info("Detecting language...")
            
            # Use GoogleTranslator to detect language
            from deep_translator import single_detection
            detected_lang = single_detection(text, api_key=None)
            
            supported_langs = GoogleTranslator().get_supported_languages(as_dict=True)
            lang_name = next((k for k, v in supported_langs.items() if v == detected_lang), detected_lang)
            
            result = {
                'language': detected_lang,
                'language_name': lang_name,
                'confidence': 1.0  # Deep translator doesn't provide confidence scores
            }
            
            logger.info(f"Detected language: {result['language_name']}")
            return result
            
        except Exception as e:
            logger.error(f"Language detection error: {str(e)}")
            raise TranslationError(f"Error during language detection: {str(e)}")
    
    def _split_text(self, text: str, max_length: int = 5000) -> List[str]:
        """
        Split text into chunks for translation
        
        Args:
            text: Text to split
            max_length: Maximum length per chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]
        
        # Split by sentences to maintain context
        sentences = text.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """
        Get all supported languages
        
        Returns:
            Dictionary mapping language codes to language names
        """
        try:
            # Get supported languages from GoogleTranslator
            translator = GoogleTranslator()
            langs = translator.get_supported_languages(as_dict=True)
            # Return with language codes as keys (swap key-value)
            return {v: k for k, v in langs.items()}
        except Exception:
            # Fallback to common languages
            return {
                'en': 'english', 'es': 'spanish', 'fr': 'french', 
                'de': 'german', 'it': 'italian', 'pt': 'portuguese',
                'nl': 'dutch', 'ru': 'russian', 'zh': 'chinese',
                'ja': 'japanese', 'ko': 'korean', 'ar': 'arabic',
                'hi': 'hindi', 'tr': 'turkish', 'pl': 'polish'
            }
