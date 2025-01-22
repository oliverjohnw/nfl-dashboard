import streamlit as st
import pandas as pd
import re

# local imports
from src.utils import read_file, streamlit_css, load_data
from src.pages import game_page

# dasboard configs
dashboard_configs = read_file("configs/dashboard_configs.yaml")

# sidebar
st.set_page_config(layout="wide")
st.sidebar.title("Select Matchup")

# Set wide layout for the app
streamlit_css("css/main.css")

# week choice
week_choice = st.sidebar.selectbox("Select Week", 
                                   ["Championship"]
                                   )

# read in schedule information
schedule_info_path = st.secrets["data"]["schedule"]
schedule_info = load_data(schedule_info_path, sheet_name = "NFL Schedule 2024-2025")

# week
if week_choice not in ["Divisional", "Championship"]:
    week = int([int(num) for num in re.findall(r'\d+', week_choice)][0])
else:
    week = week_choice

# weekly games
weekly_games_data = schedule_info.loc[schedule_info["week"] == week, :]
weekly_away_teams = weekly_games_data.loc[:, "away_team"]
weekly_home_teams = weekly_games_data.loc[:, "home_team"]
weekly_games = [away_team + " @ " + home_team for away_team, home_team in zip(weekly_away_teams, weekly_home_teams)]
weekly_games = weekly_games + ["Weekly Overview"]

# display game choice
game_choice = st.sidebar.selectbox("Select Game", weekly_games)

# weekly overview
if game_choice != "Weekly Overview":
    game_page(game_choice, week, dashboard_configs)