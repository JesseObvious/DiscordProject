#Pirate.py 
#Name: Spicy J Mu$tard
#Date: 12/3/2021

#Description:             
#   I wrote this script to download 
#   movies automatically based 
#   off the name of a movie found in a text file.

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

hdMoviesTag = 'HD Movies'
hdTVTag = 'HD TV-Shows'
moviesTag = 'Movies'
tvTag = 'TV-Shows'

#opening the txt file that drews bot spit out
with open('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt') as f:
    Input = f.read()

#removing bad characters that web servers will complain about. EG. - / 
def urlify(s):
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+", '+', s)

    return s


#setting the data from txt file to a variable named MovieName
MovieName = urlify(Input)
MovieName = str(MovieName)

#building the URL that we will use in our web scraping later
PirateURL = "https://thepiratebay.org/search.php?q=" + MovieName + '&all=on&search=Pirate+Search&page=0&orderby='

#creating HTMLsession object and building our request, also rendering the java script because we wont have data without it.
session = HTMLSession() 
session = session.get(PirateURL)
session.html.render(timeout=2000)

#good for troubleshooting VVV
#print(session.html.html)

#Parsing through the returned HTML, finding the tags I need and want.
soup = BeautifulSoup(session.html.html, 'lxml')

#finding name and description link
results = soup.find(id='st')
Link = results.find(class_ = "list-item item-name item-title")

item = soup.find(id='st')
itemType = str(item.find(class_='list-item item-type'))

f = open("/home/" + userName + "/DiscordProject/DiscordBot/TxtFiles/GoodToGo.txt", "w")
f.close()

if hdMoviesTag not in itemType and hdTVTag not in itemType and moviesTag not in itemType and tvTag not in itemType:
    os.remove("/home/" + userName + "/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt")
    os.remove("/home/" + userName + "/DiscordProject/DiscordBot/TxtFiles/GoodToGo.txt")
    print ("u lookin up some sus shit.. try something else")
    exit() 


#finding seeds
seed = soup.find(id='st')
seedNumber = seed.find(class_='list-item item-seed')
seedFilter = filter(str.isdigit, seedNumber)
seedClean = ''.join(seedFilter)
seedClean = int(seedClean)

#checking file size 
fileSize = soup.find(id = 'st')
fileSizeNum = str(fileSize.find(class_='list-item item-size'))
if 'MiB' in fileSizeNum:
    sizeType = 'MB'

else:
    sizeType = 'GB'

sizeFilter = (re.findall(r"[-+]?\d*\.\d+|\d+", fileSizeNum))

#cleaning the data that comes out
newlink = str(Link)
newlink = newlink.split('/')
Deslink = str(newlink[1])
Deslink = Deslink.split('>')

#building important variables
DescriptionLink = Deslink[0][:-1]
NameOfMovie = Deslink[1][:-1]
DownloadLink= 'https://thepiratebay.org/' + DescriptionLink

MIN_SEEDS = 8
MAX_SIZE = 8.00

#incase there are low seeds
if seedClean < MIN_SEEDS:
    os.remove("/home/" + userName + "/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt")

print(DownloadLink)


#overwriting new downloadlink file
f = open ("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt", "w")
f.write(DownloadLink)
f.close()

f = open ("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/seeds.txt", "w")
f.write(str(seedClean))
f.close()

f = open("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/FileSize.txt", "w")
f.write(str(sizeFilter[0]))
f.close()

f = open("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/FileTooBig.txt", "w")
f.write('')
f.close()

f = open("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/FileSize.txt", "r")
size = f.readline()
size = float(size)
    
if size > MAX_SIZE and sizeType == 'GB':
    os.remove("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/FileTooBig.txt")

    
f.close()

f = open("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/FileSize.txt", "w")
f.write(str(sizeFilter[0]) + ' ' + sizeType)
f.close()



f = open ("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/FullDownloadname.txt", "w")
f.write(NameOfMovie)
f.close()

#calling art.py
os.system('python3 /home/' + userName + '/DiscordProject/PythonPlex/Art/Art.py')



