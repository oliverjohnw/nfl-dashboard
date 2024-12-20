import streamlit as st
import pandas as pd

def week_page(
    week: int,
    dashboard_configs: dict,
    weekly_games_data: pd.DataFrame
):
    """
    Weekly overview page
    
    Args:
        week (int): week number
        dashboard_configs (dict): dashboard configurations
    """
    # title
    st.title(f"Week {week} Overview")
    
    # process dataframe
    weekly_games_data = weekly_games_data.drop(columns=["Unnamed: 0", "week", "div_game", "roof", "surface", "game_id"])
    st.dataframe(weekly_games_data.set_index("gameday"))