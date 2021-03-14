"""
edu project - chat

SChatServer class

server part
"""
import sys
import json
from time import time
from socket import *
from lib.routines import Messaging, logdeco

from lib.settings import ONLINE, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, RESPONSE, ERROR, CHAT_SERVER_IP_ADDRESS, \
    DEFAULT_PORT, RECV_MODE, SEND_MODE, DUPLEX_MODE, MESSAGE_TEXT, MESSAGE, SENDER
import logging
import log.config.client_log_config

c_logger = logging.getLogger('client.log')


class SChatClient(Messaging):
    """
    """
    @logdeco
    def __init__(self, mode, addr, port):
        """
            initializing socket connection
            socket params are taken from config.py
        """
        #initialize socket
        try:
            self._mode = mode
            self.client_socket = socket(AF_INET,SOCK_STREAM)
            self.client_socket.connect((addr, port))
            c_logger.info(f"Client connected to address/port: {addr}/{port}")

        except ConnectionRefusedError as e:
            c_logger.exception(f"Connection error accured: {e.strerror}")
            print("No socket created. Client stopped.")
            sys.exit()

    @logdeco
    def __del__(self):
        """
        Class destructor closes the client socket
        """
        self.client_socket.close()
        c_logger.info("Connection closed.")

    @logdeco
    def make_online(self, account='guest'):
        """
        function generates request making chat user online

        """
        online_msg =  {
            COMMAND: ONLINE,
            TIMESTAMP: time(),
            USER: {
                ACCOUNT_NAME: account
            }
        }
        c_logger.info(f'Online message for user {online_msg[USER][ACCOUNT_NAME]} '
                   f'created: {online_msg}.')

        return online_msg

    @logdeco
    def parse_server_answer(self, message):
        """
        function processes message from the server
        :param message:
        :return: dict with status
        """
        c_logger.debug(f'Parsing server message: {message}.')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                c_logger.info(f'Correct server response: {message[RESPONSE]}')
                return f'Correct message with response {message[RESPONSE]}.'
            if message[RESPONSE] == 400:    
                c_logger.warning("Bad server respnse: {message[RESPONSE]}: {message[ERROR]}")
                return f'Bad response. {message[RESPONSE]}: {message[ERROR]}'
        raise ValueError


    @logdeco
    def create_message(self, account_name='Guest'):
        """
        function creates client's message 
        """
        message_text = input('Input message text or \'q\' for exit. \n')
        if message_text == 'q':
            self.client_socket.close()
            c_logger.info(f'User {each_socket} closed the connection.')
            print('Connection closed. See you next time')
            sys.exit(0)
        message = {
            COMMAND: MESSAGE,
            TIMESTAMP: time(),
            ACCOUNT_NAME: account_name,
            MESSAGE_TEXT: message_text
        }  
        c_logger.debug(f'Message {message} prepared.')
        return  message

    @logdeco
    def recv_message(self, message):
        """
        function parces received client's message 
        """
        if COMMAND in message and message[COMMAND] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
            info = f'Message {message[MESSAGE_TEXT]} received from {message[SENDER]}'
            print(message[MESSAGE_TEXT])
            c_logger.info(info)
        else:
            c_logger.error(f'Incorrect message {message}')

    @logdeco
    def run(self):
        try:
            online_msg = self.make_online()
            self.send_message(self.client_socket, online_msg)
            c_logger.info(f'Message: {online_msg} sent to server.')
            response_message = self.parse_server_answer(self.get_message(self.client_socket))
            c_logger.info(f'Received message from the server: {response_message}.')

        except (ValueError, json.JSONDecodeError):
            c_logger.error("Incorrect client message received. Can\'t decode server message.")
            sys.exit(1)

        except ConnectionRefusedError:
            c_logger.critical(f'Can\'t connect to server.')
            sys.exit(1)

        else:
            while True:
                if self._mode == SEND_MODE:
                    self.run_in_send_mode()            
                elif self._mode == RECV_MODE:
                    self.run_in_recv_mode()            
                else:
                    self.run_in_duplex_mode()            

    @logdeco
    def run_in_send_mode(self):
        # print(f"Client is working in <send> mode")
        try:
            self.send_message(self.client_socket, self.create_message())
        except (ConnectionResetError, ConnectionError, ConnectionRefusedError):
            c_logger.error(f'Connection with server {self.addr} lost.')
            sys.exit(1)
    
    @logdeco
    def run_in_recv_mode(self):
        # print(f"Client is working in <receive> mode")
        try:
            self.recv_message(self.get_message(self.client_socket))
        except (ConnectionResetError, ConnectionError, ConnectionRefusedError):
            c_logger.error(f'Connection with server {each_server_address} lost.')
            sys.exit(1)


    def run_in_duplex_mode(self):
        print(f"Client is working in <duplex> mode")
        print('Function developmwent in progress...')
        
