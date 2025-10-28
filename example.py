"""
Example script demonstrating how to use the multimodal video transcriber.
"""

from datetime import timedelta
from transcriber import VideoTranscriber
from visualizer import TranscriptionVisualizer
from config import Config

def example_basic_transcription():
    """Example 1: Basic transcription of a YouTube video."""
    print("🎬 Example 1: Basic YouTube Transcription")
    print("-" * 50)
    
    transcriber = VideoTranscriber()
    visualizer = TranscriptionVisualizer()
    
    # Transcribe a short YouTube video
    youtube_id = "0pJn3g8dfwk"  # Google DeepMind Podcast Trailer (59s)
    
    transcription = transcriber.transcribe_youtube_video(youtube_id)
    visualizer.display_full_transcription(transcription)
    
    return transcription

def example_video_segment():
    """Example 2: Transcribe a specific segment of a video."""
    print("\n🎬 Example 2: Video Segment Transcription")
    print("-" * 50)
    
    transcriber = VideoTranscriber()
    visualizer = TranscriptionVisualizer()
    
    # Transcribe first 2 minutes of a longer video
    youtube_id = "gg7WjuFs8F4"  # Google DeepMind AlphaFold (7min 54s)
    
    transcription = transcriber.transcribe_video(
        video_uri=f"https://www.youtube.com/watch?v={youtube_id}",
        start_offset=timedelta(minutes=0),
        end_offset=timedelta(minutes=2),
    )
    visualizer.display_summary(transcription)
    
    return transcription

def example_custom_model():
    """Example 3: Using a different Gemini model."""
    print("\n🎬 Example 3: Custom Model (Gemini 2.5 Pro)")
    print("-" * 50)
    
    transcriber = VideoTranscriber()
    visualizer = TranscriptionVisualizer()
    
    # Use Gemini 2.5 Pro for complex video analysis
    youtube_id = "nQKmVhLIGcs"  # Google DeepMind AI for Science (54min 23s)
    
    transcription = transcriber.transcribe_youtube_video(
        youtube_id,
        model="gemini-2.5-pro",
        start_offset=timedelta(minutes=0),
        end_offset=timedelta(minutes=5),  # Just first 5 minutes for demo
    )
    visualizer.display_summary(transcription)
    
    return transcription

def example_custom_prompt():
    """Example 4: Using a custom transcription prompt with emotion and tonality."""
    print("\n🎬 Example 4: Custom Prompt with Emotion/Tonality Detection")
    print("-" * 50)
    
    transcriber = VideoTranscriber()
    visualizer = TranscriptionVisualizer()
    
    # Custom prompt for technical content with enhanced emotion/tonality detection
    custom_prompt = """
**Task 1 - Technical Script Segments**

- Watch the video and listen carefully to the audio.
- Identify each unique voice using a `voice_id` (1, 2, 3, etc.).
- Transcribe the video's audio verbatim with voice diarization.
- Pay special attention to technical terms, proper nouns, and company names.
- Include the `start_time` and `end_time` timecodes (HH:MM:SS:FF) for each speech segment.
- Analyze emotion, tone, energy level, and speech rate based on audio and visual cues.
- For emotion: Detect primary emotion (happy, sad, angry, neutral, excited, worried, etc.)
- For tone: Identify voice tone (casual, formal, serious, playful, enthusiastic, etc.)
- For energy_level: Assess energy (low, medium, high)
- For speech_rate: Determine pace (slow, normal, fast)
- If information cannot be determined, use `null`
- Output a JSON array where each object has the following fields:
  - `start_time`
  - `end_time`
  - `text`
  - `voice_id`
  - `emotion`
  - `tone`
  - `energy_level`
  - `speech_rate`

**Task 2 - Technical Speakers**

- For each `voice_id` from Task 1, extract information about the corresponding speaker.
- Use visual and audio cues.
- Pay special attention to technical titles, company names, and research affiliations.
- If a piece of information cannot be found, use a question mark (`?`) as the value.
- Output a JSON array where each object has the following fields:
  - `voice_id`
  - `name`
  - `company`
  - `position`
  - `role_in_video`
"""
    
    youtube_id = "gg7WjuFs8F4"  # Google DeepMind AlphaFold
    
    transcription = transcriber.transcribe_video(
        video_uri=f"https://www.youtube.com/watch?v={youtube_id}",
        start_offset=timedelta(minutes=0),
        end_offset=timedelta(minutes=3),
        custom_prompt=custom_prompt,
    )
    visualizer.display_full_transcription(transcription)
    
    return transcription

