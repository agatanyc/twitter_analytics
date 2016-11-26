import plotly.plotly as py
import plotly.graph_objs as go
import sys
from db import query_tweets

lst = ['harrys', 'Gillette', 'SchickHydro', 'DollarShaveClub']

def create_dict(n):
    d = {}
    for i in range (n):
        d[i] = [0, 0, 0]
    return d

def get_data(acc):
    """(str, int) -> dict {int : tuple}
    Get data distribution by time of day.
    Dict `d` repersents:
    {the hour the activity occured: [number of: tweets, retweets, faves]
    """
    d = create_dict(24) 
    # query the db for `created at`,`retweets` and `faves` for giver account
    tweets = query_tweets(acc)
    
    for t in tweets:
        # the hour the tweet was sent
        tweeted_at = t[0].hour
        d[tweeted_at][0] += 1
        for i in range(1, 3):
            d[tweeted_at][i] += t[i]
    return d

def create_axes(acc, index):
    # Pass index 0 for all tweets, 1 for retweets and 2 for faves
    d = get_data(acc)
    ys = []
    xs = []
    for k, v in d.iteritems():
        ys.append(v[index])
        xs.append(k)
    return ys, xs

def get_traces(lst, index):
    traces = []
    for i in range(len(lst)):
        ys, xs = create_axes(lst[i], index)
        trace = go.Scatter(x=xs,y=ys)
        traces.append(trace)
    return traces

# Create plot for all tweets
"""
def get_all_tweets_trace(lst, index):
    traces = []
    for i in range(len(lst)):
        ys, xs = create_axes(lst[i], index)
        trace = go.Scatter(x=xs,y=ys)
        traces.append(trace)
    return traces
    """

layout = dict(title = 'Engagement on Twitter',
              xaxis = dict(title = 'Time of day', fixedrange=True),
              yaxis = dict(title = 'Activity', autorange=True),
              )
index = 0
data = get_traces(lst, index)
fig = dict(data=data, layout=layout)
py.iplot(fig)

# Create plot for retweets
"""
def get_retweets_trace(lst, index):
    traces = []
    for i in range(len(lst)):
        ys, xs = create_axes(lst[i], index)
        trace = go.Scatter(x=xs,y=ys)
        traces.append(trace)
    return traces
"""
layout = dict(title = 'Engagement on Twitter/ Retweets',
              xaxis = dict(title = 'Time of day', fixedrange=True),
              yaxis = dict(title = 'Activity', autorange=True),
              )
index = 1
data = get_traces(lst, index)
fig = dict(data=data, layout=layout)
py.iplot(fig)

# Create plot for faves
"""
def get_faves_trace(lst, index):
    traces = []
    for i in range(len(lst)):
        ys, xs = create_axes(lst[i], index)
        trace = go.Scatter(x=xs,y=ys)
        traces.append(trace)
    return traces
"""
layout = dict(title = 'Engagement on Twitter/ Faves',
              xaxis = dict(title = 'Time of day', fixedrange=True),
              yaxis = dict(title = 'Activity', autorange=True),
              )
index = 2
data = get_traces(lst, index)
fig = dict(data=data, layout=layout)
py.iplot(fig)








