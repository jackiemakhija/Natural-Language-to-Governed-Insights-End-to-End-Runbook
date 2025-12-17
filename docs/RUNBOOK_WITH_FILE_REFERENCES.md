# NL to Governed Insights - End-to-End Runbook
## With Integrated Code File References

**Complete guide with all code replaced by file path references**

---

## Overview

This runbook builds a **Natural Language to Insights** experience where an LLM generates governed DAX and executes it against a Power BI Semantic Model.

**Architecture Flow:**
```
Natural Language Question
    ↓
Foundry Local LLM (generates DAX)
    ↓
Power BI Semantic Model (governed KPIs + RLS)
    ↓
ExecuteQueries API
    ↓
Results Display
```

---

## Prerequisites

- Microsoft Fabric access (permission to create Workspace, Warehouse, and Semantic Model)
- Azure CLI installed: https://learn.microsoft.com/cli/azure/install-azure-cli
- Python 3.10+ on your local machine
- Foundry Local installed and running at `http://127.0.0.1:51970/v1`

---

## Section 4: Build the Data Foundation in Fabric

### Step 4.1 - Create Workspace

**Where:** Microsoft Fabric Portal  
**Action:** Workspaces → New workspace → Name: `WS-Sales-DEV`

### Step 4.2 - Create Fabric Warehouse

**Where:** WS-Sales-DEV  
**Action:** New → Warehouse → Name: `WH_Sales_Gold`

### Step 4.3 - Open SQL Editor

**Where:** WH_Sales_Gold → New SQL Query  
**Action:** Run all SQL in the Warehouse SQL editor

### Step 4.4 - Create Tables (SQL)

**📁 File Reference:** [`github_release/sql/sample_warehouse_setup.sql`](../sql/sample_warehouse_setup.sql)

**Instructions:**
1. Open the SQL file linked above
2. Copy the **CREATE TABLE** statements (Lines 1-32)
3. Paste into Fabric Warehouse SQL editor
4. Execute

**What gets created:**
- `dbo.DimDate` - Dimension table with dates
- `dbo.FactSales` - Fact table with sales data

### Step 4.5 - Load Sample Data (SQL)

**📁 File Reference:** [`github_release/sql/sample_warehouse_setup.sql`](../sql/sample_warehouse_setup.sql)

**Instructions:**
1. Open the SQL file linked above
2. Copy the **data loading section** (Lines 35-75)
3. Paste into Fabric Warehouse SQL editor
4. Execute

**What happens:**
- Populates `dbo.DimDate` with last 90 days
- Loads 300 random `dbo.FactSales` records

### Step 4.6 - Validate Data

**📁 File Reference:** [`github_release/sql/sample_warehouse_setup.sql`](../sql/sample_warehouse_setup.sql)

Run the validation queries to confirm data loaded successfully.

---

## Section 5: Build the Semantic Model (Governed KPIs)

### Step 5.1 - Create Semantic Model

**Where:** Microsoft Fabric Portal → WS-Sales-DEV  
**Action:**
1. New → Semantic model
2. Select tables: `dbo.DimDate`, `dbo.FactSales`
3. Create/Save

### Step 5.2 - Create Relationship

**Where:** Semantic Model → Model view  
**Action:**
1. Create relationship: `FactSales[DateKey]` → `DimDate[DateKey]`
2. Relationship type: Many-to-One

### Step 5.3 - Create DAX Measures (KPIs)

**📁 File Reference:** [`github_release/dax/sample_queries.dax`](../dax/sample_queries.dax)

**Instructions:**
1. Open the DAX file linked above
2. In Semantic Model, create these measures:

```
Total Revenue = SUM(FactSales[Revenue])
Total Cost = SUM(FactSales[Cost])
Profit = [Total Revenue] - [Total Cost]
Profit Margin % = DIVIDE([Profit], [Total Revenue])
Average Revenue = AVERAGE(FactSales[Revenue])
Total Quantity = SUM(FactSales[Quantity])
```

**✅ Note:** These are the **governed KPIs** that Foundry LLM will reference when generating DAX.

---

## Section 6: Start Foundry Local

### Step 6.1 - Start Service

**📁 File Reference:** [`github_release/scripts/setup_foundry.sh`](../scripts/setup_foundry.sh)

**Instructions:**
1. Open your terminal
2. Run Foundry startup commands (see script)
3. Verify endpoint responds:

```bash
curl http://127.0.0.1:51970/v1/models
```

Expected output: List of available models (Qwen, Phi, etc.)

---

## Section 7: Streamlit App (NL → DAX → ExecuteQueries)

### Step 7.1 - Create Project + Install Dependencies

**📁 File Reference:** [`github_release/requirements.txt`](../requirements.txt)

**Windows (PowerShell):**
```powershell
# Clone or navigate to github_release folder
cd github_release

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
cd github_release
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 7.2 - Capture Workspace and Dataset IDs

**Where:** Microsoft Fabric/Power BI portal  
**How to find:**

1. **Workspace (Group) ID:**
   - Open your workspace URL in browser
   - Copy ID from URL: `/groups/`**`<GROUP_ID>`**`/`

2. **Dataset (Semantic Model) ID:**
   - Open your semantic model in Power BI
   - Copy ID from URL: `/datasets/`**`<DATASET_ID>`**

**Example:**
```
Workspace URL: https://app.powerbi.com/groups/12345678-1234-1234-1234-123456789012/
Group ID:      12345678-1234-1234-1234-123456789012

