import sys
import os
from PyQt5 import QtWidgets, uic
from DB.db import Base
from lib.settings import DB_NAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.client_history import ClientHistoryStorage
from DB.client import ClientDetailesStorage
from DB.contact import ContactStorage 
from icecream import ic


class DBConnector:
    global Base

    def __init__(self):
        self._engine = create_engine("sqlite:///"+DB_NAME, echo=False)
        Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)

    @property
    def session(self):
        return self._Session()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, db_connector):
        super().__init__()
        ui_file_path = os.path.join('./GUI', 'main.ui')
        uic.loadUi(ui_file_path, self)
        session = db_connector.session
        self.client_history = ClientHistoryStorage(session)
        self.client_detailes = ClientDetailesStorage(session)
        self.load_clients()


    def load_clients(self):
        self.clients = self.client_detailes.get_all_clients()
        rows = len(self.clients)
        self.clientTableWidget.setRowCount(rows)
        self.clientTableWidget.setColumnCount(3)
        

        for row in range(rows):
            ic(row)            
            self.clientTableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(self.clients[row].id)))
            self.clientTableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(self.clients[row].login))
            self.clientTableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(self.clients[row].password))
            
            row += 1

        self.clientTableWidget.show()

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    db_connector = DBConnector()
    w = MainWindow(db_connector)
    # w.tabWidget.tabBarClicked(0)


    w.show()
    sys.exit(app.exec_())
