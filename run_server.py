import click
from chat.schatserver import SChatServer
from lib.settings import DEFAULT_IP_ADDRESS, DEFAULT_PORT, DB_NAME
from DB.db import Base
from DB.client import ClientDetailesStorage
from DB.client_history import ClientHistoryStorage
from DB.contact import ContactStorage 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from icecream import ic


# @click.command()
# @click.option('--mode', default='broadcast')
# @click.option('--addr', default=DEFAULT_IP_ADDRESS, help='IP address listening by server')
# @click.option('--port', default=DEFAULT_PORT, help='Listening port')
def run_server(details_storage, history_storage, contacts_storage):
    my_server = SChatServer( 
                    details_storage,
                    history_storage,
                    contacts_storage, 
                    address="", 
                    port=""
        )
    # print(f'SChatServer run. Listening address: {("all addresses (by default)", address)[bool(address)]}, port: {port}')
    print(f'SChatServer is running.')
    
    my_server.run()

class DBConnector:
    global Base

    def __init__(self):
        self._engine = create_engine("sqlite:///"+DB_NAME, echo=False)
        Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)


    @property
    def session(self):
        return self._Session()

if __name__ == '__main__':
    
    # run_server()
    try:
        connector = DBConnector() 
        session = connector.session
        client_details = ClientDetailesStorage(session)
        client_history = ClientHistoryStorage(session)
        client_contacts = ContactStorage(session)

 
        # client_details.add("test1", "pass1")
        # client_details.add("test2", "pass1")
    #     client_storage.add("test3", "pass1")
        # session.commit()
    #     clients = client_storage.get_all_clients()
    #     for c in clients:
    #         ic(c)
        run_server(client_details, client_history, client_contacts)
    except ValueError as e:
        ic(e)




    

  