import logging


DEFAULT_PORT = 8888

DEFAULT_IP_ADDRESS = ''
CHAT_SERVER_IP_ADDRESS = '127.0.0.1'

MAX_CONNECTIONS = 5

MAX_PACKAGE_LEN = 1024

ENCODING = 'utf-8'

COMMAND = 'command'
TIMESTAMP = 'timestamp'
USER = 'user'
ACCOUNT_NAME = 'account_name'
PASSWORD = 'password'


ONLINE = 'online'
RESPONSE = 'response'
ERROR = 'error'
ALERT = 'alert'

SENDER = 'sender'
MESSAGE = 'message'
AUTHENTICATE = 'authenticate'
MESSAGE_TEXT = 'message_text'   
GET_CONTACTS = 'get_contacts'
DEL_CONTACT = 'del_contact'
ADD_CONTACT = 'add_contact'
CONTACT = 'contact'


# log settings
LOG_LEVEL = logging.DEBUG
LOG_PATH = './log/log/'


SEND_MODE = 's'
RECV_MODE = 'r'
DUPLEX_MODE = 'd'
PEER_TO_PEER_MODE = 'p'
BROADCAST_MODE = 'b'

###################
MIN_PORT_VALUE = 1024
MAX_PORT_VALUE = 65535

class Port:
    def __init__(self, name=""):
        self.name = '_' + name

    def __get__( self, obj, obj_type):
        if obj is None:
            return self
        return getattr(obj, self.name)
    
    def __set__( self, obj, value):
        if not (MIN_PORT_VALUE < value < MAX_PORT_VALUE):
            raise ValueError('Port value mast be between 1024 and 65535.')
        setattr(obj, self.name, value)

    def __delete__( self, obj):
        pass

############################
###########chat DB section###########

DB_NAME = './DB/chat.db'

#####################################

###TEMPORARY BLOCK################
#####CLIENT PASSWORD##############
CLIENT_PASSWORD = "pass1"