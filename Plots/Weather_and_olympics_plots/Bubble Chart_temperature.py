import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/Weather2014-15.csv')
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

#df['Unrecovered'] = df['Confirmed'] - df['Deaths'] -df['Recovered']

#df = df[(df['Country'] != 'China') & (df['Country'] != 'Others')]

new_df = df.groupby(['month']).agg(
    {'average_min_temp': 'sum', 'average_max_temp': 'sum'}).reset_index()


data = [
    go.Scatter(x=new_df['average_min_temp'],
               y=new_df['average_max_temp'],
               text=new_df['month'],
               mode='markers',
               marker=dict(size=new_df['average_min_temp'] / 100,color=new_df['average_min_temp'] / 100, showscale=True))]

layout = go.Layout(title='Average min and max temperature',
                   xaxis_title="Min temp sum",
                   yaxis_title="Max temp sum", hovermode='closest')

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='bubblechart.html')