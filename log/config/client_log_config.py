import logging
import os


from lib.settings import LOG_LEVEL, ENCODING, LOG_PATH
CLIENT_LOG_FILE = os.path.join(LOG_PATH, 'client.log')  

cl_log = logging.getLogger('client.log')
cl_handler = logging.FileHandler(CLIENT_LOG_FILE, encoding=ENCODING)
cl_handler.setLevel(LOG_LEVEL)
cl_formatter = logging.Formatter('%(asctime)-26s %(levelname)-10s %(module)-20s %(message)s')
cl_handler.setFormatter(cl_formatter)
cl_log.addHandler(cl_handler)
cl_log.setLevel(LOG_LEVEL)
