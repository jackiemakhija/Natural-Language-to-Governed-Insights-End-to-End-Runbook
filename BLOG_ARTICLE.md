# Natural Language to Governed Insights: End-to-End Runbook
## Microsoft Fabric + Semantic Model + Foundry Local
### From Questions to Trusted Decisions

---

## The Challenge: Democratizing Data Without Losing Control

Every business leader wants the same outcome: the ability to ask a simple question in plain English and receive an immediate, accurate answer.

> "What was our profit margin last quarter?"

This is the promise of AI-powered analytics. Yet for most enterprises, it remains unfulfilled.

The issue is not access to data, nor the absence of AI. The real challenge is **trust at scale**. Business users depend on technical specialists because answers live behind SQL and DAX logic. When teams answer the same question differently due to inconsistent KPI definitions, confidence erodes and decision-making slows.

This runbook presents a practical, end-to-end blueprint for delivering **Natural Language to Insights** using governed semantic models in Microsoft Fabric. By anchoring AI interactions to certified KPIs, Row-Level Security (RLS), and enterprise policies, organizations can safely scale conversational analytics from experimentation to executive decision-making.

---

## 1. What You'll Build

This solution connects three key components to enable natural language queries over governed data:

**High-level execution path:** Natural language question → Foundry Local LLM (generates DAX) → Power BI Semantic Model (certified KPIs + RLS) → ExecuteQueries API → Results (with optional narrative).

**Why it stays governed:** The semantic model enforces certified KPIs and RLS; ExecuteQueries runs inside Power BI so security/audit apply; Foundry runs locally so no data leaves your network. Expect ~3–5s NL→DAX generation and sub-second ExecuteQueries for common KPIs.

**The complete solution includes:**
- ✅ A Fabric Warehouse with a star schema (DimDate + FactSales)
- ✅ A Power BI Semantic Model with certified DAX measures (governed KPIs)
- ✅ A local LLM runtime (Foundry Local) that generates ExecuteQueries-compatible DAX
- ✅ A Streamlit UI for interactive natural language queries
- ✅ Enterprise auth (Azure CLI or App Registration)
- ✅ Results export (CSV, JSON)

---

## 2. Code Repository & Artifacts

**Complete source code and documentation:**
https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook

**Key files in the repository:**

| File | Purpose | Link |
|------|---------|------|
| `app.py` | Main Streamlit entry point and router | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/app.py) |
| `requirements.txt` | Python dependencies | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/requirements.txt) |
| `.env.example` | Environment configuration template | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/.env.example) |
| `config.py` | Central configuration management | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/config.py) |

**Core Modules:**

| Module | Purpose | Link |
|--------|---------|------|
| `modules/token_manager.py` | Azure token acquisition (CLI + App Registration) | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/token_manager.py) |
| `modules/workspace_manager.py` | Workspace and dataset discovery | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/workspace_manager.py) |
| `modules/fabric_dax_generator.py` | LLM-based DAX generation via Foundry | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/fabric_dax_generator.py) |
| `modules/power_bi_executor.py` | ExecuteQueries API client | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/power_bi_executor.py) |

**UI Pages:**

| Page | Purpose | Link |
|------|---------|------|
| `pages/workspace_config.py` | Settings and authentication | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/pages/workspace_config.py) |
| `pages/semantic_query.py` | Natural language query interface | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/pages/semantic_query.py) |

**Sample Data & Patterns:**

| File | Purpose | Link |
|------|---------|------|
| `sql/sample_warehouse_setup.sql` | DDL and ETL for Fabric Warehouse | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/sql/sample_warehouse_setup.sql) |
| `dax/sample_queries.dax` | Reference DAX patterns and measures | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/dax/sample_queries.dax) |

**Documentation:**

| Document | Purpose | Link |
|----------|---------|------|
| `docs/RUNBOOK_WITH_FILE_REFERENCES.md` | Step-by-step guide with code references | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/docs/RUNBOOK_WITH_FILE_REFERENCES.md) |
| `docs/CODE_REFERENCE_GUIDE.md` | Pattern-to-file mapping | [View](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/docs/CODE_REFERENCE_GUIDE.md) |

---

## 3. Prerequisites

Before you start, ensure you have:

- **Microsoft Fabric access** (permission to create Workspace, Warehouse, Semantic Model)
- **Azure CLI installed** and able to sign in: `az login`
- **Python 3.10+** on your local machine
- **Foundry Local installed** with LLM runtime at `http://127.0.0.1:51970/v1`
- **Git** (to clone the repository)

---

## 4. Architecture Overview

### Component 1: Data Layer (Fabric Warehouse)
The foundation starts with a Fabric Warehouse containing your dimensional data.

