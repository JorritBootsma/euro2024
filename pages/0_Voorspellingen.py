import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px

from utils.plotters import bar_chart
from utils.general import get_match_cols

df = pd.read_excel("EuroMaster.xlsm")
match_cols = get_match_cols(df)

df_match_scores = df[match_cols].dropna()
# names = df["Naam"].dropna()

# Streamlit application
st.title('Verdeling voorspellingen')

# Dropdown menu for match selection
match = st.selectbox('Select a match:', match_cols)

fig = bar_chart(df, match, 'Naam')
st.plotly_chart(fig)