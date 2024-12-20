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

    # load team records - if it doesn't exist generate it
    team_records_path = dashboard_configs["data"]["team_records"]
    team_records_path = team_records_path.format(week_number=week)

    try:
        team_records = pd.read_csv(team_records_path)
    except:
        team_records = generate_team_records()
        team_records.to_csv(team_records_path)

    with st.container():
        
        # home and away cols
        col1, col2 = st.columns([1, 1])

        # away team info
        away_logo = team_info_config[away_team]["logo"]
        away_name = team_info_config[away_team]["location"] + " " + team_info_config[away_team]["name"]
        away_color = team_info_config[away_team]["color"]
        away_record_info = team_records.loc[team_records["team"] == away_team]

        # display away team
        with col1:
            st.markdown(f"""
            <div class="team">
                <img src="{away_logo}" alt="Away Logo" class="team-logo"/>
                <div class="team-content">
                    <h3 style="background-color: {away_color};">{away_name}</h3>
                    <p class="record"><strong>Record: {away_record_info["Record"].iloc[0]}</strong></p>
                    <p class="stats"><span>🏠 {away_record_info["Home Record"].iloc[0]}</span> | <span>✈️ {away_record_info["Away Record"].iloc[0]} </span></p>
                    <p class="stats"><span>📈 ATS: {away_record_info["ATS"].iloc[0]}</span> | <span>O/U: {away_record_info["OU"].iloc[0]}</span></p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # home team info
        home_logo = team_info_config[home_team]["logo"]
        home_name = team_info_config[home_team]["location"] + " " + team_info_config[home_team]["name"]
        home_color = team_info_config[home_team]["color"]
        home_record_info = team_records.loc[team_records["team"] == home_team]

        # display home team
        with col2:
            st.markdown(f"""
            <div class="team">
                <img src="{home_logo}" alt="Home Logo" class="team-logo"/>
                <div class="team-content">
                    <h3 style="background-color: {home_color};">{home_name}</h3>
                    <p class="record"><strong>Record: {home_record_info["Record"].iloc[0]}</strong></p>
                    <p class="stats"><span>🏠 {home_record_info["Home Record"].iloc[0]}</span> | <span>✈️ {home_record_info["Away Record"].iloc[0]} </span></p>
                    <p class="stats"><span>📈 ATS: {home_record_info["ATS"].iloc[0]}</span> | <span>O/U: {home_record_info["OU"].iloc[0]}</span></p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    return

# TODO: Clean this up
def generate_team_records():
    """
    Generates team records

    Returns:
        team_records (pd.DataFrame): team records
    """
    # query schedule information + scores
    years = [2024]
    df = nfl.import_schedules(years)

    # calculate win loss record
    team_records = {}

    # Iterate through each game
    for _, row in df.iterrows():
        # Extract data for each game
        away_team, home_team = row['away_team'], row['home_team']
        away_score, home_score = row['away_score'], row['home_score']

        # Initialize teams in the dictionary if not already present
        if away_team not in team_records:
            team_records[away_team] = {'home_wins': 0, 'home_losses': 0, 'away_wins': 0, 'away_losses': 0}
        if home_team not in team_records:
            team_records[home_team] = {'home_wins': 0, 'home_losses': 0, 'away_wins': 0, 'away_losses': 0}

        # Determine the winner and update home/away stats
        if away_score > home_score:
            # Away team wins
            team_records[away_team]['away_wins'] += 1
            team_records[home_team]['home_losses'] += 1
        elif home_score > away_score:
            # Home team wins
            team_records[home_team]['home_wins'] += 1
            team_records[away_team]['away_losses'] += 1

    # Convert the dictionary into a DataFrame for better readability
    records_df = pd.DataFrame.from_dict(team_records, orient='index').reset_index()
    records_df.columns = ['team', 'home_wins', 'home_losses', 'away_wins', 'away_losses']
    records_df["Record"] = (records_df["home_wins"] + records_df["home_losses"]).astype(str) + " - " + (records_df["away_wins"] + records_df["away_losses"]).astype(str) 
    records_df["Home Record"] = records_df["home_wins"].astype(str) + " - " + records_df["home_losses"].astype(str) 
    records_df["Away Record"] = records_df["away_wins"].astype(str) + " - " + records_df["away_losses"].astype(str) 

    # calulate ATS record
    df["away_margin"] = df["away_score"] + df["spread_line"] - df["home_score"]
    df["home_margin"] = df["home_score"] - (df["away_score"] + df["spread_line"])

    ats_records = {team: {"ATS Wins": 0, "ATS Losses": 0, "ATS Pushes": 0} for team in pd.unique(df[["away_team", "home_team"]].values.ravel())}
    for _, row in df.iterrows():
        if row["away_margin"] > 0:
            ats_records[row["away_team"]]["ATS Wins"] += 1
        elif row["away_margin"] < 0:
            ats_records[row["away_team"]]["ATS Losses"] += 1
        elif row["away_margin"] == 0:
            ats_records[row["away_team"]]["ATS Pushes"] += 1
        
        if row["home_margin"] > 0:
            ats_records[row["home_team"]]["ATS Wins"] += 1
        elif row["home_margin"] < 0:
            ats_records[row["home_team"]]["ATS Losses"] += 1
        elif row["home_margin"] == 0:
            ats_records[row["home_team"]]["ATS Pushes"] += 1

    ats_df = pd.DataFrame.from_dict(ats_records, orient="index").reset_index()
    ats_df.columns = ["Team", "ATS Wins", "ATS Losses", "ATS Pushes"]
    ats_df["ATS"] = ats_df["ATS Wins"].astype(str) + " - " + ats_df["ATS Losses"].astype(str) + " - " + ats_df["ATS Pushes"].astype(str)

    # calculate O/U record
    df["over_under_result"] = df["total"] - df["total_line"]
    ou_records = {team: {"Over": 0, "Under": 0, "Push": 0} for team in pd.unique(df[["away_team", "home_team"]].values.ravel())}
    for _, row in df.iterrows():
        if row["over_under_result"] > 0:
            ou_records[row["away_team"]]["Over"] += 1
        elif row["over_under_result"] < 0:
            ou_records[row["away_team"]]["Under"] += 1
        elif row["over_under_result"] == 0:
            ou_records[row["away_team"]]["Push"] += 1
        
        if row["over_under_result"] > 0:
            ou_records[row["home_team"]]["Over"] += 1
        elif row["over_under_result"] < 0:
            ou_records[row["home_team"]]["Under"] += 1
        elif row["over_under_result"] == 0:
            ou_records[row["home_team"]]["Push"] += 1

    ou_df = pd.DataFrame.from_dict(ou_records, orient="index").reset_index()
    ou_df.columns = ["Team", "Over", "Under", "Push"]
    ou_df["OU"] = ou_df["Over"].astype(str) + " - " + ou_df["Under"].astype(str) + " - " + ou_df["Push"].astype(str)

    # concat data
    team_records = pd.concat([records_df, ats_df, ou_df], axis = 1).loc[:, ["team", "Record", "Home Record", "Away Record", "ATS", "OU"]]

    return team_records