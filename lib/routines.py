import json
from .settings import MAX_PACKAGE_LEN, ENCODING
from inspect import stack
from functools  import wraps
import logging

def logdeco(fn):
    # @wraps(fn)

    def decorated(*args, **kwargs):
        call_module = stack()[1].filename[-9:-3]
        func_name = stack()[1].function
        if call_module == 'client':
            chat_logger = logging.getLogger('client.log')
            # print('client module called.')      
        elif call_module == 'server':
            chat_logger = logging.getLogger('server.log')
            # print('server module called.')
        else: 
            result = fn(*args, **kwargs)
            return result
        old_formatter = chat_logger.handlers[0].formatter._fmt
        chat_logger.handlers[0].setFormatter(logging.Formatter('%(asctime)-26s %(message)s'))
        result = fn(*args, **kwargs)
        chat_logger.debug(f'Function {fn.__name__} called with parameters '
                            f'{args, kwargs} from function {func_name} with '
                            f'return value {result}. <Logged by "logdeco(fn)" decorator>')
        chat_logger.handlers[0].setFormatter(logging.Formatter(old_formatter))                    
        
        return result
    
    return decorated 



class Messaging():
    def get_message(self, socket):
        """
        Routine function gets message from the socket and converts it to the dict
        :param client: client socket
        :return: dict
        """
        byte_message = socket.recv(MAX_PACKAGE_LEN)
        if isinstance(byte_message, bytes):
            message = json.loads(byte_message.decode(ENCODING))
            if isinstance(message, dict):
                return message
            raise ValueError
        raise ValueError

    def send_message(self, socket, message):
        """
        Routine function sends message encoded to the socket
        :param socket:
        :param message:
        :return:
        """
        socket.send(json.dumps(message).encode(ENCODING))