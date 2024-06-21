import pandas as pd
import streamlit as st


st.title('Tests')

df = pd.read_excel("data/Jorrit.xlsx")
st.dataframe(df)
