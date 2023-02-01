import argparse
import threading
from _thread import *
import sys
import socket
from socket import socket as Socket

# A simple web server


def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind(('', args.port))
        server_socket.listen(1)

        print("server ready")

        while True:

            connection_socket = server_socket.accept()[0]
            print("Connection Accepted")
            start_new_thread(http_handle, (connection_socket,))
                
                # This is a hackish way to make sure that we can receive and process multi
                # line requests.
                #connection_socket.sendall(reply)

def req_handle(connection_socket):
    request=""
    received=connection_socket.recv(1024).decode('utf-8')
    request+=received
    http_handle(request, connection_socket)

def http_handle(connection_socket):
    request_string=""
    received=connection_socket.recv(1024).decode('utf-8')
    request_string+=received
    data = ""
    #request_string = request_string.rstrip()
    req = request_string[:request_string.find('\r')]
    req = req.split(" ")
    print(req)
    req_dic = {'METHOD' : req[0], 'URL' : req[1], 'VERSION' : req[2]}
    if "favicon" in request_string:
        data="HTTP/1.1 404 Not Found\r\n\r\n"
    
    if req_dic['METHOD'] != "GET":
        data = 'HTTP/1.1 501 Not Implemented\r\n\r\n'
    
    elif req_dic['VERSION'] != 'HTTP/1.1':
        data = 'HTTP/1.1 505 Version Not Supported\r\n\r\n'

    #elif req_dic['URL'] == '/' or req[1] == '/index.html':
    else:
        data = 'HTTP/1.1 200 OK\r\n'
        connection_socket.sendall(str.encode('HTTP/1.1 200 OK\n', 'utf-8'))
        data+= 'Connection: keep-alive\r\n'
        connection_socket.sendall(str.encode('Connection: keep-alive\n', 'utf-8'))
        data+= 'Content-Type: text/html; encoding=utf-8\r\n'
        connection_socket.sendall(str.encode('Content-Type: text/html; encoding=utf-8\n\n', 'utf-8'))
        f = open('index.html', 'r')
        # send data per line
        for l in f.readlines():
            data+=l
            connection_socket.sendall(str.encode(""+l+"", 'utf-8'))
        f.close()
        data+="\r\n\r\n"
    connection_socket.close()

    #else:
        #data="HTTP/1.1 404 Not Found\r\n\r\n"

    print("\n\nReceived request")
    print("======================")
    print(request_string.rstrip())
    print("======================")


    print("\n\nReplied with")
    print("======================")
    print(data.rstrip())
    print("======================")

if __name__ == "__main__":
    sys.exit(main())
