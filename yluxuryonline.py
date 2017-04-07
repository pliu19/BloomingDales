import requests
import urllib.request
import os
import random
from time import sleep
from bs4 import BeautifulSoup

Target_URL = "http://www.yluxuryonline.com/brands/valentino.html?brand=90&limit=all&simu_categories=169_167_165"
BRAND = "prada"

def get_link_list():
    page = requests.get(Target_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    upcoming_events_div = soup.find("ul", class_="products-grid")
    url_list = []
    for i in upcoming_events_div.select("li.item a.product-image"):
        url_list.append(i)

    return url_list


def getString(soup, className, tag):
    res = ''
    upcoming_events_div = soup.find("div", class_=className)
    for e in upcoming_events_div.select(tag):
        if e.string is None:
            break
        else:
            res += e.string + '\n'

    return res


def get_resources(url_list):

    if not os.path.exists(BRAND):
        os.makedirs(BRAND)

    item_id = 0
    for e in url_list:
        page = requests.get(e["href"])
        soup = BeautifulSoup(page.content, 'html.parser')
        file_path = "./" + BRAND + "/"+str(item_id)
        file_name = file_path + '/itemInfo.txt'

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Text information
        name = getString(soup, 'product-name', 'div')
        price = getString(soup, 'price-box', 'span')
        description = getString(soup, 'product-description', 'li')

        print(name)
        file = open(file_name,'w', encoding="utf-8")
        file.write(name)
        file.write(price)
        file.write(description)

        img = soup.find('div', class_='more-views')
        more_img = img.select('a')

        imgs = []
        for x in more_img:
            imgs.append(x['href'])

        # Save to local
        cnt = 0
        for url in imgs:
            try:
                urllib.request.urlretrieve(url, file_path + '/' + str(cnt) + '.jpg')
                cnt += 1
            except:
                print('miss 1 pic..')
                pass

        sleep(random.uniform(0.5, 1))

        item_id += 1

if __name__ == "__main__":

    url_list = get_link_list()
    get_resources(url_list)
