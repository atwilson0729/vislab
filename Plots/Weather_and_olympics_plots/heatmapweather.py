import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd

#Load CSV file from Datasets folder
df = pd.read_csv('../../Datasets/Weather2014-15.csv')


# Preparing data
# Loads the data into a plot graph object heatmap where the x-axis is the day,
# the y axis is the week, and the z axis, or the color, is the number of recovered cases
data = [go.Heatmap(x = df['day'], y = df['month'], z = df['actual_max_temp'].values.tolist(), colorscale = 'Jet')]

# Preparing layout
layout = go.Layout(title = 'Max temperature per month', xaxis_title = "Day of Week", yaxis_title = "Month of Year")

#Plot the figure and saving in a html file
fig = go.Figure(data = data, layout = layout)
pyo.plot(fig, filename = 'heatmapweather.html')
