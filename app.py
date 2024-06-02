import itertools

import pandas as pd
import streamlit as st

uploaded_files = st.file_uploader("Choose Excel files", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    first = True
    for uploaded_file in uploaded_files:
        # Read each Excel file
        filename = uploaded_file.name
        euro_data = pd.read_excel(uploaded_file)

        # Display the DataFrame
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
            # Create the DataFrame
            result_df = pd.DataFrame([row_values], columns=column_names)
            first = False
        else:
            # Append the DataFrame
            result_df = pd.concat([result_df, pd.DataFrame([row_values], columns=column_names)], ignore_index=True)
            # result_df = result_df.append(pd.DataFrame([row_values], columns=column_names))

    # Display the DataFrame
    st.write("DataFrame from the uploaded files:")
    st.dataframe(result_df)

    # st.button(
    #     "Save to Excel",
    #     on_click=lambda: result_df.to_excel("euro_data.xlsx", index=False)
    # )
