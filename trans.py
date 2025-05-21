from pytrends.request import TrendReq
import plotly.graph_objects as go
import pandas as pd
import time

# Setup pytrends
pytrends = TrendReq(hl='en-US', tz=360, retries=3)

# Choose keyword and fetch data
kw_list = ["memes"]
pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d', geo='', gprop='youtube')
data = pytrends.interest_over_time()

# 🔍 Fetch related queries
related = pytrends.related_queries()
if related and 'memes' in related:
    rising = related['memes'].get('rising')
    top = related['memes'].get('top')

    print("\n🔝 Top related keywords:")
    if top is not None:
        for i, row in top.iterrows():
            print(f"{i+1}. {row['query']} ({row['value']})")
    else:
        print("No top related queries available.")

    print("\n📈 Rising related keywords:")
    if rising is not None:
        for i, row in rising.iterrows():
            print(f"{i+1}. {row['query']} ({row['value']})")
    else:
        print("No rising related queries available.")
else:
    print("\nNo related queries found.")

# 📊 Continue with trend graph
if not data.empty:
    data = data.reset_index()
    interest = data["memes"]
    timestamps = data["date"]

    # Identify peak point
    peak_index = interest.idxmax()
    peak_time = timestamps[peak_index]
    peak_value = interest[peak_index]

    # Convert to Unix + 24h
    peak_unix = int(time.mktime(peak_time.timetuple()))
    peak_plus_24h_unix = peak_unix + 86400
    print("\n📅 Best time to upload memes (Unix + 24h):", peak_plus_24h_unix)

    # Detect rising and falling edges
    rising_index = None
    falling_index = None

    for i in range(1, len(interest)):
        if rising_index is None and interest[i] > interest[i - 1] + 10:
            rising_index = i
        if falling_index is None and i > peak_index and interest[i] < interest[i - 1] - 10:
            falling_index = i

    # Create Plotly figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=timestamps,
        y=interest,
        mode='lines+markers',
        name='Interest',
        line=dict(color='lightblue')
    ))

    fig.add_trace(go.Scatter(
        x=[peak_time],
        y=[peak_value],
        mode='markers+text',
        name='Peak (Best time)',
        marker=dict(color='red', size=10, symbol='star'),
        text=["Peak"],
        textposition="top center"
    ))

    if rising_index:
        fig.add_trace(go.Scatter(
            x=[timestamps[rising_index]],
            y=[interest[rising_index]],
            mode='markers+text',
            name='Start Rising',
            marker=dict(color='green', size=9, symbol='triangle-up'),
            text=["Rising"],
            textposition="bottom center"
        ))

    if falling_index:
        fig.add_trace(go.Scatter(
            x=[timestamps[falling_index]],
            y=[interest[falling_index]],
            mode='markers+text',
            name='Start Falling',
            marker=dict(color='orange', size=9, symbol='triangle-down'),
            text=["Falling"],
            textposition="top center"
        ))

    fig.update_layout(
        title='Google Trends (YouTube) - Memes (Past 24h)',
        xaxis_title='Time',
        yaxis_title='Interest',
        template='plotly_dark',
        hovermode='x unified'
    )

    fig.show()

else:
    print("\nNo data found for the given timeframe.")
