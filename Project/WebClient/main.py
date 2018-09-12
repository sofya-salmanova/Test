import requests

r = requests.get('http://localhost:8000')
print(r.content)

r = requests.post('http://localhost:8000')
print(r.content)

r = requests.head('http://localhost:8000')
print(r.content)
print(r.headers)


