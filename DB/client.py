from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from DB.db import Base 
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound 
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Client(Base):
        __tablename__ = "Client"
        id = Column(Integer, primary_key=True)
        login = Column(String(25), unique=True)
        password = Column(String(25))
        
        ClientHistoryRecords = relationship("ClientHistory", back_populates='ClientRecord')
        
        Contacts = relationship("Contact", 
                    primaryjoin="Client.id==Contact.contact_id",
                    back_populates='Contacts')
        
        ClientList = relationship("Contact", 
                    primaryjoin="Client.id==Contact.client_id",
                    back_populates='ClientList')
        
        # def __repr__(self):
        #     return "<Client('%s', '%s', '%s')>" % (self.id, self.login, self.password)


# Client.ClientHistoryRecords = relationship("ClienHistory", back_populates='Client')


class ClientDetailesStorage:
 
    def __init__(self, session):
        self._session = session 
    
    def add(self, login, password="password"):
        try: 
            with self._session.begin():
                self._session.add(Client(login=login, password=password))
        except IntegrityError as e:
            raise ValueError('Login mast be unique')
        except Exception as e:
            print(f'Exception accured while adding record in "Client" table. {e}')
    
    def is_client_id(self, client_id):
        result = self._session.query(Client).filter(Client.id == client_id).one()
        return result != None

    def authenticate(self, client_login, client_password):
        try:
            self._session.query(Client).filter(and_
                (
                    Client.login == client_login, 
                    Client.password == client_password
                )).one()
            return True
        except NoResultFound:
            print('Wrong login or password')
            return False


    def get_client_by_id(self, client_id):
        return self._session.query(Client).filter(Client.login == client_id).one()

    def get_client_by_name(self, client_login):
        return self._session.query(Client).filter(Client.login == client_login).one()

    def get_all_clients(self):
        return self._session.query(Client).all()
    

    def get_client_history(self, id=None):
        if id:
            pass
        return self._session.query( Client.login, 
                                    Client.ClientHistoryRecords.ip_address, 
                                    Client.ClientHistoryRecords.login_time
                                    ).all()
    