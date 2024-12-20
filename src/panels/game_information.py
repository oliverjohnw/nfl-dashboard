import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# local imports
from src.utils import streamlit_css

def game_information(
    away_team: str,
    home_team: str,
    week: int,
    dashboard_configs: dict
):
    """
    Displays game time information including:
        * Date
        * Kickoff time
        * Game location
        
    Args:
        away_team (str): away team
        home_team (str): home team
        week (int): week number
        dashboard_configs (dict): dictionary with inputs/params for app
    """
    # streamlit css
    streamlit_css("css/game_information.css")

    # Load game schedule
    schedule_info_path = dashboard_configs["configs"]["schedule"]
    schedule_info = pd.read_csv(schedule_info_path)

    # load weekly weather
    weather_data_path = dashboard_configs["data"]["weather"]
    weather_data = pd.read_excel(weather_data_path, sheet_name = f'Week {week}')

    # load game line information
    game_lines_path = dashboard_configs["data"]["game_lines"]
    game_lines = pd.read_excel(game_lines_path, sheet_name=f"Week {week}")
    game_lines.loc[:, "Spread Odds"] = game_lines["Spread Odds"].apply(lambda x: "+" + str(x) if x > 0 else str(x))
    game_lines.loc[:, "Total Odds"] = game_lines["Total Odds"].apply(lambda x: "+" + str(x) if x > 0 else str(x))

    # filter to game
    game_info = schedule_info.loc[
        (schedule_info["away_team"] == away_team) & (schedule_info["home_team"] == home_team), :
    ]
    weather_data = weather_data.loc[
        (weather_data["Away"] == away_team) & (weather_data["Home"] == home_team), :
    ]

    game_lines = game_lines.loc[
        (game_lines["Away"] == away_team) & (game_lines["Home"] == home_team), :
        ]

    # game day
    game_day = game_info["weekday"].iloc[0]

    # game date
    game_date = datetime.strptime(game_info["gameday"].iloc[0], "%m/%d/%Y").strftime("%B %d, %Y")

    # game time
    game_time = game_info["gametime"].iloc[0]

    # map to central time
    utc = pytz.timezone("EST")
    central = pytz.timezone("US/Central")
    time_obj = datetime.strptime(game_time, "%H:%M")
    time_with_date = datetime.now().replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
    localized_time = utc.localize(time_with_date)
    central_time = localized_time.astimezone(central).strftime("%I:%M %p")

    # game roof type
    game_roof = game_info["roof"].iloc[0]
    roof_map = {"dome": "Indoor"}
    game_roof = roof_map.get(game_roof, "Outdoor")

    # game field type
    game_surface = game_info["surface"].iloc[0]
    surface_map = {"grass": "Grass"}
    game_surface = surface_map.get(game_surface, "Turf")

    # weather notes
    weather_notes = weather_data["Weather Notes"].iloc[0]
    if pd.isna(weather_notes):
        weather_notes = " "

    # opening lines
    opening_spread = game_lines["Spread"].iloc[0]
    opening_spread_odds = game_lines["Spread Odds"].iloc[0]

    opening_total = game_lines["Total"].iloc[0]
    openining_total_odds = game_lines["Total Odds"].iloc[0]

    st.markdown(f"""
        <div class="game-time">
            <p class="info-header">{game_day}, {game_date} | {central_time}</p>
            <p class="info-detail">{game_roof}, {game_surface}  -  Weather: {weather_notes}</p>
            <p class="info-detail">Spread Open: {opening_spread} ({opening_spread_odds})</p>
            <p class="info-detail">Total Open: {opening_total} ({openining_total_odds})</p>
            
        </div>
        """, unsafe_allow_html=True)

    return