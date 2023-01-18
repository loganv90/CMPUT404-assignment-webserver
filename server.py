#  coding: utf-8 
import socketserver, os

# Copyright 2023 Logan Vaughan, Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):


    def get_response(self, path):
        base_path = "./www/" + path

        if not os.path.exists(base_path) or ".." in os.path.normpath(base_path):
            return "HTTP/1.1 404 Not Found\r\n\n"

        if os.path.isdir(base_path) and not base_path.endswith('/'):
            return "HTTP/1.1 301 Moved Permenantly\r\nLocation: " + path + "/\r\n\n"

        if os.path.isdir(base_path) and not os.path.exists(base_path + "index.html"):
            return "HTTP/1.1 404 Not Found\r\n\n"

        if os.path.isdir(base_path):
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\n"
            with open(base_path + "index.html", 'r') as f:
                response += f.read()
            return response

        if os.path.exists(base_path) and base_path.endswith('.html'):
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\n"
            with open(base_path, 'r') as f:
                response += f.read()
            return response

        if os.path.exists(base_path) and base_path.endswith('.css'):
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\n"
            with open(base_path, 'r') as f:
                response += f.read()
            return response

        if os.path.exists(base_path):
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\n"
            with open(base_path, 'r') as f:
                response += f.read()
            return response

        return "HTTP/1.1 404 Not Found\r\n\n"
    

    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print("Got a request of:\n%s\n" % self.data)

        request_info = self.data.decode("utf-8").split("\r\n")[0].split(" ")
        response = ''
        
        if len(request_info) < 2 or request_info[0].upper() != "GET":
            response = "HTTP/1.1 405 Method Not Allowed\r\n\n"
        else:
            response = self.get_response(request_info[1])

        self.request.sendall(bytearray(response,'utf-8'))
        #print("Sent a response of:\n%s\n" % response)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