**Create a star schema:**
- **DimDate** — Time dimension (dates, quarters, fiscal periods)
- **FactSales** — Fact table (sales transactions, amounts, quantities)
- Additional dimensions as needed for your domain

**Reference script:** https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/sql/sample_warehouse_setup.sql

This SQL script includes:
- Complete DDL for DimDate and FactSales
- Sample data loads
- Primary key and foreign key relationships
- Data quality validations

### Component 2: Semantic Layer (Power BI Semantic Model)
Governed KPIs are defined once, certified, and reused everywhere.

**Create a semantic model that:**
- Connects to your Fabric Warehouse
- Defines certified measures (e.g., `[Total Revenue]`, `[Profit Margin]`, `[YoY Growth]`)
- Implements Row-Level Security (RLS) for multi-tenant scenarios
- Documents all measures with business context

**Reference DAX patterns:** https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/dax/sample_queries.dax

Examples include:
- Aggregation patterns (SUM, AVG, COUNT)
- Time intelligence (YoY, MTD, YTD)
- Complex filtering and contextual measures
- Parameterized KPIs

### Component 3: LLM Layer (Foundry Local)
A local, offline LLM generates DAX from natural language.

**Capabilities:**
- Runs locally without internet connectivity
- Generates DAX syntax compatible with ExecuteQueries API
- Leverages Phi-4-mini or similar compact models
- Achieves ~3-5 second inference latency

**Access pattern:**
```
POST http://127.0.0.1:51970/v1/completions
{
  "model": "phi-4-mini",
  "prompt": "Generate a DAX query for total revenue by month",
  "max_tokens": 500
}
```

Implementation: See [`modules/fabric_dax_generator.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/fabric_dax_generator.py)

### Component 4: Execution Layer (Power BI ExecuteQueries API)
Queries run securely through Power BI's native API.

**Why ExecuteQueries?**
- Enforces RLS at query time
- Runs against the semantic model (not the warehouse directly)
- Returns results in milliseconds
- Integrates with Power BI audit logs and monitoring

**Implementation:** See [`modules/power_bi_executor.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/power_bi_executor.py)

### Component 5: UI Layer (Streamlit)
Multi-page application for configuration and queries.

**Pages:**
- **Settings** (`pages/workspace_config.py`) — Auth, workspace selection, validation
- **Semantic Query** (`pages/semantic_query.py`) — NL input, DAX generation, execution, export

---

## 5. Getting Started: Follow These Sections

### 🏗️ Section 1: Build Your Data Foundation

Create a Fabric Workspace and populate it with dimensional data that will power your semantic model.

**What you'll do:**
1. Create a Fabric Workspace in your Power BI tenant
2. Set up a new Warehouse to house your dimensional data
3. Load sample or production data using SQL DDL and ETL

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
1. Open Power BI Desktop
2. Connect to your Fabric Warehouse (created in Section 1)
3. Create DAX measures for key metrics (e.g., `[Total Revenue]`, `[Profit Margin]`, `[YoY Growth]`)
4. Publish the dataset/semantic model to your Fabric workspace

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
1. Start the Foundry service (if not already running)
2. Load the language model
3. Verify the service is accessible on localhost:51970

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

**Reference:** [.env.example](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/.env.example)

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

**Implementation:** See [`pages/workspace_config.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/pages/workspace_config.py)

**Step 5b: Generate and Execute Your First Query**
- Click the **Semantic Query** page in the sidebar
- Enter a natural language question: `What is total revenue?`
- Click **"Generate DAX"** — review the generated DAX query
- Click **"Execute Query"** — results should appear below
- Verify results match your expected KPI

**Implementation:** See [`pages/semantic_query.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/pages/semantic_query.py)

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

---

## 6. Key Features & Capabilities

### Natural Language to DAX (Offline)
Queries are translated to DAX using a local LLM, eliminating dependencies on cloud-based AI services and ensuring data stays within your control.

**How it works:**
1. User enters natural language question in Streamlit UI
2. Foundry Local LLM generates DAX syntax
3. DAX is validated and displayed for review
4. User approves and executes (or edits before executing)

**Code path:** [`modules/fabric_dax_generator.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/fabric_dax_generator.py)

### Governed KPI Enforcement
Only certified measures from your semantic model can be queried, ensuring consistency across the organization.

**How it works:**
1. All measures are defined and certified in Power BI
2. Semantic model acts as the contract for KPIs
3. RLS policies enforce row-level security
4. All queries execute within these guardrails

**Benefits:**
- Single source of truth for metrics
- Audit trail via Power BI's native logging
- Role-based access control
- No direct warehouse access

### Multi-Auth Support
Supports both development (Azure CLI) and production (App Registration) authentication flows.

**Azure CLI (Development):**
```powershell
az login
```
Uses your signed-in Azure identity.

**App Registration (Production):**
Configure with client ID, secret, and tenant ID for service-to-service authentication.

**Code path:** [`modules/token_manager.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/token_manager.py)

