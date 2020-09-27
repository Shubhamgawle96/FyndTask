import requests

url = 'http://127.0.0.1:5000/test_add'
myobj = {'name': 'testaddapi', 'score': '89', 'director': 'bjmkmb', 'genre': 'mkjmn', 'popularity': '7', '': ''}
x = requests.post(url, data = myobj)

print("hello",x.text)