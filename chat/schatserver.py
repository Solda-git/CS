"""
edu project - chat

SChatServer class

server part
"""
import json
from socket import *
from lib.routines import Messaging, logdeco
from lib.settings import MAX_CONNECTIONS, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, ONLINE, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER, Port, AUTHENTICATE, PASSWORD, ALERT, \
    GET_CONTACTS, ADD_CONTACT, DEL_CONTACT, CONTACT    
import select
from contextlib import closing
from time import time
import logging
import log.config.server_log_config
from icecream import ic 

s_logger = logging.getLogger('server.log')

class SChatServer(Messaging):
    """
    """
    port = Port()

    def __init__(   self, 
                    details_storage,
                    history_storage,
                    contacts_storage, 
                    address, 
                    port
                ):
        
        try:
            self.server_socket = socket(AF_INET,SOCK_STREAM)
            # self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR) #nonblocking socket!

            if (address==""):
                address = DEFAULT_IP_ADDRESS
            
            self.port = port if port else DEFAULT_PORT    
            self.server_socket.bind((address, self.port))    
            self.detailes_storage = details_storage
            self.history_storage = history_storage
            self.contacts_storage = contacts_storage
            self.server_socket.settimeout(0.2)
            # self.server_socket.bind((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
            self.server_socket.listen()
            s_logger.info(f"Server is listening the port: {self.port}")
            #initialize(drop) client's list
            # self.clients = [] # old version Client's array of socket
            self.clients = {} # new  version - client's info in format {socket: ip_address}    
            self.messages = [] #Client's messages tuple in format (sender, data, socket)
        except error as e:
            s_logger.exception(f"Server connection error accured: {e.strerror}")

    def __del__(self):
        """
        closing sockets
        """
        #closing server socket
        self.server_socket.close()
        s_logger.info('Server socket closed')

        # closing all the client sockets
        # while (len(self.clients)):
        #     s = self.clients.pop()
        #     s.close()

        if self.clients:
            while self.clients.items():
                c = self.clients.popitem()
                c[0].close()



    @logdeco
    def close_client(self, s):
        """
            normal closing of client socket
            looking for s socket, remove from the client's socket list and close it
        # """
        # for i in range(len(self.clients)):
        #     if s == self.clients[i]:
        #         self.clients.pop()
        #         s.close()   
        #         break
        self.clients.pop(s)
        s.close()


    @logdeco
    def parse_message(self, message, client):
        """
        function parses incoming message and processes it.

        :param message:
        :return: dict with response code
        """
        ic(message)
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

        elif COMMAND in message and message[COMMAND] == AUTHENTICATE and TIMESTAMP in message \
                and USER in message:
             
                is_authenticated = self.detailes_storage.authenticate(
                            message[USER][ACCOUNT_NAME], 
                            message[USER][PASSWORD]
                        )               
                if is_authenticated:
                    ###adding history rercord for authenticated client###
                    client_record = self.detailes_storage.get_client_by_name(
                            message[USER][ACCOUNT_NAME]
                        )
                    #getting client IP in format:'<IP-Address>:<Port>
                    client_ip = self.clients[client][0]+':'+str(self.clients[client][1])
                    
                    #client auth history DB logging:
                    self.history_storage.add(
                        client_id=client_record.id, 
                        ip_address=client_ip
                        )

                    s_logger.info(f'User {message[USER][ACCOUNT_NAME]} authenticated.')
                    self.send_message(client,           
                                        {
                                            RESPONSE: 200,
                                            ALERT: "Authentication completed."
                                        }
                                    )
                    return
                else:
                    s_logger.error(f'User {message[USER][ACCOUNT_NAME]} authentication request rejected.')
                    self.send_message(client,           
                                        {
                                            RESPONSE: 402,
                                            ALERT: "Wrong account name or password."
                                        }
                                    )
                    return 
        
        elif COMMAND in message and message[COMMAND] == GET_CONTACTS and TIMESTAMP in message \
                and ACCOUNT_NAME in message:
            s_logger.error(f'User {message[ACCOUNT_NAME]} is getting his contact list.')
            client_record = self.detailes_storage.get_client_by_name(
                            message[ACCOUNT_NAME]
                        )
            self.send_message(client,           
                                {
                                    RESPONSE: 202,
                                    ALERT: self.contacts_storage.get_client_contacts(client_record.id)
                                }
                            )
            return 

        elif COMMAND in message and message[COMMAND] in [ADD_CONTACT, DEL_CONTACT] \
                and TIMESTAMP in message and ACCOUNT_NAME in message and CONTACT in message:
            
            ic(message[COMMAND])
            client_record = self.detailes_storage.get_client_by_name(
                            message[ACCOUNT_NAME]
                        )
            contact_record = self.detailes_storage.get_client_by_name(
                            message[CONTACT]
                        )
            print(f'Client_record = {client_record.id} \n Contact_record = {contact_record.id}')
            if message[COMMAND] == ADD_CONTACT:
                self.contacts_storage.add(client_record.id, contact_record.id)
            else:
                self.contacts_storage.delete(client_record.id, contact_record.id)
            self.send_message(client, {RESPONSE: 200})
            return

        s_logger.error(f'Incorrect message {message}. Bad request.')
        print('bad request')
        return {
            RESPONSE: 400,
            ERROR: 'Bad request'
        }             

    def get_client_list(self):
        client_list = []
        for client in self.clients.items():
            client_list.append(client[0])
        return client_list

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
                self.clients.update({client_socket: client_address})
                # self.clients.append(client_socket)
            receiver_list = []
            sender_list = []
            err_list = []

            try:
                if self.clients: # there are active client(s) connected to the server
                    client_list = self.get_client_list()
                    # receiver_list, sender_list, err_list = select.select(self.clients, self.clients, [], 0)
                    receiver_list, sender_list, err_list = select.select(client_list, client_list, [], 0)
            except OSError:
                    pass
            if receiver_list:
                for sender in receiver_list:
                    try:
                        self.parse_message(self.get_message(sender), sender)
                    except:
                        # s_logger.info(f'Client {sender.getpeername()} has disconnected.')
                        s_logger.info(f'Client {sender} has disconnected.')
                        # self.clients.remove(sender)
                        self.clients.pop(sender)

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
                        # self.clients.remove(awaiter)
                        self.clients.pop(awaiter)
