import json
from lib.settings import MAX_PACKAGE_LEN, ENCODING

def get_message(socket):
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

def send_message(socket, message):
    """
    Routine function sends message encoded to the socket
    :param socket:
    :param message:
    :return:
    """
    socket.send(json.dumps(message).encode(ENCODING))
