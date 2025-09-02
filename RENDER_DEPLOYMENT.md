# 🚀 Render Deployment Guide

This guide will help you deploy the Multimodal Video Transcriber to Render with the latest configuration fix.

## ✅ **Issue Fixed**

The previous error `❌ Error during transcription: Invalid configuration. Please check your environment variables.` has been resolved. The app now properly handles API key configuration through the UI interface.

## 🔧 **Deployment Steps**

### **1. Connect Your Repository**

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `dollyto/multimodal-video-transcriber`
4. Select the repository

### **2. Configure the Service**

**Service Name**: `multimodal-video-transcriber` (or your preferred name)

**Environment**: `Python 3`

**Build Command**:
```bash
pip install -r requirements.txt
```

**Start Command**:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

### **3. Environment Variables**

**Required Variables**:
- `GOOGLE_GENAI_USE_VERTEXAI`: `False`
- `GOOGLE_API_KEY`: `your_api_key_here` (Get from [Google AI Studio](https://aistudio.google.com/app/apikey))

**Optional Variables**:
- `PYTHON_VERSION`: `3.9.16`

### **4. Deploy**

1. Click **"Create Web Service"**
2. Wait for the build to complete (2-3 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`

## 🎯 **Using the App**

### **1. Set Your API Key**

1. Open your deployed app
2. In the sidebar, find **"API Setup"**
3. Paste your Google AI Studio API key
4. Click **"Set API Key"**
5. You should see: ✅ **"API key set!"**

### **2. Test Transcription**

1. Go to the **"🎬 Transcribe"** tab
2. Enter a YouTube Video ID (e.g., `0pJn3g8dfwk`)
3. Click **"🚀 Start Transcription"**
4. Wait for processing (30-60 seconds for short videos)
5. View results in the **"📊 Results"** tab

## 🔍 **Troubleshooting**

### **Common Issues**

**"Invalid configuration" Error**
- ✅ **Fixed**: The app now properly handles UI-based API key configuration
- Make sure you've set your API key in the sidebar

**"API key not set" Error**
- Set your API key in the sidebar under **"API Setup"**
- Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

**Build Fails**
- Check that your repository is public or Render has access
- Verify `requirements.txt` is in the root directory
- Ensure `app.py` exists in the root directory

**App Won't Start**
- Check the logs in Render dashboard
- Verify the start command is correct
- Ensure all dependencies are installed

### **Logs and Debugging**

1. Go to your Render dashboard
2. Click on your service
3. Go to **"Logs"** tab
4. Look for any error messages

## 📊 **Expected Behavior**

### **Successful Deployment**
- ✅ Build completes without errors
- ✅ App starts and shows the Streamlit interface
- ✅ Sidebar shows API configuration options
- ✅ No "Invalid configuration" errors

### **Successful Transcription**
- ✅ API key is accepted
- ✅ Video processing starts
- ✅ Progress bar shows completion
- ✅ Results appear in tabs
- ✅ Export options work

## 🔄 **Redeploying After Updates**

When you push changes to GitHub:

1. **Automatic**: Render will automatically redeploy
2. **Manual**: Go to Render dashboard → **"Manual Deploy"**

## 💰 **Cost Considerations**

- **Free Tier**: 750 hours/month
- **Google AI Studio**: Free tier available
- **Video Processing**: ~$0.01-0.10 per minute of video

## 🎉 **Success!**

Your transcriber should now work perfectly on Render! The configuration issue has been resolved, and the app properly handles API key input through the UI.

## 📞 **Support**

If you still encounter issues:

1. Check the [GitHub repository](https://github.com/dollyto/multimodal-video-transcriber)
2. Review the [main deployment guide](DEPLOYMENT.md)
3. Check [local testing guide](LOCAL_TESTING.md) for troubleshooting

---

**Happy transcribing! 🎬**
