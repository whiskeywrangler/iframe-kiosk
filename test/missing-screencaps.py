import time
import os.path
import json
import uuid
import feedparser
import glob
import numpy as np
from PIL import Image
from selenium import webdriver
from Screenshot import Screenshot_Clipping
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
clean_missing = glob.glob('/mnt/c/repos/iframe-kiosk/test/missing-posters/*')
for f in clean_missing:
    os.remove(f)

# Loop through array and get the image at each url
SS = Screenshot_Clipping.Screenshot()

for i in data:
    browser.get(i)
    time.sleep(10)
    file_path = "/mnt/c/repos/iframe-kiosk/test/missing-posters/"
    current_file_name = "/mnt/c/repos/iframe-kiosk/test/missing-posters/missing-poster-" + str(uuid.uuid4()) + ".png"
    file_name = current_file_name[-55:]
    SS.full_Screenshot(browser, file_path, file_name)

# get list of current posters and the crop and resize them.
current_posters = glob.glob('/mnt/c/repos/iframe-kiosk/test/missing-posters/*')
for i in current_posters:
    left = 0
    top = 100
    right = 635
    bottom = 750
    img = Image.open(i)
    img.crop((left, top, right, bottom)).resize((768, 1024)).save(i)

# Close the browser.
browser.quit()

# Generate json for iframe-kiosk
missing_path = '/mnt/c/repos/iframe-kiosk/test/missing-posters/'
missing_json = []
file_list = glob.glob(missing_path + '*')

final_list = [i.replace('/mnt/c/repos/iframe-kiosk/test', '.') for i in file_list]

for f in final_list:
    missing_json.append(f)

delaySeconds = np.full_like(missing_json, 15, dtype=int)
delaySecJ = delaySeconds.tolist()
json_obj = json.dumps({"delaySec": delaySecJ, "path": missing_json}, indent=4)

with open("missing_posters.json", "w") as outfile:
    outfile.write(json_obj)