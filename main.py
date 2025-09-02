#!/usr/bin/env python3
"""
Main script for the multimodal video transcriber.
Demonstrates usage and provides command-line interface.
"""

import argparse
import json
import sys
from datetime import timedelta
from pathlib import Path

from transcriber import VideoTranscriber
from visualizer import TranscriptionVisualizer
from config import Config

def main():
    """Main function for the transcriber."""
    parser = argparse.ArgumentParser(
        description="Multimodal Video Transcriber using Google Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transcribe a YouTube video
  python main.py --youtube 0pJn3g8dfwk

  # Transcribe a video segment (first 5 minutes)
  python main.py --youtube 0pJn3g8dfwk --start 0 --end 300

  # Transcribe with custom model
  python main.py --youtube 0pJn3g8dfwk --model gemini-2.5-pro

  # Export to JSON and CSV
  python main.py --youtube 0pJn3g8dfwk --export output_transcription

  # Transcribe from Cloud Storage (Vertex AI only)
  python main.py --gs-uri gs://bucket/path/to/video.mp4
        """
    )
    
    # Video source options
    video_group = parser.add_mutually_exclusive_group(required=True)
    video_group.add_argument("--youtube", help="YouTube video ID")
    video_group.add_argument("--gs-uri", help="Google Cloud Storage URI")
    video_group.add_argument("--url", help="Direct video URL")
    
    # Processing options
    parser.add_argument("--start", type=int, help="Start time in seconds")
    parser.add_argument("--end", type=int, help="End time in seconds")
    parser.add_argument("--fps", type=float, help="Custom frame rate (0.1-24.0)")
    parser.add_argument("--model", default=Config.DEFAULT_MODEL, help="Gemini model to use")
    
    # Output options
    parser.add_argument("--export", help="Export base filename (without extension)")
    parser.add_argument("--json", help="Export to JSON file")
    parser.add_argument("--quiet", action="store_true", help="Suppress visual output")
    
    args = parser.parse_args()
    
    try:
        # Initialize transcriber
        transcriber = VideoTranscriber()
        visualizer = TranscriptionVisualizer()
        
        # Prepare video URI
        if args.youtube:
            video_uri = f"https://www.youtube.com/watch?v={args.youtube}"
        elif args.gs_uri:
            video_uri = args.gs_uri
        elif args.url:
            video_uri = args.url
        else:
            print("❌ No video source specified")
            sys.exit(1)
        
        # Prepare time offsets
        start_offset = timedelta(seconds=args.start) if args.start else None
        end_offset = timedelta(seconds=args.end) if args.end else None
        
        # Transcribe video
        print(f"🎬 Transcribing video: {video_uri}")
        if start_offset or end_offset:
            print(f"⏱️  Segment: {start_offset or 'start'} to {end_offset or 'end'}")
        
        transcription = transcriber.transcribe_video(
            video_uri=video_uri,
            start_offset=start_offset,
            end_offset=end_offset,
            fps=args.fps,
            model=args.model,
        )
        
        # Display results
        if not args.quiet:
            visualizer.display_full_transcription(transcription)
        
        # Export results
        if args.export:
            visualizer.export_to_csv(transcription, args.export)
        
        if args.json:
            with open(args.json, 'w', encoding='utf-8') as f:
                json.dump(transcription.model_dump(), f, indent=2, ensure_ascii=False)
            print(f"✅ Exported JSON to: {args.json}")
        
        # Return success
        if transcription.total_segments > 0:
            print(f"\n✅ Transcription completed successfully!")
            print(f"   📊 {transcription.total_segments} script segments")
            print(f"   👥 {transcription.total_speakers} speakers identified")
        else:
            print("\n⚠️  No transcription segments found")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ Transcription interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def demo():
    """Demo function showing various transcription examples."""
    print("🎬 Multimodal Video Transcriber Demo")
    print("=" * 50)
    
    try:
        # Initialize transcriber
        transcriber = VideoTranscriber()
        visualizer = TranscriptionVisualizer()
        
        # Example 1: Short YouTube video
        print("\n📺 Example 1: Short YouTube video (Google DeepMind Podcast Trailer)")
        youtube_id = "0pJn3g8dfwk"  # Google DeepMind Podcast Trailer (59s)
        
        transcription = transcriber.transcribe_youtube_video(youtube_id)
        visualizer.display_summary(transcription)
        
        # Example 2: Video segment
        print("\n📺 Example 2: Video segment (first 2 minutes of longer video)")
        youtube_id = "gg7WjuFs8F4"  # Google DeepMind AlphaFold (7min 54s)
        
        transcription = transcriber.transcribe_youtube_video(
            youtube_id,
            start_offset=timedelta(minutes=0),
            end_offset=timedelta(minutes=2),
        )
        visualizer.display_summary(transcription)
        
        # Example 3: Using different model
        print("\n📺 Example 3: Using Gemini 2.5 Pro for complex video")
        youtube_id = "nQKmVhLIGcs"  # Google DeepMind AI for Science (54min 23s)
        
        transcription = transcriber.transcribe_youtube_video(
            youtube_id,
            model="gemini-2.5-pro",
            start_offset=timedelta(minutes=0),
            end_offset=timedelta(minutes=5),  # Just first 5 minutes for demo
        )
        visualizer.display_summary(transcription)
        
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, run demo
        demo()
    else:
        # Run with command line arguments
        main()
