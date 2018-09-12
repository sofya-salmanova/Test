import http.server


def run(server_class=http.server.HTTPServer,
        handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class HttpProcessor(http.server.BaseHTTPRequestHandler):
    def response_common_part(self, content_length=0):
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(content_length))
        self.end_headers()

    def do_GET(self):
        body = b"<html><body><h1>I'm GET</h1></body></html>"
        self.response_common_part(len(body))
        self.wfile.write(body)


    def do_POST(self):
        body = b"<html><body><h1>I'm POST</h1></body></html>"
        self.response_common_part(len(body))
        self.wfile.write(body)


    def do_HEAD(self):
        self.response_common_part(0)


if __name__ == "__main__":
    run(handler_class=HttpProcessor)
