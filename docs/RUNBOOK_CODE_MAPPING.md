# Runbook to Code Mapping Guide

This document maps sections of the **NL_to_Governed_Insights_End_to_End_Runbook.docx** to the corresponding code implementations in this `github_release` folder.

## Overview

The runbook provides a **practical, end-to-end blueprint** for building a Natural Language to Insights experience using Microsoft Fabric and Foundry Local. This guide shows you where to find the **actual implementation code** for each runbook section.

---

## Section-by-Section Mapping

### 1. Overview & Architecture

**Runbook**: Section 1-3  
**Code Implementation**: [app.py](../app.py)

The runbook describes the high-level execution path:
- Natural Language question → LLM (generates DAX) → Power BI → Results

**See**:
- [app.py](../app.py#L1) - Main Streamlit router and chat interface
- [config.py](../config.py) - Foundry Local endpoint configuration
- [README.md](../README.md) - Full architecture documentation

---

### 2. Build the Data Foundation (Fabric Warehouse & SQL)

**Runbook**: Section 4  
**Related Code**:
- [modules/workspace_manager.py](../modules/workspace_manager.py) - Connects to Fabric workspaces
- [modules/power_bi_executor.py](../modules/power_bi_executor.py) - Executes queries against the warehouse

**Manual Steps** (from runbook):
- Create Fabric Workspace: `WS-Sales-DEV`
- Create Warehouse: `WH_Sales_Gold`
- Run provided SQL to create `DimDate` and `FactSales` tables
- Load sample data (SQL scripts in runbook)

**See**:
- [sql/sample_warehouse_setup.sql](../sql/sample_warehouse_setup.sql) - SQL scripts extracted from runbook

---

### 3. Azure Authentication & Token Acquisition

**Runbook**: Section 5  
**Code Implementation**: [modules/token_manager.py](../modules/token_manager.py)

The runbook explains how to authenticate to Power BI using Azure CLI or App Registration.

**Implementation Details**:
- `acquire_token_azure_cli()` - Uses `az account get-access-token`
- `acquire_token_app_registration()` - OAuth 2.0 Client Credentials flow
- Token refresh and caching logic

**See**:
- [modules/token_manager.py](../modules/token_manager.py) - Full implementation
- [scripts/setup_auth_azure.ps1](../scripts/setup_auth_azure.ps1) - PowerShell setup script
- [pages/workspace_config.py](../pages/workspace_config.py#L1) - UI for authentication selection

**Quick Start**:
```bash
# Azure CLI method (development)
az login
streamlit run app.py

# App Registration method (production)
# Set environment variables: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
streamlit run app.py
```

---

### 4. Set Up Foundry Local

**Runbook**: Section 6  
**Code Implementation**: [config.py](../config.py) + [scripts/setup_foundry.sh](../scripts/setup_foundry.sh)

Foundry Local provides the LLM endpoint for DAX generation.

**Configuration**:
```bash
# Default endpoint (configured in .env)
FOUNDRY_BASE=http://127.0.0.1:51970/v1
```

**Setup Steps**:
```bash
# Install Foundry (if not already installed)
foundry service start

# Run a model
foundry model run qwen2.5-14b-instruct

# Verify endpoint responds
curl http://127.0.0.1:51970/v1/models
```

**See**:
- [config.py](../config.py) - Foundry configuration constants
- [scripts/setup_foundry.sh](../scripts/setup_foundry.sh) - Setup automation script
- [modules/fabric_dax_generator.py](../modules/fabric_dax_generator.py) - DAX generation using Foundry

---

### 5. Create Power BI Semantic Model (DAX Measures)

**Runbook**: Section 7  
**Code Implementation**: [modules/fabric_dax_generator.py](../modules/fabric_dax_generator.py)

The runbook covers DAX fundamentals and creating certified measures in a semantic model.

**Key Concepts**:
- Dimension tables: `DimDate`
- Fact tables: `FactSales`
- Measures: `Total Revenue`, `Total Cost`, `Profit Margin` (as certified KPIs)
- Row-Level Security (RLS) policies

**Implementation**:
- The app **generates DAX dynamically** from natural language queries
- DAX generator uses Foundry Local LLM
- Generated DAX is validated before execution

**See**:
- [modules/fabric_dax_generator.py](../modules/fabric_dax_generator.py) - DAX generation and validation
- [dax/sample_queries.dax](../dax/sample_queries.dax) - Example DAX queries
- [pages/semantic_query.py](../pages/semantic_query.py) - Semantic query UI page

**Example Queries**:
```
"What was our total revenue last month?"
"Show revenue and profit by product category"
"Revenue YTD vs last year"
```

---

### 6. Natural Language to DAX Workflow

**Runbook**: Section 8  
**Code Implementation**: [pages/semantic_query.py](../pages/semantic_query.py) + [modules/fabric_dax_generator.py](../modules/fabric_dax_generator.py)

This is the **core NL→DAX→Results** pipeline.

**Workflow Steps**:
1. User asks a question in natural language
2. Foundry Local LLM generates DAX
3. DAX is validated
4. Power BI ExecuteQueries API executes the DAX
5. Results are displayed in interactive table

**Implementation Flow**:
```
User Input (NL Question)
    ↓
[fabric_dax_generator.py] → generate_dax()
    ↓
[fabric_dax_generator.py] → validate_dax()
    ↓
User can edit/refine the DAX
    ↓
[power_bi_executor.py] → execute_query()
    ↓
[power_bi_executor.py] → parse_results_to_dataframe()
    ↓
[components/results_display.py] → display_results_dataframe()
```

**See**:
- [pages/semantic_query.py](../pages/semantic_query.py) - Full UI page with workflow
- [modules/fabric_dax_generator.py](../modules/fabric_dax_generator.py) - DAX generation
- [modules/power_bi_executor.py](../modules/power_bi_executor.py) - Query execution
- [components/results_display.py](../components/results_display.py) - Results formatting

---

### 7. Workspace Configuration & Discovery

**Runbook**: Section 9  
**Code Implementation**: [pages/workspace_config.py](../pages/workspace_config.py) + [modules/workspace_manager.py](../modules/workspace_manager.py)

Users select their Fabric workspace and semantic model through the Settings page.

**Workflow**:
1. Authenticate to Azure AD
2. Fetch list of accessible workspaces
3. Select a workspace
4. Fetch datasets in that workspace
5. Select a semantic model (dataset)
6. Validate connection and permissions

**See**:
- [pages/workspace_config.py](../pages/workspace_config.py) - Settings page UI
- [modules/workspace_manager.py](../modules/workspace_manager.py) - Workspace/dataset API calls
- [modules/token_manager.py](../modules/token_manager.py) - Authentication

---

### 8. Chat Interface & Model Routing

**Runbook**: Section 10 (if present)  
**Code Implementation**: [app.py](../app.py)

The app includes an intelligent chat interface with **automatic model routing** between fast (Phi) and powerful (Qwen) models.

**Features**:
- Auto mode: Intelligently selects model based on query complexity
- Manual mode: User selects specific model
- Demo mode: For offline testing
- System prompt customization

**Routing Logic**:
- **Phi (Fast)**: Simple questions, <25 words
- **Qwen (Powerful)**: Complex questions, code, architecture, >25 words

**See**:
- [app.py](../app.py) - Chat page, model routing logic
- [config.py](../config.py) - Model configuration
- [.env.example](.env.example) - Environment setup

---

### 9. Deployment & Production Setup

**Runbook**: Deployment section (if present)  
**Code Implementation**: [requirements.txt](../requirements.txt) + [.env.example](.env.example) + [scripts/](../scripts/)

**Deployment Steps**:

1. **Clone repository**
   ```bash
   cd C:\MyCode\foundry-ui\github_release
   ```

2. **Install Python dependencies**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your:
   # - FOUNDRY_BASE URL
   # - AZURE_TENANT_ID
   # - Optional: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET for app registration
   ```

4. **Start Foundry Local**
   ```bash
   foundry service start
   foundry model run qwen2.5-14b-instruct
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

**See**:
- [requirements.txt](../requirements.txt) - Python dependencies
- [.env.example](.env.example) - Environment template
- [README.md](../README.md) - Full setup guide
- [scripts/setup_foundry.sh](../scripts/setup_foundry.sh) - Automation script

---

## File Organization in github_release

```
github_release/
├── app.py                          # Main Streamlit multi-page app
├── config.py                       # Configuration constants
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── README.md                       # Full documentation
│
├── modules/                        # Business logic
│   ├── token_manager.py           # Azure AD authentication
│   ├── workspace_manager.py       # Workspace/dataset discovery
│   ├── fabric_dax_generator.py    # LLM-based DAX generation
│   └── power_bi_executor.py       # DAX execution via Power BI API
│
├── pages/                          # Streamlit pages
│   ├── workspace_config.py        # Settings / configuration page
│   └── semantic_query.py          # Semantic query / NL→DAX page
│
├── components/                     # Reusable UI components
│   └── results_display.py         # Results formatting & export
│
├── .streamlit/                     # Streamlit config
│   └── config.toml                # UI theme & settings
│
├── docs/                           # Documentation
│   ├── NL_to_Governed_Insights_End_to_End_Runbook.docx  # Original runbook
│   ├── runbook_extracted.md       # Plain text extraction
│   ├── RUNBOOK_CODE_MAPPING.md    # This file
│   └── runbook_with_file_refs.md  # Runbook with file references
│
├── scripts/                        # Automation & setup scripts
│   ├── setup_foundry.sh           # Foundry installation/startup
│   ├── setup_auth_azure.ps1       # Azure CLI authentication
│   └── validate_workspace.ps1     # Workspace validation
│
├── dax/                            # DAX query examples
│   └── sample_queries.dax         # Example DAX queries from runbook
│
└── sql/                            # SQL examples
    └── sample_warehouse_setup.sql # Warehouse setup SQL from runbook
```

---

## Quick Reference: Runbook → Code Mapping

| Runbook Section | Main Code Files | Purpose |
|---|---|---|
| Architecture | app.py, config.py | Main application structure |
| Fabric Setup | sql/sample_warehouse_setup.sql | Database schema & data |
| Authentication | modules/token_manager.py | Azure AD tokens |
| Foundry Setup | config.py, scripts/setup_foundry.sh | LLM endpoint config |
| Semantic Model | modules/fabric_dax_generator.py, dax/ | DAX generation |
| NL→DAX Workflow | pages/semantic_query.py | Core user workflow |
| Workspace Config | pages/workspace_config.py, modules/workspace_manager.py | Workspace selection |
| Chat Interface | app.py | Multi-page UI |
| Deployment | requirements.txt, .env.example, README.md | Setup & run |

---

## Getting Started

1. **Read** [README.md](../README.md) for full setup instructions
2. **Review** the original runbook: [NL_to_Governed_Insights_End_to_End_Runbook.docx](../docs/NL_to_Governed_Insights_End_to_End_Runbook.docx)
3. **Follow** the deployment steps in [Section 9](#9-deployment--production-setup) above
4. **Explore** each code file mapped to understand implementation details

---

## Support

For issues or questions:
- Check [README.md](../README.md) Troubleshooting section
- Review [pages/semantic_query.py](../pages/semantic_query.py) for workflow details
- Inspect [modules/](../modules/) for business logic implementations

---

**Last Updated**: December 17, 2025  
**Version**: 1.0  
**Status**: Production Ready
