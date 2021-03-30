import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/CoronavirusTotal.csv')
df2 = pd.read_csv('../Datasets/CoronaTimeSeries.csv')
df3 = pd.read_csv('../Datasets/Weather2014-15.csv')
df4 = pd.read_csv('../Datasets/Olympic2016Rio.csv')


app = dash.Dash()

# Bar chart data
barchart_df = df4[df4['NOC'] != 'Portugal(POR)']
barchart_df = barchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.groupby(['NOC'])['Gold'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Gold'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['NOC'], y=barchart_df['Gold'])]

# Stack bar chart data
stackbarchart_df = df4.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
stackbarchart_df['Total'] = stackbarchart_df['Gold'] + stackbarchart_df['Silver'] + stackbarchart_df[
    'Bronze']
stackbarchart_df = stackbarchart_df.groupby(['NOC']).agg(
    {'Total': 'sum', 'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
stackbarchart_df = stackbarchart_df.sort_values(by=['Total'], ascending=[False]).head(20).reset_index()
trace1_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Gold'], name='Gold',
                              marker={'color': '#CD7F32'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Silver'], name='Silver',
                              marker={'color': '#9EA0A1'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Bronze'], name='Bronze',
                              marker={'color': '#FFD700'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line Chart
line_df = df3
line_df['date'] = pd.to_datetime(line_df['date'])
data_linechart = [go.Scatter(x=line_df['date'], y=line_df['average_max_temp'], mode='lines', name='average_max_temp')]

# Multi Line Chart
multiline_df = df3
multiline_df['date'] = pd.to_datetime(multiline_df['date'])
trace1_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['average_max_temp'], mode='lines', name='average_max_temp')
trace2_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['average_min_temp'], mode='lines', name='average_min_temp')
trace3_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_mean_temp'], mode='lines', name='actual_mean_temp')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
bubble_df['Unrecovered'] = bubble_df['Confirmed'] - bubble_df['Deaths'] - bubble_df['Recovered']
bubble_df = bubble_df[(bubble_df['Country'] != 'China')]
bubble_df = bubble_df.groupby(['Country']).agg(
    {'Confirmed': 'sum', 'Recovered': 'sum', 'Unrecovered': 'sum'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['Recovered'],
               y=bubble_df['Unrecovered'],
               text=bubble_df['Country'],
               mode='markers',
               marker=dict(size=bubble_df['Confirmed'] / 200, color=bubble_df['Confirmed'] / 200, showscale=True))
]

# Heatmap
data_heatmap = [go.Heatmap(x=df2['Day'],
                           y=df2['WeekofMonth'],
                           z=df2['Recovered'].values.tolist(),
                           colorscale='Jet')]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization Using Python', style={'textAlign': 'center'}),
    html.Div('A series of interactive charts', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents a series of datasets about the olympics and weather.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a continent', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-continent',
        options=[
            {'label': 'Asia', 'value': 'Asia'},
            {'label': 'Africa', 'value': 'Africa'},
            {'label': 'Europe', 'value': 'Europe'},
            {'label': 'North America', 'value': 'North America'},
            {'label': 'Oceania', 'value': 'Oceania'},
            {'label': 'South America', 'value': 'South America'}
        ],
        value='Europe'
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the Olympic 2016 gold medals.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Gold medals by country',
                                      xaxis={'title': 'NOC'}, yaxis={'title': 'Gold'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represents the medals earned during the 2016 olympics by country.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Medals earned by country in the 2016 olympics',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represents the average max temp.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Weather statistics from 2014-2015',
                                      xaxis={'title': 'date'}, yaxis={'title': 'Number of cases'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represents the average max average min and average mean temp'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Weather statistics from 2014-2015',
                      xaxis={'title': 'date'}, yaxis={'title': 'temp'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represent the Corona Virus recovered and under treatment of all reported countries except China.'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Corona Virus Confirmed Cases',
                                      xaxis={'title': 'Recovered Cases'}, yaxis={'title': 'under Treatment Cases'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat map represent the Corona Virus recovered cases of all reported cases per day of week and week of month.'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='Corona Virus Recovered Cases',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Week of Month'})
              }
              )
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-continent', 'value')])
def update_figure(selected_continent):
    filtered_df = df1[df1['Continent'] == selected_continent]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['Country'])['Confirmed'].sum().reset_index()
    new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=new_df['Country'], y=new_df['Confirmed'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Corona Virus Confirmed Cases in '+selected_continent,
                                                                   xaxis={'title': 'Country'},
                                                                   yaxis={'title': 'Number of confirmed cases'})}


if __name__ == '__main__':
    app.run_server()
