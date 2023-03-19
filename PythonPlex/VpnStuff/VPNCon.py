import os
from dotenv import load_dotenv

dotenv_path = '../../.env'
load_dotenv(dotenv_path)

userName = os.environ.get("userName")
userName = str(userName)

os.system('sudo /home/' + userName + '/DiscordProject/PythonPlex/VpnStuff/connect.sh')


