import socket
import os
import logging

#////////////////////////// CONSTANTS ///////////////////////////////////////
LISTEN_ADDRESS = '127.0.0.1'
PORT_LISTEN = 80
SOCEKET_COUTN_LISTEN = 5
BLOCK_SIZE_SOCKET_READ = 4096

#///////////////////////Constants path
FILE_MIME_TYPES = 'mime_types.txt'
LOAD_INDEX_PAGE = 'index.html';
PATH_TO_DIRICOTRY_FILES = ''
PAGE_FILE_NOT_FOUND = '404.html'
#////////////////////////////////////////////////////////////////////////////

#loads mime types
mime_type = {};
try:
    f = open(FILE_MIME_TYPES, 'r')
    for line in f:
        exten, mime = line.split('	')
        mime_type[exten] = mime
except IOError:
    print 'Error, file mime type dont loading'   



#recieve responce
def receive(sock):
    block_size = BLOCK_SIZE_SOCKET_READ
    reques = ''
    while True:
        reques += sock.recv(block_size)
        if(reques.find('\r\n\r\n') > 1):
            break; #chitaem do etogo simbola esli
            # ne ukazan v zagolovke Content-Length or Transfer-Encoding, esli ukazan to chitaem body
    return reques


def parse_method(header):
   return  header.split(' ') #(method, url, http_protocol)


def process_client(sock):
    request = receive(sock).split("\r\n") 
    
    (method, url, http_protocol) = parse_method(request[0])
    print 'method=' + method
    print 'url='+ url
    print 'http_protocol=' + http_protocol
    
    headers = {}
    for header in request[1:len(request)-2]:  #start s one and delete last \r\n
        if header == "\r\n" :
            break
        k, v = header.split(":", 1)
        headers[k] = v
        
    headers['url'] = url
    headers['http_protocol'] = http_protocol
    headers['method'] = method
    
    print 'end headers execute\n'    
    send_data_to_client(sock, url) 

def formated_path_to_file(url):
    if len(url) == 1 and url == '/':
        url += LOAD_INDEX_PAGE
    path = PATH_TO_DIRICOTRY_FILES + url[1:]
    print 'path=' + path
    return path;

def open_or_throw_file(path):
    f = open(path, "rb")
    fileContent = f.read()
    return fileContent

def send_all(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        total_sent += sent
        
def send_data_to_client(sock, url):
    path = formated_path_to_file(url)

    status = '200 OK'
    if not os.path.exists(path):
        status = '404 Not Found'
        path = PATH_TO_DIRICOTRY_FILES + PAGE_FILE_NOT_FOUND

    extension = os.path.splitext(path)[1][1:] #file extension and delete '.'
    filesize = os.path.getsize(path)
    try:
      fileContent = open_or_throw_file(path)
      sock.send("HTTP/1.1 "+ status +"\r\n")
      sock.send("Content-Length: "+str(filesize)+"\r\n")
      sock.send("Content-Type: "+ mime_type[extension] +"\r\n") 
      send_all(sock, fileContent)
      sock.close()  
    except IOError as e:
        print 'Error opening file=' + e
        
    
      

def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LISTEN_ADDRESS, PORT_LISTEN))
    server_socket.listen(5)
    #logging.info('server socket created')
    return server_socket


def start_server():
    serversocket = create_server_socket()

    while 1:
        (clientsocket, address) = serversocket.accept()
        try:
            process_client(clientsocket)
        except Exception as e:
            #logging.error('error!\n{}'.format(traceback.format_exc()))
            print e
            clientsocket.close()


print 'server start'
#logging.basicConfig(level=logging.DEBUG)
start_server()
