import http.server


def run(server_class=http.server.HTTPServer,
        handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class HttpProcessor(http.server.BaseHTTPRequestHandler):
    def response_common_part(self, code, message, body):
        self.protocol_version = "HTTP/1.1"
        self.send_response(code, message)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()

    def do_GET(self):
        body = b"<html><body><h1>I'm GET</h1></body></html>"
        self.response_common_part(200, 'OK', body)
        self.wfile.write(body)


    def do_POST(self):
        body = b"<html><body><h1>I'm POST</h1></body></html>"
        self.response_common_part(201, 'Created', body)
        self.wfile.write(body)


    def do_HEAD(self):
        body = b"<html><body><h1>I'm GET</h1></body></html>"
        self.response_common_part(204, 'No Content', body)


if __name__ == "__main__":
    run(handler_class=HttpProcessor)
