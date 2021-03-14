import logging


DEFAULT_PORT = 7777

DEFAULT_IP_ADDRESS = ''
CHAT_SERVER_IP_ADDRESS = '127.0.0.1'

MAX_CONNECTIONS = 5

MAX_PACKAGE_LEN = 1024

ENCODING = 'utf-8'

COMMAND = 'command'
TIMESTAMP = 'timestamp'
USER = 'user'
ACCOUNT_NAME = 'account_name'

ONLINE = 'online'
RESPONSE = 'response'
ERROR = 'error'
# log settings
LOG_LEVEL = logging.DEBUG
LOG_PATH = './log/log/'


SEND_MODE = 's'
RECV_MODE = 'r'
DUPLEX_MODE = 'd'