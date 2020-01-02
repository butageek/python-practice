import requests
import os
import threading
import time
from collections import deque


def crawl(index, queue):
    '''
    crawl urls in the queue
    '''

    while len(queue) != 0:
        url = queue.popleft()
        try:
            r = requests.get(url, timeout=10)
            print(len(queue), 'Thread', index, r.status_code, url)
        except Exception as e:
            print(len(queue), 'Thread', index, url, 'Error:', e)


# main
if __name__ == "__main__":
    # get websites file path
    script_dir = os.path.dirname(__file__)
    filename = 'alexa.txt'
    file_path = os.path.join(script_dir, filename)

    # initialize url queue
    url_queue = deque()

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            url = line.split('\t')[1].replace('\n', '')
            url_queue.append(url)

    # initialize thread list
    thread_list = []

    for i in range(1, 5):
        thread = threading.Thread(target=crawl, args=(i, url_queue))
        thread_list.append(thread)

    # record start time
    start = time.time()

    # start threads
    for thread in thread_list:
        thread.start()

    # wait for threads finish
    for thread in thread_list:
        thread.join()

    # record end time
    end = time.time()

    print('Total time is: {}'.format(end - start))
    print('Done')
