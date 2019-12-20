import requests
import threading
from bs4 import BeautifulSoup
from pymongo import MongoClient
# import redis
import time
import random
import re
from collections import deque
from itertools import cycle

import myfreeproxy
import myconstants


def crawl(index, url_queue, proxy_pool, user_agents):
    '''
    crawl urls in the queue
    use a different proxy each time
    '''

    while len(url_queue) != 0:
        sub_tour_list = []

        # get url from queue
        url = url_queue.popleft()

        try:
            # get next valid proxy
            proxy = next(proxy_pool)

            # get random user-agent
            user_agent = random.choice(user_agents)
            r = requests.get(
                url, headers={'user-agent': user_agent}, proxies=proxy, timeout=10)
            source = r.content.decode()
            soup = BeautifulSoup(source, 'lxml')

            tour_list_node = soup.find(
                'div', id="tour-list-view").find_all('div', class_="list-view-info")

            for tour_node in tour_list_node:
                title = tour_node.find('div', class_="tour-title").a.text
                link = tour_node.find('div', class_="tour-title").a['href']

                sub_tour_list.append({
                    "title": title,
                    "link": link
                })

                # if client.sadd('crawled_url', link) == 1:
                #     sub_tour_list.append({
                #         "title": title,
                #         "link": link
                #     })

            tour_list.extend(sub_tour_list)
        except Exception as e:
            print('Error:', e)


if __name__ == "__main__":
    # connect MongoDB
    client = MongoClient('localhost', 27017)
    db = client.tianbao
    collection = db.tour

    # connect redis
    # client = redis.StrictRedis()

    # define url root
    url_root = 'http://www.tianbaotravel.com/'

    # get number of pages
    url_anchor = 'http://www.tianbaotravel.com/tour/entry-1-505------.shtml'
    source = requests.get(url_anchor).content.decode()
    soup = BeautifulSoup(source, 'lxml')

    last_page = soup.find(id="tour-list-view").find('div',
                                                    class_="Jpagination").select("a")[-2]
    href = last_page['href']
    max_page = re.search('entry-(.*?)-', href).group(1)

    # initialize url queue
    url_queue = deque()

    for i in range(1, int(max_page)+1):
        url = url_root + f'tour/entry-{i}-505------.shtml'
        url_queue.append(url)

    # initialize tour list
    tour_list = []

    # get valid proxy list
    proxy_list = myfreeproxy.get_proxies(10)
    proxy_pool = cycle(proxy_list)

    # initialize thread list
    thread_list = []

    for i in range(1, 6):
        thread = threading.Thread(
            target=crawl, args=(i, url_queue, proxy_pool, myconstants.user_agents))
        thread_list.append(thread)

    # record start time
    start = time.time()

    # start threads
    for thread in thread_list:
        thread.start()

    # wait for threads finish
    for thread in thread_list:
        thread.join()

    # insert tours into database
    if len(tour_list) > 0:
        collection.insert_many(tour_list)

    # record end time
    end = time.time()

    time_used = end - start
    print(f'Total time is: {time_used:.2f} seconds')
    print('Done')
