import os.path
import feedparser
import glob
import time
import uuid
import json
import re
import numpy as np
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# MUST BE HEADLESS AND HAVE VERY LARGE WINDOW SIZE
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=2560x2560")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")
# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

def get_screenshot(url_path, object_id):
    chrome = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    chrome.get(url_path)
    time.sleep(3)
    chrome.execute_script("document.body.style.zoom = '200%'")     # ZOOM

    element = chrome.find_element(By.ID, object_id) # find part of the page you want image of
    location = element.location
    size = element.size
    png = chrome.get_screenshot_as_png() # saves screenshot of entire page
    chrome.quit()

    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
    (left, top, right, bottom) = (530, 0, 2010, 1645)
    im = im.crop((left, top, right, bottom)) # defines crop points
    
    im.save(f'/mnt/c/repos/iframe-kiosk/missing-posters/{object_id}.png') # saves new cropped image

# Generate json for urls no older than 30 days from Alabama NCMC rss feed
d = feedparser.parse('https://www.missingkids.org/missingkids/servlet/XmlServlet?act=rss&LanguageCountry=en_US&orgPrefix=NCMC&state=AL')
url_paths = []
for entry in d.entries:
    url_paths.append(entry.link + '/mainposter')

# Cleanup directory before saving new screenshots
clean_missing = glob.glob('/mnt/c/repos/iframe-kiosk/missing-posters/*')
for f in clean_missing:
    os.remove(f)

poster_id = []
for url in url_paths:
    posid = re.search(r'\/(\w+)\/\d\/', url)
    posterid = (posid.group()).replace("/" , "-")
    poster_id.append(posterid)


for path, ids in zip(url_paths, poster_id):
    get_screenshot(path, "mkpage-poster-NCMC" + ids + "screen")

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