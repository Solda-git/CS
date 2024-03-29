from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from DB.db import Base
from sqlalchemy.exc import IntegrityError


class Client(Base):
        __tablename__ = "Client"
        id = Column(Integer, primary_key=True)
        login = Column(String(25), unique=True)
        password = Column(String(25))

        # def __init__(self, login, pwd):
        #     self.login = login
        #     self.password = pwd

        def __repr__(self):
            return "<Client('%s', '%s', '%s')>" % (self.id, self.login, self.password)


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

    def is_client_login(self, client_login):
        result = self._session.query(Client).filter(Client.login == client_login).one()
        return result != None

    def get_client_by_id(self, client_id):
        return self._session.query(Client).filter(Client.login == client_id).one()

    def get_client_by_login(self, client_login):
        return self._session.query(Client).filter(Client.login == client_login).one()

    def get_all_clients(self):
        return self._session.query(Client).all()