def example_data_analysis():
    """Example 5: Analyzing transcription data."""
    print("\n🎬 Example 5: Data Analysis")
    print("-" * 50)
    
    # Get a transcription first
    transcriber = VideoTranscriber()
    transcription = transcriber.transcribe_youtube_video("0pJn3g8dfwk")
    
    # Analyze the data
    print(f"📊 Analysis Results:")
    print(f"   Total segments: {transcription.total_segments}")
    print(f"   Total speakers: {transcription.total_speakers}")
    
    # Find segments by speaker
    if transcription.speakers:
        first_speaker = transcription.speakers[0]
        if first_speaker.name != Config.NOT_FOUND_MARKER:
            segments = transcription.get_segments_by_speaker(first_speaker.name)
            print(f"   Segments by {first_speaker.name}: {len(segments)}")
            
            # Show first few segments
            print(f"   First 3 segments by {first_speaker.name}:")
            for i, segment in enumerate(segments[:3]):
                print(f"     {i+1}. [{segment.start_time}-{segment.end_time}] {segment.text[:50]}...")
    
    # Export to CSV
    visualizer = TranscriptionVisualizer()
    visualizer.export_to_csv(transcription, "example_analysis")
    
    return transcription

def example_emotion_tonality_analysis():
    """Example 6: Demonstrating emotion and tonality analysis for AI dubbing."""
    print("\n🎬 Example 6: Emotion and Tonality Analysis for AI Dubbing")
    print("-" * 50)
    
    transcriber = VideoTranscriber()
    visualizer = TranscriptionVisualizer()
    
    # Transcribe a video segment to analyze emotion and tonality
    youtube_id = "0pJn3g8dfwk"  # Google DeepMind Podcast Trailer
    
    transcription = transcriber.transcribe_youtube_video(
        youtube_id,
        start_offset=timedelta(seconds=0),
        end_offset=timedelta(seconds=30),
    )
    
    # Display full transcription with emotion/tonality data
    visualizer.display_full_transcription(transcription)
    
    # Export to CSV for AI dubbing use case
    visualizer.export_to_csv(transcription, "ai_dubbing_data")
    
    # Analyze emotion distribution
    if transcription.script_segments:
        emotions = [seg.emotion for seg in transcription.script_segments if seg.emotion]
        tones = [seg.tone for seg in transcription.script_segments if seg.tone]
        energies = [seg.energy_level for seg in transcription.script_segments if seg.energy_level]
        
        print(f"\n📊 Emotion Distribution:")
        from collections import Counter
        emotion_counts = Counter(emotions)
        for emotion, count in emotion_counts.items():
            print(f"   {emotion}: {count}")
        
        print(f"\n📊 Tone Distribution:")
        tone_counts = Counter(tones)
        for tone, count in tone_counts.items():
            print(f"   {tone}: {count}")
        
        print(f"\n📊 Energy Level Distribution:")
        energy_counts = Counter(energies)
        for energy, count in energy_counts.items():
            print(f"   {energy}: {count}")
    
    return transcription

def example_error_handling():
    """Example 7: Error handling and validation."""
    print("\n🎬 Example 7: Error Handling")
    print("-" * 50)
    
    transcriber = VideoTranscriber()
    
    # Test invalid YouTube ID
    try:
        transcription = transcriber.transcribe_youtube_video("invalid_id")
        print("✅ Invalid ID handled gracefully")
    except Exception as e:
        print(f"❌ Error with invalid ID: {e}")
    
    # Test invalid FPS
    try:
        transcription = transcriber.transcribe_video(
            video_uri="https://www.youtube.com/watch?v=0pJn3g8dfwk",
            fps=50.0  # Invalid FPS
        )
    except ValueError as e:
        print(f"✅ FPS validation working: {e}")
    
    return None

def main():
    """Run all examples."""
    print("🎬 Multimodal Video Transcriber Examples")
    print("=" * 60)
    
    try:
        # Run examples
        example_basic_transcription()
        example_video_segment()
        example_custom_model()
        example_custom_prompt()
        example_data_analysis()
        example_emotion_tonality_analysis()
        example_error_handling()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Example error: {e}")

if __name__ == "__main__":
    main()
