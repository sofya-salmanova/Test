import sys
import os
import logging
from urllib.parse import unquote_plus

from http import server, HTTPStatus
import magic

global root_directory

class HttpProcessor(server.BaseHTTPRequestHandler):
    MIME_TYPE_PLAIN = 'plain/text'
    MIME_TYPE_HTML = 'text/html'

    def form_body(self):
        status = HTTPStatus.OK

        if self.path == '/list':
            # Если пришел запрос на список файлов, формируем его и отправляем клиенту
            try:
                body = ';'.join(os.listdir(root_directory)).encode()
            except:
                status = HTTPStatus.INTERNAL_SERVER_ERROR
                body = sys.exc_info()[0].encode()

        elif self.path[:6] == '/file/':
            # Если пришел запрос на файл, пытаемся отправить его
            try:
                handle = open(root_directory + unquote_plus(self.path[5:]), 'rb')
                body = handle.read()
                handle.close()
            except:
                logging.warning(sys.exc_info()[0])
                body = b"<html><body><h1>File not found</h1></body></html>"
                status = HTTPStatus.NOT_FOUND
        else:
            body = b"<html><body><h1>I'm GET</h1></body></html>"

        return body, status

    def response_common_part(self, status, body=None, content_type=None, proto_ver="1.1"):
        content_type = content_type or self.MIME_TYPE_PLAIN

        self.protocol_version = f"HTTP/{proto_ver}"
        self.send_response(status)
        self.send_header('User-Agent', 'SofyaWeb')

        if body is not None:
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))

        self.end_headers()

        if body is not None and self.command != 'HEAD':
            self.wfile.write(body)

    def do_GET(self):
         body, status = self.form_body()
         self.response_common_part(status, body, magic.from_buffer(body, mime = True))

    def do_POST(self):
        body = b"<html><body><h1>I'm POST</h1></body></html>"
        self.response_common_part(HTTPStatus.CREATED, body, self.MIME_TYPE_HTML)

    def do_HEAD(self):
        body, status = self.form_body()
        self.response_common_part(status, body, magic.from_buffer(body, mime = True))
