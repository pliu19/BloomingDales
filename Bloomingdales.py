import requests
import json
import urllib.request
import os
import random
from collections import defaultdict
from time import sleep
from bs4 import BeautifulSoup

Target_URL = "http://www1.bloomingdales.com/shop/coach?id=1004771&cm_kws=coach%20"
BRAND = "coach"

PREFIX ="https://images.bloomingdales.com/is/image/BLM/products/"
PostFix = "?wid=1200&qlt=90,0&fmt=jpeg"

def get_link_list():
    page = requests.get(Target_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    upcoming_events_div = soup.find_all("a", class_="imageLink productThumbnailLink")
    url_list = []

    for i in upcoming_events_div:
        url_list.append(i['href'])

    return url_list


def getStringByClass_Price(soup, className, tag):

    upcoming_events_div = soup.find(tag, class_=className)
    return upcoming_events_div.text + "\n"

def getStringByID_Title(soup, classID, tag):

    upcoming_events_div = soup.find(tag, {"id": classID})
    return upcoming_events_div.text + "\n"

def getStringByID_list_description(soup, classID, tag):

    result = ""
    upcoming_events_div = soup.find_all(tag, {"id": classID})

    for i in upcoming_events_div:
        result += i.text
        result += "\n"

    return result

def get_resources(urllist):

    if not os.path.exists(BRAND):
        os.makedirs(BRAND)

    item_id = 0
    for e in urllist:
        page = requests.get(e)
        soup = BeautifulSoup(page.content, 'html.parser')
        file_path = "./" + BRAND + "/"+str(item_id)
        file_name = file_path + '/itemInfo.txt'

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Text information
        temp_url = e
        name = getStringByID_Title(soup, 'productName', 'div')
        price = getStringByClass_Price(soup, 'cw_price_holder priceBig', 'span')
        long_description = getStringByClass_Price(soup, 'pdp_longDescription', 'div')
        list_description = getStringByID_list_description(soup, 'productDetailsBulletText', 'li')
        webID_description = getStringByID_Title(soup, "productWebID", 'li')

        file = open(file_name,'w', encoding="utf-8")
        file.write(temp_url + "\n")
        file.write(name)
        file.write(price)
        file.write(long_description)
        file.write(list_description)
        file.write(webID_description)

        # Images
        img = soup.find('script', {'id':'pdp_data','type':'application/json'})
        json_obj = json.loads(img.text)['product']

        try:
            other_url_dict = json_obj['colorwayAdditionalImages']
            other_url_dict2 = json_obj['colorwayPrimaryImages']
        except Error:
            
            print("Skip this")
            continue


        dict_category = defaultdict(list)

        key_list = []

        for key, value in other_url_dict.items():
            key_list.append(key)
            temp_list = value.split(',')
            dict_category[key] = temp_list

        for key, value in other_url_dict2.items():
            dict_category[key].append(value)

        file.write("  ".join(key_list))
        print(name)

        for key,value in dict_category.items():
            cnt = 0
            category_path = file_path + "/" + key + "/"
            if not os.path.exists(category_path):
                os.makedirs(category_path)

            for pic in value:
                image_URL = PREFIX + pic + PostFix

                try:
                    urllib.request.urlretrieve(image_URL, category_path + '/' + str(cnt) + '.jpg')
                    cnt += 1
                except:
                    print('miss 1 pic..')
                    pass

        sleep(random.uniform(0.5, 1))
        item_id += 1

if __name__ == "__main__":

    url_list = get_link_list()
    get_resources(url_list)
