import itertools

import pandas as pd
import streamlit as st

st.title("Poulefase")

uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    first = True
    for uploaded_file in uploaded_files:
        # Read each Excel file
        filename = uploaded_file.name
        euro_data = pd.read_excel(uploaded_file)

        # Display the Input Excel as DataFrame
        # st.write(f"DataFrame from the uploaded file: {uploaded_file.name}")
        # st.dataframe(euro_data)

        match_row_indices = [11, 16, 21, 26, 31, 38]
        score_row_indices = [12, 17, 22, 27, 32, 39]
        matches = [euro_data.iloc[row_index][:18].dropna().to_list() for row_index in match_row_indices]
        scores = [euro_data.iloc[row_index][:18].dropna().to_list() for row_index in score_row_indices]

        matches = list(itertools.chain.from_iterable(matches))
        scores = list(itertools.chain.from_iterable(scores))

        # Create column names by pairing letters
        column_names = [f"{matches[i]}-{matches[i + 1]}" for i in range(0, len(matches), 2)]
        row_values = [f"{scores[i]}-{scores[i + 1]}" for i in range(0, len(scores), 2)]

        column_names = ["filename"] + column_names
        row_values = [filename] + row_values

        if first:
            # Create the Match Scores DataFrame
            result_df = pd.DataFrame([row_values], columns=column_names)
            # Create the Standings DataFrame
            euro_data.iloc[1, 0] = filename
            standings_df = euro_data.iloc[1:5, [0, 1, 4, 7, 10, 13, 16]]
            empty_row = pd.DataFrame([[None] * len(standings_df.columns)], columns=standings_df.columns)
            standings_df = pd.concat([standings_df, empty_row], ignore_index=True)
            # Keep track of having processed the first file
            first = False
        else:
            # Append the Match Scores DataFrame
            result_df = pd.concat([result_df, pd.DataFrame([row_values], columns=column_names)], ignore_index=True)
            # Append the Standings DataFrame
            euro_data.iloc[1, 0] = filename
            empty_row = pd.DataFrame([[None] * len(standings_df.columns)], columns=standings_df.columns)
            standings_df = pd.concat([standings_df, euro_data.iloc[1:5, [0, 1, 4, 7, 10, 13, 16]], empty_row], ignore_index=True)

    standings_df.columns = ["Filename", "Group A", "Group B", "Group C", "Group D", "Group E", "Group F"]

    # Display the Match Scores DataFrame
    st.write("CSV file containing scores of individual matches:")
    st.dataframe(result_df)
    # Display the Standings DataFrame
    st.write("CSV file containing standings after Poule Stage:")
    st.dataframe(standings_df)

    # Doesn't work in the deployed app:
    # st.button(
    #     "Save to Excel",
    #     on_click=lambda: result_df.to_excel("euro_data.xlsx", index=False)
    # )


