"""
edu project - chat

SChatServer class

server part
"""
import json
from socket import *
from lib.routines import Messaging, logdeco
from lib.settings import MAX_CONNECTIONS, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, ONLINE, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER, Port
import select
from contextlib import closing
from time import time
import logging
import log.config.server_log_config

s_logger = logging.getLogger('server.log')

class SChatServer(Messaging):
    """
    """
    port = Port()

    def __init__(self, address, port):
        
        try:
            self.server_socket = socket(AF_INET,SOCK_STREAM)
            # self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR) #nonblocking socket!

            if (address==""):
                address = DEFAULT_IP_ADDRESS
            
            self.port = port if port else DEFAULT_PORT    
            self.server_socket.bind((address, self.port))    

            self.server_socket.settimeout(0.2)
            # self.server_socket.bind((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
            self.server_socket.listen()
            s_logger.info(f"Server is listening the port: {self.port}")
            #initialize(drop) client's list
            self.clients = []
            self.messages = [] #Clients messages tuple in format (sender, data, socket)
        except error as e:
            s_logger.exception(f"Server connection error accured: {e.strerror}")

    def __del__(self):
        """
        closing sockets
        """
        #closing server socket
        self.server_socket.close()
        s_logger.info('Server socket closed')

        #closing all the client sockets
        while (len(self.clients)):
            s = self.clients.pop()
            s.close()
    
    @logdeco
    def close_client(self, s):
        """
            normal closing of client socket
            looking for s socket, remove from the clients socket list and close it
        """
        for i in range(len(self.clients)):
            if s == self.clients[i]:
                self.clients.pop()
                s.close()   
                break

    @logdeco
    def parse_message(self, message, client):
        """
        function parses incoming message and processes it.

        :param message:
        :return: dict with response code
        """
        s_logger.debug(f'Parsing message: {message}')
        if COMMAND in message and message[COMMAND] == ONLINE and TIMESTAMP in message \
            and USER in message and ACCOUNT_NAME in message[USER] and message[USER][ACCOUNT_NAME] == 'guest':
            s_logger.info(f'Correct message recieved:{message}')
            self.send_message(client,           
                                {
                                    RESPONSE: 200
                                }
                             )
            return
        elif COMMAND in message and message[COMMAND] == MESSAGE and TIMESTAMP in message \
            and MESSAGE_TEXT in message:
            # self.messages.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
            ####new code###
            self.messages.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT], client))
            ###end of new code###


            print(f'Message with {message[COMMAND]} command')
            return 

        s_logger.error(f'Incorrect message {message}. Bad request.')
        return {
            RESPONSE: 400,
            ERROR: 'Bad request'
        }             

    def run(self): 
        """
        running infinity cycle with homework task completion
        """
        while True:
            try:
                # getting the client socket and  adding it to the cliest list
                client_socket, client_address = self.server_socket.accept()
            except OSError:
                pass #no clients connected during timeout period
            else:
                print(f'Client {client_address} connected.')
                s_logger.info(f'Connection established. Client details: {client_address}.')
                # self.clients.append((client_socket, client_address))
                self.clients.append(client_socket)
            receiver_list = []
            sender_list = []
            err_list = []

            try:
                if self.clients: # there are active client(s) connected to the server
                    receiver_list, sender_list, err_list = select.select(self.clients, self.clients, [], 0)
            except OSError:
                    pass
            if receiver_list:
                for sender in receiver_list:
                    try:
                        self.parse_message(self.get_message(sender), sender)
                    except:
                        # s_logger.info(f'Client {sender.getpeername()} has disconnected.')
                        s_logger.info(f'Client {sender} has disconnected.')
                        self.clients.remove(sender)

            if self.messages and sender_list:
                message = {
                    COMMAND: MESSAGE,
                    SENDER: self.messages[0][0],
                    TIMESTAMP: time(),
                    MESSAGE_TEXT: self.messages[0][1]
                }
                echo_client =  self.messages[0][2]   #new code
                del self.messages[0]
                for awaiter in sender_list:
                    try:
                        if not(awaiter is echo_client): # new code
                            self.send_message(awaiter, message)
                    except:
                        s_logger.info(f'Client {awaiter.getpeername()} has disconnected.')
                        self.clients.remove(awaiter)

