# Code Reference Guide

This guide shows where code snippets from the runbook are implemented in this github_release folder.

## Language-Specific Code Locations

### Python Code
- **Authentication & Token Management**: [modules/token_manager.py](../modules/token_manager.py)
  - `acquire_token_azure_cli()`
  - `acquire_token_app_registration()`
  - `is_token_valid()`

- **Workspace & Dataset Discovery**: [modules/workspace_manager.py](../modules/workspace_manager.py)
  - `fetch_workspaces()`
  - `fetch_datasets()`
  - `validate_dataset_access()`

- **DAX Generation**: [modules/fabric_dax_generator.py](../modules/fabric_dax_generator.py)
  - `generate_dax()`
  - `validate_dax()`
  - `refine_dax()`

- **Query Execution**: [modules/power_bi_executor.py](../modules/power_bi_executor.py)
  - `execute_query()`
  - `parse_results_to_dataframe()`

- **Main Application**: [app.py](../app.py)
  - Multi-page Streamlit router
  - Chat interface with model routing

- **Settings Page**: [pages/workspace_config.py](../pages/workspace_config.py)
  - Workspace selection UI
  - Authentication workflow

- **Semantic Query Page**: [pages/semantic_query.py](../pages/semantic_query.py)
  - NL→DAX→Results workflow

### SQL Code
All SQL examples and warehouse setup scripts are located in:
- **[sql/sample_warehouse_setup.sql](../sql/sample_warehouse_setup.sql)**

Includes:
- `CREATE TABLE dbo.DimDate`
- `CREATE TABLE dbo.FactSales`
- Sample data loading
- Aggregation queries

### DAX Code
All DAX query examples are located in:
- **[dax/sample_queries.dax](../dax/sample_queries.dax)**

Includes:
- Basic ROW queries
- SUMMARIZE by dimensions
- FILTER conditions
- Year-over-year calculations
- Top N queries

### Setup & Automation Scripts

#### Bash/Shell Scripts
- **[scripts/setup_foundry.sh](../scripts/setup_foundry.sh)**
  - Foundry Local installation
  - Service startup
  - Model deployment

#### PowerShell Scripts
- **[scripts/setup_auth_azure.ps1](../scripts/setup_auth_azure.ps1)**
  - Azure CLI authentication setup
  - Token acquisition

---

## Quick Lookup by Topic

| Topic | File | Key Functions/Sections |
|-------|------|------------------------|
| Authentication | modules/token_manager.py | acquire_token_*, is_token_valid() |
| Workspaces | modules/workspace_manager.py | fetch_workspaces(), fetch_datasets() |
| DAX Generation | modules/fabric_dax_generator.py | generate_dax(), validate_dax() |
| Query Execution | modules/power_bi_executor.py | execute_query(), parse_results_to_dataframe() |
| Chat UI | app.py | home_page(), auto_route_model() |
| Settings | pages/workspace_config.py | workspace_config_page() |
| Semantic Query | pages/semantic_query.py | semantic_query_page() |
| SQL Examples | sql/sample_warehouse_setup.sql | All SQL CREATE/INSERT statements |
| DAX Examples | dax/sample_queries.dax | All EVALUATE queries |
| Foundry Setup | scripts/setup_foundry.sh | Installation & startup commands |
| Azure Auth | scripts/setup_auth_azure.ps1 | az login, token retrieval |

---

## Code Block Patterns

When you see code blocks in documentation, use this mapping:

| Pattern | Location |
|---------|----------|
| `TokenManager(...)` | modules/token_manager.py |
| `WorkspaceManager(...)` | modules/workspace_manager.py |
| `FabricDaxGenerator(...)` | modules/fabric_dax_generator.py |
| `PowerBIExecutor(...)` | modules/power_bi_executor.py |
| `CREATE TABLE dbo.` | sql/sample_warehouse_setup.sql |
| `EVALUATE ...` | dax/sample_queries.dax |
| `foundry service start` | scripts/setup_foundry.sh |
| `az login` | scripts/setup_auth_azure.ps1 |

---

## Using This Reference

1. **Find Code**: Look up the topic you need in the "Quick Lookup" table
2. **Locate File**: Open the referenced file
3. **Review**: Read the function/section and understand the implementation
4. **Adapt**: Modify for your needs and integrate into your environment

---

**Last Updated**: December 17, 2025
