#!/bin/bash
# Deploy Natural Language to Governed Insights to Hugging Face Spaces

set -e

echo "🧠 Natural Language to Governed Insights - HF Deployment"
echo "=========================================================="

# Configuration
read -p "Enter your Hugging Face username: " HF_USERNAME
read -p "Enter your Space name (e.g., nl-governed-insights): " SPACE_NAME

SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"

echo ""
echo "📋 Deployment Configuration:"
echo "  Username: $HF_USERNAME"
echo "  Space Name: $SPACE_NAME"
echo "  Space URL: $SPACE_URL"
echo ""

# Check git
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed"
    exit 1
fi

# Create deployment directory
DEPLOY_DIR="hf_deploy_temp"
echo "📁 Creating deployment directory..."
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# Initialize git
echo "🔧 Initializing git repository..."
git init
git lfs install

# Add remote
echo "🔗 Adding Hugging Face remote..."
git remote add origin $SPACE_URL

# Copy files
echo "📦 Copying application files..."
cp ../app.py .
cp ../main.py .
cp ../requirements.txt .
cp ../Dockerfile .
cp -r ../src .
cp -r ../data .
cp -r ../config .

# Copy README with HF metadata
echo "📄 Preparing README..."
cp ../README_HF.md README.md

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
.Python
.env
.venv
*.log
.pytest_cache/
logs/
EOF

# Git operations
echo "➕ Adding files to git..."
git add .

echo "💾 Creating commit..."
git commit -m "Deploy Natural Language to Governed Insights"

# Push
echo ""
echo "🚀 Pushing to Hugging Face Spaces..."
git push -u origin main --force

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📍 Next Steps:"
echo "   1. Visit: $SPACE_URL"
echo "   2. Wait for Space to build (2-3 minutes)"
echo "   3. (Optional) Add Azure AI secrets for full features:"
echo "      - AZURE_TEXT_ANALYTICS_ENDPOINT"
echo "      - AZURE_TEXT_ANALYTICS_KEY"
echo "   4. Test with sample queries!"
echo ""
echo "🔗 Space URL: $SPACE_URL"
echo ""

# Cleanup
cd ..
read -p "Remove deployment directory? (y/n): " CLEANUP
if [ "$CLEANUP" == "y" ]; then
    rm -rf $DEPLOY_DIR
    echo "✨ Cleanup complete"
fi

echo ""
echo "🎉 Deployment finished!"
