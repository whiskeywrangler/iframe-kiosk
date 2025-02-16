import time
import os.path
import uuid
import glob
import json
import numpy as np
import tempfile
from urllib.request import urlretrieve
from pdf2image import convert_from_path
from selenium import webdriver
from Screenshot import Screenshot_Clipping
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

SS = Screenshot_Clipping.Screenshot()

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
base_url = "https://www.usmarshals.gov/what-we-do/fugitive-investigations/15-most-wanted-fugitive"
browser.maximize_window()
browser.get(base_url)
# Wait for the ok alert and deal with it
time.sleep(1)
browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/button").click()
# Grab all the most wanted card container elements
most_wanted = browser.find_elements(By.CLASS_NAME, "usa-card")
individual_fugitive_links = browser.find_elements(By.CSS_SELECTOR, ".usa-card__footer [href]")
# Loop through and add individual felon links to array
full_links = []
for i in individual_fugitive_links:
    url = i.get_attribute('href')
    full_links.append(url)

pdf_links = []
# Find pdf links on individual felon pages
for link in full_links:
    browser.get(link)
    time.sleep(1)
    browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/button").click()
    pdf_url = browser.find_element(By.CSS_SELECTOR, ".file [href]")
    pdf_url_final = pdf_url.get_attribute('href')
    pdf_links.append(pdf_url_final)

# Cleanup directory before saving new screenshots
clean_marshalls = glob.glob('/mnt/c/repos/iframe-kiosk/marshall-posters/*')
for f in clean_marshalls:
    os.remove(f)

# Loop through links and screenshot pdfs
for link in pdf_links:
    file_name = "/mnt/c/repos/iframe-kiosk/marshall-posters/marshall-poster-" + str(uuid.uuid4()) + ".pdf"
    urlretrieve(link, file_name)

# Close the browser
browser.quit()

# Generate json for iframe-kiosk
marshall_path = '/mnt/c/repos/iframe-kiosk/marshall-posters/'
marshall_json = []
pdf_list = glob.glob(marshall_path + '*')
# Convert from pdf to png
for i in pdf_list:
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(i, output_folder=marshall_path, fmt="png")

png_list = glob.glob(marshall_path + "*.png")
final_list = [i.replace('/mnt/c/repos/iframe-kiosk', '.') for i in png_list]
# Cleanup pdfs
pdf_cleanup_list = glob.glob(marshall_path +'*.pdf')
for f in pdf_cleanup_list:
    os.remove(f)
# append paths to json list
for f in final_list:
    marshall_json.append(f)

delaySeconds = np.full_like(marshall_json, 15, dtype=int)
delaySecJ = delaySeconds.tolist()
json_obj = json.dumps({"delaySec": delaySecJ, "path": marshall_json}, indent=4)

with open("marshall_posters.json", "w") as outfile:
    outfile.write(json_obj)