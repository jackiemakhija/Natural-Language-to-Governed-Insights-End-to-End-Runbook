"""
Workspace and dataset manager for Power BI / Fabric.
Handles discovery and validation of workspaces and semantic models.
"""

import requests
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json


class WorkspaceManager:
    """Manages workspace and dataset discovery in Power BI / Fabric."""
    
    API_BASE_URL = "https://api.powerbi.com/v1.0/myorg"
    
    def __init__(self, token_manager):
        """
        Initialize workspace manager.
        
        Args:
            token_manager: TokenManager instance
        """
        self.token_manager = token_manager
        self.workspaces_cache: Optional[List[Dict]] = None
        self.cache_expiry: Optional[datetime] = None
        self.cache_ttl_minutes = 5
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry
    
    def fetch_workspaces(self, force_refresh: bool = False) -> Optional[List[Dict]]:
        """
        Fetch all workspaces accessible to the user.
        
        Args:
            force_refresh: Ignore cache and fetch fresh data
            
        Returns:
            List of workspace dicts with 'id' and 'name' or None if failed
        """
        if not force_refresh and self._is_cache_valid() and self.workspaces_cache:
            return self.workspaces_cache
        
        try:
            headers = self.token_manager.get_auth_headers()
            if not headers:
                print("No valid token available. Please authenticate first.")
                return None
            
            url = f"{self.API_BASE_URL}/groups"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                workspaces = [
                    {"id": ws["id"], "name": ws["name"]}
                    for ws in data.get("value", [])
                ]
                
                # Cache the result
                self.workspaces_cache = workspaces
                self.cache_expiry = datetime.now() + timedelta(minutes=self.cache_ttl_minutes)
                
                return workspaces
            else:
                print(f"Failed to fetch workspaces: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching workspaces: {e}")
            return None
    
    def fetch_datasets(self, workspace_id: str) -> Optional[List[Dict]]:
        """
        Fetch all datasets in a workspace.
        
        Args:
            workspace_id: Power BI workspace ID
            
        Returns:
            List of dataset dicts with 'id' and 'name' or None if failed
        """
        try:
            headers = self.token_manager.get_auth_headers()
            if not headers:
                print("No valid token available. Please authenticate first.")
                return None
            
            url = f"{self.API_BASE_URL}/groups/{workspace_id}/datasets"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                datasets = [
                    {"id": ds["id"], "name": ds["name"]}
                    for ds in data.get("value", [])
                ]
                return datasets
            else:
                print(f"Failed to fetch datasets: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching datasets: {e}")
            return None
    
    def validate_dataset_access(
        self, 
        workspace_id: str, 
        dataset_id: str
    ) -> bool:
        """
        Validate that we have access to a dataset.
        
        Args:
            workspace_id: Power BI workspace ID
            dataset_id: Power BI dataset ID
            
        Returns:
            True if accessible, False otherwise
        """
        try:
            headers = self.token_manager.get_auth_headers()
            if not headers:
                return False
            
            url = f"{self.API_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}"
            response = requests.get(url, headers=headers, timeout=10)
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error validating dataset access: {e}")
            return False
    
    def get_dataset_tables(
        self, 
        workspace_id: str, 
        dataset_id: str
    ) -> Optional[List[Dict]]:
        """
        Get tables and measures from a dataset.
        
        Args:
            workspace_id: Power BI workspace ID
            dataset_id: Power BI dataset ID
            
        Returns:
            List of table dicts with metadata or None if failed
        """
        try:
            headers = self.token_manager.get_auth_headers()
            if not headers:
                print("No valid token available. Please authenticate first.")
                return None
            
            url = f"{self.API_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}/tables"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("value", [])
            else:
                print(f"Failed to fetch dataset tables: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching dataset tables: {e}")
            return None
    
    def clear_cache(self):
        """Clear workspace cache."""
        self.workspaces_cache = None
        self.cache_expiry = None
