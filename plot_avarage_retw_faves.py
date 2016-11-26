import plotly.plotly as py
import plotly.graph_objs as go
import sys
from db import query_tweets
from plot_data_distribution import get_data

lst = ['harrys', 'Gillette', 'SchickHydro', 'DollarShaveClub']

def get_avarage_traces(lst, i1, i2):
    """(list, int, int) -> list
    Get average nummber of data points(retweets or faves) by a tweet in a given hour."""
    traces = []
    for i in range(len(lst)):
        # create a divt the represents:
        # {the hour the activity occured: [number of: all tweets, retweets, faves]
        data = get_data(lst[i])
        print data
        xs = []
        ys = []
        for k, v in data.iteritems():
            if v[i2] > 0:
                xs.append(k)
                # how many data points we get by one tweet on avarage
                ys.append(v[i1] / v[i2])
        trace = go.Scatter(x=xs,y=ys)
        traces.append(trace)
    return traces

# Craete a plot for avarage retweets
layout = dict(title = 'Avarage retweets',
              xaxis = dict(title = 'Time of day', fixedrange=True),
              yaxis = dict(title = 'Retweets', autorange=True),
              )
data = get_avarage_traces(lst, 1, 0)
fig = dict(data=data, layout=layout)
py.iplot(fig)

# Craete a plot for avarage faves
layout = dict(title = 'Avarage faves',
              xaxis = dict(title = 'Time of day', fixedrange=True),
              yaxis = dict(title = 'Faves', autorange=True),
              )
data = get_avarage_traces(lst, 2, 0)
fig = dict(data=data, layout=layout)
py.iplot(fig)

