"""
Workspace Configuration Page for Foundry Local + Fabric Integration.
Allows users to set up and validate their Power BI/Fabric credentials and configuration.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules import TokenManager, WorkspaceManager
from config import Config


def workspace_config_page():
    """Render the workspace configuration page."""
    
    st.title("⚙️ Settings - Configure Fabric Connection")
    
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "workspace_id" not in st.session_state:
        st.session_state.workspace_id = None
    if "dataset_id" not in st.session_state:
        st.session_state.dataset_id = None
    
    # Step 1: Authentication
    st.subheader("Step 1: Authentication")
    st.write("Connect to your Azure account to access Power BI/Fabric")
    
    auth_method = st.radio(
        "Select authentication method:",
        ["Azure CLI (Development)", "App Registration (Production)"],
        key="auth_method"
    )
    
    token_manager = None
    
    if auth_method == "Azure CLI (Development)":
        st.info("💡 Make sure you have Azure CLI installed and logged in: `az login`")
        
        if st.button("🔐 Authenticate with Azure CLI", use_container_width=True):
            with st.spinner("Attempting to get token from Azure CLI..."):
                try:
                    tenant_id = Config.AZURE_TENANT_ID or "common"
                    token_manager = TokenManager(tenant_id)
                    token = token_manager.acquire_token_azure_cli()
                    
                    if token:
                        st.session_state.access_token = token
                        st.session_state.authenticated = True
                        st.success("✅ Successfully authenticated with Azure CLI!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to get token from Azure CLI. Is Azure CLI installed and logged in?")
                
                except Exception as e:
                    st.error(f"❌ Authentication error: {str(e)}")
    
    else:  # App Registration
        st.info("💡 You need Azure AD App Registration credentials (Client ID and Secret)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            client_id = st.text_input(
                "Azure AD Client ID:",
                type="default",
                key="client_id_input"
            )
        
        with col2:
            client_secret = st.text_input(
                "Azure AD Client Secret:",
                type="password",
                key="client_secret_input"
            )
        
        tenant_id = st.text_input(
            "Azure AD Tenant ID:",
            value=Config.AZURE_TENANT_ID or "",
            key="tenant_id_input"
        )
        
        if st.button("🔐 Authenticate with App Registration", use_container_width=True):
            if not all([client_id, client_secret, tenant_id]):
                st.error("❌ Please fill in all required fields")
            else:
                with st.spinner("Attempting app registration authentication..."):
                    try:
                        token_manager = TokenManager(tenant_id)
                        token = token_manager.acquire_token_app_registration(client_id, client_secret)
                        
                        if token:
                            st.session_state.access_token = token
                            st.session_state.authenticated = True
                            st.success("✅ Successfully authenticated with App Registration!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to authenticate. Check your credentials.")
                    
                    except Exception as e:
                        st.error(f"❌ Authentication error: {str(e)}")
    
    # Check if authenticated for next steps
    if not st.session_state.authenticated or not st.session_state.access_token:
        st.info("👆 Please complete authentication to proceed")
        st.stop()
    
    # Display authentication status
    st.success("✅ Authenticated")
    
    # Step 2: Select Workspace
    st.divider()
    st.subheader("Step 2: Select Workspace")
    
    if st.button("🔄 Refresh Workspaces", use_container_width=True):
        st.session_state.workspaces_cache = None
    
    with st.spinner("Loading workspaces..."):
        try:
            token_manager = TokenManager(Config.AZURE_TENANT_ID or "common")
            token_manager.token = st.session_state.access_token
            
            workspace_manager = WorkspaceManager(token_manager)
            workspaces = workspace_manager.fetch_workspaces()
            
            if not workspaces:
                st.error("❌ No workspaces found. Make sure you have access to at least one workspace.")
                st.stop()
            
            # Create workspace options
            workspace_options = {ws["name"]: ws["id"] for ws in workspaces}
            
            selected_workspace_name = st.selectbox(
                "Select Workspace:",
                options=list(workspace_options.keys()),
                key="workspace_select"
            )
            
            selected_workspace_id = workspace_options[selected_workspace_name]
            st.session_state.workspace_id = selected_workspace_id
            st.session_state.workspace_name = selected_workspace_name
            
            # Step 3: Select Dataset
            st.divider()
            st.subheader("Step 3: Select Semantic Model (Dataset)")
            
            with st.spinner("Loading datasets..."):
                datasets = workspace_manager.fetch_datasets(selected_workspace_id)
                
                if not datasets:
                    st.error("❌ No datasets found in this workspace. Create a semantic model first.")
                    st.stop()
                
                # Create dataset options
                dataset_options = {ds["name"]: ds["id"] for ds in datasets}
                
                selected_dataset_name = st.selectbox(
                    "Select Semantic Model (Dataset):",
                    options=list(dataset_options.keys()),
                    key="dataset_select"
                )
                
                selected_dataset_id = dataset_options[selected_dataset_name]
                st.session_state.dataset_id = selected_dataset_id
                st.session_state.dataset_name = selected_dataset_name
                
                # Step 4: Validate Connection
                st.divider()
                st.subheader("Step 4: Validate Connection")
                
                if st.button("✅ Validate Connection", use_container_width=True):
                    with st.spinner("Validating connection..."):
                        is_valid = workspace_manager.validate_dataset_access(
                            selected_workspace_id,
                            selected_dataset_id
                        )
                        
                        if is_valid:
                            st.success("✅ Connection validated successfully!")
                            
                            # Show configuration summary
                            st.divider()
                            st.subheader("📋 Configuration Summary")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Workspace:** {selected_workspace_name}")
                                st.write(f"**Workspace ID:** `{selected_workspace_id}`")
                            
                            with col2:
                                st.write(f"**Semantic Model:** {selected_dataset_name}")
                                st.write(f"**Dataset ID:** `{selected_dataset_id}`")
                            
                            st.info("✅ You're all set! Go to Semantic Query page to start asking questions.")
                        
                        else:
                            st.error("❌ Connection validation failed. Check your permissions.")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()


if __name__ == "__main__":
    workspace_config_page()
