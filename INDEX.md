# GitHub Release - Complete Package

This is a **production-ready release** of the Natural Language to Governed Insights application built with **Foundry Local** + **Microsoft Fabric**.

## 📦 Package Contents

### Core Application
- **[app.py](app.py)** - Main Streamlit multi-page application (Chat, Settings, Semantic Query)
- **[config.py](config.py)** - Centralized configuration (Foundry, Power BI, Azure settings)
- **[requirements.txt](requirements.txt)** - Python dependencies

### Business Logic Modules
- **[modules/token_manager.py](modules/token_manager.py)** - Azure AD authentication (CLI + App Registration)
- **[modules/workspace_manager.py](modules/workspace_manager.py)** - Workspace & dataset discovery
- **[modules/fabric_dax_generator.py](modules/fabric_dax_generator.py)** - LLM-based DAX generation
- **[modules/power_bi_executor.py](modules/power_bi_executor.py)** - Power BI ExecuteQueries API client

### User Interface Pages
- **[pages/workspace_config.py](pages/workspace_config.py)** - Settings page (authentication, workspace selection)
- **[pages/semantic_query.py](pages/semantic_query.py)** - Semantic Query page (NL→DAX→Results workflow)

### UI Components
- **[components/results_display.py](components/results_display.py)** - Results formatting, CSV/JSON export

### Configuration
- **[.env.example](.env.example)** - Environment variables template
- **[.streamlit/config.toml](.streamlit/config.toml)** - Streamlit UI theme & settings
- **[.gitignore](.gitignore)** - Git ignore patterns

### Documentation & Runbook
- **[README.md](README.md)** - Full documentation & setup guide
- **[docs/NL_to_Governed_Insights_End_to_End_Runbook.docx](docs/NL_to_Governed_Insights_End_to_End_Runbook.docx)** - Original runbook (Word format)
- **[docs/RUNBOOK_CODE_MAPPING.md](docs/RUNBOOK_CODE_MAPPING.md)** - Maps runbook sections to code implementations
- **[docs/runbook_extracted.md](docs/runbook_extracted.md)** - Plain text extraction of runbook

### Examples & Scripts
- **[sql/sample_warehouse_setup.sql](sql/sample_warehouse_setup.sql)** - Fabric Warehouse DDL & sample data loading
- **[dax/sample_queries.dax](dax/sample_queries.dax)** - Example DAX queries for common use cases
- **[scripts/setup_foundry.sh](scripts/setup_foundry.sh)** - Foundry Local setup automation
- **[scripts/setup_auth_azure.ps1](scripts/setup_auth_azure.ps1)** - Azure CLI authentication setup

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Foundry Local installed and running at `http://127.0.0.1:51970/v1`
- Azure CLI installed (`az` command available)
- Access to Microsoft Fabric and Power BI

### Installation (5 minutes)

1. **Create Python virtual environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   # OR
   source .venv/bin/activate     # Linux/Mac
   ```

2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your settings:
   # FOUNDRY_BASE=http://127.0.0.1:51970/v1
   # AZURE_TENANT_ID=your_tenant_id
   ```

4. **Start Foundry Local**
   ```bash
   foundry service start
   foundry model run qwen2.5-14b-instruct
   ```

5. **Launch the app**
   ```bash
   streamlit run app.py
   ```

   The app opens at `http://localhost:8501`

---

## 📖 How to Use

### Page 1: Chat (💬)
- Ask any question to the Foundry Local LLM
- **Auto mode**: System intelligently routes to Phi (fast) or Qwen (powerful)
- **Manual mode**: Select specific model
- **Demo mode**: Test without Foundry running

### Page 2: Settings (⚙️)
- **Authenticate**: Connect to Azure (Azure CLI or App Registration)
- **Select Workspace**: Choose your Fabric workspace
- **Select Dataset**: Pick your semantic model (Power BI dataset)
- **Validate**: Test connection and permissions

### Page 3: Semantic Query (📊)
- **Ask**: Type a natural language question
- **Review**: See the generated DAX query
- **Execute**: Run the query against your semantic model
- **Export**: Download results as CSV or JSON

---

## 🔗 Understanding the Architecture

### End-to-End Flow
```
User Question (Natural Language)
    ↓
Foundry Local LLM (generates DAX)
    ↓
DAX Validation
    ↓
Power BI ExecuteQueries API
    ↓
Results DataFrame
    ↓
Interactive Display + Export
```

### Key Components
- **Foundry Local**: LLM endpoint providing model inference
- **Microsoft Fabric**: Cloud data warehouse with semantic models
- **Power BI**: Semantic models + governed KPIs + ExecuteQueries API
- **Streamlit**: Web UI for user interaction

### Code Organization
```
├── app.py                      Main router & chat
├── config.py                   Configuration
├── modules/                    Business logic
│   ├── token_manager.py       Auth
│   ├── workspace_manager.py   Workspace API
│   ├── fabric_dax_generator.py LLM for DAX
│   └── power_bi_executor.py   Query execution
├── pages/                      UI pages
│   ├── workspace_config.py    Settings
│   └── semantic_query.py      Semantic Query
├── components/                 UI components
│   └── results_display.py     Results formatting
└── docs/                       Runbook & mapping
    ├── RUNBOOK_CODE_MAPPING.md
    └── NL_to_Governed_Insights_End_to_End_Runbook.docx
```

