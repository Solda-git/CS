from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Float
from DB.db import Base
from sqlalchemy.orm import relationship
from time import time
from sqlalchemy import ForeignKey
from icecream import ic

class ClientHistory(Base):
        __tablename__ = "ClientHistory"
        id = Column(Integer, primary_key=True)
        client_id = Column(Integer, ForeignKey('Client.id'))
        login_time = Column(Float)
        ip_address = Column(String)
        Clients = relationship("Client", back_populates="ClientHistoryRecords")

        def __repr__(self):
            return "<ClientHistory('%s', '%s', '%s', '%s', '%s')>" % (
                self.id, 
                self.client_id, 
                self.Client.login, 
                self.login_time, 
                self.ip_address
                )


class ClientHistoryStorage:
    
    def __init__(self, session):
        self._session = session
    
    def add(self, client_id, ip_address, login_time=time()):
        try:
            # with self._session.begin():
            self._session.add(ClientHistory(
                client_id=client_id,
                ip_address=ip_address,
                login_time=login_time,
                ))
            self._session.commit()
        except Exception as e:
            ic(e)
            print('Client history error.')

    def get_client_history(self, id):
        return self._session.query(ClientHistory).filter(
            ClientHistory.client_id == id
            ).all()
            
