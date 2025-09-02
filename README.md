# 🎬 Multimodal Video Transcriber

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.0+-green.svg)](https://ai.google.dev/gemini)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/dollyto/multimodal-video-transcriber/workflows/Test/badge.svg)](https://github.com/dollyto/multimodal-video-transcriber/actions)
[![Deploy](https://img.shields.io/badge/Deploy-Render-blue.svg)](https://render.com/)

A powerful multimodal video transcription system using Google's Gemini AI model. This solution combines audio and visual cues to provide detailed speaker identification, diarization, and comprehensive transcription results.

[🌐 Live Demo](https://multimodal-video-transcriber.onrender.com) | [📖 Documentation](https://github.com/dollyto/multimodal-video-transcriber#readme) | [🚀 Deploy](https://github.com/dollyto/multimodal-video-transcriber/blob/main/DEPLOYMENT.md)

Based on the [Towards Data Science article](https://towardsdatascience.com/unlocking-multimodal-video-transcription-with-gemini/) by Laurent Picard.

## ✨ Features

- **Multimodal Transcription**: Combines audio and visual cues for comprehensive transcription
- **Speaker Diarization**: Identifies and tracks different speakers throughout the video
- **Speaker Information**: Extracts names, companies, positions, and roles
- **Flexible Input Sources**: Supports YouTube URLs, Google Cloud Storage, and direct video URLs
- **Timecode Support**: Precise MM:SS and H:MM:SS timecode formatting
- **Multiple Models**: Support for Gemini 2.0 Flash, 2.5 Flash, and 2.5 Pro
- **Export Options**: JSON and CSV export capabilities
- **Multilingual Support**: Works with 100+ languages
- **Video Segments**: Transcribe specific portions of videos
- **Custom Prompts**: Use custom prompts for specialized content

## 🏗️ Architecture

The project follows a modular architecture:

```
├── config.py          # Configuration and environment setup
├── models.py          # Pydantic data models
├── transcriber.py     # Main transcription logic
├── visualizer.py      # Results visualization and export
├── main.py           # Command-line interface
├── example.py        # Usage examples
└── requirements.txt   # Dependencies
```

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dollyto/multimodal-video-transcriber.git
   cd multimodal-video-transcriber
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**:
   ```bash
   cp test_env.txt .env
   # Edit .env with your API key from https://aistudio.google.com/app/apikey
   ```

4. **Run the web app**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**: http://localhost:8501

### Option 2: Command Line Interface

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variable**:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

3. **Run transcription**:
   ```bash
   python main.py --youtube 0pJn3g8dfwk
   ```

### 2. Configuration

Create a `.env` file with your API credentials:

```bash
# For Google AI Studio (recommended for testing)
GOOGLE_GENAI_USE_VERTEXAI=False
GOOGLE_API_KEY=your_api_key_here

# OR for Vertex AI (enterprise)
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=global
```

### 3. Basic Usage

```bash
# Transcribe a YouTube video
python main.py --youtube 0pJn3g8dfwk

# Transcribe a video segment
python main.py --youtube 0pJn3g8dfwk --start 0 --end 300

# Export results
python main.py --youtube 0pJn3g8dfwk --export my_transcription
```

## 📖 Usage Examples

### Command Line Interface

```bash
# Basic transcription
python main.py --youtube 0pJn3g8dfwk

# Video segment (first 5 minutes)
python main.py --youtube 0pJn3g8dfwk --start 0 --end 300

# Custom model
python main.py --youtube 0pJn3g8dfwk --model gemini-2.5-pro

# Export to JSON
python main.py --youtube 0pJn3g8dfwk --json output.json

# Export to CSV
python main.py --youtube 0pJn3g8dfwk --export output

# Cloud Storage (Vertex AI only)
python main.py --gs-uri gs://bucket/path/to/video.mp4

# Direct URL
python main.py --url https://example.com/video.mp4
```

### Programmatic Usage

```python
from transcriber import VideoTranscriber
from visualizer import TranscriptionVisualizer
from datetime import timedelta

# Initialize
transcriber = VideoTranscriber()
visualizer = TranscriptionVisualizer()

# Basic transcription
transcription = transcriber.transcribe_youtube_video("0pJn3g8dfwk")

# Video segment
transcription = transcriber.transcribe_video(
    video_uri="https://www.youtube.com/watch?v=0pJn3g8dfwk",
    start_offset=timedelta(minutes=0),
    end_offset=timedelta(minutes=5),
    model="gemini-2.5-pro"
)

# Display results
visualizer.display_full_transcription(transcription)

# Export to CSV
visualizer.export_to_csv(transcription, "my_transcription")
```

## 🎯 Supported Video Sources

| Source | Vertex AI | Google AI Studio | Format |
|--------|-----------|------------------|---------|
| YouTube | ✅ | ✅ | `https://www.youtube.com/watch?v=ID` |
| Cloud Storage | ✅ | ❌ | `gs://bucket/path/video.mp4` |
| Direct URL | ✅ | ❌ | `https://example.com/video.mp4` |

## 🤖 Available Models

| Model | Performance | Speed | Cost | Max Input | Max Output | Best For |
|-------|-------------|-------|------|-----------|------------|----------|
| Gemini 2.0 Flash | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 1M tokens | 8k tokens | Standard videos, up to 25min |
| Gemini 2.5 Flash | ⭐⭐ | ⭐⭐ | ⭐⭐ | 1M tokens | 64k tokens | Standard videos, 25min+ |
| Gemini 2.5 Pro | ⭐⭐⭐ | ⭐ | ⭐ | 1M tokens | 64k tokens | Complex videos or 1h+ videos |

## 📊 Output Format

The transcriber produces structured output with the following components:

### Script Segments
```json
{
  "start_time": "00:02",
  "end_time": "00:05", 
  "text": "Hello, welcome to our podcast.",
  "voice_id": 1
}
```

### Speakers
```json
{
  "voice_id": 1,
  "name": "John Doe",
  "company": "Tech Corp",
  "position": "CEO",
  "role_in_video": "Host"
}
```

### Translation Table (Optional)
```json
{
  "line_number": 1,
  "speaker": "John Doe",
  "source_iso": "Hello, welcome!",
  "target_iso": "¡Hola, bienvenido!"
}
```

## ⚙️ Configuration Options

### Environment Variables

- `GOOGLE_GENAI_USE_VERTEXAI`: Use Vertex AI (True) or Google AI Studio (False)
- `GOOGLE_API_KEY`: API key for Google AI Studio
- `GOOGLE_CLOUD_PROJECT`: Google Cloud project ID (Vertex AI)
- `GOOGLE_CLOUD_LOCATION`: Google Cloud location (Vertex AI)

### Processing Options

- **FPS**: Custom frame rate (0.1-24.0, default: 1.0)
- **Timecodes**: MM:SS or H:MM:SS format
- **Media Resolution**: Low (66 tokens/frame) or Medium (258 tokens/frame)
- **Video Segments**: Specify start and end times

## 🔧 Advanced Features

### Custom Prompts

```python
custom_prompt = """
**Task 1 - Technical Script Segments**
- Watch the video and listen carefully to the audio.
- Pay special attention to technical terms and proper nouns.
- Include the `start_time` and `end_time` timecodes (MM:SS) for each speech segment.
- Output a JSON array where each object has: `start_time`, `end_time`, `text`, `voice_id`

**Task 2 - Technical Speakers**
- For each `voice_id`, extract speaker information.
- Pay special attention to technical titles and research affiliations.
- Output a JSON array where each object has: `voice_id`, `name`, `company`, `position`, `role_in_video`
"""

transcription = transcriber.transcribe_video(
    video_uri="https://www.youtube.com/watch?v=example",
    custom_prompt=custom_prompt
)
```

### Data Analysis

```python
# Get segments by speaker
speaker = transcription.get_speaker_by_voice_id(1)
segments = transcription.get_segments_by_speaker(speaker.name)

# Export to different formats
visualizer.export_to_csv(transcription, "output")
```

## 🎨 Visualization

The visualizer provides:

- **Colored speaker identification**: Known speakers in colors, unknown in gray
- **Formatted tables**: Clean, readable output
- **Summary statistics**: Quick overview of results
- **Export capabilities**: CSV and JSON formats

## 🚨 Error Handling

The transcriber includes robust error handling:

- **API retries**: Automatic retry with exponential backoff
- **Input validation**: FPS, timecode, and URL validation
- **Graceful failures**: Clear error messages and fallbacks
- **Configuration validation**: Environment variable checks

## 📈 Performance Tips

### Cost Optimization

- Use **low media resolution** for longer videos
- **Cache video tokens** for repeated analysis
- Use **batch processing** for multiple videos
- Choose appropriate **model** for your use case

### Quality Optimization

- Use **higher FPS** for fast-paced content
- Use **custom prompts** for specialized content
- Use **Gemini 2.5 Pro** for complex videos
- Provide **additional context** in prompts

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**: Check your `.env` file and API key validity
2. **Video Not Found**: Verify YouTube ID or URL accessibility
3. **Token Limits**: Use video segments or lower resolution
4. **Poor Quality**: Try different models or custom prompts

### Debug Mode

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🧪 Local Testing

Before deploying, test your setup locally:

```bash
# Run the test script
python test_local.py

# Expected output:
# ✅ All modules imported successfully
# ✅ Transcriber initialized
# ✅ Visualizer initialized
# ✅ Streamlit works
# 🎉 All tests passed!
```

For detailed local testing instructions, see [LOCAL_TESTING.md](LOCAL_TESTING.md).

## 🚀 Deployment

Deploy your transcriber to the cloud:

- **[Render](DEPLOYMENT.md#render)** (Recommended - Free tier)
- **[Railway](DEPLOYMENT.md#railway)** (Good for production)
- **[Streamlit Cloud](DEPLOYMENT.md#streamlit-cloud)** (Native hosting)
- **[Heroku](DEPLOYMENT.md#heroku)** (Legacy support)

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0.

## 🙏 Acknowledgments

- Based on the [Towards Data Science article](https://towardsdatascience.com/unlocking-multimodal-video-transcription-with-gemini/) by Laurent Picard
- Uses Google's Gemini multimodal models
- Built with the Google Gen AI Python SDK

## 📚 Additional Resources

- [Google Gen AI Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs)
- [Gemini Models Overview](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models)
- [Video Understanding Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/video-understanding)
- [Original Notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/use-cases/video-analysis/multimodal_video_transcription.ipynb)
