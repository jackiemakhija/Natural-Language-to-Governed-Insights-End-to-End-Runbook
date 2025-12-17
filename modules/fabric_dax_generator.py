"""
DAX Generator using Foundry Local LLM.
Generates DAX queries from natural language using local models.
"""

import requests
import re
from typing import Optional, Dict, Any
from config import Config


class FabricDaxGenerator:
    """Generate DAX queries using Foundry Local LLM."""
    
    # System prompt for DAX generation
    DAX_SYSTEM_PROMPT = """You are an expert DAX (Data Analysis Expression) query generator for Power BI and Microsoft Fabric.
Your task is to convert natural language questions into valid DAX queries.

Guidelines:
1. Use EVALUATE statements for queries
2. Reference tables as [TableName]
3. Reference columns as [TableName][ColumnName]
4. Use proper DAX functions: SUM, CALCULATE, FILTER, etc.
5. Return ONLY the DAX query, no explanation
6. Ensure queries are valid and executable
7. Handle date functions properly (DATESYTD, DATESMTD, PREVIOUSMONTH, etc.)

Example:
Q: What is total revenue?
A: EVALUATE ROW("Total Revenue", [Total Revenue])

Q: Show revenue by month
A: EVALUATE SUMMARIZE(ALL(DimDate), DimDate[MonthName], "Revenue", [Total Revenue])
"""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize DAX generator.
        
        Args:
            model_name: Foundry model to use (defaults to QWEN for complex queries)
        """
        self.foundry_base = Config.FOUNDRY_BASE
        self.chat_endpoint = Config.get_foundry_chat_endpoint()
        self.model_name = model_name or Config.FOUNDRY_MODEL_QWEN
        self.timeout = Config.FOUNDRY_TIMEOUT
    
    def generate_dax(self, natural_language_query: str) -> Optional[str]:
        """
        Generate DAX query from natural language.
        
        Args:
            natural_language_query: User's question in natural language
            
        Returns:
            Generated DAX query or None if failed
        """
        try:
            # Prepare the prompt
            messages = [
                {
                    "role": "system",
                    "content": self.DAX_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Generate a DAX query for: {natural_language_query}"
                }
            ]
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": 0.3,  # Lower temperature for more consistent DAX
                "max_tokens": 500,
                "top_p": 0.9
            }
            
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                dax_query = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return dax_query.strip()
            else:
                print(f"Foundry API error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"Foundry API timeout after {self.timeout} seconds")
            return None
        except Exception as e:
            print(f"Error generating DAX: {e}")
            return None
    
    def validate_dax(self, dax_query: str) -> tuple[bool, Optional[str]]:
        """
        Basic validation of DAX query.
        
        Args:
            dax_query: DAX query to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if query is empty
        if not dax_query or not dax_query.strip():
            return False, "DAX query is empty"
        
        # Check for required keywords
        if "EVALUATE" not in dax_query.upper():
            return False, "DAX query must start with EVALUATE"
        
        # Check for unmatched brackets
        if dax_query.count("[") != dax_query.count("]"):
            return False, "Unmatched brackets in DAX query"
        
        # Check for unmatched parentheses
        if dax_query.count("(") != dax_query.count(")"):
            return False, "Unmatched parentheses in DAX query"
        
        return True, None
    
    def refine_dax(self, dax_query: str, feedback: str) -> Optional[str]:
        """
        Refine existing DAX query based on feedback.
        
        Args:
            dax_query: Original DAX query
            feedback: User feedback or error message
            
        Returns:
            Refined DAX query or None if failed
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": self.DAX_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Original DAX:\n{dax_query}\n\nFeedback: {feedback}\n\nPlease refine the DAX query."
                }
            ]
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 500,
                "top_p": 0.9
            }
            
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                refined_dax = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return refined_dax.strip()
            else:
                print(f"Foundry API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error refining DAX: {e}")
            return None
    
    def extract_dax_from_response(self, response_text: str) -> str:
        """
        Extract DAX query from LLM response (handles markdown code blocks).
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Cleaned DAX query
        """
        # Remove markdown code blocks if present
        if "```dax" in response_text.lower():
            match = re.search(r"```dax\n(.*?)\n```", response_text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        if "```" in response_text:
            match = re.search(r"```\n?(.*?)\n?```", response_text, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return response_text.strip()
