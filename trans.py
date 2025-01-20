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

try:
    # YouTube channel base URL
    channel_url = "https://www.youtube.com/@Onevilage"

    # Open the channel page
    driver.get(channel_url)

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Extract the subscriber count
    subscriber_count_element = driver.find_element(
        By.XPATH, "//span[contains(@class, 'yt-core-attributed-string') and contains(text(), 'subscribers')]"
    )
    subscriber_count = subscriber_count_element.text
    print(f"Subscriber count: {subscriber_count}")

    # Navigate to the Shorts section of the channel
    shorts_url = f"{channel_url}/shorts"
    driver.get(shorts_url)

    # Wait for the Shorts page to load
    driver.implicitly_wait(10)

    # Extract the latest Short video details
    latest_video_element = driver.find_element(By.CSS_SELECTOR, "a.shortsLockupViewModelHostEndpoint")
    latest_video_url = latest_video_element.get_attribute("href")
    print(f"Latest Short video URL: {latest_video_url}")

finally:
    # Close the browser
    driver.quit()
