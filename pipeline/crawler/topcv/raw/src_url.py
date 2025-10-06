import requests as rq
from bs4 import BeautifulSoup


raw_url = rq.get('https://www.topcv.vn/sitemap.xml')

with open('./sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(raw_url.text)


with open("./sitemap.xml", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml-xml")


locs = [loc.get_text() for loc in soup.find_all("loc")]

with open ('./all_url.txt', 'a', encoding='utf-8') as f:
    for url in locs:
        f.write (url.strip () + '\n')