import pandas as pd
import streamlit as st

from utils.general import get_question_cols
from utils.plotters import bar_chart

st.title('Verdeling vragen')

df = pd.read_excel("EuroMaster.xlsm")

questions = get_question_cols(df)

question = st.selectbox('Selecteer een vraag:', questions)

first_in_standings = st.selectbox('Highlight de score van:', df["Naam"].dropna().tolist(), index=None)
score_of_first_in_standings = None
if first_in_standings:
    score_of_first_in_standings = df[df["Naam"] == first_in_standings][question].values[0]

fig = bar_chart(df.iloc[:63], question, 'Naam', x_axis_label="Antwoorden", score_of_first_in_standings=score_of_first_in_standings)
st.plotly_chart(fig)
