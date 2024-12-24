import pandas as pd
import streamlit as st

# local imports
from src.utils import  streamlit_css, load_data

def bets(
    away_team: str,
    home_team: str,
    week: int,
    dashboard_configs: dict
):
    """
    Displays bets that I've placed for the game
    
    Args:
        away_team (str): away team
        home_team (str): home team
        week (int): week
        dashboard_configs (dict): dictionary with inputs/params for app
    """
    # streamlit custom CSS
    streamlit_css("css/bets.css")

    # load in betting data
    betting_data_path = st.secrets["data"]["bets"]
    betting_data = load_data(betting_data_path, sheet_name=f"Week {week}")

    # filter to game
    betting_data[['away_team', 'home_team']] = betting_data['Game'].str.split(' @ ', expand=True)
    game_betting_data = betting_data.loc[
        (betting_data['home_team'] == home_team) & (betting_data['away_team'] == away_team), :
    ]

    # calculate win/loss
    game_betting_data['Earnings'] = game_betting_data.apply(lambda row: row['Payout'] if row['Result'] == 'Win' else (-row['Wager'] if not pd.isna(row['Result']) else 0), axis=1)
    net_gain = game_betting_data['Earnings'].sum()
    net_gain_color = "#00FF00" if net_gain > 0 else "#ff4c4c"
    net_gain = f"${net_gain:.2f}" if net_gain > 0 else f"-${abs(net_gain):.2f}"

    net_wager = game_betting_data['Wager'].sum()
    net_wager = f"${net_wager:.2f}"

    net_payout = game_betting_data['Payout'].sum()
    net_payout = f"${net_payout:.2f}"

    # formatting
    game_betting_data.loc[:, "Wager"] = game_betting_data["Wager"].apply(lambda x: f"${x:.2f}")
    game_betting_data.loc[:, "Payout"] = game_betting_data["Payout"].apply(lambda x: f"${x:.2f}")
    game_betting_data.loc[:, "Odds"] = game_betting_data["Odds"].apply(lambda x: int(x))
    game_betting_data.loc[:, "Odds"] = game_betting_data["Odds"].apply(lambda x: "+" + str(x) if x > 0 else str(x))

    # sort
    game_betting_data = game_betting_data.sort_values(by="Description", ascending=False)

    # subset cols
    title_html = f"""
    <h2 style="text-align: center; color: white; margin-bottom: 20px;">
        Bets
    </h2>
    """

    table_html = f"""
        <table class="comparison-table">
        <thead>
            <tr>
                <th>Description</th>
                <th>Wager</th>
                <th>Payout</th>
                <th>Result</th>
            </tr>
        </thead>
        <tbody>
        """
    
    for _, row in game_betting_data.iterrows():

        if pd.isna(row["Result"]):
            result = " "
            color = "#000000"
        else:
            result = row["Result"]

            if result == "Win":
                color = "#00FF00"
            elif result == "Loss":
                color = "#ff4c4c"
            else:
                color = "#FFFF99"


        table_html += (
            f"<tr>"
                f"<td>{row['Description']} ({row['Odds']})</td>"
                f"<td>{row['Wager']}</td>"
                f"<td>{row['Payout']}</td>"
                f"<td style='background-color: {color}; color: black;'>{result}</td>"
            f"</tr>"
        )

    table_html += (
            f"<tr>"
                f"<td>RESULT</td>"
                f"<td> {net_wager} </td>"
                f"<td> </td>"
                f"<td style='background-color: {net_gain_color}; color: black;'>{net_gain}</td>"
            f"</tr>"
        )
        
    st.markdown(title_html, unsafe_allow_html=True)
    st.markdown(table_html, unsafe_allow_html=True)

