import sys
import os
import logging

from http import HTTPStatus
import magic
from urllib.parse import quote_plus, unquote_plus
from envparse import env


SERVER_ROOT_DIR = env.str('SERVER_ROOT_DIR', default=os.getcwd() + '/Files/')


def application(environ, start_response):
    status = HTTPStatus.OK
    path = environ['REQUEST_URI']


    if path == '/':
        try:
            linklist = []
            for file in os.listdir(root_dir):
                linklist.append(f'<a href="{quote_plus(root_dir + file)}" download="">{file}</a>')

            body = '<br/>'.join(linklist).encode()
        except:
            status = HTTPStatus.INTERNAL_SERVER_ERROR
            body = str(sys.exc_info()[0]).encode()
    else:
        # Если пришел запрос на файл, пытаемся отправить его
        try:
            handle = open(unquote_plus(path), 'rb')
            body = handle.read()
            handle.close()
        except:
            logging.warning(sys.exc_info()[0])
            body = b"<html><body><h1>File not found</h1></body></html>"
            status = HTTPStatus.NOT_FOUND

    start_response(str(status.value) + ' ' + status.name, [('Content-Type', magic.from_buffer(body, mime = True))])
    return [body]