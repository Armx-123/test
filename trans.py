import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pytrends.request import TrendReq
import plotly.graph_objects as go

CHROME_DRIVER_PATH = "/usr/bin/chromedriver"


def create_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)


def get_cookie() -> str:
    driver = create_driver()
    driver.get("https://trends.google.com/")
    time.sleep(5)  # Wait for the cookie to load
    cookie = driver.get_cookie("NID")
    driver.quit()
    if cookie:
        return cookie["value"]
    raise Exception("NID cookie not found")


nid_cookie = f"NID={get_cookie()}"

pytrends = TrendReq(
    hl='en-US',
    tz=360,
    retries=3,
    requests_args={"headers": {"Cookie": nid_cookie}}
)

# Choose keyword and fetch data
kw_list = ["memes"]
pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d', geo='', gprop='youtube')
data = pytrends.interest_over_time()

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
    print("Best time to upload memes (Unix + 24h):", peak_plus_24h_unix)

    # Detect rising and falling edges
    rising_index = None
    falling_index = None

    for i in range(1, len(interest)):
        if rising_index is None and interest[i] > interest[i-1] + 10:
            rising_index = i
        if falling_index is None and i > peak_index and interest[i] < interest[i-1] - 10:
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
    print("No data found for the given timeframe.")
