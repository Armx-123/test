import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pytrends.request import TrendReq
import plotly.graph_objects as go

CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
KEYWORD = "memes"


def get_cookie() -> str:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://trends.google.com/")
    time.sleep(5)  # wait for cookies to load
    cookie = driver.get_cookie("NID")["value"]
    driver.quit()
    return cookie


# Get NID cookie and setup pytrends with headers
nid_cookie = f"NID={get_cookie()}"
pytrends = TrendReq(
    hl='en-US',
    tz=360,
    requests_args={"headers": {"Cookie": nid_cookie}}
)

# Build payload
kw_list = [KEYWORD]
pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d', geo='', gprop='youtube')

# Fetch interest over time data
data = pytrends.interest_over_time()

if not data.empty:
    data = data.reset_index()
    interest = data[KEYWORD]
    timestamps = data["date"]

    peak_index = interest.idxmax()
    peak_time = timestamps[peak_index]
    peak_value = interest[peak_index]

    peak_unix = int(time.mktime(peak_time.timetuple()))
    peak_plus_24h_unix = peak_unix + 86400
    print("Best time to upload", KEYWORD, "(Unix + 24h):", peak_plus_24h_unix)

    # Detect rising and falling edges
    rising_index = None
    falling_index = None

    for i in range(1, len(interest)):
        if rising_index is None and interest[i] > interest[i - 1] + 10:
            rising_index = i
        if falling_index is None and i > peak_index and interest[i] < interest[i - 1] - 10:
            falling_index = i

    # Plot the trend
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
        title=f'Google Trends (YouTube) - {KEYWORD.capitalize()} (Past 24h)',
        xaxis_title='Time',
        yaxis_title='Interest',
        template='plotly_dark',
        hovermode='x unified'
    )

    fig.show()

    # Related and rising keywords
    related_queries = pytrends.related_queries()
    top_related = related_queries[KEYWORD].get("top", pd.DataFrame())
    rising_related = related_queries[KEYWORD].get("rising", pd.DataFrame())

    if not top_related.empty:
        print("\nTop Related Search Keywords:")
        print(top_related[['query', 'value']].head(10))

    if not rising_related.empty:
        print("\nRising Related Search Keywords:")
        print(rising_related[['query', 'value']].head(10))

else:
    print("No data found for the given timeframe.")
