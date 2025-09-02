# 🚀 Deployment Guide

This guide will help you deploy the Multimodal Video Transcriber to various cloud platforms.

## 📋 Prerequisites

1. **Google AI Studio API Key** (recommended for testing)
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the key for later use

2. **GitHub Repository**
   - Push your code to a GitHub repository
   - Make sure all files are committed

## 🎯 Deployment Options

### Option 1: Render (Recommended - Free Tier)

**Step 1: Sign up for Render**
- Go to [render.com](https://render.com)
- Sign up with your GitHub account

**Step 2: Create a new Web Service**
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select the repository with the transcriber code

**Step 3: Configure the service**
- **Name**: `multimodal-video-transcriber`
- **Environment**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- **Plan**: `Free`

**Step 4: Set Environment Variables**
- Go to "Environment" tab
- Add the following variables:
  - `GOOGLE_GENAI_USE_VERTEXAI`: `False`
  - `GOOGLE_API_KEY`: `your_api_key_here`

**Step 5: Deploy**
- Click "Create Web Service"
- Wait for the build to complete
- Your app will be available at `https://your-app-name.onrender.com`

### Option 2: Railway

**Step 1: Sign up for Railway**
- Go to [railway.app](https://railway.app)
- Sign up with your GitHub account

**Step 2: Create a new project**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository

**Step 3: Configure deployment**
- Railway will automatically detect it's a Python app
- The `railway.json` file will handle the configuration

**Step 4: Set Environment Variables**
- Go to "Variables" tab
- Add:
  - `GOOGLE_GENAI_USE_VERTEXAI`: `False`
  - `GOOGLE_API_KEY`: `your_api_key_here`

**Step 5: Deploy**
- Railway will automatically deploy your app
- Get the URL from the "Deployments" tab

### Option 3: Streamlit Cloud (Native)

**Step 1: Sign up for Streamlit Cloud**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Sign up with your GitHub account

**Step 2: Deploy**
- Click "New app"
- Select your repository
- Set the path to `app.py`
- Click "Deploy"

**Step 3: Set Environment Variables**
- Go to "Settings" → "Secrets"
- Add your API key:
```toml
GOOGLE_API_KEY = "your_api_key_here"
GOOGLE_GENAI_USE_VERTEXAI = "False"
```

### Option 4: Heroku

**Step 1: Install Heroku CLI**
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

**Step 2: Login and create app**
```bash
heroku login
heroku create your-app-name
```

**Step 3: Set environment variables**
```bash
heroku config:set GOOGLE_API_KEY=your_api_key_here
heroku config:set GOOGLE_GENAI_USE_VERTEXAI=False
```

**Step 4: Deploy**
```bash
git push heroku main
```

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Google AI Studio API key | Yes (for AI Studio) | - |
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI instead | No | `False` |
| `GOOGLE_CLOUD_PROJECT` | Google Cloud project ID | Yes (for Vertex AI) | - |
| `GOOGLE_CLOUD_LOCATION` | Google Cloud location | No | `global` |

## 🧪 Testing Your Deployment

1. **Access your deployed app**
2. **Configure API credentials** in the sidebar
3. **Test with a YouTube video ID**: `0pJn3g8dfwk`
4. **Verify transcription results**

## 🚨 Troubleshooting

### Common Issues

**Build Failures**
- Check that all dependencies are in `requirements.txt`
- Verify Python version compatibility
- Check build logs for specific errors

**API Key Issues**
- Ensure the API key is correctly set in environment variables
- Verify the key has proper permissions
- Check if you're using the correct API (AI Studio vs Vertex AI)

**Memory Issues**
- Free tiers have memory limits
- Consider using video segments for longer videos
- Use lower FPS settings

**Timeout Issues**
- Long videos may timeout on free tiers
- Use video segments to process shorter portions
- Consider upgrading to paid plans for longer processing

### Debug Mode

To enable debug logging, add this environment variable:
```
STREAMLIT_LOG_LEVEL=debug
```

## 📊 Monitoring

### Render
- Check "Logs" tab for real-time logs
- Monitor "Metrics" for performance

### Railway
- Check "Deployments" tab for logs
- Monitor resource usage

### Streamlit Cloud
- Check "Activity" for deployment status
- View logs in the app interface

## 🔄 Updates

To update your deployed app:

1. **Make changes to your code**
2. **Commit and push to GitHub**
3. **Your platform will automatically redeploy**

For manual redeploy:
- **Render**: Go to "Manual Deploy" → "Deploy latest commit"
- **Railway**: Go to "Deployments" → "Deploy"
- **Streamlit Cloud**: Changes auto-deploy

## 💰 Cost Considerations

### Free Tiers
- **Render**: 750 hours/month
- **Railway**: $5 credit/month
- **Streamlit Cloud**: Unlimited (with limitations)
- **Heroku**: Discontinued free tier

### Paid Plans
- Consider paid plans for:
  - Longer video processing
  - Higher usage limits
  - Better performance
  - Custom domains

## 🔒 Security

### Best Practices
- Never commit API keys to your repository
- Use environment variables for sensitive data
- Regularly rotate your API keys
- Monitor usage and costs

### API Key Management
- Store keys securely in your deployment platform
- Use different keys for development and production
- Set up alerts for unusual usage

## 📞 Support

If you encounter issues:

1. **Check the logs** in your deployment platform
2. **Verify environment variables** are set correctly
3. **Test locally** first with `streamlit run app.py`
4. **Check the original notebook** for reference
5. **Open an issue** in the GitHub repository

## 🎉 Success!

Once deployed, you'll have a web interface for:
- ✅ Video transcription with speaker identification
- ✅ Multiple input sources (YouTube, URLs, Cloud Storage)
- ✅ Export options (JSON, CSV)
- ✅ Analytics and visualizations
- ✅ Custom prompts and configurations

Your transcriber is now ready for testing and production use!
