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

#opening the txt file that drews bot spit out
with open('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt') as f:
    Input = f.read()

with open('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/FileTooBig.txt', 'w') as f:
    f.close()

#removing bad characters that web servers will complain about. EG. - / 
def urlify(s):
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+", '+', s)

    return s

#setting the data from txt file to a variable named MovieName
def sizeCheck(downloadLink):
    PirateURL = downloadLink

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
    print("\t\tFILE SIZE: ", sizeFilter[0], sizeType, '\n')

    

    
#setting the data from txt file to a variable named MovieName
MovieName = urlify(Input)
MovieName = str(MovieName)

#building the URL that we will use in our web scraping later
PirateURL = "https://thepiratebay.org/search.php?q=" + MovieName + '&all=on&search=Pirate+Search&page=0&orderby='
#print(PirateURL)

#Print statement to announce what is happening
#print
#creating HTMLsession object and building our request, also rendering the java script because we wont have data without it.
session = HTMLSession() 
session = session.get(PirateURL)
session.html.render()

#good for troubleshooting VVV
#print(session.html.html)

#Parsing through the returned HTML, finding the tags I need and want.
soup = BeautifulSoup(session.html.html, 'lxml')

#finding name and description link
results = soup.find(id='torrents')
seedDirty = results.find_all(class_ = "list-item item-seed")
# results = soup.find(id = 'st')
# sizeDirty = str(results.find_all(class_ = "list-item item-size"))
results = results.find_all(class_ = "list-item item-name item-title")


#cleaning it up
results = str(results)
results = results.split(',')

seedDirty = str(seedDirty)
seedDirty = seedDirty.split(',')



print("The top three results are as follows \n")

i = 0

#storing the top three links. I have position 0 set to filler so we can just refer to the first movie as 1. Dirty way but idgaf.
TopThree = ['Filler',]

print("Top 5 Results: ")
#Getting the top 3 links, storing names and links in the TopThree array.
for torrent in results:
    if i < 5:
        torrent = torrent[55:-11]
        torrent = torrent.split('>')

        TorrentDescription = torrent[0]
        TorrentName = torrent[1]

        TopThree.append(torrent)

        #Pulls the seed from seedDrity, passes in the current loop iteration number.
        seedFilter = filter(str.isdigit, seedDirty[i])
        seedClean = ''.join(seedFilter)
        seedClean = int(seedClean)

        print('\t', i + 1, '. ', TorrentName)
        print('\t\tSEEDS: ', seedClean)

        dlLink = str('https://thepiratebay.org'+TorrentDescription[:-1])
        sizeCheck(dlLink)


        f = open ("/home/" + userName + "/DiscordProject/PythonPlex/TxtFiles/Choices/"+str(i+1)+".txt", "w")
        f.write(dlLink)
        f.close()
        
        i += 1

print("\nType '!1', '!2', '!3', '!4', or '!5'")
print("You can also type '!no' to cancel")

