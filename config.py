"""
Configuration module for Foundry Local + Fabric Semantic Model integration.
Manages environment variables, validation, and centralized configuration.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


class Config:
    """Centralized configuration management."""
    
    # Foundry Local Configuration
    FOUNDRY_BASE = os.getenv("FOUNDRY_BASE", "http://127.0.0.1:51970/v1")
    FOUNDRY_MODEL_PHI = os.getenv("FOUNDRY_MODEL_PHI", "phi-3-mini")
    FOUNDRY_MODEL_QWEN = os.getenv("FOUNDRY_MODEL_QWEN", "qwen-32b")
    FOUNDRY_TIMEOUT = int(os.getenv("FOUNDRY_TIMEOUT", "180"))
    
    # Power BI / Fabric Configuration
    POWER_BI_WORKSPACE_ID = os.getenv("POWER_BI_WORKSPACE_ID", "")
    POWER_BI_DATASET_ID = os.getenv("POWER_BI_DATASET_ID", "")
    POWER_BI_BASE_URL = os.getenv("POWER_BI_BASE_URL", "https://analysis.windows.net")
    POWER_BI_RESOURCE = os.getenv("POWER_BI_RESOURCE", "https://analysis.windows.net/powerbi/api")
    
    # Azure AD / Tenant
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
    
    # User Preferences
    USER_PREFERENCE_FORMAT = os.getenv("USER_PREFERENCE_FORMAT", "json")
    CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", "5"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate_fabric_config(cls) -> bool:
        """Validate that essential Fabric configuration is present."""
        required = [cls.AZURE_TENANT_ID]
        return all(required)
    
    @classmethod
    def validate_foundry_config(cls) -> bool:
        """Validate that Foundry configuration is present."""
        return bool(cls.FOUNDRY_BASE and cls.FOUNDRY_MODEL_PHI and cls.FOUNDRY_MODEL_QWEN)
    
    @classmethod
    def get_foundry_api_models_endpoint(cls) -> str:
        """Get Foundry models API endpoint."""
        return f"{cls.FOUNDRY_BASE}/models"
    
    @classmethod
    def get_foundry_chat_endpoint(cls) -> str:
        """Get Foundry chat completion endpoint."""
        return f"{cls.FOUNDRY_BASE}/chat/completions"


# Export configuration instance
config = Config()
