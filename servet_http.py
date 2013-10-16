import socket
import logging

#////////////////////////// CONSTANTS ///////////////////////////////////////
LISTEN_ADDRESS = '127.0.0.1'
PORT_LISTEN = 80
SOCEKET_COUTN_LISTEN = 5
BLOCK_SIZE_SOCKET_READ = 4096
LOAD_INDEX_PAGE = 'index.html';
PATH_TO_DIRICOTRY_FILES = ''
PAGE_FILE_NOT_FOUND = '404.html'
#////////////////////////////////////////////////////////////////////////////

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
    for header in request[1:len(request)-2]:  #start s one
        print header
        if header == "\r\n" :
            break
        k, v = header.split(":", 1)
        headers[k] = v
    headers['url'] = url
    headers['http_protocol'] = http_protocol
    headers['method']=method
    
    print 'end headers execute\n'    
    send_data_to_client(sock, url) 
    #print headers
    #sock.send("HTTP/1.0 200 OK\r\n")       
    #sock.send("Content-Type: text/plain\r\n")  
    #sock.send("\r\n")                           
    #sock.send("Hi there!")                    
    #sock.close()  
    #print responce

def send_file_noit_found(sock):
    sock.send("HTTP/1.0 404 Not Found\r\n")       
    sock.send("Content-Type: text/plain\r\n")  
    sock.send("\r\n")                           
    sock.send(send_data_to_client(sock, '/' + PAGE_FILE_NOT_FOUND))                    
    sock.close()  

def formated_path_to_file(url):
    if len(url) == 1 and url == '/':
        url += LOAD_INDEX_PAGE
    path = PATH_TO_DIRICOTRY_FILES + url[1:]
    print 'path=' + path
    return path;

def open_or_throw_file(path):
    f = open(path, 'rb')
    fileContent = f.read()
    return fileContent

    #except IOError:
     #  print 'Oh dear.'

def send_data_to_client(sock, url):
    path = formated_path_to_file(url)
    
    try:
      fileContent = open_or_throw_file(path)
      sock.send("HTTP/1.0 200 OK\r\n")       
      sock.send("Content-Type: text/plain\r\n")  
      sock.send("\r\n")                           
      sock.send(fileContent)                    
      sock.close()  
    except IOError:
        print 'file not found'
        send_file_noit_found(sock)
        
    
      

def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LISTEN_ADDRESS, PORT_LISTEN))
    server_socket.listen(5)
    logging.info('server socket created')
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
