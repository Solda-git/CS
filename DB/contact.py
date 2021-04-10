from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import and_

from DB.db import Base

class Contact(Base):
        __tablename__ = "Contact"
        id = Column(Integer, primary_key=True)
        client_id = Column(Integer, ForeignKey('Client.id'))
        contact_id = Column(Integer, ForeignKey('Client.id'))
        ClientList  = relationship("Client", 
                            primaryjoin="Contact.client_id==Client.id", 
                            back_populates="Contacts"
                            )
        Contacts = relationship("Client", 
                            primaryjoin="Contact.contact_id==Client.id", 
                            back_populates="Contacts"
                            )

        def __repr__(self):
            return "<ClientHistory('%s', '%s', '%s')>" % (
                self.id, 
                self.Client, 
                self.Contact
                )


class ContactStorage:

    def __init__(self, session):
        self._session = session

    def add(self, client_id, contact_id):
        try: 
            with self._session.begin():
                self._session.add(Contact(client_id=client_id, contact_id=contact_id))
        except IntegrityError as e:
            raise ValueError('Login mast be unique')
        except Exception as e:
            print(f'Exception accured while adding record in "Contact" table. {e}') 

    def delete(self, client_id, contact_id):
        try:
            contact = self._session.query.Contact.filter(and_(
                    Contact.client_id == client_id,
                    Contact.contact_id == contact_id 
                )).one()
            self._session.delete(contact)
            self._session.commit()
        except Exception as e:
            print(f'Error while deleting of client\'s contact. {e}')    

    def get_client_contacts(self, client_id):
        return self._session.query.Contact.filter(
                Contact.client_id == client_id
            ).all()