# Runbook - Extracted Text

This is the extracted plain text from the original runbook.

Natural Language to Governed Insights
End-to-End Runbook (Microsoft Fabric + Semantic Model + Foundry Local)
From Questions to Trusted Decisions
Every business leader wants the same outcome: the ability to ask a simple question in plain English and receive an immediate, accurate answer.
             
“What was our profit margin last quarter?”
This is the promise of AI-powered analytics. Yet for most enterprises, it remains unfulfilled.
The issue is not access to data, nor the absence of AI. The real challenge is trust at scale. Business users depend on technical specialists because answers live behind SQL and DAX logic. When teams answer the same question differently due to inconsistent KPI definitions, confidence erodes and decision-making slows.
This runbook presents a practical, end-to-end blueprint for delivering Natural Language to Insights using governed semantic models in Microsoft Fabric. By anchoring AI interactions to certified KPIs, Row-Level Security (RLS), and enterprise policies, organizations can safely scale conversational analytics from experimentation to executive decision-making.
1.
 
Overview
This runbook builds a Natural Language (NL) to Insights experience where an LLM generates governed DAX and executes it against a Power BI Semantic Model. The semantic model remains the contract for KPIs, relationships, and security.
What you will build
A Fabric Warehouse with a simple star schema (DimDate + FactSales).
A Power BI Semantic Model with certified DAX measures (governed KPIs).
A local LLM runtime (Foundry Local) that produces ExecuteQueries-compatible DAX.
A Streamlit UI that runs DAX via the Power BI ExecuteQueries API and displays results.
2. Prerequisites
Microsoft Fabric access (permission to create Workspace, Warehouse, and Semantic Model).
Azure CLI installed and able to sign in (for a quick Power BI access token).
Python 3.10+ (recommended) on your local machine.
Foundry Local installed and able to run an OpenAI-compatible endpoint at 
http://127.0.0.1:51970/v1
.
3. Architecture
High-level execution path:
Natural Language question
  -> Foundry Local LLM (generates DAX)
  -> Power BI Semantic Model (governed KPIs + RLS)
  -> ExecuteQueries API
  -> Results + narrative (optional)
4. Build the Data Foundation in Fabric
Step 4.1 - Create Workspace
Where: Microsoft Fabric Portal
Workspaces -> New workspace -> Name: WS-Sales-DEV
Step 4.2 - Create Fabric Warehouse
Where: WS-Sales-DEV
New -> Warehouse -> Name: WH_Sales_Gold
Step 4.3 - Open SQL Editor
Where: WH_Sales_Gold -> New SQL Query
Run all SQL in the Warehouse SQL editor.
Step 4.4 - Create Tables (SQL)
Create DimDate:
SQL
CREATE TABLE dbo.DimDate (
  DateKey       INT         NOT NULL,
  [Date]        DATE        NOT NULL,
  [Year]        INT         NOT NULL,
  [MonthNumber] INT         NOT NULL,
  [MonthName]   VARCHAR(20) NOT NULL
);
Create FactSales:
SQL
CREATE TABLE dbo.FactSales (
  SalesId  BIGINT        NOT NULL,
  DateKey  INT           NOT NULL,
  Revenue  DECIMAL(18,2) NOT NULL,
  Cost     DECIMAL(18,2) NOT NULL,
  Quantity INT           NOT NULL
);
Step 4.5 - Load Sample Data (SQL)
Load DimDate (last 90 days):
SQL
DECLARE @d DATE = DATEADD(DAY, -89, CAST(GETDATE() AS DATE));
WHILE @d <= CAST(GETDATE() AS DATE)
BEGIN
  INSERT INTO dbo.DimDate (DateKey, [Date], [Year], [MonthNumber], [MonthName])
  VALUES (
    CONVERT(INT, FORMAT(@d,'yyyyMMdd')),
    @d,
    YEAR(@d),
    MONTH(@d),
    DATENAME(MONTH, @d)
  );
  SET @d = DATEADD(DAY, 1, @d);
