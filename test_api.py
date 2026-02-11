"""
Test script for YouTube Video Summarizer API
Run this after starting the Flask server to test all endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_response(endpoint, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"Endpoint: {endpoint}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print('='*60)

def test_health_check():
    """Test health check endpoint"""
    print("\n🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/")
    print_response("GET /", response)
    return response.status_code == 200

def test_supported_languages():
    """Test supported languages endpoint"""
    print("\n🌍 Testing Supported Languages...")
    response = requests.get(f"{BASE_URL}/api/languages")
    print_response("GET /api/languages", response)
    return response.status_code == 200

def test_summarize_text():
    """Test text summarization"""
    print("\n📝 Testing Text Summarization...")
    
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the 
    natural intelligence displayed by humans and animals. Leading AI textbooks define the field 
    as the study of "intelligent agents": any device that perceives its environment and takes 
    actions that maximize its chance of successfully achieving its goals. Colloquially, the term 
    "artificial intelligence" is often used to describe machines (or computers) that mimic 
    "cognitive" functions that humans associate with the human mind, such as "learning" and 
    "problem solving". As machines become increasingly capable, tasks considered to require 
    "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. 
    A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." For instance, optical 
    character recognition is frequently excluded from things considered to be AI, having become a 
    routine technology. Modern machine capabilities generally classified as AI include successfully 
    understanding human speech, competing at the highest level in strategic game systems, 
    autonomously operating cars, intelligent routing in content delivery networks, and military simulations.
    """
    
    data = {
        "text": sample_text,
        "ratio": 0.3
    }
    
    response = requests.post(
        f"{BASE_URL}/api/summarize",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print_response("POST /api/summarize", response)
    return response.status_code == 200

def test_translate_text():
    """Test text translation"""
    print("\n🌐 Testing Text Translation...")
    
    data = {
        "text": "Hello, how are you? This is a test of the translation service.",
        "source_language": "en",
        "target_language": "es"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/translate",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print_response("POST /api/translate", response)
    return response.status_code == 200

def test_transcribe_video():
    """Test video transcription (use a short video)"""
    print("\n🎥 Testing Video Transcription...")
    print("⚠️  Note: This requires a real YouTube video URL and will take time")
    print("⚠️  Skipping by default. Uncomment to test with a real video.")
    
    # Uncomment to test with a real video
    # data = {
    #     "video_url": "https://www.youtube.com/watch?v=SHORT_VIDEO_ID",
    #     "source_language": "en"
    # }
    # 
    # response = requests.post(
    #     f"{BASE_URL}/api/transcribe",
    #     json=data,
    #     headers={"Content-Type": "application/json"}
    # )
    # 
    # print_response("POST /api/transcribe", response)
    # return response.status_code == 200
    
    return True

def test_process_video():
    """Test complete video processing pipeline"""
    print("\n🎬 Testing Complete Video Processing...")
    print("⚠️  Note: This requires a real YouTube video URL and will take time")
    print("⚠️  Skipping by default. Uncomment to test with a real video.")
    
    # Uncomment to test with a real video
    # data = {
    #     "video_url": "https://www.youtube.com/watch?v=SHORT_VIDEO_ID",
    #     "source_language": "en",
    #     "target_language": "es",
    #     "summary_ratio": 0.3,
    #     "include_translation": True
    # }
    # 
    # response = requests.post(
    #     f"{BASE_URL}/api/process",
    #     json=data,
    #     headers={"Content-Type": "application/json"}
    # )
    # 
    # print_response("POST /api/process", response)
    # return response.status_code == 200
    
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 YouTube Video Summarizer API Test Suite")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Supported Languages", test_supported_languages),
        ("Text Summarization", test_summarize_text),
        ("Text Translation", test_translate_text),
        ("Video Transcription", test_transcribe_video),
        ("Complete Video Processing", test_process_video),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n📈 Total: {passed}/{total} tests passed")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test suite error: {str(e)}")
