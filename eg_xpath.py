import requests
import lxml.html

url = 'http://www.tianbaotravel.com/tour/entry-1-505------.shtml'
source = requests.get(url).content.decode()

root = lxml.html.fromstring(source)
tour_list_node = root.xpath('//*[@id="tour-list-view"]/div[2]')[0]

tour_list = []

for tour_node in tour_list_node:
    title = tour_node.xpath('div[2]/div[1]/a/text()')

    tour = {'title': title}
    tour_list.append(tour)

for tour in tour_list:
    print(tour)
