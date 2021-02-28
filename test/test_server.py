from time import time
from chat.schatserver import SChatServer
from lib.settings import RESPONSE, COMMAND, TIMESTAMP, USER, ACCOUNT_NAME, ONLINE, ERROR
import pytest


CORRECT_RESPONSE_200 = {
    RESPONSE: 200
}
INCORRECT_RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: 'Bad request'
}

CORRECT_MESSAGE = {
    COMMAND: ONLINE,
    TIMESTAMP: time(),
    USER: {
        ACCOUNT_NAME: 'guest'
    }
}

NO_COMMAND_MESSAGE = {
    TIMESTAMP: time(),
    USER: {
        ACCOUNT_NAME: 'guest'
    }
}

WRONG_COMMAND_MESSAGE = {
    COMMAND: 'probe',
    TIMESTAMP: time(),
    USER: {
        ACCOUNT_NAME: 'guest'
    }
}

NO_TIMESTAMP_MESSAGE = {
    COMMAND: 'probe',
    USER: {
        ACCOUNT_NAME: 'guest'
    }
}

NO_USER_MESSAGE = {
    COMMAND: 'probe',
    TIMESTAMP: time(),
}

NO_USER_ACCOUNT_MESSAGE = {
    COMMAND: ONLINE,
    TIMESTAMP: time(),
    USER: {

    }
}

WRONG_USER_ACCOUNT_MESSAGE = {
    COMMAND: ONLINE,
    TIMESTAMP: time(),
    USER: {
        ACCOUNT_NAME: 'admin'
    }
}

# setting up tests
@pytest.fixture
def init():
    try:
        sut = SChatServer("localhost", 8888)
        print("SChatServer instance created.")
        yield sut
    finally:
        print("SChatServer instance deleted.")    
        del sut


def test_correct_message(init):
    """
    testing of function parse_message with correct argument
    :return:
    """
    alert = "Invalid CORRECT RESPONSE parsing"
    assert init.parse_message(CORRECT_MESSAGE) == CORRECT_RESPONSE_200, alert


def test_no_command_message(init):
    """
    testing of function parse_message with incorrect argument
    :return:
    """
    alert = "Invalid parsing of message with incorrect argument"    
    assert init.parse_message(NO_COMMAND_MESSAGE) == INCORRECT_RESPONSE_400, alert
    

def test_no_timestamp_message(init):
    """
    testing of function parse_message without timestamp argument
    :return:
    """

    alert = "Invalid parsing of message without timestamp argument"    
    assert  init.parse_message(NO_TIMESTAMP_MESSAGE) != CORRECT_RESPONSE_200, alert    


def test_no_user_message(init):
    """
    testing of function parse_message without USER argument
    :return:
    """

    alert = "Invalid parsing of message without user argument"
    assert init.parse_message(NO_USER_MESSAGE) == INCORRECT_RESPONSE_400, alert


def test_no_user_account_message(init):
    """
    testing of function parse_message with without ACCOUNT argument
    :return:
    """
    alert = "Invalid parsing of message without account argument"
    assert init.parse_message(NO_USER_ACCOUNT_MESSAGE) == INCORRECT_RESPONSE_400, alert


def test_wrong_user_account_message(init):
    """
    testing of function parse_message with wrong user account name
    :return:
    """
    alert = "Invalid parsing of message with wrong user account name"
    assert init.parse_message(WRONG_USER_ACCOUNT_MESSAGE) != CORRECT_RESPONSE_200, alert

