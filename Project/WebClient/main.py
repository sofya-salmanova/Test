from sys import exc_info
import os
from urllib.parse import quote_plus, unquote_plus

import requests
import click


@click.command()
@click.argument('address')
@click.option('--protocol', default='http://')
@click.option('--port', default='8000')
@click.option('--root-dir', default=os.getcwd() + '/Files')
def main_loop(protocol, address, port, root_dir):
    """
    Connect to some Web-server

    address (server address without http://) \n
    --protocol (default http://) \n
    --port (default 8000) \n
    --root-dir (default CWD/Files)

    """
    command_dict = {1:'get', 2:'post', 3:'head', 4:'list', 0:'exit'}
    while True:

        for key, value in command_dict.items():
            print(f'[{key}] {value}')

        while True:
            try:
                index = int(input())
                if command_dict.get(index) is not None:
                    break
            except:
                continue

        if index == 0:
            break
        elif 0 < index < 4:
            connect(command_dict.get(index), protocol, address, port, root_dir)
        else:
            connect('get', protocol, address, port, root_dir, path = '/list')


def connect(method, protocol, address, port, root_dir, path=''):

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
        print(exc_info()[0])
        raise SystemExit()

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
                if 0 <= index <= len(list):
                    break
            except:
                continue

        if index != 0:
            connect(method, protocol, address, port, root_dir, '/file/' + quote_plus(list[index - 1]))

    elif path[:6] == '/file/' and r.status_code != '404':

        while True:

            if not os.path.exists(root_dir):

                try:
                    os.makedirs(root_dir)
                except:
                    print(exc_info()[0])
                    print('[1] enter path manually')
                    print('[2] use CWD/Files')
                    print('[0] cancel saving')

                    while True:
                        try:
                            index = int(input())
                            if 0 <= index < 3:
                                break
                        except:
                            continue

                    if index == 1:
                        root_dir = os.getcwd() + '/Files'
                    elif index == 2:
                        root_dir = input('enter correct path')
                    else:
                        break
            else:
                # Записываем файл в существующую директорию.
                # Если файл с таким именем уже есть, то перезаписываем его

                file_name = unquote_plus(path[6:])

                file = open(root_dir + '/' + file_name, 'wb')
                file.write(r.content)
                file.close()
                print(f'file {file_name} download in {root_dir}')
                break

    else:
        print(r.status_code)
        print(r.headers)
        print(r.content)

if __name__ == '__main__':
    main_loop()