---

## 📋 Runbook to Code Mapping

The **Runbook** describes the architecture and setup. **Code files** contain actual implementations.

| Runbook Section | Code Implementation |
|---|---|
| Overview & Architecture | [README.md](README.md), [app.py](app.py) |
| Fabric Data Setup | [sql/sample_warehouse_setup.sql](sql/sample_warehouse_setup.sql) |
| Authentication | [modules/token_manager.py](modules/token_manager.py) |
| Foundry Setup | [config.py](config.py), [scripts/setup_foundry.sh](scripts/setup_foundry.sh) |
| DAX Generation | [modules/fabric_dax_generator.py](modules/fabric_dax_generator.py), [dax/sample_queries.dax](dax/sample_queries.dax) |
| NL→DAX Workflow | [pages/semantic_query.py](pages/semantic_query.py) |
| Workspace Configuration | [pages/workspace_config.py](pages/workspace_config.py), [modules/workspace_manager.py](modules/workspace_manager.py) |
| Deployment | [requirements.txt](requirements.txt), [.env.example](.env.example) |

**Full Mapping**: See [docs/RUNBOOK_CODE_MAPPING.md](docs/RUNBOOK_CODE_MAPPING.md)

---

## 🛠️ Configuration

### Environment Variables (.env)
```bash
# Foundry Local Configuration
FOUNDRY_BASE=http://127.0.0.1:51970/v1
FOUNDRY_MODEL_PHI=phi-3-mini
FOUNDRY_MODEL_QWEN=qwen-32b
FOUNDRY_TIMEOUT=180

# Power BI / Fabric Configuration
POWER_BI_WORKSPACE_ID=your_workspace_id
POWER_BI_DATASET_ID=your_dataset_id
AZURE_TENANT_ID=your_tenant_id

# Optional: App Registration (production)
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
```

### Models
The app supports:
- **Phi-3**: Smaller, faster model for simple queries
- **Qwen**: Larger, more capable model for complex queries

Auto mode uses heuristics to choose; manual mode lets you select.

---

## 💡 Example Workflows

### Workflow 1: Quick Analysis
```
1. Settings → Authenticate → Select Workspace & Dataset
2. Semantic Query → Type: "What is total revenue?"
3. View results and download CSV
```

### Workflow 2: Complex Report
```
1. Semantic Query → Type: "Revenue and profit by product category"
2. Review auto-generated DAX
3. Edit DAX if needed
4. Execute → Export to CSV for report
```

### Workflow 3: Chat-Based Exploration
```
1. Chat → Type questions to Foundry Local
2. Auto-selects Phi for simple Q's, Qwen for complex
3. Explore patterns without hitting Power BI API
```

---

## 🔍 Troubleshooting

### "Foundry Local not responding"
```bash
# Check if Foundry is running
curl http://127.0.0.1:51970/v1/models

# Start Foundry
foundry service start
foundry model run phi-3-mini
```

### "Azure CLI not found"
```bash
# Install Azure CLI
# Windows: https://learn.microsoft.com/cli/azure/install-azure-cli-windows
# Linux/Mac: https://learn.microsoft.com/cli/azure/install-azure-cli

# Then authenticate
az login
```

### "Connection validation failed"
- Verify workspace ID and dataset ID are correct
- Check token hasn't expired (use Refresh Token button in Settings)
- Confirm user has permissions in Power BI/Fabric

### "DAX query execution failed"
- Review error message from Power BI API
- Check DAX syntax and table/column names
- Verify semantic model contains required measures

---

## 📚 Documentation

- **[README.md](README.md)** - Full setup & usage guide
- **[docs/RUNBOOK_CODE_MAPPING.md](docs/RUNBOOK_CODE_MAPPING.md)** - Runbook sections → code files
- **[docs/NL_to_Governed_Insights_End_to_End_Runbook.docx](docs/NL_to_Governed_Insights_End_to_End_Runbook.docx)** - Original runbook
- **[sql/sample_warehouse_setup.sql](sql/sample_warehouse_setup.sql)** - SQL examples
- **[dax/sample_queries.dax](dax/sample_queries.dax)** - DAX examples

---

## 🚢 Deployment

### Development
```bash
# Local development with demo mode
streamlit run app.py
```

### Production
```bash
# Ensure all requirements installed
pip install -r requirements.txt

# Configure .env with production credentials
# Run on a server or cloud instance
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 📝 License & Support

**Status**: Production Ready  
**Last Updated**: December 17, 2025  
**Version**: 1.0

For issues:
1. Check [README.md](README.md) troubleshooting
2. Review runbook: [docs/NL_to_Governed_Insights_End_to_End_Runbook.docx](docs/NL_to_Governed_Insights_End_to_End_Runbook.docx)
3. Check code mappings: [docs/RUNBOOK_CODE_MAPPING.md](docs/RUNBOOK_CODE_MAPPING.md)

---

**Built with**: Streamlit, Foundry Local, Microsoft Fabric, Power BI  
**Language**: Python 3.9+
