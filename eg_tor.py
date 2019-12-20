import requests
from stem import Signal
from stem.control import Controller


proxies = {
    'http': 'http://127.0.0.1:8118',
    'https': 'https://127.0.0.1:8118'
}

with Controller.from_port(port=9051) as controller:
    controller.authenticate(password='password')
    controller.signal(Signal.NEWNYM)

r = requests.get('https://httpbin.org/ip', proxies=proxies)
print(r.text)
