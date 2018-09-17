import sys
import os
from http import server, HTTPStatus
import click
import magic

@click.command()
@click.option('--root-dir', default=os.getcwd() + '/Files')
@click.option('--port', default=8000)
def run(root_dir, port):
    global root_directory
    root_directory = root_dir

    server_address = ('', port)
    httpd = server.HTTPServer(server_address, HttpProcessor)
    httpd.serve_forever()

class HttpProcessor(server.BaseHTTPRequestHandler):
    MIME_TYPE_PLAIN = 'plain/text'
    MIME_TYPE_HTML = 'text/html'


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

        status = HTTPStatus.OK

        if self.path == '/list':
            body = ';'.join(os.listdir(root_directory)).encode()
        elif self.path[:6] == '/file/':
            try:
                handle = open(root_directory + self.path[5:], 'rb')
                body = handle.read()
                handle.close()
            except:
                print(sys.exc_info()[0])
                body = b"<html><body><h1>File not found</h1></body></html>"
                status = HTTPStatus.NOT_FOUND
        else:
            body = b"<html><body><h1>I'm GET</h1></body></html>"

        self.response_common_part(status, body, magic.from_buffer(body, mime = True))


    def do_POST(self):
        body = b"<html><body><h1>I'm POST</h1></body></html>"
        self.response_common_part(HTTPStatus.CREATED, body, self.MIME_TYPE_HTML)


    def do_HEAD(self):
        body = b"<html><body><h1>I'm GET</h1></body></html>"
        self.response_common_part(HTTPStatus.NO_CONTENT, body, self.MIME_TYPE_HTML)


if __name__ == "__main__":
    run()
