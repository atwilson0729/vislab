import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folders
df = pd.read_csv('../Datasets/CoronavirusTotal.csv')

# Removing empty spaces from State column to avoid errors
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Creating unrecovered column
df['Unrecovered'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

# Removing China and others from data frame
df = df[(df['Country'] != 'China')]

# Creating sum of number of cases group by Country Column
new_df = df.groupby(['Country']).agg(
    {'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered' : 'sum', 'Unrecovered': 'sum'}).reset_index()

# Sorting values and select 20 first value
new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20).reset_index()

# Preparing data
# Creates three plotly graph objects for bar chart data,  each with an x-axis of 'Country' in a pandas df
# Each of the three plotly objects is a different color on the stacked chart
# The first object has a y-axis of Unrecovered data in pandas df
# The second object has a y-axis of recovered data in pandas df
# The third object has a y-axis of deaths data in pandas df
# The graph objects are then all stored in a list named data
trace1 = go.Bar(x=new_df['Country'], y=new_df['Unrecovered'], name='Unrecovered', marker={'color': '#CD7F32'})
trace2 = go.Bar(x=new_df['Country'], y=new_df['Recovered'],name='Recovered', marker={'color': '#9EA0A1'})
trace3= go.Bar(x=new_df['Country'], y=new_df['Deaths'], name='Deaths', marker={'color': '#FFD700'})
data= [trace1, trace2, trace3]

# Preparing layout
layout = go.Layout(title='CoronaVirus Cases in the first 20 countries except China',
                    xaxis_title="Country",
                    yaxis_title="Number of Cases", barmode='stack')

# Plot the figure and saving in an HTML file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='stackbarchart.html')

#data = [
#    go.Scatter(x=new_df['Recovered'],
#               y=new_df['Unrecovered'],
#               text=new_df['Country'],
#               mode='markers',
#               marker=dict(size=new_df['Confirmed'] /
#100,color=new_df['Confirmed'] /100, showscale=True))
#]

#layout = go.Layout(title='Corona Virus Confirmed Cases', xaxis_title="Recovered Cases",
#                   yaxis_title="Unrecovered Cases", hovermode='closest')

#fig = go.Figure(data=data, latout=layout)
#pyo.plot(fig, filename='bubblechart.html')