END;
Load FactSales (random sample):
SQL
DECLARE @i INT = 1;
WHILE @i <= 300
BEGIN
  DECLARE @dt DATE = DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 90, CAST(GETDATE() AS DATE));
  DECLARE @dateKey INT = CONVERT(INT, FORMAT(@dt,'yyyyMMdd'));
  INSERT INTO dbo.FactSales (SalesId, DateKey, Revenue, Cost, Quantity)
  VALUES (
    @i,
    @dateKey,
    CAST(50 + (ABS(CHECKSUM(NEWID())) % 5000) / 10.0 AS DECIMAL(18,2)),
    CAST(20 + (ABS(CHECKSUM(NEWID())) % 3000) / 10.0 AS DECIMAL(18,2)),
    1 + (ABS(CHECKSUM(NEWID())) % 10)
  );
  SET @i += 1;
END;
Step 4.6 - Validate Data
SQL
SELECT TOP 5 * FROM dbo.DimDate ORDER BY [Date] DESC;
SELECT TOP 5 * FROM dbo.FactSales ORDER BY SalesId DESC;
5. Build the Semantic Model (Governed KPIs)
Step 5.1 - Create Semantic Model
Where: Warehouse page (WH_Sales_Gold)
New -> Semantic model -> Select tables: dbo.DimDate, dbo.FactSales -> Create/Save
Step 5.2 - Create Relationship
Where: Semantic Model -> Model view
Create: FactSales[DateKey] -> DimDate[DateKey] (Many-to-One)
Step 5.3 - Create DAX Measures (KPIs)
Where: Semantic Model -> Model view
DAX
Total Revenue = SUM ( FactSales[Revenue] )
Total Cost    = SUM ( FactSales[Cost] )
Profit        = [Total Revenue] - [Total Cost]
Margin %      = DIVIDE ( [Profit], [Total Revenue] )
Revenue MTD = CALCULATE ( [Total Revenue], DATESMTD ( DimDate[Date] ) )
Revenue YTD = CALCULATE ( [Total Revenue], DATESYTD ( DimDate[Date] ) )
Revenue Last Month = CALCULATE ( [Total Revenue], PREVIOUSMONTH ( DimDate[Date] ) )
6. Start Foundry Local
Step 6.1 - Start Service
Where: local terminal
Start your Foundry Local service (command depends on your installation).
Verify the model catalog:
Bash
curl http://127.0.0.1:51970/v1/models
7. Streamlit App (NL -> DAX -> ExecuteQueries)
Step 7.1 - Create Project + Install Dependencies
Bash
mkdir
 
foundry_fabric_chat
cd 
foundry_fabric_chat
python -m venv .venv
Windows (PowerShell):
PowerShell
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install streamlit requests pandas
Step 7.2 - Capture Workspace and Dataset IDs
Workspace (Group) ID: from the workspace URL: /groups/<GROUP_ID>/
Dataset ID: from the semantic model URL: /datasets/<DATASET_ID>
Step 7.3 - Get a Power BI Access Token (Azure CLI)
Bash
az login
az account get-access-token --resource https://analysis.windows.net/powerbi/api --query accessToken -o tsv
Step 7.4 - Create app.py
Create a file named app.py in the project folder and paste the code below.
Python (app.py)
import json
import re
import requests
import pandas as pd
import streamlit as st
FOUNDRY_BASE = "http://127.0.0.1:51970/v1"
st.set_page_config(page_title="NL -> Governed Insights (DAX)", page_icon="📊", layout="wide")
st.title("📊 Natural Language -> Governed Insights (Semantic Model + DAX)")
@st.cache_data(ttl=10)
def fetch_models():
    r = requests.get(f"{FOUNDRY_BASE}/models", timeout=30)
    r.raise_for_status()
    data = r.json()
    return sorted([m["id"] for m in data.get("data", [])])
def call_foundry_chat(model_id: str, system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1
    }
    r = requests.post(f"{FOUNDRY_BASE}/chat/completions", json=payload, timeout=120)
    r.raise_for_status()
    out = r.json()
    return out["choices"][0]["message"]["content"]
def extract_dax(text: str) -> str:
    m = re.search(r"```(?:DAX|dax)?\s*(.*?)```", text, flags=re.S)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"(EVALUATE\s+.*)", text, flags=re.S | re.I)
    if m2:
        return m2.group(1).strip()
    return text.strip()
