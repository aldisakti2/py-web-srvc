import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="Data Ternak",
                   layout="wide")
st.header('data')
st.subheader('isi data')


##load dataframe

df = pd.read_excel(
    io="data-penumpang-bus-transjakarta-desember-2021.xlsx",
    engine='openpyxl',
    sheet_name='Worksheet',
    usecols='A:F',
    nrows=200,
)

st.dataframe(df)


##Sidebar

    ##filter dataframe

st.sidebar.header("please filter here:")
jenis = st.sidebar.multiselect(
    "select the year:",
    options=df["jenis"].unique(),
    default=df["jenis"].unique()
)

kode_trayek = st.sidebar.multiselect(
    "select the code of route:",
    options=df["kode_trayek"].unique(),
    default=df["kode_trayek"].unique()
)

trayek = st.sidebar.multiselect(
    "select the route:",
    options=df["trayek"].unique(),
    default=df["trayek"].unique()
)

    ##Filter actual dataframe

df_selection = df.query(
    "jenis == @jenis & kode_trayek == @kode_trayek & trayek == @trayek"
)

###show df_selection
    ### st.dataframe(df_selection)

### mainpagee

st.title(":bar_chart: Dashboard")
st.markdown("##")

total_penumpang = int(df_selection["jumlah_penumpang"].sum())
average_penumpang_by_route = round(df_selection["jumlah_penumpang"].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("jumlah penumpang:")
    st.subheader(f"{total_penumpang:,}")

with middle_column:
    st.subheader("rata-rata jumlah penumpang:")
    st.subheader(f"{average_penumpang_by_route:,}")

st.markdown("---")

##jenis by jumlah penumpang
total_penumpang_by_jenis = (
    df_selection.groupby(by=["jenis"]).sum()[["jumlah_penumpang"]].sort_values(by="jumlah_penumpang")
)

fig_total_penumpang_by_jenis = px.bar(
    total_penumpang_by_jenis,
    x="jumlah_penumpang",
    y=total_penumpang_by_jenis.index,
    orientation="h",
    title="<b> jumlah penumpang by jenis </b>",
    color_discrete_sequence=["#0083B8"] * len(total_penumpang_by_jenis),
    template="plotly_white"
)

fig_total_penumpang_by_jenis.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

##trayek by jumlah penumpang
total_penumpang_by_trayek = (
    df_selection.groupby(by=["trayek"]).sum()[["jumlah_penumpang"]].sort_values(by="jumlah_penumpang")
)

fig_jumlah_penumpang_trayek = px.bar(
    total_penumpang_by_trayek,
    x="jumlah_penumpang",
    y=total_penumpang_by_trayek.index,
    orientation="h",
    title="<b> jumlah penumpang by trayek </b>",
    color_discrete_sequence=["#0083B8"] * len(total_penumpang_by_trayek),
    template="plotly_white"
)

fig_jumlah_penumpang_trayek.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

##kode_trayek by jumlah penumpang
total_penumpang_by_kode_trayek = (
    df_selection.groupby(by=["kode_trayek"]).sum()[["jumlah_penumpang"]].sort_values(by="jumlah_penumpang")
)

fig_total_penumpang_by_kode_trayek = px.bar(
    total_penumpang_by_kode_trayek,
    x="jumlah_penumpang",
    y=total_penumpang_by_kode_trayek.index,
    orientation="h",
    title="<b> jumlah penumpang by kode trayek </b>",
    color_discrete_sequence=["#0083B8"] * len(total_penumpang_by_kode_trayek),
    template="plotly_white"
)

fig_total_penumpang_by_kode_trayek.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

left_column,middle_column,right_column = st.columns(3)

left_column.plotly_chart(fig_total_penumpang_by_jenis, use_container_width=True)
middle_column.plotly_chart(fig_jumlah_penumpang_trayek, use_container_width=True)
right_column.plotly_chart(fig_total_penumpang_by_kode_trayek, use_container_width=True)

###hide streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
"""

st.markdown(hide_st_style, unsafe_allow_html=True)
