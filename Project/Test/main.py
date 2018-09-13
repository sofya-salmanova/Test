from http import server, HTTPStatus


def run(server_class=server.HTTPServer,
        handler_class=server.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class HttpProcessor(server.BaseHTTPRequestHandler):
    MIME_TYPE_PLAIN = 'plain/text'
    MIME_TYPE_HTML = 'text/html'

    def response_common_part(self, status, body=None, content_type=None, proto_ver="1.1"):
        content_type = content_type or self.MIME_TYPE_PLAIN

        self.protocol_version = f"HTTP/{proto_ver}"
        self.send_response(status)

        if body is not None:
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))

        self.end_headers()

        if body is not None and self.command != 'HEAD':
            self.wfile.write(body)


    def do_GET(self):
        body = b"<html><body><h1>I'm GET</h1></body></html>"
        self.response_common_part(HTTPStatus.OK, body, self.MIME_TYPE_HTML)


    def do_POST(self):
        body = b"<html><body><h1>I'm POST</h1></body></html>"
        self.response_common_part(HTTPStatus.CREATED, body, self.MIME_TYPE_HTML)


    def do_HEAD(self):
        body = b"<html><body><h1>I'm GET</h1></body></html>"
        self.response_common_part(HTTPStatus.NO_CONTENT, body, self.MIME_TYPE_HTML)


if __name__ == "__main__":
    run(handler_class=HttpProcessor)
