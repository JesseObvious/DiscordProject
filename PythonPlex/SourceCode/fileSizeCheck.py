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

with open('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/FileTooBig.txt', 'w') as f:
    f.close()

#removing bad characters that web servers will complain about. EG. - / 
def urlify(s):
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+", '+', s)

    return s

#setting the data from txt file to a variable named MovieName
with open('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt') as f:
    PirateURL = f.read()


session = HTMLSession()
session = session.get(PirateURL)
session.html.render(timeout = 2000)

soup = BeautifulSoup(session.html.html, 'lxml')

#checking file size 
fileSize = soup.find(id = 'size')
fileSize = str(fileSize)
if 'MiB' in fileSize:
    sizeType = 'MB'

else:
    sizeType = 'GB'

sizeFilter = (re.findall(r"[-+]?\d*\.\d+|\d+", fileSize))


MAX_SIZE = 8.00

f = open("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/FileSize.txt", "w+")
f.write(str(sizeFilter[0]))
f.close()


f = open("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/FileSize.txt", "r")
size = f.readline()
size = float(size)

if size > MAX_SIZE and sizeType == 'GB':
    print("File size is too big.. check with dmoney if you really want this")
    os.remove("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/FileTooBig.txt")

else:
    print("Type '!download' to start or '!no' to cancel..")

f.close()


