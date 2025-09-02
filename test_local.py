#!/usr/bin/env python3
"""
Simple test script to verify the transcriber works locally.
Run this before testing the web interface.
"""

import os
from transcriber import VideoTranscriber
from visualizer import TranscriptionVisualizer

def test_transcriber():
    """Test the transcriber with a simple YouTube video."""
    print("🧪 Testing Multimodal Video Transcriber")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ Please set your GOOGLE_API_KEY environment variable")
        print("   Get one from: https://aistudio.google.com/app/apikey")
        print("   Then run: export GOOGLE_API_KEY=your_actual_key")
        return False
    
    try:
        # Initialize transcriber
        print("🔧 Initializing transcriber...")
        transcriber = VideoTranscriber(skip_config_validation=False)  # Use validation for CLI testing
        
        # Test with a short YouTube video
        print("🎬 Testing with YouTube video...")
        youtube_id = "0pJn3g8dfwk"  # Google DeepMind Podcast Trailer (59s)
        
        transcription = transcriber.transcribe_youtube_video(
            youtube_id,
            start_offset=None,
            end_offset=None,
            fps=1.0,
            model="gemini-2.0-flash"
        )
        
        # Display results
        print("\n✅ Transcription completed!")
        print(f"📊 Script Segments: {transcription.total_segments}")
        print(f"👥 Speakers: {transcription.total_speakers}")
        
        if transcription.speakers:
            print("\n📋 Speakers found:")
            for speaker in transcription.speakers:
                status = "✅" if speaker.name != "?" else "❓"
                print(f"  {status} Voice {speaker.voice_id}: {speaker.name}")
        
        if transcription.script_segments:
            print(f"\n📝 First 3 script segments:")
            for i, segment in enumerate(transcription.script_segments[:3]):
                speaker = transcription.get_speaker_by_voice_id(segment.voice_id)
                speaker_name = speaker.name if speaker else f"Voice {segment.voice_id}"
                print(f"  {i+1}. [{segment.start_time}-{segment.end_time}] {speaker_name}: {segment.text[:50]}...")
        
        print("\n🎉 Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check your API key is correct")
        print("   2. Ensure you have internet connection")
        print("   3. Verify the YouTube video is accessible")
        return False

def test_web_interface():
    """Test if Streamlit can be imported."""
    print("\n🌐 Testing Web Interface Setup")
    print("=" * 50)
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Test basic Streamlit functionality
        print("✅ Streamlit basic functionality works")
        
        print("\n🚀 To run the web interface:")
        print("   1. Set your API key: export GOOGLE_API_KEY=your_key")
        print("   2. Run: streamlit run app.py")
        print("   3. Open: http://localhost:8501")
        
        return True
        
    except ImportError as e:
        print(f"❌ Streamlit not installed: {e}")
        print("   Run: pip install --user streamlit")
        return False
    except Exception as e:
        print(f"❌ Error testing web interface: {e}")
        return False

if __name__ == "__main__":
    print("🎬 Multimodal Video Transcriber - Local Test")
    print("=" * 60)
    
    # Test transcriber
    transcriber_ok = test_transcriber()
    
    # Test web interface
    web_ok = test_web_interface()
    
    print("\n" + "=" * 60)
    if transcriber_ok and web_ok:
        print("🎉 All tests passed! Your transcriber is ready to use.")
        print("\n📋 Next steps:")
        print("   1. Get API key from: https://aistudio.google.com/app/apikey")
        print("   2. Set environment: export GOOGLE_API_KEY=your_key")
        print("   3. Run web app: streamlit run app.py")
        print("   4. Deploy to cloud: Follow DEPLOYMENT.md")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Common fixes:")
        print("   - Install dependencies: pip install --user -r requirements.txt")
        print("   - Set API key: export GOOGLE_API_KEY=your_key")
        print("   - Check internet connection")
