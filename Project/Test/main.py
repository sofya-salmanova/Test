import http.server


def run(server_class=http.server.HTTPServer,
        handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class HttpProcessor(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>I'm GET</h1></body></html>")


    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>I'm POST</h1></body></html>")


    def do_HEAD(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>I'm HEAD</h1></body></html>")


run(handler_class=HttpProcessor)
