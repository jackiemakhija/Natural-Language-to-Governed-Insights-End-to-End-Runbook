---
title: Natural Language to Governed Insights
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
app_file: Dockerfile
pinned: false
license: mit
---


# Natural Language to Governed Insights 🧠

## Core Use Case
Enable business users to ask questions in natural language and receive accurate, governed, compliant insights—no SQL, DAX, or technical queries required.

### Purpose & Business Value
- Democratize analytics and enable self-service BI
- Reduce dependency on data analysts
- Provide an AI-powered backend for Copilot/Agent scenarios
- Ensure compliance, governance, and auditability
- Achieve 90% faster insights, 40–60% analyst workload reduction, and 3–5x faster decision-making

### Required Skills & Architecture
- RAG (Retrieval-Augmented Generation) architecture design
- LLM orchestration and prompt engineering
- Integration with Azure OpenAI/LLM APIs
- Use of Azure AI Search for vector and hybrid retrieval
- Semantic modeling and data governance (RLS, lineage, audit logs)
- Python and REST API development
- Azure security (Entra ID, RBAC, Key Vault)

### Technical Flow
1. User submits a natural language query
2. LLM interprets intent
3. Query is grounded using a semantic layer, structured models, and vector embeddings
4. Retrieval is performed via Azure AI Search (vector + keyword hybrid)
5. LLM generates an answer using the retrieved context
6. All queries are logged for audit and compliance

---

Transform natural language questions into governed insights using Azure AI Services. This application demonstrates NLP-powered sentiment analysis, key phrase extraction, and automated insight generation.

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python 3.11"/>
  <img src="https://img.shields.io/badge/Streamlit-1.28-red" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Azure_AI-Enabled-blue" alt="Azure AI"/>
</div>

## ✨ Features

### 🤖 Natural Language Processing
- **Sentiment Analysis**: Automatically detect positive, negative, or neutral sentiment
- **Key Phrase Extraction**: Identify important topics and themes
- **Entity Recognition**: Extract people, organizations, locations from text
- **Automated Insights**: Generate actionable recommendations based on analysis

### 🎯 Use Cases
- Customer feedback analysis
- Support ticket categorization
- Product review insights
- Social media monitoring
- Survey response analysis
- Quality assurance monitoring

### 💡 Demo Mode
- Works out-of-the-box with **mock responses** (no Azure credentials needed)
- Configure Azure AI credentials for **real-time analysis**
- Perfect for testing and demonstrations



## 🚀 Live Demo

### Hugging Face Space

Try the app live on Hugging Face Spaces:

