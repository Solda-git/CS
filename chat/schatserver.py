"""
edu project - chat

SChatServer class

server part
"""
import json
from socket import *
from lib.routines import Messaging, logdeco
from lib.settings import MAX_CONNECTIONS, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, ONLINE, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER
import select
from contextlib import closing

import logging
import log.config.server_log_config

s_logger = logging.getLogger('server.log')

class SChatServer(Messaging):
    """
    """
    @logdeco
    def __init__(self, address, port):
        
        try:
            self.server_socket = socket(AF_INET,SOCK_STREAM)

            if (address==""):
                address = DEFAULT_IP_ADDRESS
            if port <= 0:
                port =  DEFAULT_PORT    
            self.server_socket.bind((address, port))    

            self.server_socket.settimeout(0.2)
            # self.server_socket.bind((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
            self.server_socket.listen()
            s_logger.info(f"Server is listening the port: {port}")
            #initialize(drop) client's list
            self.clients = []
            self.messages = []
        except error:
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
            s[0].close()
    
    @logdeco
    def close_client(self, s):
        """
            normal closing of client socket
            looking for s socket, remove from the clients socket list and close it
        """
        for i in range(len(self.clients)):
            if s == self.clients[i][0]:
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
            self.messages.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
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
        #
        print('SChatServer.run()')
        while True:
            try:
                # getting the client socket and  adding it to the cliest list
                client_socket, client_address = self.server_socket.accept()
            except OSError:
                pass #no clients connected during timeout period
            else:
                print(f'Client {client_address} connected.')
                s_logger.info(f'Connection established. Client details: {client_address}.')
                self.clients.append((client_socket, client_address))

            receiver_list = []
            sender_list = []
            #err_list = []

            try:
                if self.clients: # there are active client(s) connected to the server
                    receiver_list, sender_list, err_list = select.select(self.clients, self.clients, [], 0)
            except OSError as os_error:
                    pass
            if receiver_list:
                for sender in receiver_list:
                    try:
                        self.parse_message(self.get_message(sender), sender)
                    except:
                        s_logger.info(f'Client {sender.getpeername()} has disconnected.')
                        clients.remove(sender)

            if self.messages and sender_list:
                message = {
                    COMMAND: MESSAGE,
                    SENDER: messages[0][0],
                    TIMESTAMP: time(),
                    MESSAGE_TEXT: messages[0][1]
                }
                del messages[0]
                for awaiter in sender_list:
                    try:
                        self.send_message(awaiter, message)
                    except:
                        s_logger.info(f'Client {awaiter.getpeername()} has disconnected.')
                        clients.remove(awaiter)

