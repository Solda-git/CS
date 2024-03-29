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
    DEFAULT_PORT, RECV_MODE, SEND_MODE, PEER_TO_PEER_MODE, DUPLEX_MODE, BROADCAST_MODE, MESSAGE_TEXT, MESSAGE, SENDER, \
    Port
import logging
import log.config.client_log_config
import select
import _io

c_logger = logging.getLogger('client.log')


class SChatClient(Messaging):
    """
    """
    server_port = Port()
    @logdeco
    def __init__(self, mode, addr, port, name='guest'):
        """
            initializing socket connection
            socket params are taken from config.py
        """
        #initialize socket
        try:
            self._mode = mode
            self.client_socket = socket(AF_INET,SOCK_STREAM)
            self.server_port = port
            print(f'Type of "port" property: {type(self.server_port)}')
            self.client_socket.connect((addr, self.server_port))
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
        # message_text = input('Input message text or \'q\' for exit. \n')
        message_text = input('>')
        if message_text == 'q':
            self.client_socket.close()
            c_logger.info(f'User {self.client_socket} closed the connection.')
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
            return message[MESSAGE_TEXT]
        else:
            c_logger.error(f'Incorrect message {message}')

    @logdeco
    def run(self, conn=None):
        if conn is None:
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
                    elif self._mode == BROADCAST_MODE:
                        self.run_in_broadcast_mode()      
                    else:
                        self.run_in_duplex_mode()            
        else:
            self.run_in_p2p_mode(conn)



    def run_in_p2p_mode(self, conn):
        receiver_list = []
        sender_list = []
        err_list = []  
        while True:
            try: 
                receiver_list, sender_list, err_list = select.select([conn, sys.stdin], [conn], [], 0)
            except OSError:
                    pass
            try:
                if receiver_list:
                    for receiver in receiver_list:
                        if (type(receiver)==_io.TextIOWrapper):
                            conn.send(input('>')) 
                        else:
                            conn.recv()

            except:
                c_logger.error(f'Pipe error in main process')
                conn.close()
                sys.exit(1)

    def run_in_pipe(self, conn):
        print("run_in_pipe running")
        while True:
            try:
                mirror_msg = "Received: " + conn.recv()
                print(mirror_msg)
                conn.send(mirror_msg)
            except EOFError:
                break
        print("run_in_pipe finishing")


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
            c_logger.error(f'Connection with server {self.addr} lost.')
            sys.exit(1)

    @logdeco
    def run_in_broadcast_mode(self):
        receiver_list = []
        sender_list = []
        err_list = []    
        try: 
            receiver_list, sender_list, err_list = select.select([self.client_socket, sys.stdin], [self.client_socket], [], 0)
        except OSError:
                pass
        try:
            if receiver_list:
                for receiver in receiver_list:
                    if (type(receiver)==_io.TextIOWrapper):
                        self.send_message(self.client_socket, self.create_message())
                    else:
                        self.recv_message(self.get_message(self.client_socket))
        except (ConnectionResetError, ConnectionError, ConnectionRefusedError):
            c_logger.error(f'Connection with server {self.addr} lost.')
            sys.exit(1)

    def run_in_duplex_mode(self):
        print(f"Client is working in <duplex> mode")
        print('Function developmwent in progress...')
        

