#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import traceback
import docker


client = docker.from_env()


# noinspection PyPep8Naming
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.do_update()

    def do_POST(self):
        self.do_update()

    def do_PUT(self):
        self.do_update()

    def result(self, status, message=None):
        if message:
            self.send_response(status)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(message, 'utf8'))
        else:
            self.send_response(status)
            self.end_headers()

    def do_update(self):
        try:
            self.update()
        except:
            traceback.print_exc()
            self.result(500, 'Internal error - check logs')

    def update(self):
        print(f"IN {self.path}")
        path = self.path[1:]

        if '/' not in path:
            self.result(400, f"Path must be /service-name/image-name")
            return

        service_name, image = path.split("/", maxsplit=1)
        print(f"Received request for '{service_name}' '{image}'")

        services = client.services.list(filters=dict(name=service_name))

        if len(services) != 1:
            self.result(400, f"Did not find 1 instance of {service_name}")
            return

        services[0].update(image=image)

        print(f"DONE {self.path}")
        self.result(200)


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        port = int(argv[1])
    else:
        port = 8000

    httpd = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Serving on 0.0.0.0:{port}")
    httpd.serve_forever()
