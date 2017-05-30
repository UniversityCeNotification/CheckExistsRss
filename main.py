import requests
import json
import re
import feedparser
import io
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

def feedfinder(url, domain):
    """https://gist.github.com/pleycpl/46953ff26e7da165c9f20dfbe1cd8256"""
    print(url)
    raw = False
    try:
        raw = requests.get(url).content
    except Exception as e:
        print('Website doesn\'t exists: ', e)
        return 0

    if not raw:
        print('Lxml doesn\'t work')
        return 0

    result = []
    possibleFeeds = []
    tree = html.fromstring(raw)
    feedUrls = tree.xpath("//link[@rel='alternate']")
    if feedUrls:
        for feed in feedUrls:
            t = feed.xpath('@type')
            if t:
                t = t[0]
                if "rss" in t or "xml" in t:
                    href = feed.xpath('@href')
                    if href:
                        href = href[0]
                        possibleFeeds.append(urljoin(url, href))

    atags = tree.xpath("//a")
    for a in atags:
        href = a.xpath('@href')
        if href:
            href = href[0]
            if "xml" in href or "rss" in href or "feed" in href:
                possibleFeeds.append(urljoin(url, href))

    for link in list(set(possibleFeeds)):
        # Thanks for https://stackoverflow.com/questions/9772691/feedparser-with-timeout
        try:
            resp = requests.get(link, timeout=10.0)
        except Exception as e:
            print("Timeout when reading RSS %s", link, ' e:', e)
            return

        content = io.BytesIO(resp.content)

        f = feedparser.parse(content)
        if len(f.entries) > 0:
            if url not in result:
                result.append(link)

    return (result)

def main():
    with open("tr-sites.json") as SitesJsonData:
        sites = json.load(SitesJsonData)
        for site in sites[:]:
            result = feedfinder(site['web_page'], site['domain'])
            print(result)
            if result:
                print('Rss Exists: ', result[0])
                dumpJson(site['name'], site['domain'], result[0])

if __name__ == '__main__':
    main()
