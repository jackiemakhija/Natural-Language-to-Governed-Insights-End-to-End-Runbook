# Natural Language to Governed Insights - End-to-End Runbook

**Transform natural language questions into governed insights using Microsoft Fabric + Foundry Local LLM**

## 📖 Overview

This project builds an end-to-end **Natural Language to Insights** experience where a local LLM generates governed DAX queries and executes them against Power BI Semantic Models, ensuring compliance with centralized KPIs and security policies.

**Source:** [GitHub Repository by Jagjeet Makhija](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook)

**LinkedIn Article:** [Natural Language Governed Insights](https://www.linkedin.com/pulse/natural-language-governed-insights-end-to-end-runbook-jagjeet-makhija-arbtc/)

## 🎯 Architecture Flow

```
Natural Language Question
    ↓
Foundry Local LLM (generates DAX)
    ↓
Power BI Semantic Model (governed KPIs + RLS)
    ↓
Power BI ExecuteQueries API
    ↓
Results Display & Export
```

## 🚀 Quick Start

### Prerequisites

- **Microsoft Fabric** access (permission to create Workspace, Warehouse, and Semantic Model)
- **Azure CLI** installed: [Install Guide](https://learn.microsoft.com/cli/azure/install-azure-cli)
- **Python 3.10+** on your local machine
- **Foundry Local** installed and running at `http://127.0.0.1:51970/v1`

### Installation

```powershell
# Navigate to project directory
cd NL-Governed-Insights

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
copy .env.template .env
# Edit .env with your settings
```

### Start Foundry Local

```bash
foundry service start
foundry model run qwen2.5-14b-instruct
curl http://127.0.0.1:51970/v1/models  # Verify
```

### Launch the Application

```bash
streamlit run main.py
```

Application will open at: `http://localhost:8501`

## 📁 Project Structure

This folder contains a **simplified version** for demonstration. The full implementation is available in the [GitHub repository](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook).

```
NL-Governed-Insights/
├── README.md                    # This file
├── architecture.md              # Architecture documentation
├── main.py                      # Demo application entry point
├── requirements.txt             # Python dependencies
├── .env.template                # Environment variables template
│
├── src/                         # Source code modules
│   ├── __init__.py
│   ├── data_ingestion.py       # Data ingestion from Azure
│   ├── nlp_processor.py        # NLP processing with Azure AI
│   └── insights_generator.py   # Insights generation engine
│
├── config/                      # Configuration files
│   └── settings.json           # Application settings
│
└── data/                        # Sample data
    └── sample_data.json        # Demo queries and feedback
```

## 🏗️ Full Repository Structure

For the **complete production-ready implementation**, refer to the GitHub repository:

```
github_release/
├── app.py                          # Main Streamlit multi-page application
├── config.py                       # Centralized configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
│
├── modules/                        # Core business logic
│   ├── token_manager.py           # Azure AD authentication
│   ├── workspace_manager.py       # Workspace/dataset discovery
│   ├── fabric_dax_generator.py    # LLM-based DAX generation
│   └── power_bi_executor.py       # Power BI ExecuteQueries API client
│
├── pages/                          # Streamlit UI pages
│   ├── workspace_config.py        # Settings page
│   └── semantic_query.py          # Semantic Query page (NL→DAX→Results)
│
├── components/                     # Reusable UI components
│   └── results_display.py         # Results formatting & export
│
├── sql/                            # Sample SQL scripts
│   └── sample_warehouse_setup.sql # Fabric Warehouse DDL & data
│
├── dax/                            # DAX query examples
│   └── sample_queries.dax         # Example DAX patterns
│
├── scripts/                        # Setup automation
│   ├── setup_foundry.sh           # Foundry Local setup
│   └── setup_auth_azure.ps1       # Azure CLI authentication
│
└── docs/                           # Documentation
    ├── RUNBOOK_CODE_MAPPING.md    # Runbook → Code mapping
    ├── CODE_REFERENCE_GUIDE.md    # Quick reference guide
    └── NL_to_Governed_Insights_End_to_End_Runbook.docx
```

## 🎨 Features

### Multi-Page Streamlit Application

1. **💬 Chat Page**
   - Intelligent Foundry Local chat
   - Auto model routing (Phi for simple, Qwen for complex queries)
   - Manual model selection option

2. **⚙️ Settings Page**
   - Azure AD authentication (CLI or App Registration)
   - Workspace and dataset discovery
   - Connection validation

3. **📊 Semantic Query Page**
   - Natural language input
   - Automatic DAX generation
   - DAX validation and editing
   - Query execution against semantic models
   - Results export (CSV, JSON)

### Key Capabilities

- ✅ **Governed KPIs**: All queries use certified measures from semantic models
- ✅ **Row-Level Security**: Enforced through Power BI semantic models
- ✅ **Local LLM**: Foundry Local for offline DAX generation
- ✅ **Azure Integration**: Seamless authentication and resource discovery
- ✅ **Export Options**: Download results as CSV or JSON

## 📊 Example Queries

Try these natural language questions:

- "What is total revenue?"
- "Show revenue by month for this year"
- "What is the profit margin percentage?"
- "Revenue YTD by sales region"
- "Top 10 products by quantity sold"

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Foundry Local Configuration
FOUNDRY_BASE=http://127.0.0.1:51970/v1
FOUNDRY_MODEL_PHI=phi-3-mini
FOUNDRY_MODEL_QWEN=qwen2.5-14b-instruct
FOUNDRY_TIMEOUT=180

# Power BI / Fabric Configuration
POWER_BI_WORKSPACE_ID=your_workspace_id
POWER_BI_DATASET_ID=your_dataset_id

# Azure AD / Tenant
AZURE_TENANT_ID=your_tenant_id
```

## 📚 Documentation & Resources

### GitHub Repository
- **Main Repository:** https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook
- **README:** [Full Documentation](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/README.md)
- **Code Reference Guide:** [Reference](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/docs/CODE_REFERENCE_GUIDE.md)

### Key Files in Repository
- **app.py** - Main Streamlit application ([View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/app.py))
- **modules/fabric_dax_generator.py** - DAX generation ([View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/fabric_dax_generator.py))
- **modules/power_bi_executor.py** - Query execution ([View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/power_bi_executor.py))
- **sql/sample_warehouse_setup.sql** - SQL examples ([View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/sql/sample_warehouse_setup.sql))
- **dax/sample_queries.dax** - DAX examples ([View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/dax/sample_queries.dax))

## 🛠️ Troubleshooting

**Foundry Local not reachable:**
- Confirm service is running: `curl http://127.0.0.1:51970/v1/models`

**ExecuteQueries 401/403:**
- Ensure access token is valid
- Check Power BI permissions for workspace/dataset

**Empty results:**
- Try simpler question
- Confirm semantic model contains data and measures

**Slow responses:**
- Use smaller local model (Phi instead of Qwen)
- Reduce prompt verbosity

## 🚀 Next Steps

1. **Clone full repository** for production-ready code
2. **Set up Microsoft Fabric** workspace and warehouse
3. **Create semantic model** with governed KPIs
4. **Configure authentication** (Azure CLI or App Registration)
5. **Start Foundry Local** with your preferred model
6. **Run the application** and explore!

## 📝 License

See LICENSE file for details.

---

**Last Updated:** December 26, 2025  
**Version:** 1.0  
**Status:** Demo/Reference Implementation
