import streamlit as st
import pandas as pd

# local imports
from src.utils import streamlit_css

def game_lines(
    away_team: str,
    home_team: str,
    week: int,
    dashboard_configs: dict
):
    """
    Displays game line information including:
        * Opening Spread
        * Opening Total
        * Current Spread (TODO)
        * Current Total (TODO)
     
    Args:
        away_team (str): away team
        home_team (str): home team
        week (int): week chosen by user
        dashboard_configs (dict): dictionary with inputs/params for app
    """
    # stremalit css
    streamlit_css("css/game_lines.css")

    # load game line information
    game_lines_path = dashboard_configs["data"]["game_lines"]
    game_lines = pd.read_excel(game_lines_path, sheet_name=f"Week {week}")

    # filter to game
    game_lines = game_lines.loc[
        (game_lines["Away"] == away_team) &
        (game_lines["Home"] == home_team), :]
    
    # opening lines
    opening_spread = game_lines["Spread"].iloc[0]
    opening_spread_odds = game_lines["Spread Odds"].iloc[0]

    opening_total = game_lines["Total"].iloc[0]
    openining_total_odds = game_lines["Total Odds"].iloc[0]

    # TODO: add preseason spread
    pre_spread = ""
    pre_total = ""

    # TODO: add current spread
    current_spread = ""
    current_spread_odds = ""

    current_total = ""
    current_total_odds = ""

    st.markdown(f"""
        <div class="game-line compact">
            <table>
                <thead>
                    <tr>
                        <th> </th>
                        <th>Spread</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Opening</td>
                        <td>{opening_spread} ({opening_spread_odds})</td>
                        <td>{opening_total} ({openining_total_odds})</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    return