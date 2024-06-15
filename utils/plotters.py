import plotly.express as px


def bar_chart(df, match, names_column_name):
    # Get the selected match scores
    scores = df[[names_column_name, match]]

    # Prepare the data for plotting
    score_counts = scores.groupby(match).agg({
        'Naam': lambda x: ','.join(x),
        match: 'count'
    }).rename(columns={match: 'count'}).reset_index()

    # Plotting the bar chart with Plotly
    fig = px.bar(score_counts, x=match, y='count', hover_data=['Naam'], labels={match: 'Scores', 'count': 'Counts'}, title=f'Verdeling voorspellingen {match}')
    return fig