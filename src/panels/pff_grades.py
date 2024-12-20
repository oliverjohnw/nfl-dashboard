import pandas as pd
import streamlit as st

# local imports
from src.utils import  streamlit_css

def pff_grades(
    away_team: str,
    home_team: str, 
    week: int,
    dashboard_configs: dict
):
    """
    Loads in, formats, and displays data for PFF grades for the two teams in the game.
    
    Args:
        away_team (str): away team
        home_team (str): home team
        week (int): week number
        dashboard_configs (dict): dictionary with inputs/params for app
    """
    # streamlit custom CSS
    streamlit_css("css/pff_grades.css")

    # load in PFF grades
    pff_team_grade_data_path = dashboard_configs["data"]["pff_team_grades"]
    pff_team_grade_data = pd.read_excel(pff_team_grade_data_path, sheet_name=f"Week {week}")

    # filter data
    needed_cols = ["OVER", "OFF", "DEF", "PASS", "PBLK", "RUN", "RBLK", "PRSH", "RDEF", "COV", "TACK"]
    away_data = pff_team_grade_data.set_index("Team").loc[:, away_team].T
    home_data = pff_team_grade_data.set_index("Team").loc[:, home_team].T

    away_data = away_data[needed_cols]
    home_data = home_data[needed_cols]

    # Ensure numeric values
    away_data = away_data.apply(pd.to_numeric, errors="coerce").fillna(0).clip(0, 100)
    home_data = home_data.apply(pd.to_numeric, errors="coerce").fillna(0).clip(0, 100)

    # table cols
    overall_cols = ["OVER", "OFF", "DEF"]
    off_cols = ["PASS", "PBLK", "RUN", "RBLK"]
    def_cols = ["COV", "PRSH", "RDEF", "TACK"]
        
    # display tables
    pff_table(overall_cols, overall_cols, away_team, home_team, away_data, home_data, "Overall")
    pff_table(off_cols, def_cols, away_team, home_team, away_data, home_data, "Away Off")
    pff_table(def_cols, off_cols, away_team, home_team, away_data, home_data, "Home Off")
    
def pff_table(
    away_cols: list,
    home_cols: list, 
    away_team: str, 
    home_team: str, 
    away_data: pd.DataFrame, 
    home_data: pd.DataFrame,
    label: str
):
    """
    Generates table with PFF grades for the two teams.

    Args:
        away_cols (list): list of columns for away team
        home_cols (list): list of columns for home team
        away_team (str): away team
        home_team (str): home team
        away_data (pd.DataFrame): away team data
        home_data (pd.DataFrame): home team data
        label (str): label for table
    """
    # table headers
    if label in ["Overall", "Away Off"]:
        table_html = f"""
        <div class="table-container">
            <table class="comparison-table">
            <thead>
                <tr>
                    <th> </th>
                    <th>{away_team}</th>
                    <th>{home_team}</th>
                </tr>
            </thead>
            <tbody>
        """
    else:
        table_html = f"""
        <div class="table-container">
            <table class="comparison-table">
            <thead>
                <tr>
                    <th> </th>
                    <th>{home_team}</th>
                    <th>{away_team}</th>
                </tr>
            </thead>
            <tbody>
        """

    # team stats
    for i, away_stat in enumerate(away_cols):
        home_stat = home_cols[i]
        away_color = compute_color(away_data[away_stat])
        home_color = compute_color(home_data[home_stat])

        if label in ["Overall", "Away Off"]:
            table_html += (
                f"<tr>"
                f"<td style='color: white'>{away_stat}</td>"
                f"<td style='background-color: {away_color}; color: black;'>{away_data[away_stat]}</td>"
                f"<td style='background-color: {home_color}; color: black;'>{home_data[home_stat]}</td>"
                f"<td style='color: white'>{home_stat}</td>"
                f"</tr>"
            )

        else:
            table_html += (
                f"<tr>"
                f"<td style='color: white'>{home_stat}</td>"
                f"<td style='background-color: {home_color}; color: black;'>{home_data[home_stat]}</td>"
                f"<td style='background-color: {away_color}; color: black;'>{away_data[away_stat]}</td>"
                f"<td style='color: white'>{away_stat}</td>"
                f"</tr>"
            )

    table_html += """
            </tbody>
        </table>
    </div>
    """

    st.markdown(table_html, unsafe_allow_html=True)

    return

def compute_color(value):
    """Returns a background color based on value."""
    value = float(value)
    if value < 50:
        return "#ff4c4c"  # Red
    elif 50 <= value < 60:
        return "#ff6666"  # Light Red
    elif 60 <= value < 70:
        return "#FFD700"  # Light Blue
    elif 70 <= value < 80:
        return "#FFFF99"  # Lighter Blue
    elif 80 <= value < 90:
        return "#99ff99"  # Light Green
    else:
        return "#4caf50"  # Green