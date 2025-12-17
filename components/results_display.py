"""
Results display components for Streamlit.
Handles formatting and rendering of query results.
"""

import streamlit as st
import pandas as pd
from typing import Optional


def display_results_dataframe(df: pd.DataFrame, title: str = "Query Results"):
    """
    Display results as an interactive table.
    
    Args:
        df: Results DataFrame
        title: Display title
    """
    st.subheader(title)
    
    # Display summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Size (bytes)", df.memory_usage(deep=True).sum())
    
    # Display table
    st.dataframe(df, use_container_width=True, height=400)


def display_results_json(json_str: str, title: str = "Query Results (JSON)"):
    """
    Display results as formatted JSON.
    
    Args:
        json_str: JSON formatted string
        title: Display title
    """
    st.subheader(title)
    st.json(json_str)


def display_results_csv(csv_str: str, title: str = "Query Results (CSV)"):
    """
    Display results as CSV with download option.
    
    Args:
        csv_str: CSV formatted string
        title: Display title
    """
    st.subheader(title)
    st.download_button(
        label="Download CSV",
        data=csv_str,
        file_name="query_results.csv",
        mime="text/csv"
    )
    st.text(csv_str[:500] + "..." if len(csv_str) > 500 else csv_str)


def display_error(error_message: str, title: str = "Error"):
    """
    Display error message.
    
    Args:
        error_message: Error message
        title: Display title
    """
    st.error(f"{title}: {error_message}")


def display_warning(warning_message: str, title: str = "Warning"):
    """
    Display warning message.
    
    Args:
        warning_message: Warning message
        title: Display title
    """
    st.warning(f"{title}: {warning_message}")


def display_info(info_message: str, title: str = "Info"):
    """
    Display info message.
    
    Args:
        info_message: Info message
        title: Display title
    """
    st.info(f"{title}: {info_message}")


def display_dax_query(dax_query: str, editable: bool = False) -> Optional[str]:
    """
    Display DAX query with optional editing capability.
    
    Args:
        dax_query: DAX query to display
        editable: Whether to allow editing
        
    Returns:
        Edited query if editable, original query otherwise
    """
    st.subheader("Generated DAX Query")
    
    if editable:
        edited_query = st.text_area(
            "Edit DAX Query:",
            value=dax_query,
            height=150,
            key="dax_editor"
        )
        return edited_query
    else:
        st.code(dax_query, language="sql")
        return dax_query
