import itertools

import numpy as np
import pandas as pd
import streamlit as st

from configs import configs

st.title("Knock-outfase")

uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)


def get_results_row(data, teams_row_index, team_col_indices, tournament_round=""):
    score_row_index = teams_row_index + 1
    penalties_row_index = teams_row_index + 3
    teams = data.iloc[teams_row_index, team_col_indices]
    goals_scored = data.iloc[score_row_index, team_col_indices]
    penalties_scored = data.iloc[penalties_row_index, team_col_indices]

    matches = [f"{teams[i]}-{teams[i + 1]}" for i in range(0, len(teams), 2)]
    scores = [f"{goals_scored[i]}-{goals_scored[i + 1]}" for i in
                      range(0, len(goals_scored), 2)]
    penalties = [f"{penalties_scored[i]}-{penalties_scored[i + 1]}"
                 if penalties_scored[i] is not np.nan else np.nan
                 for i in range(0, len(penalties_scored), 2)
                 ]
    penalty_columns = [f"(P) {match}" for match in matches]

    column_names = list(itertools.chain(*zip(matches, penalty_columns)))
    column_names = [f"{tournament_round} {column_name}" for column_name in column_names]
    column_names = ["filename"] + column_names
    row_values = [filename] + list(itertools.chain(*zip(scores, penalties)))
    return {column_name: row_value for column_name, row_value in zip(column_names, row_values)}


if uploaded_files:
    first = True
    for uploaded_file in uploaded_files:
        # Read Excel file
        filename = uploaded_file.name
        data = pd.read_excel(uploaded_file)

        # Display the Input Excel as DataFrame
        # st.write(f"DataFrame from the uploaded file: {uploaded_file.name}")
        # st.dataframe(data)

        # Get the results of the R16 matches
        row_values_dict = get_results_row(
            data,
            configs.ROUND16_TEAM_ROW,
            configs.ROUND16_TEAM_COLS,
            tournament_round="R16"
        )
        # Get the results of the quarter final matches
        row_values_dict.update(get_results_row(
            data,
            configs.QFINAL_TEAM_ROW,
            configs.QFINAL_TEAM_COLS,
            tournament_round="R8"
        ))
        # Get the results of the semi final matches
        row_values_dict.update(get_results_row(
            data,
            configs.SEMIFINAL_TEAM_ROW,
            configs.SEMIFINAL_TEAM_COLS,
            tournament_round="R4"
        ))
        # Get the results of the final matches
        row_values_dict.update(get_results_row(
            data,
            configs.FINAL_TEAM_ROW,
            configs.FINAL_TEAM_COLS,
            tournament_round="R2"
        ))

        if first:
            result_df = pd.DataFrame(columns=list(row_values_dict.keys()))
            result_df = pd.concat([result_df, pd.DataFrame([row_values_dict])], ignore_index=True)
            first = False
        else:
            result_df = pd.concat([result_df, pd.DataFrame([row_values_dict])], ignore_index=True)

        # st.dataframe(result_df)

    # Display the Match Scores DataFrame
    st.write("CSV file containing scores of individual matches:")
    st.dataframe(result_df)

    # Save the Match Scores DataFrame as a CSV file
    result_df.to_csv("data/resultaten_knockoutfase.csv", index=False)