"""
Token manager for Azure AD and Power BI authentication.
Handles token acquisition, refresh, and validation.
"""

import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json


class TokenManager:
    """Manages Azure AD tokens for Power BI API access."""
    
    AZURE_AUTH_ENDPOINT = "https://login.microsoftonline.com"
    POWER_BI_RESOURCE = "https://analysis.windows.net/powerbi/api"
    
    def __init__(self, tenant_id: str):
        """
        Initialize token manager.
        
        Args:
            tenant_id: Azure AD tenant ID
        """
        self.tenant_id = tenant_id
        self.token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
    
    def acquire_token_azure_cli(self) -> Optional[str]:
        """
        Acquire token using Azure CLI (for development).
        Requires: az login to be executed first.
        
        Returns:
            Access token or None if failed
        """
        try:
            import subprocess
            result = subprocess.run(
                ["az", "account", "get-access-token", 
                 "--resource", self.POWER_BI_RESOURCE,
                 "--query", "accessToken", "-o", "tsv"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.token = result.stdout.strip()
                # Azure CLI tokens are typically valid for 1 hour
                self.token_expiry = datetime.now() + timedelta(hours=1)
                return self.token
            else:
                print(f"Azure CLI error: {result.stderr}")
                return None
                
        except FileNotFoundError:
            print("Azure CLI not found. Please install it: https://learn.microsoft.com/cli/azure/install-azure-cli")
            return None
        except Exception as e:
            print(f"Error acquiring token via Azure CLI: {e}")
            return None
    
    def acquire_token_app_registration(
        self, 
        client_id: str, 
        client_secret: str
    ) -> Optional[str]:
        """
        Acquire token using app registration (for production).
        
        Args:
            client_id: Azure AD app client ID
            client_secret: Azure AD app client secret
            
        Returns:
            Access token or None if failed
        """
        try:
            auth_url = f"{self.AZURE_AUTH_ENDPOINT}/{self.tenant_id}/oauth2/v2.0/token"
            
            payload = {
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": f"{self.POWER_BI_RESOURCE}/.default",
                "grant_type": "client_credentials"
            }
            
            response = requests.post(auth_url, data=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                expires_in = data.get("expires_in", 3600)
                self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                return self.token
            else:
                print(f"Token acquisition failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error acquiring token via app registration: {e}")
            return None
    
    def is_token_valid(self) -> bool:
        """Check if current token is valid and not expired."""
        if not self.token or not self.token_expiry:
            return False
        
        # Consider token expired if less than 5 minutes remaining
        return datetime.now() < (self.token_expiry - timedelta(minutes=5))
    
    def get_token(self) -> Optional[str]:
        """
        Get valid token. Returns current token if valid, None otherwise.
        
        Returns:
            Valid access token or None
        """
        if self.is_token_valid():
            return self.token
        return None
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authorization headers for Power BI API requests.
        
        Returns:
            Dictionary with Authorization header
        """
        token = self.get_token()
        if not token:
            return {}
        
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
