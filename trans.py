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
    # YouTube channel URL (replace with the desired creator's channel URL)
    channel_url = "https://www.youtube.com/@Onevilage"

    # Open the channel page
    driver.get(channel_url)

    # Extract subscriber count
    subscriber_count_element = driver.find_element(By.CSS_SELECTOR, "#subscriber-count")
    subscriber_count = subscriber_count_element.text
    print(f"Subscriber count: {subscriber_count}")

    # Scroll to the "Videos" tab (if not already on the videos tab)
    videos_tab = driver.find_element(By.XPATH, "//a[contains(@href, '/videos')]")
    videos_tab.click()

    # Wait for the page to load
    driver.implicitly_wait(5)

    # Extract the latest video title and link
    latest_video = driver.find_element(By.CSS_SELECTOR, "#video-title")
    latest_video_title = latest_video.get_attribute("title")
    latest_video_url = latest_video.get_attribute("href")

    print(f"Latest video title: {latest_video_title}")
    print(f"Latest video URL: {latest_video_url}")

finally:
    # Close the browser
    driver.quit()
