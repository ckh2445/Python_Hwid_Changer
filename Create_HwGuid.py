import requests
from bs4 import BeautifulSoup

class HwGuid_Create():
    def __init__(self):
        super().__init__()
        self.url = "https://www.uuidgenerator.net/"
        
        self.response = requests.get(self.url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        
        self.hw_list = self.soup.select_one('#generated-uuid')
        
        print(self.hw_list.get_text())

if __name__ == '__main__':
    HwGuid_Create()