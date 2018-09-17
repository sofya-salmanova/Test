import sys
import requests
import click

@click.command()
@click.argument('address')
@click.option('--protocol', default='http://')
@click.option('--port', default='8000')
def main_loop(protocol, address, port):
    command_dict = {1:'get', 2:'post', 3:'head', 4:'list', 0:'exit'}
    while True:

        for key, value in command_dict.items():
            print(f'[{key}] {value}')

        while True:
            try:
                index = int(input())
                if command_dict.get(index) != None:
                    break
            except:
                continue

        if index == 0:
            break
        elif 0 < index < 4:
            connect(command_dict.get(index), protocol, address, port)
        else:
            connect('get', protocol, address, port, path = '/list')


def connect(method, protocol, address, port, path = ''):
    """
    Connect to some Web-server

    address (server address without http://) \n
    --protocol (default http://) \n
    --port (default 8000)

    """
    url = protocol + address + ':' + port + path
    method = method.lower()


    try:
        r = getattr(requests, method)(url)
    except AttributeError:
        print('input method %s is not supported' % method)
        raise SystemExit()
    except requests.exceptions.ConnectionError:
        print("can't connect")
        raise SystemExit()
    except:
        print(sys.exc_info()[0])
        raise SystemExit()

    print(r.status_code)
    print(r.headers)

    if path == '/list':

        list = r.text.split(';')

        count = 1
        for file in list:
            print(f'[{count}] {file}')
            count += 1
        print('[0] exit')

        while True:
            try:
                index = int(input())
                break
            except:
                continue

        if index != 0:
            connect(method, protocol, address, port, '/file/' + list[index - 1])
    else:
        print(r.content)

if __name__ == '__main__':
    main_loop()



