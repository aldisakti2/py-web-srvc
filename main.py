import streamlit as st #lib to build web app
import pandas as pd #lib to handle dataframe and webscrapping
import matplotlib.pyplot as plt #to create plot
import plotly.express as px
from datetime import date as dt #for get most recent year
import base64   #to handle data download (csv file)

st.set_page_config(page_title="NBA STATS",layout="wide")
st.title("VISUALIZATION DATA USING STREAMLIT")
expender_bar = st.expander("About")
expender_bar.markdown("""
            * ***Data Source:*** [Basketball-reference.com](https://www.basketball-reference.com/)  
            * ***Anggota Kelompok Tugas Besar Pemrograman Fungsional:***
            1. Aldi (21102270)
            2. Agyl (21102291)
            3. Reynant (21102326)        
            """)
st.markdown("""
            ---
            """)

# sidebar year
st.sidebar.header('NBA STATS')
st.sidebar.subheader('`Filter` Here') 
today = dt.today()
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1970,today.year+1))))  

# web scraping
# data pre processing

@st.cache(allow_output_mutation=True)
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
#st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
#st.write('Total of Players: ', df_rows) 
st.dataframe(df_selected_team)


# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# visualization
#1 bar chart
playerstats['G'] = pd.to_numeric(playerstats['G'], errors='coerce')
x1 = (playerstats.nlargest(10, ['G']))

playerstats['PTS'] = playerstats['PTS'].astype(float)
x2 = playerstats.sort_values(['PTS'],ascending=False).head(10)


fig_x1 = px.bar(
    x1,
    x="Player",
    y='G',
    orientation="v",
    color_discrete_sequence=["#0083B8"] * len(x1),
    template="plotly_white",
)

fig_x1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    barmode='group'
)

fig_x2 = px.bar(
    x2,
    x="Player",
    y='PTS',
    orientation="v",
    color_discrete_sequence=["#0083B8"] * len(x2),
    template="plotly_white",
)

fig_x2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    barmode='group'
)

if st.button('TOP 10 MOST PLAYED PLAYER'):
    st.header(f'Top 10 Most Played Player {selected_year}')
    st.plotly_chart(fig_x1, theme="streamlit", use_container_width=True)
    
st.markdown("""---""")

if st.button('TOP 10 MOST SCORED PLAYER'):
    st.header(f'Top 10 Most Played Player {selected_year}')
    st.plotly_chart(fig_x2, theme="streamlit", use_container_width=True) 
            
st.markdown("""---""")

###hide streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
"""
st.markdown(hide_st_style, unsafe_allow_html=True)