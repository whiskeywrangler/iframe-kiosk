import json
import feedparser
import time

d = feedparser.parse('https://www.missingkids.org/missingkids/servlet/XmlServlet?act=rss&LanguageCountry=en_US&orgPrefix=NCMC&state=AL')

links = []

for entry in d.entries:
    if (time.time() - time.mktime(entry.published_parsed)) >= 2592000:
        links.append(entry.link)



json_obj = json.dumps(links, indent=4)

with open("missingKidsiFrameURL.json", "w") as outfile:
    outfile.write(json_obj)
