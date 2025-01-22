import streamlit as st
import pandas as pd
import nfl_data_py as nfl

# local imports
from src.utils import streamlit_css

def team_information(
    away_team: str,
    home_team: str,
    week: int,
    team_info_config: dict,
    dashboard_configs: dict
):
    """
    Displays team information including:
        * Team logo
        * Team name
        * Team record
        * Team stats
        
    Args:
        away_team (str): away team
        home_team (str): home team
        week (int): week chosen by user
        team_info_config (dict): dictionary with team information
        dashboard_configs (dict): dictionary with inputs/params for app
    """
    # streamlit css
    streamlit_css("css/team_information.css")

    with st.container():
        
        # home and away cols
        col1, col2 = st.columns([1, 1])

        # away team info
        away_logo = team_info_config[away_team]["logo"]
        away_name = team_info_config[away_team]["location"] + " " + team_info_config[away_team]["name"]
        away_color = team_info_config[away_team]["color"]

        # TODO: Fix records
        # display away team
        with col1:
            st.markdown(f"""
            <div class="team">
                <img src="{away_logo}" alt="Away Logo" class="team-logo"/>
                <div class="team-content">
                    <h3 style="background-color: {away_color};">{away_name}</h3>
                    <p class="record"><strong>Record:</strong></p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # home team info
        home_logo = team_info_config[home_team]["logo"]
        home_name = team_info_config[home_team]["location"] + " " + team_info_config[home_team]["name"]
        home_color = team_info_config[home_team]["color"]

        # display home team
        with col2:
            st.markdown(f"""
            <div class="team">
                <img src="{home_logo}" alt="Home Logo" class="team-logo"/>
                <div class="team-content">
                    <h3 style="background-color: {home_color};">{home_name}</h3>
                    <p class="record"><strong>Record:</strong></p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    return