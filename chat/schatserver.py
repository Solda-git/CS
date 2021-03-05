"""
edu project - chat

SChatServer class

server part
"""
import json
from socket import *
from lib.routines import Messaging
from lib.settings import MAX_CONNECTIONS, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, ONLINE, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS, RESPONSE, ERROR

from contextlib import closing

import logging
import log.config.server_log_config

s_logger = logging.getLogger('server.log')

class SChatServer(Messaging):
    """
    """

    def __init__(self, address, port):
        
        try:
            self.server_socket = socket(AF_INET,SOCK_STREAM)

            if (address==""):
                address = DEFAULT_IP_ADDRESS
            if port <= 0:
                port =  DEFAULT_PORT    
            self.server_socket.bind((address, port))    
            # self.server_socket.bind((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
            self.server_socket.listen()
            s_logger.info(f"Server is listening the port: {port}")
            #initialize(drop) client's list
            self.clients = []
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

    def parse_message(self, message):
        """
        function parses incoming message and processes it.

        :param message:
        :return: dict with response code
        """
        s_logger.debug(f'Parsing message: {message}')
        if COMMAND in message and message[COMMAND] == ONLINE and TIMESTAMP in message \
            and USER in message and ACCOUNT_NAME in message[USER] and message[USER][ACCOUNT_NAME] == 'guest':
            s_logger.info(f'Correct message recieved:{message}')
            return {
                RESPONSE: 200
            }
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
            # getting the client socket and  adding it to the cliest list
            
            client_socket, client_address = self.server_socket.accept()
            s_logger.info(f'Connection established. Client details: {client_address}.')
            with closing(client_socket) as cs:
                self.clients.append((client_socket, client_address))
                try:
                    client_message = self.get_message(client_socket)
                    s_logger.info(f'Received message {client_message} from client {client_address}.')
                    server_response = self.parse_message(client_message)
                    self.send_message(client_socket, server_response)
                    s_logger.info(f'Server answer: {server_response}')
                except (ValueError, json.JSONDecodeError) as e:
                    s_logger.exception("Incorrect client message received.")        
                    

