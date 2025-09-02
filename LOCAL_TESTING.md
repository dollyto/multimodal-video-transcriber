# 🧪 Local Testing Guide

This guide will help you test the Multimodal Video Transcriber locally before deploying to cloud platforms.

## ✅ **Prerequisites Check**

The test script shows that everything is working! Here's what we verified:

- ✅ **Dependencies installed**: All required packages are installed
- ✅ **Transcriber working**: Successfully transcribed a YouTube video
- ✅ **Speaker identification**: Found 6 speakers with names
- ✅ **Script segments**: Generated 13 timecoded segments
- ✅ **Web interface ready**: Streamlit is properly configured

## 🚀 **Quick Start for Local Testing**

### **1. Get Your API Key**
- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a new API key
- Copy the key

### **2. Set Environment Variable**
```bash
export GOOGLE_API_KEY=your_actual_api_key_here
```

### **3. Run the Web Interface**
```bash
streamlit run app.py
```

### **4. Open Your Browser**
- Go to: http://localhost:8501
- You should see the Multimodal Video Transcriber interface

## 🎬 **Testing the App**

### **Basic Test**
1. **Configure API**: In the sidebar, paste your API key and click "Set API Key"
2. **Input Video**: Use YouTube Video ID: `0pJn3g8dfwk`
3. **Start Transcription**: Click "🚀 Start Transcription"
4. **View Results**: Check the "📊 Results" tab

### **Advanced Testing**
- **Video Segments**: Enable segments to test specific time ranges
- **Different Models**: Try Gemini 2.5 Pro for complex videos
- **Custom Prompts**: Test with specialized content
- **Export Options**: Download JSON and CSV files

## 📊 **Expected Results**

For the test video (`0pJn3g8dfwk`), you should see:

- **6 Speakers identified**:
  - Professor Hannah Fry
  - Demis Hassabis
  - Anca Dragan
  - Pushmeet Kohli
  - Jeff Dean
  - Douglas Eck

- **13 Script Segments** with timecodes
- **Interactive visualizations** in the Analytics tab
- **Export options** for JSON and CSV

## 🔧 **Troubleshooting**

### **Common Issues**

**API Key Error**
```bash
❌ Please set your GOOGLE_API_KEY environment variable
```
**Solution**: Set your API key: `export GOOGLE_API_KEY=your_key`

**Import Errors**
```bash
❌ ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Install dependencies: `pip install --user -r requirements.txt`

**Permission Errors**
```bash
❌ Permission denied
```
**Solution**: Use `--user` flag: `pip install --user -r requirements.txt`

### **Test Script**
Run the test script anytime to verify everything works:
```bash
python test_local.py
```

## 🌐 **Web Interface Features**

### **Sidebar Configuration**
- **API Setup**: Choose between Google AI Studio and Vertex AI
- **Model Settings**: Select Gemini model and frame rate
- **Processing Options**: Enable video segments and time ranges
- **Export Options**: Choose JSON and CSV export

### **Main Interface**
- **🎬 Transcribe Tab**: Input video and start transcription
- **📊 Results Tab**: View speakers and script segments
- **📈 Analytics Tab**: Interactive charts and visualizations
- **ℹ️ About Tab**: Documentation and resources

### **Input Methods**
- YouTube Video ID
- YouTube URL
- Direct Video URL
- Google Cloud Storage URI

## 📈 **Performance Notes**

### **Processing Times**
- **Short videos** (< 1 min): ~30-60 seconds
- **Medium videos** (1-5 min): ~2-5 minutes
- **Long videos** (5+ min): ~5-15 minutes

### **Token Usage**
- **Input tokens**: ~17k for 1-minute video
- **Output tokens**: ~1.3k for transcription
- **Cost**: Very low with Google AI Studio free tier

### **Memory Usage**
- **Local testing**: ~200-500MB RAM
- **Web interface**: Additional ~100MB for Streamlit

## 🎯 **Next Steps**

Once local testing is successful:

1. **Deploy to Render** (recommended):
   - Follow `DEPLOYMENT.md` guide
   - Use free tier for testing

2. **Deploy to Railway**:
   - Alternative platform
   - Good for production use

3. **Deploy to Streamlit Cloud**:
   - Native Streamlit hosting
   - Easy deployment

## 🔒 **Security Notes**

- **Never commit API keys** to your repository
- **Use environment variables** for sensitive data
- **Test with free tier** before production use
- **Monitor usage** to avoid unexpected costs

## 📞 **Support**

If you encounter issues:

1. **Run the test script**: `python test_local.py`
2. **Check the logs**: Look for error messages
3. **Verify API key**: Ensure it's correct and active
4. **Check internet**: Ensure YouTube access
5. **Review dependencies**: Make sure all packages are installed

## 🎉 **Success!**

Your transcriber is now ready for:
- ✅ Local testing and development
- ✅ Web interface usage
- ✅ Cloud deployment
- ✅ Production use

Happy transcribing! 🎬
