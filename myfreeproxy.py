import requests
from bs4 import BeautifulSoup


def get_proxies(max_proxies):
    '''
    get proxies and verify if usable
    return valid proxy list
    '''

    # define request headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    # get proxy table
    url = 'https://free-proxy-list.net/'

    print(f'Starting to get valid proxies from {url}')

    try:
        source = requests.get(
            url, headers=headers).content.decode('utf-8', 'ignore')
        soup = BeautifulSoup(source, 'lxml')
        proxy_rows = soup.find('table', id='proxylisttable').find(
            'tbody').find_all('tr')
    except Exception as e:
        print(f'Error: {e}')

    proxy_list = []

    i = 1

    for proxy_row in proxy_rows:
        if i > max_proxies:
            break

        # get https proxies
        https = proxy_row.select('tr > td:nth-of-type(7)')[0].text

        if https == 'yes':
            ip_address = proxy_row.select('tr > td:nth-of-type(1)')[0].text
            port = proxy_row.select('tr > td:nth-of-type(2)')[0].text

            # add valid proxy to list
            try:
                proxy = {'https': f'https://{ip_address}:{port}'}
                test_url = 'https://www.google.ca/'
                r = requests.get(test_url, headers=headers, timeout=5)

                if r.status_code == 200:
                    proxy_list.append(proxy)
                    i += 1
            except:
                continue

    print('Finished getting proxies')

    return proxy_list
