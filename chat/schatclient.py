"""
edu project - chat

SChatServer class

server part
"""
import sys
import json
from time import time
from socket import *
# from lib.routines import Messaging 
from lib.routines import Messaging
from lib.settings import ONLINE, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, RESPONSE, ERROR, CHAT_SERVER_IP_ADDRESS, \
    DEFAULT_PORT

import logging
import log.config.client_log_config

c_logger = logging.getLogger('client.log')


class SChatClient(Messaging):
    """
    """

    def __init__(self, addr, port):
        """
            initializing socket connection
            socket params are taken from config.py
        """
        #initialize socket
        try:
            self.client_socket = socket(AF_INET,SOCK_STREAM)
            self.client_socket.connect((addr, port))
            c_logger.info(f"Client connected to address/port: {addr}/{port}")

        except ConnectionRefusedError as e:
            c_logger.exception(f"Connection error accured: {e.strerror}")
            print("No socket created. Client stopped.")
            sys.exit()

    def __del__(self):
        """
        Class destructor closes the client socket
        """
        self.client_socket.close()
        c_logger.info("Connection closed.")


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


    def run(self):
        self.send_message(self.client_socket, self.make_online())
        try:
            print(self.parse_server_answer(self.get_message(self.client_socket)))
        except (ValueError, json.JSONDecodeError) as e:
            c_logger.exception(f'Incorrect message format: {e.strerror}')
            print("Can't decode server message")

