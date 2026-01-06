# Quick Deployment Guide - Natural Language to Governed Insights

**5-Minute Deployment to Hugging Face Spaces** 🚀

## Two Deployment Options

### Option 1: Automated Script ⚡ (Recommended)

**Windows:**
```cmd
cd "c:\Users\kpkro\AppData\Local\Temp\Natural-Language-to-Governed-Insights"
deploy-to-huggingface.bat
```

**Linux/Mac:**
```bash
cd /path/to/Natural-Language-to-Governed-Insights
chmod +x deploy-to-huggingface.sh
./deploy-to-huggingface.sh
```

The script will:
- ✅ Create deployment package
- ✅ Initialize git repository
- ✅ Push to Hugging Face Space
- ✅ Guide you through setup

---

### Option 2: Manual Deployment 🔧

#### Step 1: Create HF Space (2 min)
1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Configure:
   - **Name**: `nl-governed-insights`
   - **SDK**: **Docker** ⚠️ (Important!)
   - **Hardware**: CPU basic (free)
4. Click **"Create Space"**

#### Step 2: Clone & Push (3 min)
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/nl-governed-insights
cd nl-governed-insights

# Copy these files from the project:
# - app.py (NEW Streamlit app)
# - main.py (original entry point)
# - requirements.txt (updated)
# - Dockerfile (NEW)
# - src/ (folder)
# - data/ (folder with sample_data.json)
# - config/ (folder)
# - Copy README_HF.md as README.md

git add .
git commit -m "Deploy Natural Language to Governed Insights"
git push
```

#### Step 3: Wait & Test (3 min)
- Space builds automatically (2-3 minutes)
- Test with: "What are the main customer complaints this month?"

---

## Configuration Options

### Demo Mode (Default) - No Setup Required
- Works immediately
- Uses mock sentiment analysis
- Perfect for testing
- No Azure account needed

### Full Azure AI Mode (Optional)
Add these secrets in Space Settings → Variables and secrets:

| Secret Name | Value | Get From |
|-------------|-------|----------|
| `AZURE_TEXT_ANALYTICS_ENDPOINT` | `https://YOUR-RESOURCE.cognitiveservices.azure.com/` | Azure Portal |
| `AZURE_TEXT_ANALYTICS_KEY` | `your-api-key` | Azure Portal → Keys |

---

## Quick Test Scenarios

### Test 1: Positive Feedback
```
"The customer service was excellent and resolved my issue quickly."
```
**Expected**: Sentiment = POSITIVE, Confidence ~75%

### Test 2: Negative Feedback
```
"Very disappointed with the long wait times and lack of communication."
```
**Expected**: Sentiment = NEGATIVE, Confidence ~75%

### Test 3: Neutral Feedback
```
"Website is okay but checkout process could be simpler."
```
**Expected**: Sentiment = NEUTRAL, Mixed scores

---

## Files Ready for Deployment

✅ **Core Files**
- `app.py` - Streamlit web application (NEW)
- `main.py` - Original CLI entry point
- `requirements.txt` - Updated with Streamlit
- `Dockerfile` - Docker configuration (NEW)

✅ **Application Code**
- `src/data_ingestion.py` - Data ingestion module
- `src/nlp_processor.py` - NLP processing with Azure AI
- `src/insights_generator.py` - Insight generation engine

✅ **Data & Config**
- `data/sample_data.json` - Enhanced with 8 feedback samples
- `config/settings.json` - Application settings

✅ **Deployment Files** (NEW)
- `README_HF.md` - HF Space README (use as README.md)
- `deploy-to-huggingface.bat` - Windows script
- `deploy-to-huggingface.sh` - Linux/Mac script

---

## Validation Checklist

Before deploying:
- [x] Python 3.11.9 installed
- [x] No code errors
- [x] Streamlit app created
- [x] Docker configuration ready
- [x] Sample data enhanced (8 examples)
- [x] Demo mode working (no Azure needed)
- [x] Deployment scripts ready

---

## Common Issues & Solutions

### Build Fails
- **Check**: SDK must be "Docker" not "Streamlit"
- **Check**: Dockerfile exists in root
- **Check**: Port 7860 is exposed

### App Loads but Shows Errors
- Normal in demo mode - uses mock responses
- Configure Azure secrets for real NLP

### Azure Connection Fails
- Verify endpoint URL format
- Check API key is valid
- Ensure Text Analytics resource is active

---

## What Users Will See

### Landing Page
- Clean Streamlit interface
- "Demo Mode" warning (if no Azure secrets)
- 3 tabs: Analyze Text, Sample Data, History

### Sample Queries
- Pre-loaded clickable queries
- 8 sample feedback items to analyze
- Instant analysis results

### Analysis Output
- Sentiment (Positive/Negative/Neutral)
- Confidence score
- Key topics/phrases
- Automated recommendations
- Confidence breakdown

---

## Demo Mode Features

Works WITHOUT Azure credentials:
- ✅ Sentiment detection (keyword-based)
- ✅ Simple key phrase extraction
- ✅ Confidence scoring
- ✅ Recommendation generation
- ✅ Full UI functionality

Perfect for:
- Testing the interface
- Demonstrating capabilities
- No-cost evaluation

---

## Total Deployment Time

- **Automated**: ~5 minutes
- **Manual**: ~10 minutes
- **Build time**: 2-3 minutes

---

## After Deployment

1. **Share your Space URL**
2. **Test all sample queries**
3. **Try your own text**
4. **(Optional) Add Azure secrets for full AI**
5. **Monitor in HF Analytics**

---

## Support Resources

- 📖 Full README: [README_HF.md](README_HF.md)
- 🏗️ Architecture: [architecture.md](architecture.md)
- 📊 Sample data: [data/sample_data.json](data/sample_data.json)
- 🔗 GitHub: https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook

---

**🎯 Ready to Deploy!**

Choose your method above and get started in ~5 minutes!

**Cost**: FREE (HF free tier + optional Azure)
