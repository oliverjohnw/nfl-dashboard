import streamlit as st

def game_notes(away_team, home_team, week, dashboard_configs):
    """
    Function to display game notes

    Args:
        away_team (str): away team
        home_team (str): home team
        week (int): week
        dashboard_configs (dict): dictionary with inputs/params for app
    """
    title_html = f"""
    """
    st.markdown(title_html, unsafe_allow_html=True)