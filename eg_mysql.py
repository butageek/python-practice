import requests
from bs4 import BeautifulSoup
import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root',
                       passwd='tianbao0', db='scraping', charset='utf8')
cur = conn.cursor()

url = 'http://www.tianbaotravel.com/tour/entry-1-505------.shtml'
source = requests.get(url).content.decode()
soup = BeautifulSoup(source, 'lxml')

tour_list_node = soup.find(
    'div', id="tour-list-view").find_all('div', class_="list-view-info")

tour_list = []

for tour_node in tour_list_node:
    url = tour_node.find('div', class_="tour-title").a['href']
    title = tour_node.find('div', class_="tour-title").a.text
    cur.execute("insert into urls (url, content) values (%s, %s)", (url, title))

cur.close()
conn.commit()
conn.close()
