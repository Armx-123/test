from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up Chromium options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Specify the Chromedriver path
chrome_driver_path = "/usr/bin/chromedriver"

# Create a Service object
service = Service(chrome_driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# List of channel IDs (replace with desired channel usernames or IDs)
channel_ids = ["jeffreyxreacts", "zackdfilms", "JaySharon","duolingo","Lionfield","sigma_monkey"]

try:
    for channel_id in channel_ids:
        print(f"Fetching data for channel: {channel_id}")

        # Construct the channel URL
        channel_url = f"https://www.youtube.com/@{channel_id}"

        # Open the channel page
        driver.get(channel_url)
        driver.implicitly_wait(10)

        # Extract the subscriber count
        try:
            subscriber_count_element = driver.find_element(
                By.XPATH, "//span[contains(@class, 'yt-core-attributed-string') and contains(text(), 'subscribers')]"
            )
            subscriber_count = subscriber_count_element.text
        except Exception as e:
            subscriber_count = "Could not fetch subscriber count"
            print(f"Error fetching subscriber count for {channel_id}: {e}")

        # Navigate to the Shorts section of the channel
        shorts_url = f"{channel_url}/shorts"
        driver.get(shorts_url)
        driver.implicitly_wait(10)

        # Extract the latest Short video details
        try:
            latest_video_element = driver.find_element(By.CSS_SELECTOR, "a.shortsLockupViewModelHostEndpoint")
            latest_video_url = latest_video_element.get_attribute("href")
        except Exception as e:
            latest_video_url = "Could not fetch latest video"
            print(f"Error fetching latest video for {channel_id}: {e}")

        # Print the results for the channel
        print(f"Channel: {channel_id}")
        print(f"Subscriber Count: {subscriber_count}")
        print(f"Latest Short Video URL: {latest_video_url}")
        print("-" * 50)

finally:
    # Close the browser
    driver.quit()
