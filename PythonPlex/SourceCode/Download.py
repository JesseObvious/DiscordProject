import os.path
import os
import re
import time
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from dotenv import load_dotenv

dotenv_path = '../../.env'
load_dotenv(dotenv_path)

userName = os.environ.get("userName")
userName = str(userName)

#opening movie link
with open('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt') as f:
        Input = f.read()
        Inputlink = Input.strip()

#creating HTMLsession object and building our request, also rendering the java script because we wont have data without it.
session = HTMLSession() 
session = session.get(Input)
session.html.render()

#good for troubleshooting VVV
#print(session.html.html)

#Parsing through the returned HTML, finding the tags I need and want.
print('Searching for your download link')

soup = BeautifulSoup(session.html.html, 'lxml')

#Checking to see if it is a movie or tv show so it knows the right directory to output the file to
ContentType = soup.find(id='cat')
print("Path = ")

ContentType = str(ContentType)
print(ContentType)
subStrMovieHD = 'HD Movies'
subStrMovie = 'Movies'
filePath = ''

if ContentType.find(subStrMovieHD) != -1 or ContentType.find(subStrMovie) != -1:
    filePath = '/mnt/plex/Movies/'

else:
    filePath = '/mnt/plex/TV/'

print("THIS IS YOUR FILE PATH " + filePath)

#finding the downloadlink
results = soup.find(id='d')
results = str(results)
results = results.split('<')

magnet = []
for bit in results:
    if 'magnet:' in bit:
        print('Download link found')
        magnet.append(bit)

magnet = magnet[0]
magnet = magnet.split('"')
magnet = str(magnet[1])


print('Connecting to VPN')

os.system('nohup python3 /home/' + userName + '/DiscordProject/PythonPlex/VpnStuff/VPNCon.py &')
time.sleep(10)

print('Starting torrent')

MagnetCommand = 'transmission-cli "'+magnet+'" -w ' + filePath + ' -f /home/' + userName + '/DiscordProject/PythonPlex/VpnStuff/disconnect.sh'

os.system(MagnetCommand)

print('Torrent download has finished')

time.sleep(10)

print('Killing VPN')

os.system('nohup python3 /home/' + userName + '/DiscordProject/PythonPlex/VpnStuff/VPNKill.py')

print("Movie should be downloaded, VPN should be disconnected, Have a great day :)")



