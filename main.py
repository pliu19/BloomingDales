import requests
import urllib.request

from bs4 import BeautifulSoup
from urllib.request import urlopen


Target_URL = "http://www.yluxuryonline.com/brands/3-1-phillip-lim.html?___SID=U"

# content = urlopen(Target_URL).read()
page = requests.get(Target_URL)
# print(page.content.decode("utf-8","ignore"))

soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())

upcoming_events_div = soup.find("ul", class_="products-grid")

url_list = []
for i in upcoming_events_div.select("li.item a.product-image"):
    url_list.append(i)
    # print(i["href"])
    # print("*" * 130)


def getString(soup, className, tag):
    res = ''
    # upcoming_events_div = soup.find("div", class_="product-description")
    upcoming_events_div = soup.find("div", class_=className)
    for e in upcoming_events_div.select(tag):
        res += e.string + '\n'
    return res


for e in url_list:
    page = requests.get(e["href"])
    soup = BeautifulSoup(page.content, 'html.parser')

    # Text information
    name = getString(soup, 'product-name', 'div')
    price = getString(soup, 'price-box', 'span')
    description = getString(soup, 'product-description', 'li')

    print(name)
    print(price)
    print(description)

    # Images
    img = [soup.find_all('img', id='image')[0]['src']]
    more_img = soup.find_all('a', class_='cloud-zoom-gallery')
    for x in more_img:
        img += x.select('img')[0]['src'],

    # Save to local
    cnt = 0
    for url in img:
        urllib.request.urlretrieve(url, name + "/" + str(cnt))
        cnt += 1
    print(img)

    print("*" * 130)