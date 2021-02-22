"""
edu project - chat

SChatServer class

server part
"""


from socket import *
from lib.routines import get_message, send_message
from lib.settings import ONLINE, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, RESPONSE, ERROR, CHAT_SERVER_IP_ADDRESS, \
    DEFAULT_PORT

class SChatClient:
    """
    """

    def __init__(self):
        """
            initializing socket connection
            socket params are taken from config.py
        """

        #initialize socket
        self.client_socket = socket(AF_INET,SOCK_STREAM)
        self.client_socket.connect((CHAT_SERVER_IP_ADDRESS,DEFAULT_PORT))

        #drop all clients
        self.clients = []

    def __del__(self):
        """
        Class destructor closes the client socket
        """
        client_socket.close()


    def make_online(self):
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
        send_message(client_socket, self.make_online())
        try:
            print(self.parse_server_answer(get_message(client_socket)))
        except (ValueError, json.JSONDecodeError):
            print("Can't decode server message")


# main function
if __name__ == '__main__':
   print('Hello')