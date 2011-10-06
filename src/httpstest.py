'''
Created on Oct 6, 2011

@author: yongkimleng
'''

import socket, os
from socketserver import BaseServer
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
import ssl


class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        
        ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        
        fpem = '../cacert.crt'
        ctx.load_verify_locations(fpem)
        ctx.verify_mode = ssl.CERT_NONE
        
        self.socket = ssl.SSLSocket(ctx, socket.socket(self.address_family,
                                                       self.socket_type),
                                    certfile = fpem)
        self.server_bind()
        self.server_activate()

class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        #
        # something
        #
        #self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        #self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        print("HTTP HEAD")
        print(self.requestline)
        
    def do_GET(self):
        print("HTTP GET")
        print(self.requestline)
    
    def do_CONNECT(self):
        print("HTTP CONNECT")
        print(self.requestline)

        

def test(HandlerClass = SecureHTTPRequestHandler,
         ServerClass = SecureHTTPServer):
    server_address = ('', 4033) # (address, port)
    httpd = ServerClass(server_address, HandlerClass)
    sa = httpd.socket.getsockname()
    print("Serving HTTPS on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()

def test2(HandlerClass = ProxyHTTPRequestHandler,
         ServerClass = HTTPServer):
    server_address = ('', 8080) # (address, port)
    httpd = ServerClass(server_address, HandlerClass)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()

if __name__ == '__main__':
    test2()