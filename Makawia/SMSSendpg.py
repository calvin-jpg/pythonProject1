import sys, serial, time, mysql.connector, serial.tools.list_ports
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QDialog, QApplication, QWidget,
                             QVBoxLayout, QListWidget, QListWidgetItem,QLineEdit)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QTimer
from PyQt5.QtGui import QPixmap, QFont,QIcon
from threading import Thread
def responder():
    phone = serial.Serial("COM6", 115200, timeout=5)
    rsp = []
    phone.write(('AT+CMGF=1\r').encode())
    time.sleep(1)
    phone.write(('AT+CMGS="0652557543"\r').encode())
    time.sleep(1)
    phone.write(('Hello\r').encode())
    time.sleep(1)
    phone.write(bytes([26]))
    m = phone.readlines()
    for i in m:
               rsp.append(i.decode())
    for i in rsp:
        print(i)
responder()
