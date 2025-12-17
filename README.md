# Foundry Local + Fabric Semantic Model Integration

Turn natural language into governed Power BI insights — end-to-end.

## Code Repository

- Repo: https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook
- Sample SQL scripts: https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/tree/main/sql
  - Example: https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/sql/sample_warehouse_setup.sql
- Streamlit app (app.py): https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/app.py
- Dependencies (requirements.txt): https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/requirements.txt
- Configuration template (.env.example): https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/.env.example
- Operational runbook (Markdown): https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/docs/RUNBOOK_WITH_FILE_REFERENCES.md
- Plain-text runbook: https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/docs/runbook_extracted.md
- Note: A .pbit template is not included; use your existing semantic model or build one as described below.

## Getting Started: Follow These Sections

### 🏗️ Section 1: Build Your Data Foundation
Start by creating a Fabric Workspace and populating it with dimensional data that will power your semantic model.

**What you'll do:**
- Create a Fabric Workspace in your Power BI tenant
- Set up a new Warehouse to house your dimensional data
- Load sample or production data using SQL DDL and ETL

**Reference SQL script:**
https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/sql/sample_warehouse_setup.sql

This script includes:
- DimDate, FactSales table definitions
- Sample data loads
- Data quality validations

**After you complete this section:**
Copy and save your **Workspace ID** — you'll need it when configuring the Streamlit app.

---

### 📊 Section 2: Define Governed KPIs with DAX
Design your semantic model in Power BI by creating certified DAX measures that represent your organization's governed KPIs.

**What you'll do:**
- Open Power BI Desktop
- Connect to your Fabric Warehouse (created in Section 1)
- Create DAX measures for key metrics (e.g., [Total Revenue], [Profit Margin], [YoY Growth])
- Publish the dataset/semantic model to your Fabric workspace

**Reference DAX patterns:**
https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/dax/sample_queries.dax

This reference includes:
- Common aggregation patterns
- Year-over-year calculations
- Filtering and contextual KPIs

**After you complete this section:**
Copy and save your **Dataset ID** (also called Semantic Model ID) — you'll need it when configuring the app.

---

### 🤖 Section 3: Start the Local LLM Service (Foundry)
Set up the Foundry LLM service on your machine to enable natural language to DAX translation.

**What you'll do:**
- Start the Foundry service (if not already running)
- Load the language model
- Verify the service is accessible on localhost:51970

**Run these commands:**
```powershell
foundry service start
foundry model run phi-4-mini
```

**Verify it's working:**
```powershell
Invoke-WebRequest http://127.0.0.1:51970/v1/models -UseBasicParsing
```

**Expected response:**
HTTP 200 status with a list of available models (including phi-4-mini)

**Note:** This service runs locally and does not require internet connectivity for inference. It powers the natural language query generation in the Streamlit app.

---

### 🚀 Section 4: Deploy and Configure the Streamlit Application
Clone the repository, set up your Python environment, and configure credentials to connect to Fabric.

**Clone the repository:**
```bash
git clone https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook.git
cd Natural-Language-to-Governed-Insights-End-to-End-Runbook
```

**Create and activate virtual environment:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Configure environment variables:**
```bash
copy .env.example .env
```

Open `.env` and populate these values (from Sections 1 and 2):
```
POWER_BI_WORKSPACE_ID=<your workspace ID from Section 1>
POWER_BI_DATASET_ID=<your dataset ID from Section 2>
AZURE_TENANT_ID=<your Azure tenant ID>
FOUNDRY_BASE=http://127.0.0.1:51970/v1
```

**Launch the app:**
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

### ✅ Section 5: Test and Validate the End-to-End Flow
Verify that authentication, query generation, and execution all work as expected.

**Step 5a: Authenticate and Select Your Data**
- Navigate to the **Settings** page in the sidebar
- Choose an authentication method:
  - **Azure CLI** (for development): Run `az login` first, then select "Azure CLI"
  - **App Registration** (for production): Provide app credentials
- Select your Workspace (created in Section 1)
- Select your Semantic Model/Dataset (created in Section 2)
- Click **"Validate Connection"** — you should see a success message

**Step 5b: Generate and Execute Your First Query**
- Click the **Semantic Query** page in the sidebar
- Enter a natural language question: `What is total revenue?`
- Click **"Generate DAX"** — review the generated DAX query
- Click **"Execute Query"** — results should appear below
- Verify results match your expected KPI

**Step 5c: Test Additional Scenarios**
Try these sample queries to exercise different capabilities:
- `Revenue by month for this year`
- `Top 5 products by quantity sold`
- `What is the profit margin trend?`

Compare the generated DAX against the reference patterns:
https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/dax/sample_queries.dax

Export results as CSV or JSON to validate data integrity.

**Expected outcomes (all should pass):**
- ✅ Settings page successfully authenticates and displays your workspace and dataset
- ✅ Semantic Query page generates syntactically valid DAX queries
- ✅ Queries execute without errors and return expected results
- ✅ Results can be exported in multiple formats (CSV, JSON)
- ✅ Generated DAX queries align with your governance guidelines

