import time
import os.path
import json
import uuid
import feedparser
import glob
import numpy as np
from PIL import Image
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

# Generate json for urls no older than 30 days from Alabama NCMC rss feed
d = feedparser.parse('https://www.missingkids.org/missingkids/servlet/XmlServlet?act=rss&LanguageCountry=en_US&orgPrefix=NCMC&state=AL')
data = []
for entry in d.entries:
    if (time.time() - time.mktime(entry.published_parsed)) >= 2592000:
        data.append(entry.link)

# Cleanup directory before saving new screenshots
clean_missing = glob.glob('/mnt/c/repos/iframe-kiosk/missing-posters/*')
for f in clean_missing:
    os.remove(f)

# Loop through array and get the image at each url
for i in data:
    browser.get(i)
    time.sleep(1)
    file_name = "/mnt/c/repos/iframe-kiosk/missing-posters/ALposter-" + str(uuid.uuid4()) + ".png"
    browser.find_element(By.CSS_SELECTOR, "iframe").screenshot(file_name)
    image = Image.open(file_name)
    image_resized = image.resize((1080, 1920))
    image_resized.save(file_name)
    time.sleep(1)

# Close the browser.
browser.quit()

# Generate json for iframe-kiosk
missing_path = '/mnt/c/repos/iframe-kiosk/missing-posters/'
missing_json = []
file_list = glob.glob(missing_path + '*')

final_list = [i.replace('/mnt/c/repos/iframe-kiosk', '.') for i in file_list]

for f in final_list:
    missing_json.append(f)

delaySeconds = np.full_like(missing_json, 15, dtype=int)
delaySecJ = delaySeconds.tolist()
json_obj = json.dumps({"delaySec": delaySecJ, "path": missing_json}, indent=4)

with open("missing_posters.json", "w") as outfile:
    outfile.write(json_obj)