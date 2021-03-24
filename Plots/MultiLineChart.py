import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/CoronaTimeSeries.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Preparing data
# creates three plotly graph objects for the multiple lines
# all three have x-axis as the date in a pandas df
# First obj has y-axis of number of deaths as y axis
# second obj has y axis of number of recovered cases
# Third obj has a y-axis of number of unrecovered cases
# all three graph objects are stored in a list
trace1 = go.Scatter(x=df['Date'], y=df['Death'], mode='lines', name='Death')
trace2 = go.Scatter(x=df['Date'], y=df['Recovered'], mode='lines', name='Recovered')
trace3 = go.Scatter(x=df['Date'], y=df['Unrecovered'], mode='lines', name='Unrecovered')
data = [trace1, trace2, trace3]

# Preparing layout
layout = go.Layout(title='Corona Virus Death and Recovered Cases From 2020-01-22 to '
                         '2020-03-17', xaxis_title="Date", yaxis_title="Number of cases")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='multilinechart')