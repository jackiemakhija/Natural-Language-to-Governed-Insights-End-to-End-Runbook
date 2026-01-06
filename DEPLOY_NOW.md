# 🚀 Deploy Natural Language to Governed Insights - Step by Step

## Step 1: Get Hugging Face Credentials (2 minutes)

### Option A: Create New Account (if you don't have one)
1. Go to https://huggingface.co
2. Click "Sign Up" (top right)
3. Create free account
4. Verify your email

### Option B: Get Access Token (recommended)
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it: "git-deployment"
4. Type: "Write"
5. Click "Generate"
6. **Copy the token** (starts with `hf_...`)

---

## Step 2: Create Your Space (2 minutes)

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in:
   - **Owner**: Your username
   - **Space name**: `nl-governed-insights` (or your choice)
   - **License**: MIT
   - **Space SDK**: **Docker** ⚠️ **CRITICAL - Must be Docker!**
   - **Space hardware**: CPU basic (free)
4. Click **"Create Space"**
5. **Copy your Space URL** (you'll need it)

---

## Step 3: Deploy Files (5 minutes)

### Quick Deploy Commands:

```powershell
# Navigate to project
cd "c:\Users\kpkro\AppData\Local\Temp\Natural-Language-to-Governed-Insights"

# Create deployment folder
mkdir hf_deploy_temp
cd hf_deploy_temp

# Initialize git
git init
git lfs install

# Add your Space as remote (replace YOUR_USERNAME and SPACE_NAME)
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME

# Copy files
Copy-Item ..\app.py .
Copy-Item ..\main.py .
Copy-Item ..\requirements.txt .
Copy-Item ..\Dockerfile .
Copy-Item ..\README_HF.md README.md
Copy-Item -Recurse ..\src .
Copy-Item -Recurse ..\data .
Copy-Item -Recurse ..\config .

# Create .gitignore
@"
__pycache__/
*.pyc
.env
.venv
*.log
logs/
"@ | Out-File -FilePath .gitignore -Encoding UTF8

# Git add and commit
git add .
git commit -m "Deploy Natural Language to Governed Insights"

# Push to Hugging Face
git push -u origin main --force
```

**When prompted for credentials:**
- **Username**: Your HF username
- **Password**: Your HF token (the `hf_...` token you copied)

---

## Step 4: Wait for Build (2-3 minutes)

1. Go to your Space URL
2. You'll see "Building..." with logs
3. Wait for "Running" status
4. App will be live!

---

## Step 5: Test Demo Mode (1 minute)

The app works immediately in **DEMO MODE** - no additional setup needed!

Try these:
1. "What are the main customer complaints this month?"
2. "Show me the positive feedback trends"
3. Click the sample feedback items

---

## 🎯 Credentials Summary

### ✅ REQUIRED (for deployment):
- **Hugging Face username** (free account)
- **Hugging Face token** (for git push)
  - Get at: https://huggingface.co/settings/tokens
  - Type: Write access
  - Used once for deployment

### ✅ NOT REQUIRED (works without):
- ❌ Azure credentials - App has built-in demo mode!
- ❌ OpenAI API key
- ❌ Any other paid services

### 🔌 OPTIONAL (for full AI features):
If you want real Azure AI (optional), add these in Space Settings after deployment:
- `AZURE_TEXT_ANALYTICS_ENDPOINT`
- `AZURE_TEXT_ANALYTICS_KEY`

---

## 🔐 How to Use Hugging Face Token

### When Git Asks for Credentials:

**Method 1: During Push**
```
Username: your-hf-username
Password: hf_YourTokenHere
```

**Method 2: Store Credentials (Windows)**
```powershell
git config --global credential.helper wincred
```
Then enter credentials once, they'll be saved.

**Method 3: Clone with Token in URL**
```
git clone https://your-username:hf_TOKEN@huggingface.co/spaces/your-username/space-name
```

---

## 📊 Quick Deploy Summary

| Step | Time | What You Need |
|------|------|---------------|
| 1. Get HF credentials | 2 min | Email for signup |
| 2. Create Space | 2 min | HF account |
| 3. Deploy files | 5 min | HF token |
| 4. Build | 3 min | Nothing (automatic) |
| 5. Test | 1 min | Nothing (works immediately) |
| **TOTAL** | **~13 min** | **Just HF account!** |

---

## ✨ Key Points

1. **Demo Mode Works Immediately**
   - No Azure credentials needed
   - No API costs
   - Perfect for testing
   - Full functionality

2. **One-Time Deployment**
   - HF token used only for git push
   - No recurring credentials needed
   - Token can be revoked after deployment

3. **Free Hosting**
   - HF Spaces free tier
   - No credit card required
   - Always-on deployment

---

## 🆘 Troubleshooting

### "Permission denied" during push
- **Solution**: Use your HF **token**, not password
- Get token at: https://huggingface.co/settings/tokens

### "SDK must be Docker"
- **Solution**: Edit Space settings, change SDK to Docker

### Build fails
- **Check**: All files copied correctly
- **Check**: Dockerfile exists in root
- **Solution**: Check build logs in HF Space

### App shows errors
- **Normal!** Demo mode uses mock responses
- App is working correctly
- Optional: Add Azure credentials for real AI

---

## 🎯 Ready to Deploy?

1. **Get your HF token**: https://huggingface.co/settings/tokens
2. **Create Space** with Docker SDK
3. **Run the commands above** (replace YOUR_USERNAME and SPACE_NAME)
4. **Enter your HF token** when prompted
5. **Wait for build**
6. **Test immediately!**

---

**Your Space will be live at:**
`https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME`

**No other credentials needed - it works in demo mode out of the box!** ✨
