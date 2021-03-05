import logging
import logging.handlers

from lib.settings import LOG_LEVEL, ENCODING, LOG_PATH 
import os

SERVER_LOG_FILE = os.path.join(LOG_PATH, 'server.log')  

srv_log = logging.getLogger('server.log')
srv_handler = logging.handlers.TimedRotatingFileHandler(
    SERVER_LOG_FILE,
    encoding=ENCODING,
    interval=1,
    when='D'
)
srv_formatter = logging.Formatter('%(asctime)-26s %(levelname)-10s %(module)-20s %(message)s')
srv_handler.setFormatter(srv_formatter)
srv_log.addHandler(srv_handler)
srv_log.setLevel(LOG_LEVEL)