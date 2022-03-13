import winreg
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import requests
from bs4 import BeautifulSoup
import wmi   
form_class = uic.loadUiType("my_design.ui")[0]

class My_Window(QMainWindow, form_class): #design.Ui_mainWindow
    def __init__(self):
        super().__init__() 
        self.setupUi(self)
        
        self.c = wmi.WMI()
        self.show_HWID()
        self.m = self.c.Win32_PhysicalMedia()
        
        for item in self.m:
            print(item)
        self.BT_Create.clicked.connect(self.Create_GUID_Clicked)
        self.BT_Change.clicked.connect(self.Change_GUID_Cliecked)
        #key = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001',0, winreg.KEY_SET_VALUE)

    def show_HWID(self): #label에 현재 HwProfileGuid display
        self.key = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001',0, winreg.KEY_READ)
        (value,typevalue) = winreg.QueryValueEx(self.key,'HwProfileGuid')
        self.label_2.setText("HwProfileGuid")
        self.label_4.setText( str(value) )

    def Create_GUID_Clicked(self): #GUID 버튼 클릭 시 발생하는 이벤트
        self.url = "https://www.uuidgenerator.net/"
        self.response = requests.get(self.url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.hw_list = self.soup.select_one('#generated-uuid')
        
        self.label_6.setText(self.hw_list.get_text())

    def Change_GUID_Cliecked(self): #Change 버튼 클릭 시 발생하는 이벤트
        if self.label_6.text() == "":
            QMessageBox.warning(self,"Warning","Create HwProfileGuid")
        else:
            self.Create_GUID = self.label_6.text()
            self.HwProfileGuid_key = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001',0, winreg.KEY_SET_VALUE)
            self.MachineGuid_key = winreg.OpenKey( winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Cryptography',0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(self.HwProfileGuid_key , 'HwProfileGuid', 0, winreg.REG_SZ, '{' + self.Create_GUID + '}')
            winreg.SetValueEx(self.MachineGuid_key , 'MachineGuid', 0, winreg.REG_SZ, self.Create_GUID)
            winreg.CloseKey(self.HwProfileGuid_key)
            winreg.CloseKey(self.MachineGuid_key)
            QMessageBox.about(self,"","Success")
            
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