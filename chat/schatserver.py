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

class SChatServer(Messaging):
    """
    """

    def __init__(self, address, port):
        self.server_socket = socket(AF_INET,SOCK_STREAM)

        if (address==""):
            address = DEFAULT_IP_ADDRESS
        if port <= 0:
            port =  DEFAULT_PORT    
        self.server_socket.bind((address, port))    
        # self.server_socket.bind((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
        self.server_socket.listen()

        #initialize(drop) client's list
        self.clients = []
 
    def __del__(self):
        """
        closing sockets
        """
        #closing server socket
        self.server_socket.close()

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
        if COMMAND in message and message[COMMAND] == ONLINE and TIMESTAMP in message \
            and USER in message and ACCOUNT_NAME in message[USER] and message[USER][ACCOUNT_NAME] == 'guest':
            return {
                RESPONSE: 200
            }
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
            with closing(client_socket) as cs:
                self.clients.append((client_socket, client_address))
                try:
                    client_message = self.get_message(client_socket)
                    print(client_message)
                    server_response = self.parse_message(client_message)
                    self.send_message(client_socket, server_response)
                except (ValueError, json.JSONDecodeError):
                    print('Incorrect client message received.')
