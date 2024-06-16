import plotly.express as px
from unidecode import unidecode


def bar_chart(df, target_var_column, names_column_name, x_axis_label):
    # Get the selected target_var_column values
    target_var = df[[names_column_name, target_var_column]]
    target_var[target_var_column] = target_var[target_var_column].map(lambda x: unidecode(x.capitalize().strip()) if isinstance(x, str) else x)

    # Prepare the data for plotting
    score_counts = target_var.groupby(target_var_column).agg({
        'Naam': lambda x: ','.join(x),
        target_var_column: 'count'
    }).rename(columns={target_var_column: 'count'}).reset_index()

    # Plotting the bar chart with Plotly
    fig = px.bar(
        score_counts,
        x=target_var_column,
        y='count',
        hover_data=['Naam'],
        labels={target_var_column: x_axis_label, 'count': 'Aantal'},
        title=f'Verdeling voorspellingen {target_var_column}'
    )
    fig.update_xaxes(tickangle=90)

    return fig
