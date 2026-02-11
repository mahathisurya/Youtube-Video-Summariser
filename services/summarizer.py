"""
BERT-based extractive summarization service
"""
import logging
import torch
from transformers import BertTokenizer, BertModel
from typing import List, Dict, Tuple
import numpy as np
from utils.error_handlers import SummarizationError

logger = logging.getLogger(__name__)

class BERTSummarizer:
    """BERT-based extractive text summarizer"""
    
    def __init__(self, model_name: str = 'bert-base-uncased'):
        """
        Initialize BERT model for summarization
        
        Args:
            model_name: Name of BERT model to use
        """
        try:
            logger.info(f"Loading BERT model: {model_name}")
            self.tokenizer = BertTokenizer.from_pretrained(model_name)
            self.model = BertModel.from_pretrained(model_name)
            self.model.eval()
            
            # Use GPU if available
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            
            logger.info(f"BERT model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load BERT model: {str(e)}")
            raise SummarizationError(f"Failed to initialize summarizer: {str(e)}")
    
    def summarize(
        self, 
        text: str, 
        ratio: float = 0.3,
        min_sentences: int = 3,
        max_sentences: int = None
    ) -> Dict:
        """
        Generate extractive summary using BERT embeddings
        
        Args:
            text: Text to summarize
            ratio: Target ratio of summary length (0.1 to 0.5)
            min_sentences: Minimum number of sentences in summary
            max_sentences: Maximum number of sentences in summary
            
        Returns:
            Dictionary containing summary and statistics
        """
        try:
            if not text or not text.strip():
                raise SummarizationError("Text cannot be empty")
            
            logger.info(f"Starting summarization with ratio {ratio}")
            
            # Split text into sentences
            sentences = self._split_sentences(text)
            
            if len(sentences) < min_sentences:
                logger.warning("Text has fewer sentences than minimum, returning original text")
                return {
                    'summary': text,
                    'original_length': len(text),
                    'summary_length': len(text),
                    'reduction_ratio': 0.0,
                    'num_sentences': len(sentences),
                    'summary_sentences': len(sentences)
                }
            
            # Calculate number of sentences for summary
            num_summary_sentences = max(
                min_sentences,
                int(len(sentences) * ratio)
            )
            
            if max_sentences:
                num_summary_sentences = min(num_summary_sentences, max_sentences)
            
            logger.info(f"Selecting {num_summary_sentences} sentences from {len(sentences)} total")
            
            # Get sentence embeddings
            sentence_embeddings = self._get_sentence_embeddings(sentences)
            
            # Calculate sentence scores based on similarity to document embedding
            scores = self._calculate_sentence_scores(sentence_embeddings)
            
            # Select top sentences
            summary_sentences = self._select_top_sentences(
                sentences, 
                scores, 
                num_summary_sentences
            )
            
            # Generate summary
            summary = ' '.join(summary_sentences)
            
            # Calculate statistics
            original_length = len(text)
            summary_length = len(summary)
            reduction_ratio = 1 - (summary_length / original_length)
            
            result = {
                'summary': summary,
                'original_length': original_length,
                'summary_length': summary_length,
                'reduction_ratio': round(reduction_ratio, 2),
                'num_sentences': len(sentences),
                'summary_sentences': len(summary_sentences),
                'compression_percentage': round(reduction_ratio * 100, 1)
            }
            
            logger.info(f"Summarization complete: {result['compression_percentage']}% reduction")
            return result
            
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            raise SummarizationError(f"Error during summarization: {str(e)}")
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with NLTK)
        import re
        
        # Split on common sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter out empty sentences and very short ones
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        return sentences
    
    def _get_sentence_embeddings(self, sentences: List[str]) -> np.ndarray:
        """
        Get BERT embeddings for sentences
        
        Args:
            sentences: List of sentences
            
        Returns:
            Numpy array of sentence embeddings
        """
        embeddings = []
        
        with torch.no_grad():
            for sentence in sentences:
                # Tokenize and get BERT embeddings
                inputs = self.tokenizer(
                    sentence,
                    return_tensors='pt',
                    truncation=True,
                    max_length=512,
                    padding=True
                ).to(self.device)
                
                outputs = self.model(**inputs)
                
                # Use [CLS] token embedding as sentence representation
                sentence_embedding = outputs.last_hidden_state[0][0].cpu().numpy()
                embeddings.append(sentence_embedding)
        
        return np.array(embeddings)
    
    def _calculate_sentence_scores(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Calculate importance scores for sentences
        
        Args:
            embeddings: Sentence embeddings
            
        Returns:
            Array of sentence scores
        """
        # Calculate document embedding (mean of all sentence embeddings)
        doc_embedding = np.mean(embeddings, axis=0)
        
        # Calculate cosine similarity between each sentence and document
        scores = []
        for embedding in embeddings:
            similarity = self._cosine_similarity(embedding, doc_embedding)
            scores.append(similarity)
        
        return np.array(scores)
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _select_top_sentences(
        self, 
        sentences: List[str], 
        scores: np.ndarray, 
        num_sentences: int
    ) -> List[str]:
        """
        Select top-scoring sentences while maintaining order
        
        Args:
            sentences: List of sentences
            scores: Sentence scores
            num_sentences: Number of sentences to select
            
        Returns:
            List of selected sentences in original order
        """
        # Get indices of top-scoring sentences
        top_indices = np.argsort(scores)[-num_sentences:]
        
        # Sort indices to maintain original order
        top_indices = sorted(top_indices)
        
        # Select sentences
        selected_sentences = [sentences[i] for i in top_indices]
        
        return selected_sentences
    
    def summarize_with_keywords(
        self, 
        text: str, 
        keywords: List[str],
        ratio: float = 0.3
    ) -> Dict:
        """
        Generate summary with emphasis on specific keywords
        
        Args:
            text: Text to summarize
            keywords: List of keywords to emphasize
            ratio: Target ratio of summary length
            
        Returns:
            Dictionary containing summary and statistics
        """
        try:
            sentences = self._split_sentences(text)
            
            # Boost scores for sentences containing keywords
            sentence_embeddings = self._get_sentence_embeddings(sentences)
            scores = self._calculate_sentence_scores(sentence_embeddings)
            
            # Boost scores based on keyword presence
            for i, sentence in enumerate(sentences):
                keyword_count = sum(1 for keyword in keywords if keyword.lower() in sentence.lower())
                scores[i] += keyword_count * 0.1  # Boost factor
            
            num_summary_sentences = max(3, int(len(sentences) * ratio))
            summary_sentences = self._select_top_sentences(
                sentences, 
                scores, 
                num_summary_sentences
            )
            
            summary = ' '.join(summary_sentences)
            
            return {
                'summary': summary,
                'keywords_used': keywords,
                'summary_length': len(summary),
                'original_length': len(text),
                'reduction_ratio': round(1 - (len(summary) / len(text)), 2)
            }
            
        except Exception as e:
            logger.error(f"Keyword-based summarization error: {str(e)}")
            raise SummarizationError(f"Error during keyword summarization: {str(e)}")
