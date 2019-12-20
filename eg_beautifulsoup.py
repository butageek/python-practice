import requests
from bs4 import BeautifulSoup

url = 'http://www.tianbaotravel.com/tour/entry-1-505------.shtml'
source = requests.get(url).content.decode()
soup = BeautifulSoup(source, 'lxml')

tour_list_node = soup.find(
    'div', id="tour-list-view").find_all('div', class_="list-view-info")

tour_list = []

for tour_node in tour_list_node:
    title = tour_node.find('div', class_="tour-title").a.text
    tour_list.append({"title": title})

for tour in tour_list:
    print(tour)
