import time
import os.path
import uuid
import glob
import json
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
# Get the most wanted page
browser.get("https://www.usmarshals.gov/what-we-do/fugitive-investigations/15-most-wanted-fugitive")
# Wait for the ok alert and deal with it
time.sleep(1)
browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/button").click()
# Grab all the most wanted card container elements
most_wanted = browser.find_elements(By.CLASS_NAME, "usa-card__container")

# Cleanup directory before saving new screenshots
clean_marshalls = glob.glob('/mnt/c/repos/iframe-kiosk/marshall-posters/*')
for f in clean_marshalls:
    os.remove(f)

# Loop through the most wanted cards and save them
for element in most_wanted:
    # Delay to allow screen to undim
    time.sleep(1)
    file_name = "/mnt/c/repos/iframe-kiosk/marshall-posters/marshall-poster-" + str(uuid.uuid4()) + ".png"
    png_data = element.screenshot_as_png
    png_file = open(file_name, "wb")
    png_file.write(png_data)
    png_file.close

# Close the browser
browser.quit()

# Generate json for iframe-kiosk
marshall_path = '/mnt/c/repos/iframe-kiosk/marshall-posters/'
marshall_json = []
file_list = glob.glob(marshall_path + '*')

final_list = [i.replace('/mnt/c/repos/iframe-kiosk', '.') for i in file_list]

for f in final_list:
    marshall_json.append(f)

delaySeconds = np.full_like(marshall_json, 15, dtype=int)
delaySecJ = delaySeconds.tolist()
json_obj = json.dumps({"delaySec": delaySecJ, "path": marshall_json}, indent=4)

with open("marshall_posters.json", "w") as outfile:
    outfile.write(json_obj)