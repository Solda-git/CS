from  chat.schatclient import SChatClient
import pytest
from time import time

from lib.settings  import COMMAND, ONLINE, TIMESTAMP, USER, ACCOUNT_NAME, ERROR, RESPONSE




ONLINE_MESSAGE = {
    COMMAND: ONLINE,
    TIMESTAMP: '',
    USER: {
        ACCOUNT_NAME: 'guest'
    }
}

ONLINE_USER_MESSAGE = {
    COMMAND: ONLINE,
    TIMESTAMP: '',
    USER: {
        ACCOUNT_NAME: 'test_user'
    }
}

CORRECT_SERVER_RESPONSE = {
    RESPONSE: 200
}

ERROR_SERVER_RESPONSE = {
    RESPONSE: 400,
    ERROR: 'Bad request'
}


# setting up tests
@pytest.fixture
def init():
    try:
        sut = SChatClient("", 7777)
        print("SChatClient instance created.")
        yield sut
    finally:
        print("SChatClient instance deleted.")    
        del sut


def test_make_online(init):
    """
        testing of function make_online with correct argument
    """
    result = init.make_online()
    result[TIMESTAMP] = ONLINE_MESSAGE[TIMESTAMP] = time()
    print("starting assertion")
    assert result == ONLINE_MESSAGE, "Incorrect ONLINE message"
    

def test_make_online_user(init):
    """
        testing of function make_online with correct argument
    """
    user = ONLINE_USER_MESSAGE[USER][ACCOUNT_NAME] = 'test_user'
    result = init.make_online(user)
    result[TIMESTAMP] = ONLINE_USER_MESSAGE[TIMESTAMP] = time()
    assert result == ONLINE_USER_MESSAGE, "Incorrect argument in function make_online"


def test_parse_correct_response(init):
    """
    testing of function parse_server_answer with correct server response
    :return:
    """
    check_message = f'Correct message with response {CORRECT_SERVER_RESPONSE[RESPONSE]}.'
    assert init.parse_server_answer(CORRECT_SERVER_RESPONSE) == check_message, 'Invalid correct server response'
        

def test_parse_error_response(init):
    """
    testing of function parse_server_answer with bad server response
    :return:
    """
    
    check_message = f'Bad response. {ERROR_SERVER_RESPONSE[RESPONSE]}: {ERROR_SERVER_RESPONSE[ERROR]}'
    print(check_message)
    assert init.parse_server_answer(ERROR_SERVER_RESPONSE) == check_message, 'Invalid incorrect server response'
        