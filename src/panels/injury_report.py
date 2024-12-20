import streamlit as st
import pandas as pd

# local imports
from src.utils import streamlit_css

def injury_report(
    away_team: str,
    home_team: str,
    week: int,
    dashboard_configs: dict
):
    """
    Function to display injury report for both teams for the week.

    Args:
        away_team (str): away team
        home_team (str): home team
        dashboard_configs (dict): dictionary with inputs/params for app
    """
    # streamlit custom CSS
    streamlit_css("css/injury_report.css")

    # load injury report
    injury_report_data_path = dashboard_configs["data"]["injury_report"]
    injury_report_data_path = injury_report_data_path.format(week_number=week)
    injury_report_data = pd.read_excel(injury_report_data_path, sheet_name=f"Week {week}")

    # filter by team
    away_injury_report = injury_report_data[injury_report_data["Team"] == away_team]
    home_injury_report = injury_report_data[injury_report_data["Team"] == home_team]

    # filter and cast
    away_injury_report = away_injury_report.loc[:, ["Player", "Position", "Status", "Ruling"]].astype(str)
    home_injury_report = home_injury_report.loc[:, ["Player", "Position", "Status", "Ruling"]].astype(str)

    # sort
    away_injury_report = away_injury_report.sort_values(by="Position", ascending=True)
    home_injury_report = home_injury_report.sort_values(by="Position", ascending=True)

    st.markdown(render_table(away_injury_report, away_team), unsafe_allow_html=True)
    st.markdown(render_table(home_injury_report, home_team), unsafe_allow_html=True)


def render_table(data: pd.DataFrame, team_name: str):
    if data.empty:
        return f"<p style='text-align: center; font-size: 1.1rem;'>No injuries reported for {team_name}.</p>"
    
    table_html = f"""
    <div class='table-container'>
        <h3>{team_name}</h3>
        <table>
            <thead>
                <tr>
                    {"".join(f"<th>{col}</th>" for col in data.columns)}
                </tr>
            </thead>
            <tbody>
    """
    for _, row in data.iterrows():
        table_html += "<tr>"
        for col in data.columns:
            cell_value = row[col]
            if col == "Ruling":
                if cell_value == "In":
                    bg_color = "Green"
                elif cell_value == "Out":
                    bg_color = "red"
                else:
                    cell_value = "Monitor"
                    bg_color = "black"
                color = "white"  # Text color for readability
                table_html += (
                    f"<td style='padding: 4px; border: 1px solid #666; text-align: center; "
                    f"background-color: {bg_color}; color: {color};'>{cell_value}</td>"
                )
            else:
                table_html += f"<td>{cell_value}</td>"
        table_html += "</tr>"
    
    table_html += "</tbody></table></div>"
    return table_html