import sys
import os
import socket
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

soc = socket.socket()
soc.connect(('localhost', 1111))

Form, Window = uic.loadUiType("form.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

form.setWindowTitle('arvendra')


def onsendclick():
    soc.send(form.send_text.text().encode('utf-8'))

    form.send_and_rec_text.append('\n' + 'you: ' +
                                  form.sendtext.text()
                                  + '\n' + soc.recv(2048).decode())


form.pushButton.clicked.connect(onsendclick)
sys.exit(app.exec())   
soc.close()
