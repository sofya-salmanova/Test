import os

from http import server
import click

import server as my_server


@click.command()
@click.option('--root-dir', default=os.getcwd() + '/Files')
@click.option('--port', default=8000)
def run(root_dir, port):
    """
    Web-server

    --root-dir (default CWD/Files) \n
    --port (default 8000)

    """
    my_server.HttpProcessor.root_directory = root_dir

    server_address = ('', port)
    httpd = server.HTTPServer(server_address, my_server.HttpProcessor)

    httpd.serve_forever()


if __name__ == "__main__":
    run()
