import streamlit as st
import pandas as pd

# local imports
from src.panels import game_information, team_information
from src.panels import pff_grades, injury_report, bets, game_notes
from src.utils import read_file, streamlit_css

def game_page(
    game_choice: str, 
    week: int,
    dashboard_configs: dict
):
    """
    Function to display game page

    Displays the followings:

    Args:
        game_choice (str): game chosen by user
        week (int): week
        dashboard_configs (dict): dictionary with inputs/params for app
    """
    # streamlit custom CSS
    streamlit_css("css/matchup_information.css")

    # teams
    away_team = game_choice.split(" @ ")[0]
    home_team = game_choice.split(" @ ")[1]

    # Load team information
    team_info_config_path = dashboard_configs["configs"]["team_info"]
    team_info_config = read_file(team_info_config_path)

    with st.container():
        game_information(away_team, home_team, week, dashboard_configs)
        team_information(away_team, home_team, week, team_info_config, dashboard_configs)
    st.divider()

    # dropdown option for bottom of page
    view_choice = st.radio(
        label="View Options",
        options=["Summary", "Picks"],
        index=0, 
        horizontal=True
    )

    # summary page
    if view_choice == "Summary":
        left_column, middle_column, right_column = st.columns([1, 1, 1])

        # display pff grades + injury report
        with left_column:
            with st.container():
                st.subheader("PFF Grades")
                pff_grades(away_team, home_team, week, dashboard_configs)

        with middle_column:
            with st.container():
                st.subheader("Injury Report")
                injury_report(away_team, home_team, week, dashboard_configs)
                

        with right_column:
            with st.container():
                st.subheader("Game Notes")
                game_notes(away_team, home_team, week, dashboard_configs)

    # picks page
    if view_choice == "Picks":
        with st.container():
            st.subheader("Bets")
            bets(away_team, home_team, week, dashboard_configs)


        # with right_column:
        #     with st.container():
        #         st.subheader("Game Notes")
        #         game_notes(away_team, home_team, week, dashboard_configs)


    #     with st.container():
    #         st.subheader("Injury Report")
    #         injury_report(away_team, home_team, week, dashboard_configs)

    # with st.container():
    #     st.subheader("Game Notes")
    #     game_notes(away_team, home_team, week, dashboard_configs)

    # # bets
    # with right_column:
    #     with st.container():
    #         st.subheader("Bets")
    #         bets(away_team, home_team, week, dashboard_configs)
