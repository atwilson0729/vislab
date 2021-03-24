import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../../Datasets/Olympic2016Rio.csv')

# Filtering US Cases
filtered_df = df

# Removing empty spaces from Countries column to avoid errors
filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Sorting values and select first 20 countries
filtered_df = filtered_df.sort_values(by=['Total'], ascending=[False]).head(20)


# Preparing data
#loads data into a plotly graph object where the x-axis is the country and is loaded into pandas df, and the y axis is the number of total medals loaded into a pandas df
data = [go.Bar(x=filtered_df['NOC'], y=filtered_df['Total'])]


# Preparing layout
layout = go.Layout(title='2016 Olympics Medal Totals', xaxis_title="Name of Country",
                   yaxis_title="Number of total medals")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='barchartolympics.html')
