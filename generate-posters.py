import os.path
import feedparser
import glob
import time
import uuid
import json
import re
import numpy as np
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
# MUST BE HEADLESS AND HAVE VERY LARGE WINDOW SIZE
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=6000x5000")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")
"""
# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

# Choose Chrome Browser
chrome = webdriver.Chrome(service=webdriver_service, options=chrome_options)
"""

# Generate json for urls no older than 30 days from Alabama NCMC rss feed
d = feedparser.parse('https://www.missingkids.org/missingkids/servlet/XmlServlet?act=rss&LanguageCountry=en_US&orgPrefix=NCMC&state=AL')
url_paths = []
for entry in d.entries:
    if (time.time() - time.mktime(entry.published_parsed)) >= 2592000:
        url_paths.append(entry.link + '/mainposter')

# Cleanup directory before saving new screenshots
clean_missing = glob.glob('/mnt/c/repos/iframe-kiosk/missing-posters/*')
for f in clean_missing:
    os.remove(f)

poster_id = []
for url in url_paths:
    posid = re.search(r'\d{6,}', url)
    print(posid.group())

"""
for i in url_paths:
    ## Setup chrome options
    chrome.get(i)
    chrome.execute_script("document.body.style.zoom = '300%'")     # ZOOM

    element = chrome.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div') # find part of the page you want image of
    location = element.location
    size = element.size
    png = chrome.get_screenshot_as_png() # saves screenshot of entire page
    chrome.quit()

    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

    left = location['x'] * 3 # must mutliply all these numbers by your zoom
    top = location['y'] * 3
    right = (location['x'] + size['width']) * 3
    bottom = (location['y'] + size['height']) * 3

    im = im.crop((left, top, right, bottom)) # defines crop points
    file_name = "/mnt/c/repos/iframe-kiosk/missing-posters/missing-poster-" + str(uuid.uuid4()) + ".png"
    im.save(f'{file_name}') # saves new cropped image
    """

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