def execute_dax(group_id: str, dataset_id: str, access_token: str, dax_query: str) -> pd.DataFrame:
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/executeQueries"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "queries": [{"query": dax_query}],
        "serializerSettings": {"includeNulls": True}
    }
    r = requests.post(url, headers=headers, data=json.dumps(body), timeout=120)
    r.raise_for_status()
    data = r.json()
    results = data.get("results", [])
    if not results:
        return pd.DataFrame()
    tables = results[0].get("tables", [])
    if not tables:
        return pd.DataFrame()
    rows = tables[0].get("rows", [])
    return pd.DataFrame(rows)
st.sidebar.header("Configuration")
if st.sidebar.button("Refresh Models"):
    st.cache_data.clear()
models = fetch_models()
model_id = st.sidebar.selectbox("Foundry Model", models)
group_id = st.sidebar.text_input("Workspace (Group) ID", placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
dataset_id = st.sidebar.text_input("Dataset (Semantic Model) ID", placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
access_token = st.sidebar.text_area("Power BI Access Token", height=140, placeholder="Paste token from Azure CLI")
st.sidebar.divider()
semantic_contract = st.sidebar.text_area(
    "Semantic Contract (recommended)",
    height=220,
    value=(
        "You generate ONLY a Power BI DAX query for ExecuteQueries.\n"
        "Use the governed measures:\n"
        "- [Total Revenue], [Total Cost], [Profit], [Margin %], [Revenue MTD], [Revenue YTD], [Revenue Last Month]\n"
        "Use DimDate[Date] and DimDate[MonthName] for time/grouping.\n"
        "Return ONLY the DAX query (preferably wrapped in ```DAX```).\n"
        "If a table output is needed, use EVALUATE with SUMMARIZECOLUMNS.\n"
    )
)
st.subheader("Ask a business question")
question = st.text_input("Question", placeholder="e.g., Show revenue YTD by month")
run_btn = st.button("Generate DAX + Run", type="primary")
if run_btn:
    if not group_id or not dataset_id or not access_token.strip():
        st.error("Please provide Workspace ID, Dataset ID, and Access Token in the sidebar.")
        st.stop()
    if not question.strip():
        st.error("Please enter a question.")
        st.stop()
    system_prompt = (
        "You are a Power BI DAX expert.\n"
        "Generate an ExecuteQueries-compatible DAX query based on the user's request.\n"
        "Follow the semantic contract strictly.\n\n"
        f"{semantic_contract}"
    )
    with st.spinner("Generating governed DAX..."):
        raw = call_foundry_chat(model_id=model_id, system_prompt=system_prompt, user_prompt=question)
    dax = extract_dax(raw)
    st.markdown("### Generated DAX")
    st.code(dax, language="DAX")
    with st.spinner("Executing via Power BI ExecuteQueries API..."):
        try:
            df = execute_dax(group_id=group_id, dataset_id=dataset_id, access_token=access_token.strip(), dax_query=dax)
        except Exception as e:
            st.error(f"ExecuteQueries failed: {e}")
            st.stop()
    st.markdown("### Results")
    if df.empty:
        st.info("Query returned no rows (or response parsing found no table). Try a different question.")
    else:
        st.dataframe(df, use_container_width=True)
Step 7.5 - Run the App
Bash
streamlit run app.py
8. Test Prompts
Try these questions in the UI:
What is total revenue?
What is revenue last month?
Show revenue YTD by month
What is margin %?
9. Troubleshooting
Foundry Local not reachable: confirm the service is running and /v1/models returns model IDs.
ExecuteQueries 401/403: ensure the access token is valid and has Power BI permissions for the workspace/dataset.
Empty results: try a simpler question or confirm the semantic model contains data and measures.
Slow responses: use a smaller local model or reduce prompt verbosity in the semantic contract.
10. Production Hardening Checklist
Use a proper auth strategy (service principal / managed identity) rather than a copied CLI token.
Add query guardrails (row limits, timeouts, allowed measures/columns) before execution.
Log prompts, generated DAX, and execution metadata for audit and troubleshooting.
Cache common questions and/or DAX templates for faster responses.
Version and certify semantic models; keep KPI definitions centralized and controlled.
Natural Language to Governed Insights
End-to-End Runbook (Microsoft Fabric + Semantic Model + Foundry Local)


From Questions to Trusted Decisions


Every business leader wants the same outcome: the ability to ask a simple question in plain English and receive an immediate, accurate answer.
             
“What was our profit margin last quarter?”
This is the promise of AI-powered analytics. Yet for most enterprises, it remains unfulfilled.
The issue is not access to data, nor the absence of AI. The real challenge is trust at scale. Business users depend on technical specialists because answers live behind SQL and DAX logic. When teams answer the same question differently due to inconsistent KPI definitions, confidence erodes and decision-making slows.
This runbook presents a practical, end-to-end blueprint for delivering Natural Language to Insights using governed semantic models in Microsoft Fabric. By anchoring AI interactions to certified KPIs, Row-Level Security (RLS), and enterprise policies, organizations can safely scale conversational analytics from experimentation to executive decision-making.


1.
 
Overview


This runbook builds a Natural Language (NL) to Insights experience where an LLM generates governed DAX and executes it against a Power BI Semantic Model. The semantic model remains the contract for KPIs, relationships, and security.


What you will build


A Fabric Warehouse with a simple star schema (DimDate + FactSales).


A Power BI Semantic Model with certified DAX measures (governed KPIs).


A local LLM runtime (Foundry Local) that produces ExecuteQueries-compatible DAX.


A Streamlit UI that runs DAX via the Power BI ExecuteQueries API and displays results.


2. Prerequisites


Microsoft Fabric access (permission to create Workspace, Warehouse, and Semantic Model).


Azure CLI installed and able to sign in (for a quick Power BI access token).


Python 3.10+ (recommended) on your local machine.


Foundry Local installed and able to run an OpenAI-compatible endpoint at 
http://127.0.0.1:51970/v1
.


3. Architecture


High-level execution path:


Natural Language question
  -> Foundry Local LLM (generates DAX)
  -> Power BI Semantic Model (governed KPIs + RLS)
  -> ExecuteQueries API
  -> Results + narrative (optional)


4. Build the Data Foundation in Fabric


Step 4.1 - Create Workspace


Where: Microsoft Fabric Portal


Workspaces -> New workspace -> Name: WS-Sales-DEV


Step 4.2 - Create Fabric Warehouse


Where: WS-Sales-DEV


New -> Warehouse -> Name: WH_Sales_Gold


Step 4.3 - Open SQL Editor


Where: WH_Sales_Gold -> New SQL Query


Run all SQL in the Warehouse SQL editor.


Step 4.4 - Create Tables (SQL)


Create DimDate:


SQL
CREATE TABLE dbo.DimDate (
  DateKey       INT         NOT NULL,
  [Date]        DATE        NOT NULL,
  [Year]        INT         NOT NULL,
  [MonthNumber] INT         NOT NULL,
  [MonthName]   VARCHAR(20) NOT NULL
);


Create FactSales:


SQL
CREATE TABLE dbo.FactSales (
  SalesId  BIGINT        NOT NULL,
  DateKey  INT           NOT NULL,
  Revenue  DECIMAL(18,2) NOT NULL,
  Cost     DECIMAL(18,2) NOT NULL,
  Quantity INT           NOT NULL
);


Step 4.5 - Load Sample Data (SQL)


Load DimDate (last 90 days):


SQL
DECLARE @d DATE = DATEADD(DAY, -89, CAST(GETDATE() AS DATE));
WHILE @d <= CAST(GETDATE() AS DATE)
BEGIN
  INSERT INTO dbo.DimDate (DateKey, [Date], [Year], [MonthNumber], [MonthName])
  VALUES (
    CONVERT(INT, FORMAT(@d,'yyyyMMdd')),
    @d,
    YEAR(@d),
    MONTH(@d),
    DATENAME(MONTH, @d)
  );
  SET @d = DATEADD(DAY, 1, @d);
END;


Load FactSales (random sample):


SQL
DECLARE @i INT = 1;
WHILE @i <= 300
BEGIN
  DECLARE @dt DATE = DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 90, CAST(GETDATE() AS DATE));
  DECLARE @dateKey INT = CONVERT(INT, FORMAT(@dt,'yyyyMMdd'));
  INSERT INTO dbo.FactSales (SalesId, DateKey, Revenue, Cost, Quantity)
  VALUES (
    @i,
    @dateKey,
    CAST(50 + (ABS(CHECKSUM(NEWID())) % 5000) / 10.0 AS DECIMAL(18,2)),
    CAST(20 + (ABS(CHECKSUM(NEWID())) % 3000) / 10.0 AS DECIMAL(18,2)),
    1 + (ABS(CHECKSUM(NEWID())) % 10)
  );
  SET @i += 1;
END;


Step 4.6 - Validate Data


SQL
SELECT TOP 5 * FROM dbo.DimDate ORDER BY [Date] DESC;
SELECT TOP 5 * FROM dbo.FactSales ORDER BY SalesId DESC;


5. Build the Semantic Model (Governed KPIs)


Step 5.1 - Create Semantic Model


Where: Warehouse page (WH_Sales_Gold)


New -> Semantic model -> Select tables: dbo.DimDate, dbo.FactSales -> Create/Save


Step 5.2 - Create Relationship


Where: Semantic Model -> Model view


Create: FactSales[DateKey] -> DimDate[DateKey] (Many-to-One)


Step 5.3 - Create DAX Measures (KPIs)


Where: Semantic Model -> Model view


DAX
Total Revenue = SUM ( FactSales[Revenue] )
Total Cost    = SUM ( FactSales[Cost] )
Profit        = [Total Revenue] - [Total Cost]
Margin %      = DIVIDE ( [Profit], [Total Revenue] )
Revenue MTD = CALCULATE ( [Total Revenue], DATESMTD ( DimDate[Date] ) )
Revenue YTD = CALCULATE ( [Total Revenue], DATESYTD ( DimDate[Date] ) )
Revenue Last Month = CALCULATE ( [Total Revenue], PREVIOUSMONTH ( DimDate[Date] ) )


6. Start Foundry Local


Step 6.1 - Start Service


Where: local terminal


Start your Foundry Local service (command depends on your installation).


Verify the model catalog:


Bash
curl http://127.0.0.1:51970/v1/models


7. Streamlit App (NL -> DAX -> ExecuteQueries)


Step 7.1 - Create Project + Install Dependencies


Bash
mkdir
 
foundry_fabric_chat
cd 
foundry_fabric_chat
python -m venv .venv


Windows (PowerShell):


PowerShell
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install streamlit requests pandas


Step 7.2 - Capture Workspace and Dataset IDs


Workspace (Group) ID: from the workspace URL: /groups/<GROUP_ID>/


Dataset ID: from the semantic model URL: /datasets/<DATASET_ID>


Step 7.3 - Get a Power BI Access Token (Azure CLI)


Bash
az login
az account get-access-token --resource https://analysis.windows.net/powerbi/api --query accessToken -o tsv


Step 7.4 - Create app.py


Create a file named app.py in the project folder and paste the code below.


Python (app.py)
import json
import re
import requests
import pandas as pd
import streamlit as st
FOUNDRY_BASE = "http://127.0.0.1:51970/v1"
st.set_page_config(page_title="NL -> Governed Insights (DAX)", page_icon="📊", layout="wide")
st.title("📊 Natural Language -> Governed Insights (Semantic Model + DAX)")
@st.cache_data(ttl=10)
def fetch_models():
    r = requests.get(f"{FOUNDRY_BASE}/models", timeout=30)
    r.raise_for_status()
    data = r.json()
    return sorted([m["id"] for m in data.get("data", [])])
def call_foundry_chat(model_id: str, system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1
    }
    r = requests.post(f"{FOUNDRY_BASE}/chat/completions", json=payload, timeout=120)
    r.raise_for_status()
    out = r.json()
    return out["choices"][0]["message"]["content"]
def extract_dax(text: str) -> str:
    m = re.search(r"```(?:DAX|dax)?\s*(.*?)```", text, flags=re.S)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"(EVALUATE\s+.*)", text, flags=re.S | re.I)
    if m2:
        return m2.group(1).strip()
    return text.strip()
