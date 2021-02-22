"""
edu project - chat

SChatServer class

server part
"""

from socket import *
from lib.routines import get_message, send_message
from lib.settings import MAX_CONNECTIONS, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, ONLINE, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS, RESPONSE, ERROR


class SChatServer:
    def __init__():
    """
        initializing socket connection
        socket params are taken from config.py
    """
        #initialize socket
        self.s = socket(AF_INET,SOCK_STREAM)
        self.s.bind(("",SERVER_PORT))
        self.listen()

        #drop all clients
        self.clients = []
 
    def __del__():
        """
        closing sockets
        """
        #closing server socket
        self.s.close()

        #closing all the client sockets
        while (len(self.clients)):
            s = self.clients.pop
            s.close()
    
    def run(): """
        running infinity cycle with homework task completion
    """
        while (1):



# main function
if __name__ == '__main__':
