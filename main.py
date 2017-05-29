import requests
import json
import re
from lxml import html
from urllib.parse import urljoin

def dumpJson(siteName, siteDomain, rssLink):
    data = {
        "university": siteName,
        "faculity": "Computer Engineering",
        "rss": rssLink
    }
    with open('sites/' + siteDomain + '.json', 'w') as f:
        json.dump(data, f)

def checkExistRss(site):
    print(site['web_page'])
    page = False
    try:
        page = requests.get(site['web_page'], allow_redirects=False)
    except Exception as e:
        print('Website doesn\'t exists: ', e)
        return 0

    if not page or not page.content:
        print('Lxml doesn\'t work')
        return 0
    # Checking <link href='/rss' type='application/rss+xml'> tag in Main Page
    tree = html.fromstring(page.content)
    link = tree.xpath("//link[@type='application/rss+xml']/@href")
    if link:
        link = link[0]
        rssLink = urljoin(site['web_page'], link)
        print('Rss Exists: ', rssLink)
        dumpJson(site['name'], site['domain'], rssLink)
        return True
    return False

def main():
    with open("tr-sites.json") as SitesJsonData:
        sites = json.load(SitesJsonData)
        for site in sites[:]:
            checkExistRss(site)

if __name__ == '__main__':
    main()
