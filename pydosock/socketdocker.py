from __future__ import print_function
import sys, socket, json
try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection

class BaseSocketDocker(object):
    server = ''

    def __init__(self, server):
        self.__class__.server = server
        self.url = ''
        self.data = None

    def open_http(self, method):
        headers = {}
        headers['Host'] = 'localhost'
        #headers['Connection'] = 'close'

        http_conn = self.socket_http_factory(self.url)

        if self.data is not None:
            headers['Content-Type'] = 'application/json'
            http_conn.request(method, self.url, self.data, headers)
        else:
            http_conn.request(method, self.url, headers=headers)

        try:
            response = http_conn.getresponse()
            return response
        except Exception as e:
            print(e)
            return None

    @classmethod
    def socket_http_factory(cls, host):
        http = HTTPConnection(host, 80)
        http.sock = cls.socket_conn(cls.server)
        return http

    @staticmethod
    def socket_conn(server):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.connect(server)
            return sock
        except PermissionError:
            print('Permission error while opening socket')
            return None



class SocketDocker(BaseSocketDocker):

    def get_http(self, path):
        self.url = path
        return self.open_http('GET')

    def post_http(self, path, data):
        print(path)
        print(data)
        self.url = path
        self.data = data
        return self.open_http('POST')

    def delete_http(self, path, data):
        self.url = path
        self.data = data
        return self.open_http('DELETE')
