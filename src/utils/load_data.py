import streamlit as st
import pandas as pd

@st.cache_data
def load_data(file_path: str, sheet_name: str):
    """
    Load data from file path and sheet name
    
    Args:
        file_path (str): path to file
        sheet_name (str): sheet name
        
    Returns:
        pd.DataFrame
    """
    data = pd.read_excel(file_path, sheet_name=f"{sheet_name}", engine = "openpyxl")

    return data