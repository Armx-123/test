from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up Chromium options
options = Options()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Specify the path to your ChromeDriver
chrome_driver_path = "chromedriver.exe"  # Update with your Chromedriver path

# Create a Service object
service = Service(chrome_driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open a website
    driver.get("https://example.com")
    
    # Print the title of the page
    print("Page title:", driver.title)
    
    # Find an element on the page (optional example)
    heading = driver.find_element(By.TAG_NAME, "h1")
    print("Heading text:", heading.text)
finally:
    # Close the browser
    driver.quit()
