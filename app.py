"""
Streamlit web application for the multimodal video transcriber.
Provides a user-friendly interface for testing the transcriber.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import json
import time
from pathlib import Path

from transcriber import VideoTranscriber
from visualizer import TranscriptionVisualizer
from config import Config
from models import VideoTranscription

# Page configuration
st.set_page_config(
    page_title="Multimodal Video Transcriber",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🎬 Multimodal Video Transcriber</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Google Gemini AI</p>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Configuration
        st.subheader("API Setup")
        use_vertex_ai = st.checkbox("Use Vertex AI (instead of Google AI Studio)", value=False)
        
        if use_vertex_ai:
            project_id = st.text_input("Google Cloud Project ID", placeholder="your-project-id")
            location = st.text_input("Location", value="global", placeholder="global")
            
            if st.button("Set Vertex AI Config"):
                st.session_state.vertex_ai_config = {
                    "use_vertex_ai": True,
                    "project_id": project_id,
                    "location": location
                }
                st.success("Vertex AI configuration set!")
        else:
            api_key = st.text_input("Google AI Studio API Key", type="password", placeholder="your-api-key")
            
            if st.button("Set API Key"):
                st.session_state.api_key = api_key
                st.success("API key set!")
        
        # Model Configuration
        st.subheader("Model Settings")
        model = st.selectbox(
            "Gemini Model",
            ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-pro"],
            index=0
        )
        
        fps = st.slider("Frame Rate (FPS)", 0.1, 24.0, 1.0, 0.1)
        
        # Processing Options
        st.subheader("Processing Options")
        enable_segments = st.checkbox("Enable Video Segments", value=False)
        
        if enable_segments:
            start_minutes = st.number_input("Start (minutes)", min_value=0, value=0)
            start_seconds = st.number_input("Start (seconds)", min_value=0, max_value=59, value=0)
            end_minutes = st.number_input("End (minutes)", min_value=0, value=5)
            end_seconds = st.number_input("End (seconds)", min_value=0, max_value=59, value=0)
        
        # Export Options
        st.subheader("Export Options")
        export_json = st.checkbox("Export JSON", value=True)
        export_csv = st.checkbox("Export CSV", value=True)
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🎬 Transcribe", "📊 Results", "📈 Analytics", "ℹ️ About"])
    
    with tab1:
        st.header("Video Transcription")
        
        # Input method selection
        input_method = st.radio(
            "Select input method:",
            ["YouTube Video ID", "YouTube URL", "Direct Video URL", "Google Cloud Storage URI"],
            horizontal=True
        )
        
        # Input field based on selection
        video_input = ""
        if input_method == "YouTube Video ID":
            video_input = st.text_input("YouTube Video ID", placeholder="0pJn3g8dfwk")
        elif input_method == "YouTube URL":
            video_input = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=0pJn3g8dfwk")
        elif input_method == "Direct Video URL":
            video_input = st.text_input("Video URL", placeholder="https://example.com/video.mp4")
        elif input_method == "Google Cloud Storage URI":
            video_input = st.text_input("GCS URI", placeholder="gs://bucket/path/to/video.mp4")
        
        # Custom prompt option
        use_custom_prompt = st.checkbox("Use custom prompt", value=False)
        custom_prompt = ""
        if use_custom_prompt:
            custom_prompt = st.text_area(
                "Custom Prompt",
                value="""**Task 1 - Script Segments**

