import requests
import os
from multiprocessing.dummy import Process
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
            print(len(queue), 'Process', index, r.status_code, url)
        except Exception as e:
            print(len(queue), 'Process', index, url, 'Error:', e)


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

# initialize process list
process_list = []

for i in range(1, 5):
    p = Process(target=crawl, args=(i, url_queue))
    process_list.append(p)

# record start time
start = time.time()

# start processes
for p in process_list:
    p.start()

# wait for processes to finish
for p in process_list:
    p.join()

# record end time
end = time.time()

print('Total time is: {}'.format(end - start))
print('Done')
