from nba_api.stats.endpoints import playercareerstats, playergamelog, playerawards, commonplayerinfo
from nba_api.stats.static import players, teams
import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600, show_spinner="Loading...")
def find_id(search):
    """
    Passes through a player name and finds the Id 
    associated with them.
    """
    matches = players.find_players_by_full_name(search)
    if matches:
        return matches[0]["id"]
    return None

@st.cache_data(ttl=3600, show_spinner="Loading...")
def display_stats(ID, SZ=None):
    """
    Returns the data of a specific player's stats based off player id.
    """
    if SZ is None:
        return playercareerstats.PlayerCareerStats(player_id=ID).get_data_frames()[0]
    else:
        return playergamelog.PlayerGameLog(player_id=ID, season=SZ).get_data_frames()[0]


@st.cache_data(ttl=3600, show_spinner="Loading...")
def sort_season(ID):
    """
    Reverses season order, prioritizing newer seasons.
    """
    sort_season = {}
    for i in ID:
        season = playercareerstats.PlayerCareerStats(player_id=i).get_data_frames()[0]

        all_season = season["SEASON_ID"].dropna().tolist()
        all_season.sort(key=lambda s: int(s[:4]), reverse=True)

        sort_season[i] = all_season
    return sort_season

@st.cache_data(ttl=3600, show_spinner="Loading...")
def find_team_id(ID):
    """
    Uses player id to find the last team played for by the player.
    """
    df = display_stats(ID)
    if df is None or df.empty:
        return None
    TID = df[df["TEAM_ID"] != 0]
    if df.empty:
        return None

    return TID.iloc[-1]["TEAM_ID"]   

@st.cache_data(ttl=3600, show_spinner="Loading...")
def award(ID):
    """
    Displays and filters through player awards and combines
    all important awards, ordering from most to least.
    """
    accolades = playerawards.PlayerAwards(player_id=ID).get_data_frames()[0]
    counts = (
        accolades["DESCRIPTION"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    important_awards = [
    "NBA Champion",
    "NBA Most Valuable Player",
    "NBA Finals Most Valuable Player",
    "NBA All-Star",
    "All-NBA",
    "All-Defensive Team",
    "NBA Rookie of the Year",
    "All-Rookie Team",
    "Olympic Gold Medal",
    "Olympic Silver Medal",
    "Olympic Bronze Medal",
    "NBA All-Star Most Valuable Player",
    "Defensive Player of the Year",
    "Sixth Man of the Year",
    ]

    counts.columns = ["Award", "Count"]
    counts["Display"] = counts["Award"] + " (" + counts["Count"].astype(str) + "x)"
    counts = counts.sort_values("Count", ascending=False)
    counts = counts[counts["Award"].isin(important_awards)]


    return counts

@st.cache_data(ttl=3600, show_spinner="Loading...")
def player_info(ID):
    """
    Grabs certain columns from the CommonPlayerInfo
    """
    df = commonplayerinfo.CommonPlayerInfo(player_id=ID).get_data_frames()[0]

    #Changes data into easy to read values 
    df["BIRTHDATE"] = (
        pd.to_datetime(df["BIRTHDATE"])
        .dt.strftime("%B %d, %Y")
    )

    sort = [
        "HEIGHT",
        "WEIGHT",
        "BIRTHDATE",
        "POSITION",
        "TEAM_NAME",
        "FROM_YEAR",
        "TO_YEAR"
    ]
    info = df[sort]
    

    return info
        


@st.cache_data(ttl=3600, show_spinner="Loading...")
def get_team_name(team_id):
    """
    Finds current team name using the team id
    """
    team = teams.find_team_name_by_id(team_id)
    if team:
        return team["full_name"]
    return "Unknown Team"




   

            