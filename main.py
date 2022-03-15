import winreg
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import requests
from bs4 import BeautifulSoup
#import wmi   
import subprocess
import regex as re
import string
import random

form_class = uic.loadUiType("my_design.ui")[0]

class My_Window(QMainWindow, form_class): #design.Ui_mainWindow
    def __init__(self):
        super().__init__() 
        self.setupUi(self)
        self.network_interface_reg_path = r"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}"
        self.transport_name_regex = re.compile("{.+}")
        self.mac_address_regex = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")
        
        # #self.c = wmi.WMI()
        # #self.m = self.c.Win32_PhysicalMedia()
        # for item in self.m:
        #     print(item)
        
        #test
        #self.test = self.get_connected_adapters_mac_address()
        #print(self.test)
        
        #Hwid display
        self.show_HWID()
        
        #button 리스너
        self.BT_Create.clicked.connect(self.Create_GUID_Clicked)
        self.BT_Change.clicked.connect(self.Change_GUID_Cliecked)
        self.BT_Create_Mac.clicked.connect(self.get_random_macaddress_Clicked)
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
            
    def get_random_macaddress_Clicked(self):
        self.url = "https://miniwebtool.com/mac-address-generator/"
        self.response = requests.get(self.url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.hw_list = self.soup.select_one('#re1 > div.print > div.r1')
        
        print(self.hw_list)
    def get_connected_adapters_mac_address(self):
        # make a list to collect connected adapter's MAC addresses along with the transport name
        self.connected_adapters_mac = []
        # use the getmac command to extract 
        for self.potential_mac in subprocess.check_output("getmac").decode().splitlines():
            # parse the MAC address from the line
            mac_address = self.mac_address_regex.search(self.potential_mac)
            # parse the transport name from the line
            transport_name = self.transport_name_regex.search(self.potential_mac)
            if mac_address and transport_name:
                # if a MAC and transport name are found, add them to our list
                self.connected_adapters_mac.append((mac_address.group(), transport_name.group()))
        return self.connected_adapters_mac
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = My_Window()
    window.show()
    app.exec_()