### Workspace & Dataset Discovery
Automatically discover available workspaces and semantic models instead of hardcoding IDs.

**Code path:** [`modules/workspace_manager.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/workspace_manager.py)

### Export & Integration
Results can be exported as CSV or JSON for downstream tools and dashboards.

**Code path:** [`pages/semantic_query.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/pages/semantic_query.py)

---

## 7. Use Cases

### Business Analysts
Query data without writing DAX or SQL. Ask questions in plain English and get instant answers with full transparency into the generated query.

### Finance Teams
Self-service reporting on P&L KPIs, budget variance, and financial forecasts — all within governance constraints.

### Sales Teams
Ad-hoc queries on pipeline, revenue, and forecasts without waiting for reports or IT involvement.

### C-Suite Executives
Secure, governed analytics access with drill-down capability and explanation of how metrics are calculated.

### Data Governance Teams
Enforce KPI definitions, audit query history, and maintain compliance — all through the semantic model layer.

---

## 8. Best Practices

### Define Clear, Measurable KPIs
Before implementing, document your top 10–15 KPIs:
- Business definition
- DAX formula
- Refresh frequency
- Owner and steward
- Governance rules

### Optimize Your Semantic Model
- Certify measures in Power BI
- Implement RLS for multi-tenant scenarios
- Use calculated tables for slowly changing dimensions
- Monitor query performance and adjust indexing

### Secure Your Credentials
- Use Azure Key Vault for storing secrets in production
- Rotate secrets regularly
- Audit token usage via Azure logs
- Never commit `.env` files to git (use `.env.example` template)

### Performance Optimization
- Cache frequently used measures
- Pre-aggregate high-volume fact tables
- Index dimension keys
- Test DAX queries for performance before deployment

**Reference:** [config.py](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/config.py)

---

## 9. Troubleshooting & FAQ

**Q: Why is my query slow?**
A: Check your semantic model's measure definitions and warehouse table statistics. Index large dimension tables. See [`sql/sample_warehouse_setup.sql`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/sql/sample_warehouse_setup.sql) for optimization patterns.

**Q: Authentication failed — what should I do?**
A: Ensure `az login` has been run for Azure CLI mode, or verify your app registration credentials. Check [`modules/token_manager.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/token_manager.py) for auth flow details.

**Q: No results returned — why?**
A: Verify the dataset ID and workspace ID in `.env`. Check that your Workspace and Semantic Model are accessible. See [`pages/workspace_config.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/pages/workspace_config.py) for validation steps.

**Q: Foundry Local is not responding — how do I fix it?**
A: Run `foundry service start` and `foundry model run phi-4-mini`. Verify with: `Invoke-WebRequest http://127.0.0.1:51970/v1/models -UseBasicParsing`. Expected response: HTTP 200 with model list.

**Q: Generated DAX is syntactically invalid — what now?**
A: Review the generated query in the UI before executing. Compare against reference patterns in [`dax/sample_queries.dax`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/dax/sample_queries.dax). Consider refining your question or the LLM prompt in [`modules/fabric_dax_generator.py`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/modules/fabric_dax_generator.py).

---

## 10. Next Steps & Support

### Immediate Actions
1. Clone the repository: https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook
2. Follow Sections 1–5 in order
3. Run test queries from Section 5c
4. Export and validate results

### Documentation
- **Full implementation guide:** [`docs/RUNBOOK_WITH_FILE_REFERENCES.md`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/docs/RUNBOOK_WITH_FILE_REFERENCES.md)
- **Code patterns:** [`docs/CODE_REFERENCE_GUIDE.md`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/docs/CODE_REFERENCE_GUIDE.md)
- **Sample data & DAX:** [`dax/sample_queries.dax`](https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/blob/main/dax/sample_queries.dax)

### Support & Contributions
- **GitHub repository:** https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook
- **Issues & questions:** Open an issue on the repository
- **Contributions welcome:** Fork, improve, and submit pull requests

---

## Conclusion

By combining Microsoft Fabric, Power BI semantic models, Foundry Local LLMs, and Streamlit, you've built a **democratized yet governed** analytics platform. Business users can ask questions in plain English, AI generates the queries, and the semantic model enforces trust and consistency.

This is not just AI-powered analytics—it's **enterprise-grade, trustworthy analytics at scale**.

**Ready to start?** Clone the repository and follow Sections 1–5:
https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook

---

**Last Updated:** December 17, 2025
**Repository:** https://github.com/jackiemakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook
