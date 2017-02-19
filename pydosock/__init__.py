#!/bin/env python
from __future__ import print_function

__author__ = 'Aldo Ridhoni'

import os, json, re, fnmatch
try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from http.server import HTTPServer, BaseHTTPRequestHandler

from socketdocker import SocketDocker
from configreader import ConfigReader

class RequestHandler(BaseHTTPRequestHandler):
    def send_json(self, response):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        #self.send_header('Connection', 'close')
        self.end_headers()
        try:
            self.wfile.write(json.dumps(response))
        except:
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def send_request_socket(self, method):
        resp = getattr(service, method + '_http')
        content_len = int(self.headers.get('content-length', 0))
        try:
            data = self.rfile.read(content_len)
            resp = resp(self.path, data).read
        except:
            resp = resp(self.path).read

        resp_decoded = resp().decode('utf-8')
        if len(resp_decoded):
            resp_obj = json.loads(resp_decoded)
        else:
            resp_obj = resp_decoded
        self.send_json(resp_obj)

    def do_GET(self):
        self.send_request_socket('get')

    def do_POST(self):
        self.send_request_socket('post')

    def do_DELETE(self):
        self.send_request_socket('delete')

if __name__ == '__main__':
    config = ConfigReader()
    service = SocketDocker(config.socket)
    httpd = HTTPServer((config.host, config.port), RequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