Dataset URL: https://app.powerbi.com/groups/.../datasets/87654321-4321-4321-4321-210987654321
Dataset ID:  87654321-4321-4321-4321-210987654321
```

### Step 7.3 - Get a Power BI Access Token (Azure CLI)

**📁 File Reference:** [`github_release/scripts/setup_auth_azure.ps1`](../scripts/setup_auth_azure.ps1)

**Instructions:**

1. **Windows (PowerShell):**
```powershell
# Login to Azure
az login

# Get token for Power BI
az account get-access-token --resource https://analysis.windows.net/powerbi/api --query accessToken -o tsv
```

2. **Linux/Mac:**
```bash
# Login to Azure
az login

# Get token
az account get-access-token --resource https://analysis.windows.net/powerbi/api --query accessToken -o tsv
```

3. **Copy the token** (long string) - you'll paste it into the Streamlit app

### Step 7.4 - Run the Streamlit App

**📁 File Reference:** [`github_release/app.py`](../app.py)

This is the complete production-ready Streamlit application with:
- Multi-page interface (Chat, Settings, Semantic Query)
- Automatic model routing
- Demo mode for offline testing
- Workspace/dataset configuration
- Natural language to DAX pipeline

**No modifications needed** - just run it!

### Step 7.5 - Run the App

```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Open browser:** http://localhost:8501

---

## Section 8: Test the Application

### Page 1: Chat (💬)
- Ask questions to Foundry Local LLM
- Auto model routing (Phi for simple, Qwen for complex)
- Manual model selection available

### Page 2: Settings (⚙️)
1. **Authenticate:** Choose Azure CLI or App Registration
2. **Select Workspace:** Pick your Fabric workspace
3. **Select Dataset:** Choose your semantic model
4. **Validate:** Test connection

### Page 3: Semantic Query (📊)
1. **Ask:** Enter natural language question
   - "What is total revenue?"
   - "Show revenue by month"
   - "Revenue YTD by product category"

2. **Review:** System generates DAX query
3. **Execute:** Run against your semantic model
4. **Export:** Download results as CSV or JSON

---

## Test Prompts

Try these questions in the Semantic Query page:

- What is total revenue?
- What is revenue last month?
- Show revenue YTD by month
- What is profit margin percentage?
- Revenue by product category

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Foundry Local not reachable** | Confirm service is running: `curl http://127.0.0.1:51970/v1/models` |
| **ExecuteQueries 401/403 error** | Ensure access token is valid and has Power BI permissions |
| **Empty results** | Try simpler question or confirm semantic model contains data |
| **Slow responses** | Use smaller model or reduce prompt verbosity |
| **"Azure CLI not found"** | Install Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli |

---

## Production Hardening Checklist

- [ ] Use service principal / managed identity instead of CLI token
- [ ] Add query guardrails (row limits, timeouts, allowed measures)
- [ ] Log prompts, DAX, and execution metadata for audit
- [ ] Cache common questions and DAX templates
- [ ] Version and certify semantic models
- [ ] Centralize KPI definitions and controls

---

## File Organization Reference

```
github_release/
├── app.py                          Main application (Step 7.4)
├── config.py                       Configuration settings
├── requirements.txt                Dependencies (Step 7.1)
├── .env.example                    Environment template
├── README.md                       Full documentation
│
├── modules/
│   ├── token_manager.py           Azure authentication
│   ├── workspace_manager.py       Workspace discovery
│   ├── fabric_dax_generator.py    DAX generation
│   └── power_bi_executor.py       Query execution
│
├── pages/
│   ├── workspace_config.py        Settings page
│   └── semantic_query.py          Semantic Query page
│
├── components/
│   └── results_display.py         Results formatting
│
├── docs/
│   ├── RUNBOOK_CODE_MAPPING.md    Detailed mappings
│   ├── CODE_LOCATION_SUMMARY.txt  Quick lookup
│   ├── CODE_REFERENCE_GUIDE.md    Code patterns → files
│   └── runbook_extracted.md       Plain text runbook
│
├── scripts/
│   ├── setup_foundry.sh           Foundry setup (Step 6.1)
│   └── setup_auth_azure.ps1       Azure auth (Step 7.3)
│
├── sql/
│   └── sample_warehouse_setup.sql SQL examples (Steps 4.4-4.6)
│
└── dax/
    └── sample_queries.dax         DAX examples (Step 5.3)
```

---

## Quick Command Reference

### Setup
```bash
cd github_release
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### Authentication
```bash
az login
az account get-access-token --resource https://analysis.windows.net/powerbi/api --query accessToken -o tsv
```

### Foundry
```bash
foundry service start
foundry model run qwen2.5-14b-instruct
curl http://127.0.0.1:51970/v1/models
```

### Run App
```bash
streamlit run app.py
```

---

## File References Summary

| Step | Description | File |
|------|-------------|------|
| 4.4 | Create Tables | [sql/sample_warehouse_setup.sql](../sql/sample_warehouse_setup.sql) |
| 4.5 | Load Data | [sql/sample_warehouse_setup.sql](../sql/sample_warehouse_setup.sql) |
| 5.3 | DAX Measures | [dax/sample_queries.dax](../dax/sample_queries.dax) |
| 6.1 | Foundry Setup | [scripts/setup_foundry.sh](../scripts/setup_foundry.sh) |
| 7.1 | Dependencies | [requirements.txt](../requirements.txt) |
| 7.3 | Azure Auth | [scripts/setup_auth_azure.ps1](../scripts/setup_auth_azure.ps1) |
| 7.4 | Main App | [app.py](../app.py) |

---

**Status:** Production Ready  
**Last Updated:** December 17, 2025  
**Version:** 1.0