def execute_dax(group_id: str, dataset_id: str, access_token: str, dax_query: str) -> pd.DataFrame:
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/executeQueries"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "queries": [{"query": dax_query}],
        "serializerSettings": {"includeNulls": True}
    }
    r = requests.post(url, headers=headers, data=json.dumps(body), timeout=120)
    r.raise_for_status()
    data = r.json()
    results = data.get("results", [])
    if not results:
        return pd.DataFrame()
    tables = results[0].get("tables", [])
    if not tables:
        return pd.DataFrame()
    rows = tables[0].get("rows", [])
    return pd.DataFrame(rows)
st.sidebar.header("Configuration")
if st.sidebar.button("Refresh Models"):
    st.cache_data.clear()
models = fetch_models()
model_id = st.sidebar.selectbox("Foundry Model", models)
group_id = st.sidebar.text_input("Workspace (Group) ID", placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
dataset_id = st.sidebar.text_input("Dataset (Semantic Model) ID", placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
access_token = st.sidebar.text_area("Power BI Access Token", height=140, placeholder="Paste token from Azure CLI")
st.sidebar.divider()
semantic_contract = st.sidebar.text_area(
    "Semantic Contract (recommended)",
    height=220,
    value=(
        "You generate ONLY a Power BI DAX query for ExecuteQueries.\n"
        "Use the governed measures:\n"
        "- [Total Revenue], [Total Cost], [Profit], [Margin %], [Revenue MTD], [Revenue YTD], [Revenue Last Month]\n"
        "Use DimDate[Date] and DimDate[MonthName] for time/grouping.\n"
        "Return ONLY the DAX query (preferably wrapped in ```DAX```).\n"
        "If a table output is needed, use EVALUATE with SUMMARIZECOLUMNS.\n"
    )
)
st.subheader("Ask a business question")
question = st.text_input("Question", placeholder="e.g., Show revenue YTD by month")
run_btn = st.button("Generate DAX + Run", type="primary")
if run_btn:
    if not group_id or not dataset_id or not access_token.strip():
        st.error("Please provide Workspace ID, Dataset ID, and Access Token in the sidebar.")
        st.stop()
    if not question.strip():
        st.error("Please enter a question.")
        st.stop()
    system_prompt = (
        "You are a Power BI DAX expert.\n"
        "Generate an ExecuteQueries-compatible DAX query based on the user's request.\n"
        "Follow the semantic contract strictly.\n\n"
        f"{semantic_contract}"
    )
    with st.spinner("Generating governed DAX..."):
        raw = call_foundry_chat(model_id=model_id, system_prompt=system_prompt, user_prompt=question)
    dax = extract_dax(raw)
    st.markdown("### Generated DAX")
    st.code(dax, language="DAX")
    with st.spinner("Executing via Power BI ExecuteQueries API..."):
        try:
            df = execute_dax(group_id=group_id, dataset_id=dataset_id, access_token=access_token.strip(), dax_query=dax)
        except Exception as e:
            st.error(f"ExecuteQueries failed: {e}")
            st.stop()
    st.markdown("### Results")
    if df.empty:
        st.info("Query returned no rows (or response parsing found no table). Try a different question.")
    else:
        st.dataframe(df, use_container_width=True)


Step 7.5 - Run the App


Bash
streamlit run app.py


8. Test Prompts


Try these questions in the UI:


What is total revenue?


What is revenue last month?


Show revenue YTD by month


What is margin %?


9. Troubleshooting


Foundry Local not reachable: confirm the service is running and /v1/models returns model IDs.


ExecuteQueries 401/403: ensure the access token is valid and has Power BI permissions for the workspace/dataset.


Empty results: try a simpler question or confirm the semantic model contains data and measures.


Slow responses: use a smaller local model or reduce prompt verbosity in the semantic contract.


10. Production Hardening Checklist


Use a proper auth strategy (service principal / managed identity) rather than a copied CLI token.


Add query guardrails (row limits, timeouts, allowed measures/columns) before execution.


Log prompts, generated DAX, and execution metadata for audit and troubleshooting.


Cache common questions and/or DAX templates for faster responses.


Version and certify semantic models; keep KPI definitions centralized and controlled.

