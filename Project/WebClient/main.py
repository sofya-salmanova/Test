import requests
import argparse

parser = argparse.ArgumentParser(description='Connect to some Web-server.')
parser.add_argument('method', default='get', help='supported methods: get, post, head')
parser.add_argument('protocol', default='http://')
parser.add_argument('address', default='localhost', help='server address without http://')
parser.add_argument('port', default='8000')

args = parser.parse_args()
url = args.protocol + args.address + ':' + args.port
method = args.method.lower()


try:
    r = getattr(requests, method)(url)
except AttributeError:
    print('input method %s is not supported' % method)
    raise SystemExit()

print(r.status_code)
print(r.headers)
print(r.content)





