import requests

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
    print(i["href"])
    print("*"*30)

