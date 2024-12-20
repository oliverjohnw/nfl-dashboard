import streamlit as st
import pandas as pd
import re

# local imports
from src.utils import read_file, streamlit_css
from src.pages import game_page, week_page

# dasboard configs
dashboard_configs = read_file("configs/dashboard_configs.yaml")

# sidebar
st.set_page_config(layout="wide")
st.sidebar.title("Select Matchup")

# Set wide layout for the app
streamlit_css("css/main.css")

# week choice
week_choice = st.sidebar.selectbox("Select Week", 
                                   ["Week 16", "Week 17", "Week 18", "Week 13", "Week 14", "Week 15"]
                                   )

# read in schedule information
schedule_info_path = dashboard_configs["configs"]["schedule"]
schedule_info = pd.read_csv(schedule_info_path)

# week
week = int([int(num) for num in re.findall(r'\d+', week_choice)][0])

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

# weekly overview
else:
    week_page(week, dashboard_configs, weekly_games_data)