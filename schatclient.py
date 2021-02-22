"""
edu project - chat

SChatServer class

server part
"""
import json
from time import time
from socket import *
# from lib.routines import get_message, send_message
from lib.routines import Messaging
from lib.settings import ONLINE, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, RESPONSE, ERROR, CHAT_SERVER_IP_ADDRESS, \
    DEFAULT_PORT
import click

class SChatClient(Messaging):
    """
    """

    def __init__(self, addr, port):
        """
            initializing socket connection
            socket params are taken from config.py
        """
        #initialize socket
        self.client_socket = socket(AF_INET,SOCK_STREAM)
        self.client_socket.connect((addr, port))


    def __del__(self):
        """
        Class destructor closes the client socket
        """
        self.client_socket.close()


    def make_online(self, account='guest'):
        """
        function generates request making chat user online

        """
        return {
            COMMAND: ONLINE,
            TIMESTAMP: time(),
            USER: {
                ACCOUNT_NAME: account
            }
        }

    def parse_server_answer(self, message):
        """
        function processes message from the server
        :param message:
        :return: dict with status
        """
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return f'Correct message with response {message[RESPONSE]}.'
            return f'Bad response. {message[RESPONSE]: {message[ERROR]}}'
        raise ValueError

    def run(self):
        send_message(self.client_socket, self.make_online())
        try:
            print(self.parse_server_answer(get_message(self.client_socket)))
        except (ValueError, json.JSONDecodeError):
            print("Can't decode server message")


@click.command()
@click.option('--addr', default=CHAT_SERVER_IP_ADDRESS,help='Chat server IP-address')
@click.option('--port', default=DEFAULT_PORT, help='Chat server port')
def run_client(addr, port):
    print("run_client")
    my_client = SChatClient(addr, port)
    print(f"Client is connected to the address/port: {addr}/{port}")
    #send_message(my_client.client_socket,my_client.make_online())
    my_client.send_message(my_client.client_socket,my_client.make_online())
    try:
        #print(my_client.parse_server_answer(get_message(my_client.client_socket)))
        print(my_client.parse_server_answer(my_client.get_message(my_client.client_socket)))
    except (ValueError, json.JSONDecodeError):
        print("Can't decode server message")

# main function
if __name__ == '__main__':
   run_client()
