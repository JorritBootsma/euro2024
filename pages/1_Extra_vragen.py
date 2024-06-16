import pandas as pd
import streamlit as st

from utils.general import get_question_cols
from utils.plotters import bar_chart

st.title('Verdeling vragen')

df = pd.read_excel("EuroMaster.xlsm")

questions = get_question_cols(df)

question = st.selectbox('Select a question:', questions)

fig = bar_chart(df.iloc[:63], question, 'Naam', x_axis_label="Antwoorden")
st.plotly_chart(fig)
