import requests
import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.blog_database
collection = db.blog

url = 'http://www.tianbaotravel.com/tour/entry-1-505------.shtml'
source = requests.get(url).content.decode()
soup = BeautifulSoup(source, 'lxml')

tour_list_node = soup.find(
    'div', id="tour-list-view").find_all('div', class_="list-view-info")

for tour_node in tour_list_node:
    url = tour_node.find('div', class_="tour-title").a['href']
    title = tour_node.find('div', class_="tour-title").a.text
    post = {
        "url": url,
        "title": title,
        "date": datetime.datetime.utcnow()
    }
    collection.insert_one(post)
