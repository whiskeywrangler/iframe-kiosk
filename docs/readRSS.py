import json
import feedparser
import time
import numpy as np

d = feedparser.parse('https://www.missingkids.org/missingkids/servlet/XmlServlet?act=rss&LanguageCountry=en_US&orgPrefix=NCMC&state=AL')

links = []
# link = '/mainposter/#'

for entry in d.entries:
    if (time.time() - time.mktime(entry.published_parsed)) >= 2592000:
        links.append(entry.link)

# urls = [i + link for i in links]
urls = links
delaySeconds = np.full_like(urls, 15, dtype=int)
delaySecJ = delaySeconds.tolist()

json_obj = json.dumps({"delaySec": delaySecJ, "url": urls}, indent=4)

with open("urls.json", "w") as outfile:
    outfile.write(json_obj)