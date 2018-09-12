import requests
import argparse

parser = argparse.ArgumentParser(description='Connect to some Web-server.')
parser.add_argument('method', default='get', help='supported methods: get, post, head')
parser.add_argument('address', default='localhost', help='server address without http://')
parser.add_argument('port', default='8000')

args = parser.parse_args()
url = 'http://' + args.address + ':' + args.port
method = args.method.lower()

if method == 'get':
    r = requests.get(url)
elif method == 'post':
    r = requests.post(url)
elif method == 'head':
    r = requests.head(url)
else:
    print('input method is not supported')

if r.status_code == 200:
    print(r.content)
    print(r.headers)
else:
    print('Error:' + str(r.status_code))



