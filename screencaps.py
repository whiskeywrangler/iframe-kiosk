"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(executable_path='/mnt/c/tools/chromedriver/stable/chromedriver')
driver.get("https://www.missingkids.org/poster/NCMC/1460865/1/mainposter")
driver.savescreenshot('./posters/ALposter.png')
driver.quit()
"""
import time
import os.path
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

## Setup chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless") # Ensure GUI is off
#chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Get the list of URLs to screenshot from urls.json
with open('/mnt/c/repos/iframe-kiosk/docs/urls.json', 'r') as openfile:
    data = json.load(openfile)

# Loop through array and get the image at each url
for i in data:
    # Get page
    print(data)
    print(data[url])
    print(data[delaySec])
    #browser.get(data.url)
    

# Extract description from page and print
"""
description = browser.find_element(By.NAME, "description").get_attribute("content")
print(f"{description}")
"""
time.sleep(5)
browser.get_screenshot_as_file('/mnt/c/repos/iframe-kiosk/posters/ALposter.png')

#Wait for 10 seconds
time.sleep(10)
browser.quit()