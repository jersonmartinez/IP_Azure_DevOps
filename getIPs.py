import urllib.request
import wget
from bs4 import BeautifulSoup

url = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519'

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent, }

request = urllib.request.Request(url, None, headers)

datos = urllib.request.urlopen(request).read().decode()

soup = BeautifulSoup(datos)
tags = soup('a')

matchUrl = 'https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/'
cadUrl2 = len(matchUrl)

for tag in tags:
    cadUrl = tag.get('href')
    subCadena = cadUrl[0:cadUrl2]

    if matchUrl == subCadena:
        #print("Son iguales")
        wget.download(cadUrl, '/home/marlon/Descargas/DevopsAzureIPs.json')
