import os
import subprocess
from dotenv import load_dotenv

dotenv_path = '../../.env'
load_dotenv(dotenv_path)

userName = os.environ.get("userName")
userName = str(userName)

command = 'ls /mnt/plex/Movies | xargs -0 echo > /home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/CurrentLib.txt'
#Writing all the files that exist in Plex to a txt file called CurrentLib.txt
History = os.system(command)

#opening up the Movietitle.txt to get the user input
with open('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt') as d:
    Input = d.read()
    Input = Input.strip()
    Input = Input.lower()
    d.close()

i = 0
array = {}

#checking library for title
inThere = False

with open('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/CurrentLib.txt', 'r') as f:
    Lib = f.readlines()
    for line in Lib:
        line = line.lower()

        if Input in line:
            inThere = True
            array[i] = line.title()
            i += 1

    f.close()

#checking if there is match to print list
if inThere == True:
    print("Plex server already has the following titles:\n")

    for i in range(len(array)):
        print('\t' + array[i])

    print("Would you like to download anyways?\n")


    