[Natural-Language-to-Governed-Insights on Hugging Face Spaces](https://huggingface.co/spaces/jackiemakhija/Natural-Language-to-Governed-Insights)

### GitHub Repository

View the full source code and contribute on GitHub:

[https://github.com/jagjeetmakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook](https://github.com/jagjeetmakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook)

### Sample Queries
1. "What are the main customer complaints this month?"
2. "Show me the positive feedback trends"
3. "Identify areas needing improvement in customer service"

## 🏗️ Architecture

```
User Input
    ↓
Natural Language Query
    ↓
Azure AI Text Analytics
    ├─> Sentiment Analysis
    ├─> Key Phrase Extraction
    └─> Entity Recognition
    ↓
Insights Generator
    ├─> Pattern Detection
    ├─> Recommendation Engine
    └─> Confidence Scoring
    ↓
Visualized Results
```

## 🔧 Configuration (Optional)

### For Full Azure AI Integration

This Space can run in two modes:

**1. Demo Mode (Default)**
- No configuration needed
- Uses mock responses
- Perfect for testing

**2. Azure AI Mode (Full Features)**
Add these secrets in Space Settings:

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `AZURE_TEXT_ANALYTICS_ENDPOINT` | Azure Text Analytics endpoint | Azure Portal → Text Analytics Resource |
| `AZURE_TEXT_ANALYTICS_KEY` | Azure API key | Resource → Keys and Endpoint |

### Setting Up Azure Text Analytics (Optional)

1. Go to [Azure Portal](https://portal.azure.com)
2. Create a **Text Analytics** resource
3. Copy the **Endpoint** and **Key**
4. Add them as secrets in your HF Space

## 📊 Sample Data Included

### Pre-loaded Feedback Examples
- ✅ Customer service feedback
- ✅ Product quality reviews
- ✅ Shipping & logistics comments
- ✅ Website usability feedback

### Demo Scenarios
1. **Customer Service Analysis** - Analyze support team performance
2. **Product Quality Assessment** - Evaluate product satisfaction
3. **Shipping & Logistics Review** - Understand delivery experience

## 🧪 How to Use

### Method 1: Custom Text Analysis
1. Enter your text in the input box
2. Click **Analyze**
3. Review sentiment, key phrases, and recommendations

### Method 2: Sample Queries
1. Click any sample query button
2. Instant analysis results appear
3. Review detailed breakdown

### Method 3: Analyze Sample Feedback
1. Go to **Sample Data** tab
2. Expand any feedback item
3. Click **Analyze This Feedback**

## 📈 Features in Detail

### Sentiment Analysis
- Classifies text as positive, negative, or neutral
- Provides confidence scores for each sentiment
- Tracks sentiment trends over time

### Key Phrase Extraction
- Identifies main topics and themes
- Highlights important keywords
- Groups related concepts

### Automated Recommendations
- Generates actionable insights
- Suggests next steps based on sentiment
- Prioritizes critical issues

### Analysis History
- Track all processed queries
- Review past insights
- Export results for reporting

## 🎓 Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **NLP Engine**: Azure AI Text Analytics
- **Language**: Python 3.11
- **Deployment**: Docker on Hugging Face Spaces
- **Cloud**: Azure AI Services (optional)

## 🔒 Security & Governance

- **Data Privacy**: No data stored permanently
- **Secure Credentials**: All secrets encrypted by HF Spaces
- **Compliance Ready**: Enterprise-grade security practices
- **Audit Trail**: All operations logged
- **Access Control**: Can be integrated with Azure RBAC

## 💡 Real-World Applications

### Customer Experience
- Monitor customer satisfaction in real-time
- Identify trending issues before they escalate
- Track improvement over time

### Support Operations
- Automatically categorize support tickets
- Prioritize urgent issues
- Measure team performance

### Product Management
- Understand feature reception
- Gather user sentiment on launches
- Guide product roadmap decisions

### Marketing & Social
- Monitor brand sentiment
- Track campaign performance
- Identify influencer opportunities

## 📖 Example Outputs

### Positive Sentiment Example
```
Text: "The customer service was excellent and resolved my issue quickly."
Sentiment: POSITIVE (75% confidence)
Key Topics: customer service, resolved issue
Recommendations:
- Maintain current positive practices
- Share success stories with team
```

### Negative Sentiment Example
```
Text: "Very disappointed with the long wait times and lack of communication."
Sentiment: NEGATIVE (75% confidence)
Key Topics: wait times, lack communication
Recommendations:
- Consider addressing negative feedback promptly
- Investigate root causes of dissatisfaction
```

## 🚦 Getting Started

### Immediate Use
1. Open the Space
2. Try sample queries
3. Analyze your own text

### With Azure AI (Optional)
1. Configure Azure secrets
2. Restart Space
3. Enjoy full NLP capabilities

## 🔗 Resources

- [Azure AI Text Analytics Docs](https://learn.microsoft.com/azure/cognitive-services/language-service/)
- [Streamlit Documentation](https://docs.streamlit.io)
- [GitHub Repository](https://github.com/jagjeetmakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook)
- [LinkedIn Article](https://www.linkedin.com/pulse/natural-language-governed-insights-end-to-end-runbook-jagjeet-makhija-arbtc/)

## 📝 License

MIT License - Free to use for personal and commercial projects

## 🤝 Contributing

Contributions welcome! This project demonstrates best practices for:
- NLP-powered analytics
- Azure AI integration
- Governed insight generation
- Enterprise-ready deployments

## 💬 Feedback

Found an issue or have a suggestion? Open an issue on the GitHub repository.

## 🎯 Next Steps

1. **Try It Now** - Start with sample queries
2. **Analyze Your Data** - Paste your own feedback/reviews
3. **Configure Azure** - Enable full AI capabilities
4. **Export Insights** - Use for reporting and decision-making

---

**Built with ❤️ for the data and AI community**

*Transform unstructured feedback into actionable insights with the power of Azure AI*
