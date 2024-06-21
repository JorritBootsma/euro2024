import plotly.express as px
from unidecode import unidecode

import streamlit as st

def simplify_string(x):
    return unidecode(x.capitalize().strip()) if isinstance(x, str) else x


def bar_chart(df, target_var_column, names_column_name, x_axis_label, score_of_first_in_standings=None):
    # Get the selected target_var_column values
    target_var = df[[names_column_name, target_var_column]]
    target_var[target_var_column] = target_var[target_var_column].map(
        simplify_string
    )

    # Prepare the data for plotting
    target_var_counts = target_var.groupby(target_var_column).agg({
        names_column_name: lambda x: ','.join(x),
        target_var_column: 'count'
    }).rename(columns={target_var_column: 'count'}).reset_index()

    if score_of_first_in_standings:
        # Add a column to color the bars based on the first_in_standings column
        target_var_counts['color'] = target_var_counts[target_var_column].apply(lambda x: 'Huidige #1' if x==simplify_string(score_of_first_in_standings) else 'Rest')

    # Plotting the bar chart with Plotly
    fig = px.bar(
        target_var_counts,
        x=target_var_column,
        y='count',
        hover_data=[names_column_name],
        labels={target_var_column: x_axis_label, 'count': 'Aantal', "color": "Legenda"},
        title=f'Verdeling voorspellingen {target_var_column}',
        color='color' if score_of_first_in_standings else None,
        # color_discrete_map={'Current #1': '#d62728', 'Rest': '#1f77b4'} if score_of_first_in_standings else None
    )
    fig.update_xaxes(tickangle=90)

    return fig
