import winreg
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal
import sys
import requests
from bs4 import BeautifulSoup

form_class = uic.loadUiType("my_design.ui")[0]

class My_Window(QMainWindow, form_class): #design.Ui_mainWindow
    def __init__(self):
        super().__init__() 
        self.setupUi(self)
        self.show_HWID()
        
        self.BT_Create.clicked.connect(self.Create_GUID_Clicked)
        self.BT_Change.clicked.connect(self.Change_GUID_Cliecked)
        #key = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001',0, winreg.KEY_SET_VALUE)

    def show_HWID(self):
        self.key = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001',0, winreg.KEY_READ)
        (value,typevalue) = winreg.QueryValueEx(self.key,'HwProfileGuid')
        self.label_2.setText("HwProfileGuid")
        self.label_4.setText(str(value))

    def Create_GUID_Clicked(self):
        self.url = "https://www.uuidgenerator.net/"
        self.response = requests.get(self.url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.hw_list = self.soup.select_one('#generated-uuid')
        
        self.label_6.setText(self.hw_list.get_text())

    def Change_GUID_Cliecked(self):
        if self.label_6.text() == "":
            QMessageBox.warning(self,"Warning","캐릭터를 찾을 수 없습니다.")
        else:
            pass
        
        

class Warning(QMessageBox):
    def __init__(self):
        QMessageBox.__init__(self)
        #self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        #self.setupUi(self)
        #self.move(500,500)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = My_Window()
    window.show()
    app.exec_()