A comprehensive Streamlit application that combines **Foundry Local** (local LLM inference) with **Microsoft Fabric Semantic Models** for intelligent natural language to DAX query generation and execution.

## Features

✨ **Three Integrated Pages:**
1. **💬 Chat** - Intelligent Foundry Local chat with auto model routing (Phi/Qwen)
2. **⚙️ Settings** - Configure and validate Power BI/Fabric workspace connection
3. **📊 Semantic Query** - Ask natural language questions, generate DAX, execute on semantic models

🤖 **Smart Model Routing:**
- Automatically routes queries between Phi (fast) and Qwen (powerful)
- Manual model selection option
- Customizable system prompts

🔌 **Fabric Integration:**
- Azure AD authentication (Azure CLI or App Registration)
- Workspace and dataset discovery
- Real-time DAX generation from natural language
- ExecuteQueries API integration
- Results export (CSV, JSON)

## Architecture

```
app.py (Multi-page Router)
├── Home Page (Foundry Local Chat)
├── Settings Page (Workspace Configuration)
│   ├── Token Management (token_manager.py)
│   └── Workspace Discovery (workspace_manager.py)
└── Semantic Query Page (DAX Generation & Execution)
    ├── DAX Generator (fabric_dax_generator.py)
    └── Query Executor (power_bi_executor.py)

Supporting Modules:
├── config.py (Centralized Configuration)
├── modules/ (Core Business Logic)
│   ├── token_manager.py (Azure AD Token Management)
│   ├── workspace_manager.py (Power BI Workspace Discovery)
│   ├── fabric_dax_generator.py (LLM-based DAX Generation)
│   └── power_bi_executor.py (ExecuteQueries API Client)
├── pages/ (Streamlit Pages)
│   ├── workspace_config.py (Settings Page)
│   └── semantic_query.py (Semantic Query Page)
└── components/ (Reusable UI Components)
    └── results_display.py (Results Formatting)
```

## Quick Start

1. Create venv and activate
```
python -m venv .venv
 .\.venv\Scripts\Activate.ps1
```
2. Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```
3. Configure environment
```
copy .env.example .env
# Edit .env with Azure + Fabric settings
```
4. Start Foundry Local and verify
```
foundry service start
# Verify models endpoint is reachable
curl http://127.0.0.1:51970/v1/models
```
5. Run the app
```
streamlit run app.py
```

## Setup

### Prerequisites

- Python 3.9+
- Foundry Local installed and running
- Azure account with Power BI/Fabric access
- At least one semantic model in Fabric

### Installation

1. **Clone/Setup the Project**
```bash
cd c:\MyCode\foundry-ui
```

2. **Create Python Environment**
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. **Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
# Copy and edit .env file
copy .env.example .env
# Edit .env with your Azure credentials and Fabric settings
```

5. **Start Foundry Local**
```bash
foundry service start
foundry model run qwen2.5-14b-instruct  # Or your preferred model
```

6. **Run the App**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Configuration (.env)

```bash
# Foundry Local Configuration
FOUNDRY_BASE=http://127.0.0.1:51970/v1
FOUNDRY_MODEL_PHI=phi-3-mini
FOUNDRY_MODEL_QWEN=qwen-32b

# Power BI / Fabric Configuration
POWER_BI_WORKSPACE_ID=your_workspace_id
POWER_BI_DATASET_ID=your_dataset_id
POWER_BI_BASE_URL=https://analysis.windows.net

# Azure AD / Tenant
AZURE_TENANT_ID=your_tenant_id

# User Preferences
USER_PREFERENCE_FORMAT=json
CACHE_TTL_MINUTES=5
LOG_LEVEL=INFO
```

## Usage Guide

### 1. **Chat Page** (💬)
- Default page with Foundry Local chat
- Auto mode: System intelligently routes to Phi or Qwen
- Manual mode: Select specific model
- Customize system prompt
- Chat history is maintained during session

**Auto Routing Logic:**
- **Phi (Fast):** Simple questions, short prompts
- **Qwen (Powerful):** Complex questions, debugging, architecture, code optimization, ≥25 words or ≥160 chars

### 2. **Settings Page** (⚙️)

**Step 1: Authenticate**
- **Option A (Dev):** Use Azure CLI (`az login` first)
- **Option B (Prod):** Use App Registration (Client ID + Secret)

**Step 2: Select Workspace**
- Lists all accessible Power BI/Fabric workspaces
- Automatically loads datasets for selected workspace

**Step 3: Select Semantic Model**
- Choose the semantic model (dataset) to query against
- Displays all tables available in the model

**Step 4: Validate Connection**
- Tests connectivity and permissions
- Confirms DAX execution capability

### 3. **Semantic Query Page** (📊)

