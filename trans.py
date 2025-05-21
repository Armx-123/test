import time
import pandas as pd
from pytrends.request import TrendReq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import plotly.graph_objects as go

CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
KEYWORD = "memes"


def get_cookie():
    """Launches a headless browser to get the NID cookie from Google Trends."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://trends.google.com/")
    time.sleep(5)  # wait for the page to load and set the cookie

    nid = driver.get_cookie("NID")["value"]
    driver.quit()
    return nid


# Set up pytrends with proper cookie
# Set up pytrends with proper cookie
nid_cookie = f"NID={get_cookie()}"
print(nid_cookie)
pytrends = TrendReq(
    hl='en-US',
    tz=360,
    retries=3,
    requests_args={"headers": {"Cookie": nid_cookie}}
)

# Fetch interest over time with retry logic (exponential backoff)
kw_list = [KEYWORD]
data = None
max_retries = 5

for attempt in range(max_retries):
    try:
        pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d', geo='', gprop='youtube')
        data = pytrends.interest_over_time()
        if not data.empty:
            break  # Success, exit loop
    except Exception as e:
        wait = 2 ** attempt
        print(f"[Attempt {attempt + 1}] Failed to fetch data: {e}. Retrying in {wait}s...")
        time.sleep(wait)
else:
    print("Failed to fetch data after several attempts.")
    data = pd.DataFrame()  # Empty fallback

if not data.empty:
    data = data.reset_index()
    interest = data[KEYWORD]
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

    # Plotting the data
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

    if rising_index is not None:
        fig.add_trace(go.Scatter(
            x=[timestamps[rising_index]],
            y=[interest[rising_index]],
            mode='markers+text',
            name='Start Rising',
            marker=dict(color='green', size=9, symbol='triangle-up'),
            text=["Rising"],
            textposition="bottom center"
        ))

    if falling_index is not None:
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

    # Get related search queries
    try:
        related_queries = pytrends.related_queries()
        keyword_data = related_queries.get(KEYWORD)

        if keyword_data:
            top_related = keyword_data.get("top")
            rising_related = keyword_data.get("rising")

            if isinstance(top_related, pd.DataFrame) and not top_related.empty:
                print("\nTop Related Search Keywords:")
                print(top_related[['query', 'value']].head(10))

            if isinstance(rising_related, pd.DataFrame) and not rising_related.empty:
                print("\nRising Related Search Keywords:")
                print(rising_related[['query', 'value']].head(10))
        else:
            print("No related search keywords found.")

    except Exception as e:
        print(f"Error fetching related keywords: {e}")

else:
    print("No data found for the given timeframe.")
