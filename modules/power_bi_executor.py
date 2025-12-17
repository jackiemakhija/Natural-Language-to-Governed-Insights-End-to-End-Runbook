"""
Power BI Query Executor using ExecuteQueries API.
Executes DAX queries against semantic models and returns results.
"""

import requests
import pandas as pd
from typing import Optional, List, Dict, Any


class PowerBIExecutor:
    """Execute DAX queries against Power BI semantic models."""
    
    API_BASE_URL = "https://api.powerbi.com/v1.0/myorg"
    
    def __init__(self, token_manager):
        """
        Initialize Power BI executor.
        
        Args:
            token_manager: TokenManager instance
        """
        self.token_manager = token_manager
    
    def execute_query(
        self,
        dax_query: str,
        workspace_id: str,
        dataset_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Execute DAX query against a semantic model.
        
        Args:
            dax_query: DAX query to execute
            workspace_id: Power BI workspace ID
            dataset_id: Power BI dataset ID
            
        Returns:
            Query results dict or None if failed
        """
        try:
            headers = self.token_manager.get_auth_headers()
            if not headers:
                print("No valid token available. Please authenticate first.")
                return None
            
            # Power BI ExecuteQueries API endpoint
            url = f"{self.API_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}/executeQueries"
            
            payload = {
                "queries": [
                    {
                        "query": dax_query
                    }
                ],
                "serializerSettings": {
                    "includeNulls": True
                }
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                # DAX syntax error
                error_data = response.json()
                print(f"DAX Syntax Error: {error_data}")
                return {"error": "DAX Syntax Error", "details": error_data}
            elif response.status_code == 401:
                print("Authentication failed. Token may have expired.")
                return None
            elif response.status_code == 403:
                print("Access denied. Check workspace and dataset permissions.")
                return None
            else:
                print(f"Query execution failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("Query execution timeout (30 seconds)")
            return None
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    def parse_results_to_dataframe(self, query_results: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """
        Convert Power BI API results to pandas DataFrame.
        
        Args:
            query_results: Results from execute_query
            
        Returns:
            DataFrame or None if parsing failed
        """
        try:
            if not query_results or "error" in query_results:
                return None
            
            results = query_results.get("results", [])
            if not results:
                return None
            
            # Get the first result table
            first_result = results[0]
            tables = first_result.get("tables", [])
            
            if not tables:
                return None
            
            # Get the first table
            table = tables[0]
            columns = table.get("columns", [])
            rows = table.get("rows", [])
            
            if not columns or not rows:
                return pd.DataFrame()
            
            # Extract column names
            column_names = [col.get("name", f"Column_{i}") for i, col in enumerate(columns)]
            
            # Create DataFrame
            df = pd.DataFrame(rows, columns=column_names)
            
            return df
            
        except Exception as e:
            print(f"Error parsing results: {e}")
            return None
    
    def format_results_as_json(self, df: pd.DataFrame) -> str:
        """
        Format DataFrame as JSON.
        
        Args:
            df: Results DataFrame
            
        Returns:
            JSON string
        """
        return df.to_json(orient="records", indent=2)
    
    def format_results_as_csv(self, df: pd.DataFrame) -> str:
        """
        Format DataFrame as CSV.
        
        Args:
            df: Results DataFrame
            
        Returns:
            CSV string
        """
        return df.to_csv(index=False)
    
    def get_result_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics of results.
        
        Args:
            df: Results DataFrame
            
        Returns:
            Summary dict
        """
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.to_dict()
        }
