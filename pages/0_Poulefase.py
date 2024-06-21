import pandas as pd
import streamlit as st

from utils.plotters import bar_chart
from utils.general import get_match_cols

df = pd.read_excel("EuroMaster.xlsm")
match_cols = get_match_cols(df)

df_match_scores = df[match_cols].dropna()

# Streamlit application
st.title('Verdeling voorspellingen')

# Dropdown menu for match selection
match = st.selectbox('Select a match:', match_cols)
first_in_standings = st.selectbox('Highlight de score van:', df["Naam"].dropna().tolist(), index=None)
score_of_first_in_standings = None
if first_in_standings:
    score_of_first_in_standings = df[df["Naam"] == first_in_standings][match].values[0]

fig = bar_chart(df, match, names_column_name="Naam", x_axis_label="Score", score_of_first_in_standings=score_of_first_in_standings)
st.plotly_chart(fig)