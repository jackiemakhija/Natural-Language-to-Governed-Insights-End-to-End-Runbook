"""
Semantic Query Page for Foundry Local + Fabric Integration.
Allows users to ask natural language questions and get DAX-generated results.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules import (
    FabricDaxGenerator, 
    PowerBIExecutor, 
    TokenManager,
    WorkspaceManager
)
from components.results_display import (
    display_results_dataframe,
    display_error,
    display_warning,
    display_info,
    display_dax_query
)
from config import Config


def semantic_query_page():
    """Render the semantic query page."""
    
    st.title("📊 Semantic Query - Natural Language to DAX")
    
    # Check if authentication is configured
    if not st.session_state.get("authenticated"):
        st.warning("⚠️ Please configure your credentials first in Settings")
        st.stop()
    
    # Get configured values from session state
    workspace_id = st.session_state.get("workspace_id")
    dataset_id = st.session_state.get("dataset_id")
    token = st.session_state.get("access_token")
    
    if not all([workspace_id, dataset_id, token]):
        st.error("Missing configuration. Please go to Settings to configure workspace and dataset.")
        st.stop()
    
    # Initialize modules
    token_manager = TokenManager(tenant_id=Config.AZURE_TENANT_ID)
    token_manager.token = token  # Use session token
    
    dax_generator = FabricDaxGenerator()
    executor = PowerBIExecutor(token_manager)
    workspace_manager = WorkspaceManager(token_manager)
    
    # Get dataset tables for context
    dataset_tables = None
    try:
        dataset_tables = workspace_manager.get_dataset_tables(workspace_id, dataset_id)
    except Exception as e:
        st.warning(f"Could not load dataset metadata: {e}")
    
    # Display dataset info
    with st.expander("📋 Dataset Information", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Workspace ID:** {workspace_id}")
        with col2:
            st.write(f"**Dataset ID:** {dataset_id}")
        
        if dataset_tables:
            st.write("**Available Tables:**")
            for table in dataset_tables:
                st.write(f"- {table.get('name', 'Unknown')}")
    
    # Query input section
    st.subheader("🔍 Ask a Question")
    
    user_query = st.text_area(
        "Enter your question in natural language:",
        placeholder="e.g., What is the total revenue for this year? or Show revenue by month",
        height=80,
        key="user_query"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        generate_btn = st.button("🚀 Generate DAX", use_container_width=True)
    
    with col2:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    
    with col3:
        refresh_btn = st.button("🔄 Refresh Token", use_container_width=True)
    
    # Handle button clicks
    if clear_btn:
        st.session_state.last_dax_query = None
        st.session_state.last_results = None
        st.rerun()
    
    if refresh_btn:
        with st.spinner("Refreshing authentication token..."):
            try:
                token_manager.acquire_token_azure_cli()
                if token_manager.is_token_valid():
                    st.session_state.access_token = token_manager.token
                    st.success("✅ Token refreshed successfully")
                else:
                    st.error("❌ Failed to refresh token")
            except Exception as e:
                st.error(f"❌ Token refresh failed: {str(e)}")
    
    # Process query
    if generate_btn and user_query.strip():
        with st.spinner("🔄 Generating DAX query..."):
            try:
                # Generate DAX
                dax_query = dax_generator.generate_dax(user_query)
                
                if not dax_query:
                    display_error("Failed to generate DAX query. Please try again.")
                    st.stop()
                
                # Validate DAX
                is_valid, error_msg = dax_generator.validate_dax(dax_query)
                if not is_valid:
                    display_warning(f"DAX validation warning: {error_msg}")
                
                # Display and allow editing
                st.session_state.last_dax_query = display_dax_query(dax_query, editable=True)
                
                # Execute query button
                execute_btn = st.button("▶️ Execute Query", use_container_width=True)
                
                if execute_btn:
                    with st.spinner("⏳ Executing query..."):
                        try:
                            # Execute the (possibly edited) DAX query
                            results = executor.execute_query(
                                st.session_state.last_dax_query,
                                workspace_id,
                                dataset_id
                            )
                            
                            if not results:
                                display_error("Query execution failed. Check your credentials and try again.")
                                st.stop()
                            
                            if "error" in results:
                                error_details = results.get("details", "Unknown error")
                                display_error(f"Query Error: {error_details}")
                                st.stop()
                            
                            # Parse results
                            df = executor.parse_results_to_dataframe(results)
                            
                            if df is None or df.empty:
                                display_info("Query executed successfully but returned no results.")
                                st.stop()
                            
                            # Store results
                            st.session_state.last_results = df
                            
                            # Display results
                            display_results_dataframe(df)
                            
                            # Download options
                            st.subheader("📥 Download Results")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                csv_data = executor.format_results_as_csv(df)
                                st.download_button(
                                    label="📄 Download as CSV",
                                    data=csv_data,
                                    file_name="query_results.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            
                            with col2:
                                json_data = executor.format_results_as_json(df)
                                st.download_button(
                                    label="📋 Download as JSON",
                                    data=json_data,
                                    file_name="query_results.json",
                                    mime="application/json",
                                    use_container_width=True
                                )
                            
                            # Summary
                            summary = executor.get_result_summary(df)
                            with st.expander("📊 Result Summary"):
                                st.write(f"**Rows:** {summary['rows']}")
                                st.write(f"**Columns:** {summary['columns']}")
                                st.write(f"**Column Names:** {', '.join(summary['column_names'])}")
                        
                        except Exception as e:
                            display_error(f"Unexpected error during query execution: {str(e)}")
            
            except Exception as e:
                display_error(f"Unexpected error: {str(e)}")
    
    # Display previous results if available
    if st.session_state.get("last_results") is not None:
        st.divider()
        st.subheader("Previous Results")
        display_results_dataframe(st.session_state.last_results)


if __name__ == "__main__":
    semantic_query_page()
