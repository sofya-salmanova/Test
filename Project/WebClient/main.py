import requests
import argparse

functions = {'get': requests.get, 'post': requests.post, 'head': requests.head}

parser = argparse.ArgumentParser(description='Connect to some Web-server.')
parser.add_argument('method', default='get', help='supported methods: get, post, head')
parser.add_argument('protocol', default='http://')
parser.add_argument('address', default='localhost', help='server address without http://')
parser.add_argument('port', default='8000')

args = parser.parse_args()
url = args.protocol + args.address + ':' + args.port
method = args.method.lower()


try:
    fmethod = functions[method]
except KeyError:
    print('input method %s is not supported' % method)
    raise SystemExit()

r = fmethod(url)
print(r.status_code)
print(r.content)
print(r.headers)




