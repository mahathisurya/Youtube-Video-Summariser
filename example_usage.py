"""
Example usage of YouTube Video Summarizer API
Demonstrates how to use the API programmatically
"""
import requests
import json
from typing import Dict, Optional

class VideoSummarizerClient:
    """Client for YouTube Video Summarizer API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def process_video(
        self,
        video_url: str,
        source_language: str = "en",
        target_language: Optional[str] = None,
        summary_ratio: float = 0.3,
        include_translation: bool = False
    ) -> Dict:
        """
        Process a YouTube video through complete pipeline
        
        Args:
            video_url: YouTube video URL
            source_language: Source language code
            target_language: Target language for translation
            summary_ratio: Summary compression ratio (0.1-0.5)
            include_translation: Whether to include translation
            
        Returns:
            API response dictionary
        """
        data = {
            "video_url": video_url,
            "source_language": source_language,
            "summary_ratio": summary_ratio,
            "include_translation": include_translation
        }
        
        if target_language:
            data["target_language"] = target_language
        
        response = requests.post(
            f"{self.base_url}/api/process",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
    
    def transcribe_video(
        self,
        video_url: str,
        source_language: str = "en"
    ) -> Dict:
        """Transcribe a YouTube video"""
        data = {
            "video_url": video_url,
            "source_language": source_language
        }
        
        response = requests.post(
            f"{self.base_url}/api/transcribe",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
    
    def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: str = "auto"
    ) -> Dict:
        """Translate text"""
        data = {
            "text": text,
            "source_language": source_language,
            "target_language": target_language
        }
        
        response = requests.post(
            f"{self.base_url}/api/translate",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
    
    def summarize_text(
        self,
        text: str,
        ratio: float = 0.3
    ) -> Dict:
        """Summarize text"""
        data = {
            "text": text,
            "ratio": ratio
        }
        
        response = requests.post(
            f"{self.base_url}/api/summarize",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
    
    def get_supported_languages(self) -> Dict:
        """Get list of supported languages"""
        response = requests.get(f"{self.base_url}/api/languages")
        return response.json()


def example_1_basic_summary():
    """Example 1: Basic video summarization"""
    print("\n" + "="*60)
    print("Example 1: Basic Video Summarization")
    print("="*60)
    
    client = VideoSummarizerClient()
    
    # Replace with actual video URL
    video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
    
    print(f"\n📹 Processing video: {video_url}")
    print("⏳ This may take a few minutes...")
    
    result = client.process_video(
        video_url=video_url,
        source_language="en",
        summary_ratio=0.3
    )
    
    if result.get('success'):
        print("\n✅ Success!")
        print(f"\n📊 Video: {result['metadata']['title']}")
        print(f"⏱️  Duration: {result['metadata']['duration']} seconds")
        print(f"\n📝 Transcript: {result['transcription']['word_count']} words")
        print(f"\n✂️  Summary: {result['summary']['word_count']} words")
        print(f"📉 Reduction: {result['summary']['compression_percentage']}%")
        print(f"\n💬 Summary:\n{result['summary']['text'][:500]}...")
    else:
        print(f"\n❌ Error: {result.get('error')}")


def example_2_with_translation():
    """Example 2: Transcribe, translate, and summarize"""
    print("\n" + "="*60)
    print("Example 2: Transcribe, Translate & Summarize")
    print("="*60)
    
    client = VideoSummarizerClient()
    
    video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
    
    print(f"\n📹 Processing video: {video_url}")
    print("🌐 Translating to Spanish...")
    print("⏳ This may take a few minutes...")
    
    result = client.process_video(
        video_url=video_url,
        source_language="en",
        target_language="es",
        summary_ratio=0.25,
        include_translation=True
    )
    
    if result.get('success'):
        print("\n✅ Success!")
        print(f"\n📊 Video: {result['metadata']['title']}")
        print(f"\n🇬🇧 Original: {result['transcription']['word_count']} words")
        print(f"🇪🇸 Translated: {result['translation']['word_count']} words")
        print(f"✂️  Summary: {result['summary']['compression_percentage']}% reduction")
        print(f"\n💬 Spanish Summary:\n{result['summary']['text'][:500]}...")
    else:
        print(f"\n❌ Error: {result.get('error')}")


def example_3_just_transcribe():
    """Example 3: Just transcribe a video"""
    print("\n" + "="*60)
    print("Example 3: Transcribe Only")
    print("="*60)
    
    client = VideoSummarizerClient()
    
    video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
    
    print(f"\n📹 Transcribing video: {video_url}")
    
    result = client.transcribe_video(
        video_url=video_url,
        source_language="en"
    )
    
    if result.get('success'):
        print("\n✅ Success!")
        print(f"\n📊 Video: {result['metadata']['title']}")
        print(f"📝 Transcript: {result['transcription']['word_count']} words")
        print(f"\n💬 Transcript:\n{result['transcription']['text'][:500]}...")
    else:
        print(f"\n❌ Error: {result.get('error')}")


def example_4_text_operations():
    """Example 4: Translate and summarize text directly"""
    print("\n" + "="*60)
    print("Example 4: Direct Text Operations")
    print("="*60)
    
    client = VideoSummarizerClient()
    
    # Sample long text
    sample_text = """
    Artificial intelligence (AI) is revolutionizing industries across the globe. 
    From healthcare to finance, AI applications are transforming how we work and live. 
    Machine learning algorithms can now diagnose diseases, predict market trends, and 
    even create art. Natural language processing enables computers to understand and 
    generate human language with remarkable accuracy. Computer vision allows machines 
    to interpret and analyze visual information from the world around us. As AI 
    technology continues to advance, we're seeing breakthroughs in autonomous vehicles, 
    personalized medicine, and climate modeling. However, these advances also raise 
    important ethical questions about privacy, bias, and the future of work. Researchers 
    and policymakers are working together to ensure AI develops in a responsible and 
    beneficial way for all of humanity.
    """
    
    # Summarize
    print("\n📝 Summarizing text...")
    summary_result = client.summarize_text(sample_text, ratio=0.3)
    
    if summary_result.get('success'):
        print(f"\n✅ Summary complete!")
        print(f"📉 Reduction: {summary_result['summary']['compression_percentage']}%")
        print(f"\n💬 Summary:\n{summary_result['summary']['summary']}")
    
    # Translate
    print("\n\n🌐 Translating to French...")
    translation_result = client.translate_text(
        summary_result['summary']['summary'],
        target_language="fr"
    )
    
    if translation_result.get('success'):
        print(f"\n✅ Translation complete!")
        print(f"\n💬 French:\n{translation_result['translation']['translated_text']}")


def example_5_supported_languages():
    """Example 5: Get supported languages"""
    print("\n" + "="*60)
    print("Example 5: Supported Languages")
    print("="*60)
    
    client = VideoSummarizerClient()
    
    result = client.get_supported_languages()
    
    if result.get('success'):
        print("\n✅ Supported Languages:")
        print(f"\n🎤 Transcription: {len(result['languages']['transcription'])} languages")
        print(f"   {', '.join(result['languages']['transcription'][:10])}...")
        print(f"\n🌐 Translation: {len(result['languages']['translation'])} languages")
        print(f"   {', '.join(list(result['languages']['translation'].keys())[:10])}...")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("🎬 YouTube Video Summarizer - Usage Examples")
    print("="*60)
    print("\n⚠️  Note: Replace 'YOUR_VIDEO_ID' with actual YouTube video IDs")
    print("⚠️  Make sure the Flask server is running at http://localhost:5000")
    
    # Run examples that don't require video URLs
    try:
        example_4_text_operations()
        example_5_supported_languages()
        
        # Uncomment to run video examples (requires actual video URLs)
        # example_1_basic_summary()
        # example_2_with_translation()
        # example_3_just_transcribe()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("   Make sure the Flask server is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "="*60)
    print("✅ Examples Complete!")
    print("="*60)


if __name__ == "__main__":
    main()