**Workflow:**
1. Enter natural language question (e.g., "What is revenue by month?")
2. Click "Generate DAX" - LLM generates the DAX query
3. Review and optionally edit the DAX query
4. Click "Execute Query" to run against semantic model
5. Results displayed in interactive table
6. Export results as CSV or JSON

**Example Queries:**
- "What is total revenue?"
- "Show revenue by month for this year"
- "What is the profit margin percentage?"
- "Revenue YTD by sales region"
- "Top 10 products by quantity sold"

## Workflow Examples

### Example 1: Quick Analysis
```
1. Settings → Authenticate → Select Workspace & Dataset → Validate
2. Semantic Query → "Total revenue last month?" 
3. System generates: EVALUATE ROW("Total Revenue LM", [Revenue Last Month])
4. Results display automatically
```

## Examples

- Warehouse setup SQL: [sql/sample_warehouse_setup.sql](sql/sample_warehouse_setup.sql)
- Common DAX patterns: [dax/sample_queries.dax](dax/sample_queries.dax)
- Runbook (markdown extract): [docs/runbook_extracted.md](docs/runbook_extracted.md)
- Runbook with code references (DOCX): [docs/NL_to_Governed_Insights_End_to_End_Runbook_WITH_CODE_REFS.docx](docs/NL_to_Governed_Insights_End_to_End_Runbook_WITH_CODE_REFS.docx)

### Example 2: Complex Report
```
1. Semantic Query → "Show revenue and profit by product category"
2. Generated DAX: EVALUATE SUMMARIZE(ALL(Products), Products[Category], "Revenue", [Total Revenue], "Profit", [Profit])
3. Edit DAX if needed
4. Execute → Download CSV for report
```

## API Integration

### Foundry Local
- **Models Endpoint:** `GET /v1/models`
- **Chat Endpoint:** `POST /v1/chat/completions`
- **Timeout:** 180 seconds (configurable)

### Power BI / Fabric
- **Auth:** Azure AD Bearer Token
- **ExecuteQueries:** `POST /v1.0/myorg/groups/{groupId}/datasets/{datasetId}/executeQueries`
- **Models Endpoint:** `GET /v1.0/myorg/groups`
- **Datasets Endpoint:** `GET /v1.0/myorg/groups/{groupId}/datasets`

## Token Management

- **Azure CLI (Development):** Tokens acquired via `az account get-access-token`
- **App Registration (Production):** Uses Client Credentials OAuth 2.0 flow
- **Token Refresh:** Automatic if expiring (< 5 min remaining)
- **Caching:** 5-minute workspace/dataset metadata cache

## Error Handling

- **DAX Syntax Errors:** Displayed with details from Power BI API
- **Authentication Failures:** Clear guidance on credential issues
- **Network Timeouts:** 30-second fetch + 180-second query timeouts
- **Permission Errors:** User-friendly messages for access issues

## Performance Optimization

- Workspace/dataset metadata cached for 5 minutes
- Model list cached for 5 minutes
- Streamlit session state for credential management
- Async request handling (future enhancement)

## Security

- ✅ Credentials stored in `.env` (git-ignored)
- ✅ Tokens stored in session state only (no persistence)
- ✅ Azure AD authentication (enterprise-grade)
- ✅ Power BI API requires valid token
- ✅ No hardcoded secrets in code

## Troubleshooting

### "No models found"
```bash
# Start Foundry and run at least one model
foundry service start
foundry model run phi-3-mini
# Then refresh the app
```

### "Azure CLI not found"
```bash
# Install Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli
# Then authenticate
az login
```

### "Connection validation failed"
- Verify workspace/dataset IDs are correct
- Check token hasn't expired (use Refresh Token button)
- Confirm user has permissions in Power BI/Fabric

### "DAX query execution failed"
- Check query syntax (try editing and re-executing)
- Verify table/column names exist in semantic model
- Check Power BI/Fabric service status

## Advanced Configuration

### Custom DAX System Prompt
Edit `modules/fabric_dax_generator.py` → `DAX_SYSTEM_PROMPT` to customize LLM behavior

### Change Routing Logic
Modify `auto_route_model()` function in `app.py` for different model selection heuristics

### Token Refresh Strategy
In `modules/token_manager.py`, adjust `is_token_valid()` logic (currently 5 min buffer)

## Future Enhancements

- [ ] Direct Power BI URL paste (auto-extract workspace/dataset IDs)
- [ ] Query history and saved queries
- [ ] DAX validation before execution
- [ ] Results visualization (charts, tables)
- [ ] Multi-workspace query federation
- [ ] Role-based query templates
- [ ] Audit logging
- [ ] Scheduled query execution

## Support & Issues

For issues or feature requests, check:
1. `.env` configuration is correct
2. Foundry Local is running and accessible
3. Power BI/Fabric semantic model is accessible
4. Azure AD token is valid and not expired

## License

Internal Use - Conquer Systems

## Authors

- Built with Foundry Local + Microsoft Fabric
- Streamlit UI Framework
- Python 3.9+
