"""
Data models for the multimodal video transcriber.
Uses Pydantic for structured output and validation.
"""

from datetime import timedelta
from typing import List, Optional
import pydantic
from config import Config

class TranscriptSegment(pydantic.BaseModel):
    """Represents a single transcript segment."""
    start_time: str = pydantic.Field(description="Start time in HH:MM:SS:FF format (hours:minutes:seconds:frames)")
    end_time: str = pydantic.Field(description="End time in HH:MM:SS:FF format (hours:minutes:seconds:frames)")
    text: str = pydantic.Field(description="Transcribed text")
    voice_id: int = pydantic.Field(description="Voice identifier for speaker diarization")
    emotion: Optional[str] = pydantic.Field(default=None, description="Emotion detected: happy, sad, angry, neutral, excited, worried, etc.")
    tone: Optional[str] = pydantic.Field(default=None, description="Tone of voice: casual, formal, serious, playful, enthusiastic, etc.")
    energy_level: Optional[str] = pydantic.Field(default=None, description="Energy level: low, medium, high")
    speech_rate: Optional[str] = pydantic.Field(default=None, description="Speech rate: slow, normal, fast")
    
    class Config:
        json_schema_extra = {
            "example": {
                "start_time": "00:00:02:00",
                "end_time": "00:00:05:00",
                "text": "Hello, welcome to our podcast.",
                "voice_id": 1,
                "emotion": "happy",
                "tone": "casual",
                "energy_level": "medium",
                "speech_rate": "normal"
            }
        }

class Speaker(pydantic.BaseModel):
    """Represents a speaker identified in the video."""
    voice_id: int = pydantic.Field(description="Voice identifier matching transcript segments")
    name: str = pydantic.Field(description="Speaker name or '?' if not found")
    company: str = pydantic.Field(description="Speaker's company or '?' if not found")
    position: str = pydantic.Field(description="Speaker's position or '?' if not found")
    role_in_video: str = pydantic.Field(description="Speaker's role in the video or '?' if not found")
    
    class Config:
        json_schema_extra = {
            "example": {
                "voice_id": 1,
                "name": "John Doe",
                "company": "Tech Corp",
                "position": "CEO",
                "role_in_video": "Host"
            }
        }

class TranslationTable(pydantic.BaseModel):
    """Translation table for multilingual support."""
    line_number: int = pydantic.Field(description="Line number in the transcript")
    speaker: str = pydantic.Field(description="Speaker name")
    source_iso: str = pydantic.Field(description="Source language text (ISO code)")
    target_iso: str = pydantic.Field(description="Target language text (ISO code)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "line_number": 1,
                "speaker": "John Doe",
                "source_iso": "Hello, welcome!",
                "target_iso": "¡Hola, bienvenido!"
            }
        }

class VideoTranscription(pydantic.BaseModel):
    """Complete video transcription with all components."""
    # Script Segments (following user preference)
    script_segments: List[TranscriptSegment] = pydantic.Field(
        default_factory=list,
        description="Transcribed script segments with timecodes"
    )
    
    # Speakers
    speakers: List[Speaker] = pydantic.Field(
        default_factory=list,
        description="Identified speakers with their information"
    )
    
    # Translation table (optional)
    translation_table: List[TranslationTable] = pydantic.Field(
        default_factory=list,
        description="Translation table for multilingual support"
    )
    
    # Metadata
    video_duration: Optional[str] = pydantic.Field(
        default=None,
        description="Total video duration"
    )
    
    total_segments: int = pydantic.Field(
        default=0,
        description="Total number of script segments"
    )
    
    total_speakers: int = pydantic.Field(
        default=0,
        description="Total number of identified speakers"
    )
    
    language_detected: Optional[str] = pydantic.Field(
        default=None,
        description="Primary language detected in the video"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "script_segments": [
                    {
                        "start_time": "00:00:02:12",
                        "end_time": "00:00:05:23",
                        "text": "Hello, welcome to our podcast.",
                        "voice_id": 1
                    }
                ],
                "speakers": [
                    {
                        "voice_id": 1,
                        "name": "John Doe",
                        "company": "Tech Corp",
                        "position": "CEO",
                        "role_in_video": "Host"
                    }
                ],
                "translation_table": [],
                "video_duration": "00:05:30:00",
                "total_segments": 1,
                "total_speakers": 1,
                "language_detected": "en"
            }
        }
    
    def update_counts(self) -> None:
        """Update the count fields."""
        self.total_segments = len(self.script_segments)
        self.total_speakers = len(self.speakers)
    
    def get_speaker_by_voice_id(self, voice_id: int) -> Optional[Speaker]:
        """Get speaker by voice ID."""
        for speaker in self.speakers:
            if speaker.voice_id == voice_id:
                return speaker
        return None
    
    def get_segments_by_speaker(self, speaker_name: str) -> List[TranscriptSegment]:
        """Get all segments for a specific speaker."""
        segments = []
        speaker = None
        
        # Find the speaker
        for s in self.speakers:
            if s.name == speaker_name:
                speaker = s
                break
        
        if speaker:
            # Get all segments for this speaker's voice_id
            for segment in self.script_segments:
                if segment.voice_id == speaker.voice_id:
                    segments.append(segment)
        
        return segments
