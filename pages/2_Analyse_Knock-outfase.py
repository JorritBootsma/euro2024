from pathlib import Path

import pandas as pd
import streamlit as st

from utils.general import get_match_cols
from utils.plotters import bar_chart

st.title('Verdeling voorspellingen Knockout')

dict_for_sorting = {
    "R16": "a",
    "R8": "b",
    "R4": "c",
    "R2": "d",
}

try:
    df = pd.read_csv("data/resultaten_knockoutfase.csv")
    match_cols = get_match_cols(df)
    match_cols.sort(key=lambda x: dict_for_sorting[x.split()[0]])
    df["Naam"] = df["filename"].map(lambda x: Path(x).stem)
    name_column = "Naam"

    # Dropdown menu for match selection
    match = st.selectbox('Select a match:', match_cols)
    first_in_standings = st.selectbox('Highlight de score van:', df[name_column].dropna().tolist(), index=None)
    score_of_first_in_standings = None
    if first_in_standings:
        score_of_first_in_standings = df[df[name_column] == first_in_standings][match].values[0]

    fig = bar_chart(df, match, names_column_name=name_column, x_axis_label="Score", score_of_first_in_standings=score_of_first_in_standings)
    st.plotly_chart(fig)
except FileNotFoundError:
    st.error("Er zijn nog geen voorspellingen voor de knock-outfase geupload.")