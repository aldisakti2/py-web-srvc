import streamlit as st #lib to build web app
import pandas as pd #lib to handle dataframe and webscrapping
import matplotlib.pyplot as plt #to create plot
import plotly.express as px
import base64   #to handle data download (csv file)

st.set_page_config(page_title="NBA STATS",layout="wide")
st.title("VISUALIZATION DATA USING STREAMLIT")
expender_bar = st.expander("About")
expender_bar.markdown("""
            * ***Data Source:*** [Basketball-reference.com](https://www.basketball-reference.com/)  
            * ***Anggota Kelompok Tugas Besar Pemrograman Fungsional:***
            1. Aldi (2110)
            2. Agyl (21102291)
            3. Reynant (2110)        
            """)
st.markdown("""
            ---
            """)

# sidebar year
st.sidebar.header('NBA STATS')
st.sidebar.subheader('`Filter` Here') 
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1970,2021))))  

# web scraping
# data pre processing

@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    #delete
    raw = df.drop(df[df.Age == 'Age'].index) 
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis = 1)
    return playerstats
playerstats = load_data(selected_year) #custom function retrieve nba player stat by selected year

# sidebar team
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team',sorted_unique_team,sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

#slidebar - age
age_unique = sorted(playerstats.Age.unique())
selected_age = st.sidebar.multiselect('Age', age_unique,age_unique)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos)) & (playerstats.Age.isin(selected_age))]
df_rows = len(playerstats.axes[0])

st.header(":basketball: Dashboard")
st.markdown("""
            **Display Plyer Stats of Selected Filter**
            """)
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.write('Total of Players: ', df_rows) 
st.dataframe(df_selected_team)


# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
"""
# visualization
#1 bar chart


total_game_by_team = (
    playerstats.groupby(by=["G"]).sum()[["Tm"]].sort_values(by="Tm")
)

fig_total_game_by_team = px.bar(
    total_game_by_team,
    x = "Tm",
    y = total_game_by_team.index,
    orientation = "h",
    title = "<b> GAME by TEAM </b>",
    color_discrete_sequence=["#0083B8"] * len(total_game_by_team),
    template="plotly_white",
)

fig_total_game_by_team.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    barmode='group'
)

#BAR CHART
if st.button('Bar Chart'):
    st.plotly_chart(fig_total_game_by_team, theme="streamlit", use_container_width=True)
    
"""


