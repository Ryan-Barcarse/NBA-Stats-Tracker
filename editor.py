from data import display_stats
import streamlit as st
import pandas as pd

def overall_stats(player):
    """
    Filters though given dataframe and only 
    displays chosen/renamed columns for the overall stats.
    """
    info = display_stats(player)
    columns = [
            "SEASON_ID",
            "TEAM_ABBREVIATION",
            "GP",
            "PTS",
            "AST",
            "REB"
        ]
    
    info = info[columns]

    info = info.rename(columns={
        "SEASON_ID": "SEASON",
        "TEAM_ABBREVIATION": "TEAM"
    })
    return info

def season_stats(player, season):
    """
    Filters though given dataframe and only 
    displays chosen/renamed columns for the season stats.
    """
    info = display_stats(player, season)
    columns = [
            "GAME_DATE",
            "MATCHUP",
            "WL",
            "MIN",
            "FG_PCT",
            "REB",
            "AST",
            "BLK",
            "STL",
            "PF",
            "TOV",
            "PTS"

        ]
    
    info = info[columns]

    info = info.rename(columns={
        "GAME_DATE": "DATE",
        "MATCHUP": "OPP",
        "WL": "RESULT",
        "FG_PCT": "FG%",
        "TOV": "TO"
    })

    start_year = int(season[:4])

    if start_year > 1985: #Safety net for older NBA statistic errors with rounding
        info["FG%"] = pd.to_numeric(info["FG%"], errors="coerce")
        info["FG%"] = (info["FG%"] * 100).round(1)
    else:
        info = info.drop(columns=["FG%"])

    return info

def render_accolades(accolades_list, cols=3):
    """
    Displays a list of player accolades in a grid layout using Streamlit columns.

    Parameters:
        accolades_list (list): List of formatted accolade strings to display.
        cols (int): Number of columns per row.
    """
    rows = (len(accolades_list) + cols - 1) // cols
    idx = 0
    for _ in range(rows):
        c = st.columns(cols)
        for j in range(cols):
            if idx >= len(accolades_list):
                break
            c[j].markdown(f"- {accolades_list[idx]}")
            idx += 1
