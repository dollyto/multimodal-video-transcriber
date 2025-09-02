"""
Visualization module for displaying transcription results.
"""

import itertools
from typing import Dict, List
import pandas as pd
from pandas import DataFrame
from pandas.io.formats.style import Styler
from pandas.io.formats.style_render import CSSDict

from config import Config
from models import VideoTranscription, Speaker, TranscriptSegment

class TranscriptionVisualizer:
    """Visualizer for transcription results."""
    
    def __init__(self):
        """Initialize the visualizer."""
        self.bgcolor_column = "bg_color"  # Hidden column for row colors
        
        # Color palettes for speakers
        self.known_speaker_colors = [
            "#669DF6", "#EE675C", "#FCC934", "#5BB974",  # Primary colors
            "#8AB4F8", "#F28B82", "#FDD663", "#81C995",  # Secondary colors
            "#AECBFA", "#F6AEA9", "#FDE293", "#A8DAB5",  # Tertiary colors
            "#D2E3FC", "#FAD2CF", "#FEEFC3", "#CEEAD6",  # Quaternary colors
            "#E8F0FE", "#FCE8E6", "#FEF7E0", "#E6F4EA",  # Quinary colors
        ]
        
        self.unknown_speaker_colors = [
            "#80868B", "#9AA0A6", "#BDC1C6", "#DADCE0", "#E8EAED", "#F1F3F4"
        ]
    
    def get_color_for_voice_mapping(self, speakers: List[Speaker]) -> Dict[int, str]:
        """Get color mapping for voice IDs."""
        known_colors = itertools.cycle(self.known_speaker_colors)
        unknown_colors = itertools.cycle(self.unknown_speaker_colors)
        
        mapping: Dict[int, str] = {}
        for speaker in speakers:
            if speaker.name != Config.NOT_FOUND_MARKER:
                color = next(known_colors)
            else:
                color = next(unknown_colors)
            mapping[speaker.voice_id] = color
        
        return mapping
    
    def get_table_styler(self, df: DataFrame) -> Styler:
        """Get styled table for display."""
        def join_styles(styles: List[str]) -> str:
            return ";".join(styles)
        
        table_css = [
            "color: #202124",
            "background-color: #BDC1C6",
            "border: 0",
            "border-radius: 0.5rem",
            "border-spacing: 0px",
            "outline: 0.5rem solid #BDC1C6",
            "margin: 1rem 0.5rem",
        ]
        th_css = ["background-color: #E8EAED"]
        th_td_css = ["text-align:left", "padding: 0.25rem 1rem"]
        
        table_styles = [
            CSSDict(selector="", props=join_styles(table_css)),
            CSSDict(selector="th", props=join_styles(th_css)),
            CSSDict(selector="th,td", props=join_styles(th_td_css)),
        ]
        
        return df.style.set_table_styles(table_styles).hide()
    
    def change_row_bgcolor(self, row: pd.Series) -> List[str]:
        """Change row background color."""
        style = f"background-color:{row[self.bgcolor_column]}"
        return [style] * len(row)
    
    def display_speakers(self, transcription: VideoTranscription) -> None:
        """Display speakers table."""
        def sanitize_field(s: str, symbol_if_unknown: str) -> str:
            return symbol_if_unknown if s == Config.NOT_FOUND_MARKER else s
        
        def yield_rows():
            yield ["voice_id", "name", "company", "position", "role_in_video", self.bgcolor_column]
            
            color_for_voice = self.get_color_for_voice_mapping(transcription.speakers)
            for speaker in transcription.speakers:
                yield [
                    str(speaker.voice_id),
                    sanitize_field(speaker.name, Config.NOT_FOUND_MARKER),
                    sanitize_field(speaker.company, Config.NOT_FOUND_MARKER),
                    sanitize_field(speaker.position, Config.NOT_FOUND_MARKER),
                    sanitize_field(speaker.role_in_video, Config.NOT_FOUND_MARKER),
                    color_for_voice.get(speaker.voice_id, "red"),
                ]
        
        data = list(yield_rows())
        df = DataFrame(columns=data[0], data=data[1:])
        styler = self.get_table_styler(df)
        styler.apply(self.change_row_bgcolor, axis=1)
        styler.hide([self.bgcolor_column], axis="columns")
        
        print(f"\n### Speakers ({len(transcription.speakers)})")
        print(styler.to_string())
    
    def display_script_segments(self, transcription: VideoTranscription) -> None:
        """Display script segments table."""
        def yield_rows():
            yield ["start_time", "end_time", "speaker", "text", self.bgcolor_column]
            
            color_for_voice = self.get_color_for_voice_mapping(transcription.speakers)
            speaker_for_voice = {
                speaker.voice_id: speaker for speaker in transcription.speakers
            }
            previous_voice = None
            
            for segment in transcription.script_segments:
                current_voice = segment.voice_id
                speaker_label = ""
                
                if speaker := speaker_for_voice.get(current_voice):
                    if speaker.name != Config.NOT_FOUND_MARKER:
                        speaker_label = speaker.name
                    elif speaker.position != Config.NOT_FOUND_MARKER:
                        speaker_label = f"[voice {current_voice}][{speaker.position}]"
                    elif speaker.role_in_video != Config.NOT_FOUND_MARKER:
                        speaker_label = f"[voice {current_voice}][{speaker.role_in_video}]"
                
                if not speaker_label:
                    speaker_label = f"[voice {current_voice}]"
                
                # Use quote mark for consecutive segments from same speaker
                display_speaker = speaker_label if current_voice != previous_voice else '"'
                
                yield [
                    segment.start_time,
                    segment.end_time,
                    display_speaker,
                    segment.text,
                    color_for_voice.get(current_voice, "red"),
                ]
                previous_voice = current_voice
        
        data = list(yield_rows())
        df = DataFrame(columns=data[0], data=data[1:])
        styler = self.get_table_styler(df)
        styler.apply(self.change_row_bgcolor, axis=1)
        styler.hide([self.bgcolor_column], axis="columns")
        
        print(f"\n### Script Segments ({len(transcription.script_segments)})")
        print(styler.to_string())
    
    def display_translation_table(self, transcription: VideoTranscription) -> None:
        """Display translation table."""
        if not transcription.translation_table:
            return
        
        def yield_rows():
            yield ["line_number", "speaker", "source_iso", "target_iso"]
            
            for translation in transcription.translation_table:
                yield [
                    str(translation.line_number),
                    translation.speaker,
                    translation.source_iso,
                    translation.target_iso,
                ]
        
        data = list(yield_rows())
        df = DataFrame(columns=data[0], data=data[1:])
        styler = self.get_table_styler(df)
        
        print(f"\n### Translation Table ({len(transcription.translation_table)})")
        print(styler.to_string())
    
    def display_summary(self, transcription: VideoTranscription) -> None:
        """Display transcription summary."""
        print("\n" + "=" * 80)
        print("TRANSCRIPTION SUMMARY")
        print("=" * 80)
        
        print(f"📊 Total Script Segments: {transcription.total_segments}")
        print(f"👥 Total Speakers: {transcription.total_speakers}")
        
        if transcription.video_duration:
            print(f"⏱️  Video Duration: {transcription.video_duration}")
        
        if transcription.language_detected:
            print(f"🌐 Language Detected: {transcription.language_detected}")
        
        # Speaker breakdown
        if transcription.speakers:
            print(f"\n📋 Speakers Breakdown:")
            for speaker in transcription.speakers:
                status = "✅" if speaker.name != Config.NOT_FOUND_MARKER else "❓"
                print(f"  {status} Voice {speaker.voice_id}: {speaker.name}")
        
        print("=" * 80)
    
    def display_full_transcription(self, transcription: VideoTranscription) -> None:
        """Display complete transcription with all components."""
        self.display_summary(transcription)
        self.display_speakers(transcription)
        self.display_script_segments(transcription)
        self.display_translation_table(transcription)
    
    def export_to_csv(self, transcription: VideoTranscription, base_filename: str) -> None:
        """Export transcription to CSV files."""
        # Export script segments
        segments_data = []
        for segment in transcription.script_segments:
            speaker = transcription.get_speaker_by_voice_id(segment.voice_id)
            segments_data.append({
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "speaker_name": speaker.name if speaker else Config.NOT_FOUND_MARKER,
                "speaker_company": speaker.company if speaker else Config.NOT_FOUND_MARKER,
                "speaker_position": speaker.position if speaker else Config.NOT_FOUND_MARKER,
                "text": segment.text,
                "voice_id": segment.voice_id,
            })
        
        segments_df = pd.DataFrame(segments_data)
        segments_df.to_csv(f"{base_filename}_segments.csv", index=False)
        
        # Export speakers
        speakers_data = []
        for speaker in transcription.speakers:
            speakers_data.append({
                "voice_id": speaker.voice_id,
                "name": speaker.name,
                "company": speaker.company,
                "position": speaker.position,
                "role_in_video": speaker.role_in_video,
            })
        
        speakers_df = pd.DataFrame(speakers_data)
        speakers_df.to_csv(f"{base_filename}_speakers.csv", index=False)
        
        # Export translation table if available
        if transcription.translation_table:
            translation_data = []
            for translation in transcription.translation_table:
                translation_data.append({
                    "line_number": translation.line_number,
                    "speaker": translation.speaker,
                    "source_iso": translation.source_iso,
                    "target_iso": translation.target_iso,
                })
            
            translation_df = pd.DataFrame(translation_data)
            translation_df.to_csv(f"{base_filename}_translations.csv", index=False)
        
        print(f"\n✅ Exported transcription to:")
        print(f"   📄 {base_filename}_segments.csv")
        print(f"   📄 {base_filename}_speakers.csv")
        if transcription.translation_table:
            print(f"   📄 {base_filename}_translations.csv")
