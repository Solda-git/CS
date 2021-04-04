from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Float
from DB.db import Base
from sqlalchemy.orm import relationship

class ClientHistory(Base):
        __tablename__ = "ClientHistory"
        id = Column(Integer, primary_key=True)
        client_id = Column(Integer, ForeignKey('Clients.id'))
        login_time = Column(Float)
        ip_address = Column(String)

        Client = relationship("Client", order_by='Client.id', back_populates="Clients")


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

    
    def add(self, id, ip_address, login_time=time()):
        with self._session.begin():
            self._session.add(ClientHistory(
                client_id=id,
                ip_address=ip_address,
                login_time=login_time 
                ))

    def get_client_history(self, id):
        return self._session.query(ClientHistory).filter(
            ClientHistory.client_id == id
            ).all()
            
