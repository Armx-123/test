import time
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

pytrends.build_payload(kw_list=['memes'], cat=182, timeframe='now 1-d', gprop='youtube')
time.sleep(5)  # Wait 5 seconds before next request

df = pytrends.interest_over_time()