- Watch the video and listen carefully to the audio.
- Identify each unique voice using a `voice_id` (1, 2, 3, etc.).
- Transcribe the video's audio verbatim with voice diarization.
- Include the `start_time` and `end_time` timecodes (HH:MM:SS:FF) for each speech segment.
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
  - `role_in_video`""",
                height=300
            )
        
        # Transcribe button
        if st.button("🚀 Start Transcription", type="primary", use_container_width=True):
            if not video_input:
                st.error("Please enter a video source!")
                return
            
            # Check configuration
            if not st.session_state.get('api_key') and not st.session_state.get('vertex_ai_config'):
                st.error("Please configure your API credentials in the sidebar!")
                return
            
            # Prepare video URI
            video_uri = video_input
            if input_method == "YouTube Video ID":
                video_uri = f"https://www.youtube.com/watch?v={video_input}"
            
            # Prepare time offsets
            start_offset = None
            end_offset = None
            if enable_segments:
                start_offset = timedelta(minutes=start_minutes, seconds=start_seconds)
                end_offset = timedelta(minutes=end_minutes, seconds=end_seconds)
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Set configuration
                if st.session_state.get('vertex_ai_config'):
                    config = st.session_state.vertex_ai_config
                    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
                    os.environ["GOOGLE_CLOUD_PROJECT"] = config["project_id"]
                    os.environ["GOOGLE_CLOUD_LOCATION"] = config["location"]
                else:
                    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
                    os.environ["GOOGLE_API_KEY"] = st.session_state.api_key
                
                status_text.text("Initializing transcriber...")
                progress_bar.progress(10)
                
                # Initialize transcriber with config validation skipped since we set env vars in the UI
                transcriber = VideoTranscriber(skip_config_validation=True)
                status_text.text("Processing video...")
                progress_bar.progress(30)
                
                # Transcribe
                transcription = transcriber.transcribe_video(
                    video_uri=video_uri,
                    start_offset=start_offset,
                    end_offset=end_offset,
                    fps=fps,
                    model=model,
                    custom_prompt=custom_prompt if use_custom_prompt else None
                )
                
                progress_bar.progress(90)
                status_text.text("Finalizing results...")
                
                # Store results in session state
                st.session_state.transcription = transcription
                st.session_state.video_uri = video_uri
                
                progress_bar.progress(100)
                status_text.text("Transcription completed!")
                
                # Export if requested
                if export_json or export_csv:
                    timestamp = int(time.time())
                    base_filename = f"transcription_{timestamp}"
                    
                    if export_json:
                        json_data = transcription.model_dump()
                        st.download_button(
                            label="📥 Download JSON",
                            data=json.dumps(json_data, indent=2),
                            file_name=f"{base_filename}.json",
                            mime="application/json"
                        )
                    
                    if export_csv:
                        # Create CSV data
                        segments_df = pd.DataFrame([
                            {
                                "start_time": seg.start_time,
                                "end_time": seg.end_time,
                                "text": seg.text,
                                "voice_id": seg.voice_id,
                                "emotion": seg.emotion or "",
                                "tone": seg.tone or "",
                                "energy_level": seg.energy_level or "",
                                "speech_rate": seg.speech_rate or ""
                            } for seg in transcription.script_segments
                        ])
                        
                        speakers_df = pd.DataFrame([
                            {
                                "voice_id": sp.voice_id,
                                "name": sp.name,
                                "company": sp.company,
                                "position": sp.position,
                                "role_in_video": sp.role_in_video
                            } for sp in transcription.speakers
                        ])
                        
                        # Combine into one CSV
                        combined_data = []
                        for seg in transcription.script_segments:
                            speaker = transcription.get_speaker_by_voice_id(seg.voice_id)
                            combined_data.append({
                                "start_time": seg.start_time,
                                "end_time": seg.end_time,
                                "speaker_name": speaker.name if speaker else "?",
                                "speaker_company": speaker.company if speaker else "?",
                                "speaker_position": speaker.position if speaker else "?",
                                "text": seg.text,
                                "voice_id": seg.voice_id,
                                "emotion": seg.emotion or "",
                                "tone": seg.tone or "",
                                "energy_level": seg.energy_level or "",
                                "speech_rate": seg.speech_rate or ""
                            })
                        
                        combined_df = pd.DataFrame(combined_data)
                        csv_data = combined_df.to_csv(index=False)
                        
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv_data,
                            file_name=f"{base_filename}.csv",
                            mime="text/csv"
                        )
                
                st.success("✅ Transcription completed successfully!")
                
            except Exception as e:
                st.error(f"Error during transcription: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    with tab2:
        st.header("Transcription Results")
        
        if 'transcription' not in st.session_state:
            st.info("No transcription results available. Please run a transcription first.")
            return
        
        transcription = st.session_state.transcription
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Script Segments", transcription.total_segments)
        with col2:
            st.metric("Speakers", transcription.total_speakers)
        with col3:
            st.metric("Language", transcription.language_detected or "Unknown")
        with col4:
            st.metric("Duration", transcription.video_duration or "Unknown")
        
        # Speakers table
        st.subheader("👥 Speakers")
        if transcription.speakers:
            speakers_data = []
            for speaker in transcription.speakers:
                speakers_data.append({
                    "Voice ID": speaker.voice_id,
                    "Name": speaker.name,
                    "Company": speaker.company,
                    "Position": speaker.position,
                    "Role": speaker.role_in_video
                })
            
            speakers_df = pd.DataFrame(speakers_data)
            st.dataframe(speakers_df, use_container_width=True)
        else:
            st.info("No speakers identified.")
        
        # Script segments table
        st.subheader("📝 Script Segments")
        if transcription.script_segments:
            segments_data = []
            for segment in transcription.script_segments:
                speaker = transcription.get_speaker_by_voice_id(segment.voice_id)
                segments_data.append({
                    "Start Time": segment.start_time,
                    "End Time": segment.end_time,
                    "Speaker": speaker.name if speaker else f"Voice {segment.voice_id}",
                    "Emotion": segment.emotion or "-",
                    "Tone": segment.tone or "-",
                    "Energy": segment.energy_level or "-",
                    "Rate": segment.speech_rate or "-",
                    "Text": segment.text,
                    "Voice ID": segment.voice_id
                })
            
            segments_df = pd.DataFrame(segments_data)
            st.dataframe(segments_df, use_container_width=True)
        else:
            st.info("No script segments found.")
        
        # Raw JSON view
        with st.expander("🔍 Raw JSON Data"):
            st.json(transcription.model_dump())
    
    with tab3:
        st.header("Analytics")
        
        if 'transcription' not in st.session_state:
            st.info("No transcription results available. Please run a transcription first.")
            return
        
        transcription = st.session_state.transcription
        
        if not transcription.script_segments:
            st.info("No data available for analytics.")
            return
        
        # Emotion distribution
        if transcription.script_segments and any(seg.emotion for seg in transcription.script_segments):
            st.subheader("📊 Emotion Distribution")
            emotion_data = [{"emotion": seg.emotion} for seg in transcription.script_segments if seg.emotion]
            if emotion_data:
                emotion_df = pd.DataFrame(emotion_data)
                fig = px.pie(
                    emotion_df,
                    names="emotion",
                    title="Emotion Distribution",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Tone distribution
        if transcription.script_segments and any(seg.tone for seg in transcription.script_segments):
            st.subheader("🎭 Tone Distribution")
            tone_data = [{"tone": seg.tone} for seg in transcription.script_segments if seg.tone]
            if tone_data:
                tone_df = pd.DataFrame(tone_data)
                fig = px.bar(
                    tone_df["tone"].value_counts(),
                    title="Tone Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(xaxis_title="Tone", yaxis_title="Count")
                st.plotly_chart(fig, use_container_width=True)
        
        # Energy level distribution
        if transcription.script_segments and any(seg.energy_level for seg in transcription.script_segments):
            st.subheader("⚡ Energy Level Distribution")
            energy_data = [{"energy": seg.energy_level} for seg in transcription.script_segments if seg.energy_level]
            if energy_data:
                energy_df = pd.DataFrame(energy_data)
                fig = px.bar(
                    energy_df["energy"].value_counts(),
                    title="Energy Level Distribution",
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                fig.update_layout(xaxis_title="Energy Level", yaxis_title="Count")
                st.plotly_chart(fig, use_container_width=True)
        
        # Speaker distribution
        st.subheader("👥 Speaker Distribution")
        if transcription.speakers:
            speaker_names = [sp.name if sp.name != "?" else f"Voice {sp.voice_id}" for sp in transcription.speakers]
            speaker_counts = []
            
            for speaker in transcription.speakers:
                segments = transcription.get_segments_by_speaker(speaker.name) if speaker.name != "?" else []
                speaker_counts.append(len(segments))
            
            fig = px.pie(
                values=speaker_counts,
                names=speaker_names,
                title="Script Segments by Speaker"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Timeline visualization
        st.subheader("Timeline")
        if transcription.script_segments:
            timeline_data = []
            for segment in transcription.script_segments:
                speaker = transcription.get_speaker_by_voice_id(segment.voice_id)
                timeline_data.append({
                    "Start": segment.start_time,
                    "End": segment.end_time,
                    "Speaker": speaker.name if speaker else f"Voice {segment.voice_id}",
                    "Text": segment.text[:50] + "..." if len(segment.text) > 50 else segment.text
                })
            
            timeline_df = pd.DataFrame(timeline_data)
            
            # Create timeline chart
            fig = go.Figure()
            
            colors = px.colors.qualitative.Set3
            for i, speaker in enumerate(timeline_df['Speaker'].unique()):
                speaker_data = timeline_df[timeline_df['Speaker'] == speaker]
                
                fig.add_trace(go.Scatter(
                    x=[speaker_data['Start'].iloc[0], speaker_data['End'].iloc[-1]],
                    y=[speaker] * 2,
                    mode='lines+markers',
                    name=speaker,
                    line=dict(color=colors[i % len(colors)], width=8),
                    hovertemplate='<b>%{y}</b><br>Time: %{x}<extra></extra>'
                ))
            
            fig.update_layout(
                title="Speaker Timeline",
                xaxis_title="Time",
                yaxis_title="Speaker",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("About")
        
        st.markdown("""
        ## 🎬 Multimodal Video Transcriber
        
        This application uses Google's Gemini AI model to transcribe videos with detailed speaker identification.
        
        ### ✨ Features
        - **Multimodal Processing**: Combines audio and visual cues
        - **Speaker Diarization**: Identifies and tracks different speakers
        - **Speaker Information**: Extracts names, companies, positions, and roles
        - **Emotion & Tonality Detection**: Analyzes emotion, tone, energy level, and speech rate for AI dubbing
        - **Multiple Input Sources**: YouTube, Cloud Storage, direct URLs
        - **Export Options**: JSON and CSV formats
        - **Multilingual Support**: Works with 100+ languages
        
        ### 🤖 Models
        - **Gemini 2.0 Flash**: Fast, cost-effective for standard videos
        - **Gemini 2.5 Flash**: Balanced performance for longer videos
        - **Gemini 2.5 Pro**: High-quality for complex content
        
        ### 📊 Output Format
        The transcriber produces structured data with:
        - **Script Segments**: Timecoded transcription with speaker identification, emotion, tone, energy, and speech rate
        - **Speakers**: Detailed speaker information
        - **Translation Table**: Optional multilingual support
        - **AI Dubbing Data**: Emotion, tone, energy level, and speech rate for voice synthesis
        
        ### 🔧 Configuration
        - **Google AI Studio**: Free tier for testing (requires API key)
        - **Vertex AI**: Enterprise-grade (requires Google Cloud project)
        
        ### 📚 Resources
        - [Towards Data Science Article](https://towardsdatascience.com/unlocking-multimodal-video-transcription-with-gemini/)
        - [Google Gen AI Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs)
        - [Original Notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/use-cases/video-analysis/multimodal_video_transcription.ipynb)
        
        ### 🚀 Deployment
        This app can be deployed to:
        - **Render**: Free tier available
        - **Railway**: Easy deployment
        - **Streamlit Cloud**: Native Streamlit hosting
        """)

if __name__ == "__main__":
    main()
