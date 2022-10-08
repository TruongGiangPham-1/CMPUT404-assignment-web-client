#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

from sqlite3 import connect
import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data: str):
#get_code gets the response code and then you change the code to whatever you get from the response
#they just have 500 there as a place holder
        assert(len(data) > 0) 
        dataToken = self.parseGetResponse(data)
        StatusLine =  dataToken[0]
        
        if ("404" in StatusLine):
            return 404
        elif ("200" in StatusLine):
            return 200
        else:
            return -1  # error code

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')


    
    def createGETrequestHeader(self, host:str, port:int, path:str):
        # host header specify the host and port this request is sent to 
        print("reached here")
        if (port != ''): 
            hostAndPort = host + ":" + str(port)  
        else:
            hostAndPort = host  # if they didint have port
        requestHeader = ""
        requestLine = f'GET {path} HTTP/1.1\r\n'
        HostHeader = f'Host: {hostAndPort}\r\n'
        ConnectionHeader = f'Connection: keep-alive\r\n'

        requestHeader = requestLine + HostHeader + ConnectionHeader + "\r\n"

        #print(requestHeader)
        return requestHeader

    def GET(self, url, args=None):
        # I need to connect to the server and get its body content
        code = 500
        body = ""
        o = urllib.parse.urlparse(url)
        print("in url, the host is  " , o.hostname)
        print("in url, the port is " , o.port)
        print("in url, the path is " , o.path)
        hostname = o.hostname
        port = o.port
        path = o.path

        # connect to the server to get the get
        requestHeader = self.createGETrequestHeader(hostname, port, path)
        #self.close()
        self.connect(hostname, port) 
        print("established connection")
        self.sendall(requestHeader)
        print("sent the data")
        response = self.recvall(self.socket)        
        print("response is")
        print(response)

        code = self.get_code(response)  # parse and get status code
        assert(code != -1)
        print("----")
        print("got the code", code)
        print("-----")
        self.close()

        return HTTPResponse(code, body)


    def POST(self, url, args=None):

        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    

    # split by \r\n to tokenize response header into subheaders
    def parseGetResponse(self, responseHeader):
        l = responseHeader.split("\r\n")
        return l

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
