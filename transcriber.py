"""
Main transcriber module for multimodal video transcription using Google Gemini.
"""

import os
import re
from datetime import timedelta
from typing import Optional, List
import tenacity
from google import genai
from google.genai.errors import ClientError
from google.genai.types import (
    FileData,
    FinishReason,
    GenerateContentConfig,
    GenerateContentResponse,
    Part,
    VideoMetadata,
    MediaResolution,
    ThinkingConfig,
)

from config import Config
from models import VideoTranscription, TranscriptSegment, Speaker

class VideoTranscriber:
    """Main class for video transcription using Google Gemini."""
    
    def __init__(self, skip_config_validation: bool = False):
        """Initialize the transcriber."""
        # Setup configuration only if not skipping validation
        if not skip_config_validation:
            Config.setup_environment()
            
            if not Config.validate_config():
                raise ValueError("Invalid configuration. Please check your environment variables.")
        
        # Initialize Gemini client
        # Always check for API key in environment first, regardless of skip_config_validation
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            # Ensure the API key is set in environment for the client
            os.environ["GOOGLE_API_KEY"] = api_key
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = genai.Client()
        
        self.service_name = Config.get_service_name()
        
        print(f"✅ Using {self.service_name} API")
    
    def get_transcription_prompt(self, timecode_format: str = "MM:SS") -> str:
        """Get the transcription prompt with proper formatting."""
        return f"""
**Task 1 - Script Segments**

- Watch the video and listen carefully to the audio.
- Identify each unique voice using a `voice_id` (1, 2, 3, etc.).
- Transcribe the video's audio verbatim with voice diarization.
- Include the `start_time` and `end_time` timecodes ({timecode_format}) for each speech segment.
- Output a JSON array where each object has the following fields:
  - `start_time`
  - `end_time`
  - `text`
  - `voice_id`

**Task 2 - Speakers**

- For each `voice_id` from Task 1, extract information about the corresponding speaker.
- Use visual and audio cues.
- If a piece of information cannot be found, use a question mark (`?`) as the value.
- Output a JSON array where each object has the following fields:
  - `voice_id`
  - `name`
  - `company`
  - `position`
  - `role_in_video`
"""
    
    def get_video_part(
        self,
        video_uri: str,
        start_offset: Optional[timedelta] = None,
        end_offset: Optional[timedelta] = None,
        fps: Optional[float] = None,
    ) -> Optional[Part]:
        """Create a video part for Gemini processing."""
        # Convert Cloud Storage URI to HTTPS if using Google AI Studio
        if not self.client.vertexai and video_uri.startswith("gs://"):
            video_uri = f"https://storage.googleapis.com/{video_uri.removeprefix('gs://')}"
        
        # Check if YouTube URL is supported
        if not self.client.vertexai and not video_uri.startswith("https://www.youtube.com/watch?v="):
            print("❌ Google AI Studio API: Only YouTube URLs are currently supported")
            return None
        
        file_data = FileData(file_uri=video_uri, mime_type="video/*")
        
        # Create video metadata
        video_metadata = VideoMetadata()
        if start_offset:
            video_metadata.start_offset = f"{start_offset.total_seconds()}s"
        if end_offset:
            video_metadata.end_offset = f"{end_offset.total_seconds()}s"
        if fps:
            video_metadata.fps = fps
        
        return Part(file_data=file_data, video_metadata=video_metadata)
    
    def get_generate_content_config(
        self,
        model: str = None,
        media_resolution: MediaResolution = None,
    ) -> GenerateContentConfig:
        """Get the configuration for content generation."""
        model = model or Config.DEFAULT_MODEL
        
        config = GenerateContentConfig(
            temperature=Config.DEFAULT_TEMPERATURE,
            top_p=Config.DEFAULT_TOP_P,
            seed=Config.DEFAULT_SEED,
            response_mime_type="application/json",
            response_schema=VideoTranscription,
        )
        
        # Set media resolution if provided
        if media_resolution:
            config.media_resolution = media_resolution
        
        # Set thinking config for Gemini 2.5 models
        if "2.5" in model:
            if "flash" in model:
                config.thinking_config = ThinkingConfig(thinking_budget=0, include_thoughts=False)
            elif "pro" in model:
                config.thinking_config = ThinkingConfig(thinking_budget=128, include_thoughts=False)
        
        return config
    
    def get_retrier(self) -> tenacity.Retrying:
        """Get retry configuration for API calls."""
        return tenacity.Retrying(
            stop=tenacity.stop_after_attempt(7),
            wait=tenacity.wait_incrementing(start=10, increment=1),
            retry=self._should_retry_request,
            reraise=True,
        )
    
    def _should_retry_request(self, retry_state: tenacity.RetryCallState) -> bool:
        """Determine if a request should be retried."""
        if not retry_state.outcome:
            return False
        
        err = retry_state.outcome.exception()
        if not isinstance(err, ClientError):
            return False
        
        print(f"❌ ClientError {err.code}: {err.message}")
        
        retry = False
        if err.code == 400 and err.message and " try again " in err.message:
            retry = True
        elif err.code == 429:
            retry = True
        
        print(f"🔄 Retry: {retry}")
        return retry
    
    def get_timecode_format(self, video_duration: Optional[timedelta] = None) -> str:
        """Get the appropriate timecode format based on video duration."""
        if video_duration and video_duration >= timedelta(hours=1):
            return Config.EXTENDED_TIMECODE_FORMAT
        return Config.DEFAULT_TIMECODE_FORMAT
    
    def transcribe_video(
        self,
        video_uri: str,
        start_offset: Optional[timedelta] = None,
        end_offset: Optional[timedelta] = None,
        fps: Optional[float] = None,
        model: str = None,
        custom_prompt: str = None,
    ) -> VideoTranscription:
        """
        Transcribe a video using Gemini.
        
        Args:
            video_uri: URI of the video (YouTube URL, Cloud Storage, or web URL)
            start_offset: Start time offset for video segment
            end_offset: End time offset for video segment
            fps: Custom frame rate (0.1 to 24.0)
            model: Gemini model to use
            custom_prompt: Custom transcription prompt
            
        Returns:
            VideoTranscription object with results
        """
        model = model or Config.DEFAULT_MODEL
        
        # Validate FPS
        if fps and (fps < Config.MIN_FPS or fps > Config.MAX_FPS):
            raise ValueError(f"FPS must be between {Config.MIN_FPS} and {Config.MAX_FPS}")
        
        # Get video part
        video_part = self.get_video_part(video_uri, start_offset, end_offset, fps)
        if not video_part:
            return VideoTranscription()
        
        # Get prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            timecode_format = self.get_timecode_format(end_offset - start_offset if start_offset and end_offset else None)
            prompt = self.get_transcription_prompt(timecode_format)
        
        # Get configuration
        config = self.get_generate_content_config(model)
        
        # Prepare contents
        contents = [video_part, prompt.strip()]
        
        print(f" {model} ".center(80, "-"))
        
        # Make API call with retries
        response = None
        for attempt in self.get_retrier():
            with attempt:
                response = self.client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config,
                )
                self._display_response_info(response)
        
        # Parse response
        return self._parse_response(response)
    
    def _display_response_info(self, response: GenerateContentResponse) -> None:
        """Display response information."""
        if usage_metadata := response.usage_metadata:
            if usage_metadata.prompt_token_count:
                print(f"Input tokens   : {usage_metadata.prompt_token_count:9,d}")
            if usage_metadata.candidates_token_count:
                print(f"Output tokens  : {usage_metadata.candidates_token_count:9,d}")
            if usage_metadata.thoughts_token_count:
                print(f"Thoughts tokens: {usage_metadata.thoughts_token_count:9,d}")
        
        if not response.candidates:
            print("❌ No `response.candidates`")
            return
        
        if (finish_reason := response.candidates[0].finish_reason) != FinishReason.STOP:
            print(f"❌ {finish_reason = }")
        
        if not response.text:
            print("❌ No `response.text`")
            return
    
    def _parse_response(self, response: GenerateContentResponse) -> VideoTranscription:
        """Parse the response into a VideoTranscription object."""
        if not isinstance(response.parsed, VideoTranscription):
            print("❌ Could not parse the JSON response")
            return VideoTranscription()
        
        transcription = response.parsed
        transcription.update_counts()
        
        return transcription
    
    def transcribe_youtube_video(
        self,
        youtube_id: str,
        **kwargs
    ) -> VideoTranscription:
        """Transcribe a YouTube video by ID."""
        youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
        return self.transcribe_video(youtube_url, **kwargs)
    
    def transcribe_cloud_storage_video(
        self,
        bucket: str,
        path: str,
        **kwargs
    ) -> VideoTranscription:
        """Transcribe a video from Google Cloud Storage."""
        gs_uri = f"gs://{bucket}/{path}"
        return self.transcribe_video(gs_uri, **kwargs)
