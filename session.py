import requests

login_url = 'http://exercise.kingname.info/exercise_login'
login_success_url = 'http://exercise.kingname.info/exercise_login_success'

data = {
    'username': 'kingname',
    'password': 'genius',
    'rememberme': 'Yes'
}

session = requests.Session()
before_login = session.get(login_success_url).text
print(before_login)

print('===starting to login===')
session.post(login_url, data=data)
after_login = session.get(login_success_url).text
print(after_login)
