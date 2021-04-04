
from dataclasses import dataclass
from time import time 


@dataclass
class ClientDetails:
    login: str
    password: str

@dataclass
class ClientHistoryInfo:
    clien_ID: int
    login_time: float
    ip_address: str


class ClientStorage:
 
    def __init__(conn):
        self._conn = conn

    
    def add(self, login, password="password"):
        pass

    def find(self, id):
        pass

class ClientHistoryStorage:
    
    def __init__(conn):
        self._conn = conn

    
    def add(self, id, ip_address, login_time=time()):
        pass

    def get_history(self, id):
        pass


