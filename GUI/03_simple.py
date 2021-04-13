# ---------------- Графический интерфейс пользователя. PyQt5 ------------------
#                           Простое приложение PyQt

import sys

from PyQt5.QtWidgets import QApplication, QWidget  # [1]

# from pyqt5_helper import setup_plugin_path

if __name__ == "__main__":
    # setup_plugin_path()

    # Обязательно нужно создать объект-приложение
    app = QApplication(sys.argv)  # [2]

    # Виджет основного окна приложения и его настройка
    w = QWidget()  # [3]
    w.resize(250, 150)  # [4]
    w.move(300, 300)  # [5]
    w.setWindowTitle("Simple")  # [6]
    # Отобразить виджет
    w.show()  # [7]

    # Запустить приложение (цикл опроса событий)
    sys.exit(app.exec_())  # [8]
