#cleans the links and left over files
import os
from dotenv import load_dotenv
from dotenv import load_dotenv

dotenv_path = '../../.env'
load_dotenv(dotenv_path)

userName = os.environ.get("userName")
userName = str(userName)

TitleTest = os.path.exists('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt')
TitleTest2 = os.path.exists('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt')

if TitleTest == True:
    os.remove('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt')

if TitleTest2 == True:
    os.remove('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt')


