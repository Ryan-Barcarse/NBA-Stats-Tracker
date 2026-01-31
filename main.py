import streamlit as st
from editor import overall_stats, season_stats, render_accolades
from data import find_id, find_team_id, award, player_info, get_team_name
from nba_api.stats.static import players

def player_header(id):
    """
    Displays the image of the player, player common stats, and the player's team logo
    if availiable.
    """
    left, col2, right = st.columns([2, 3, 2])
    player_image= f"https://cdn.nba.com/headshots/nba/latest/1040x760/{id}.png"
    team_id = find_team_id(id)

    team_image = None # prevents UnboundLocalError for players without a valid team

    if team_id is None:
        st.warning("Team logo not available for this player.")
    else:
        team_image = f"https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg"
        
    with left:

        st.image(player_image, width=220)
    


    with col2:
        player_common_info = player_info(id)
        from_year = player_common_info.loc[0, "FROM_YEAR"]
        to_year = player_common_info.loc[0, "TO_YEAR"]
        height = player_common_info.loc[0, "HEIGHT"]
        weight = player_common_info.loc[0, "WEIGHT"]
        position = player_common_info.loc[0, "POSITION"]
        team = get_team_name(team_id)
        birth = player_common_info.loc[0, "BIRTHDATE"]

        st.markdown(
            f"""
            <div style="
                padding:16px;
                border-radius:12px;
                font-size:12px;
                line-height:1.7;
            ">
                <div><b>Team:</b> {team}</div>
                <div><b>Career:</b> {from_year} – {to_year}</div>
                <div><b>Born:</b> {birth}</div>
                <div><b>Position:</b> {position}</div>
                <div><b>Height:</b> {height}</div>
                <div><b>Weight:</b> {weight}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        if team_image:
            st.image(team_image, width=100,)

def search_func(toggle):
    """
    Determines what players arer displayed depending on if the toggle
    is returning a True or False Value.
    """
    all_players = players.get_players()
    if toggle == True:
        names = [p["full_name"] for p in all_players if p["is_active"]]
    else:
        names = [p["full_name"] for p in all_players]
    search = st.selectbox("Player Name", names, index=None, placeholder="Select")
    if search is not None:
        pid = find_id(search)
        if not search:
            return  
        if search and (pid != None):
            return pid
    
def main():
    """
    Main entry point for the Streamlit application.
    Handles user input, data retrieval, and UI rendering.
    """
    # Page Header ----------------------
    st.logo("https://static.vecteezy.com/system/resources/previews/027/127/440/original/nba-logo-nba-icon-transparent-free-png.png",  size="large")
    st.title("""NBA Player Stats Tracker""")
    st.subheader("""Made by Ryan Barcarse 
    Version 1.2.0""")
    st.divider()

    # Player search --------------------
    on = st.toggle("Current players")
    id = search_func(on)

    # Player stats display -------------
    if id is not None:
        player_header(id)

        if award(id).empty == False:
            top6 = award(id)["Display"].head(6).tolist()
            all_awards = award(id)["Display"].tolist()
            with st.container(border=True):
                st.subheader("Accolades")
                render_accolades(top6, cols=3)

            with st.expander("Show all"):
                render_accolades(all_awards, cols=3)

        st.dataframe(overall_stats(id), hide_index=True)
        table = overall_stats(id).drop_duplicates(subset="SEASON")

        # Season selection ------------
        sselect = []
        for i in table["SEASON"]:
            sselect.append(i) 

        date = st.selectbox(label="Choose a Season", options=sorted(sselect, reverse=True), index=None, placeholder="Select")

        if date is not None:
            df = season_stats(id, date)

            avg_pts = df["PTS"].mean().round(1)
            avg_reb = df["REB"].mean().round(1)
            avg_ast = df["AST"].mean().round(1)

            if "FG%" in df.columns:
                fg_avg = df["FG%"].mean().round(1)
                st.header(f"PTS: {avg_pts} REB: {avg_reb} AST: {avg_ast} FG%: {fg_avg}", divider="red")
            else:
                st.warning("Some data are unavailable for some older NBA seasons")
                st.header(f"PTS: {avg_pts} REB: {avg_reb} AST: {avg_ast}", divider="red")

            st.dataframe(df, hide_index=True)


if __name__ == "__main__":
    main()