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
    # Replace with the desired YouTube channel URL (without '/videos')
    channel_url = "https://www.youtube.com/@Onevilage"

    # Open the channel page
    driver.get(channel_url)

    # Wait for the page to load
    driver.implicitly_wait(5)

    # Extract subscriber count
    subscriber_count_element = driver.find_element(
        By.CSS_SELECTOR,
        "span.yt-core-attributed-string[role='text']",
    )
    subscriber_count = subscriber_count_element.text
    print(f"Subscriber count: {subscriber_count}")

    # Navigate to the Videos tab
    driver.get(f"{channel_url}/videos")
    driver.implicitly_wait(5)

    # Extract the latest video title and URL
    latest_video_element = driver.find_element(By.CSS_SELECTOR, "a#video-title-link")
    latest_video_title = latest_video_element.get_attribute("title")
    latest_video_url = "https://www.youtube.com" + latest_video_element.get_attribute("href")

    print(f"Latest video title: {latest_video_title}")
    print(f"Latest video URL: {latest_video_url}")

finally:
    # Close the browser
    driver.quit()
