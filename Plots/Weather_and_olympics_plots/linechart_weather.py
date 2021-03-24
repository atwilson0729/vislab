import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CVS file from the Datasets folder
df = pd.read_csv('../../Datasets/Weather2014-15.csv')
df['Date'] = pd.to_datetime(df['date'])

# Preparing data
data = [go.Scatter(x=df['Date'], y=df['actual_max_temp'], mode='lines', name='actual_max_temp')]

# Preparing layout
layout = go.Layout(title='Actual Max temp from 2014-2015',
                   xaxis_title="Date", yaxis_title="Max Temp")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='linechart.html')
#complete