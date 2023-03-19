- **Overview**
	- The topology of this setup depends on having 2 VMs. One that will run the Plex server and host the media. The other VM will run the Discord bot and handle the torrent download.
	- The setup also require you to have a VPN with a .ovpn connection.
		- I use express VPN which supports .ovpn

- **Create Plex VM**
	- Download newest version of ubuntu desktop and install it onto a VM.
	- Setup plex on this server
		- https://linuxize.com/post/how-to-install-plex-media-server-on-ubuntu-20-04/
- Create Discord Bot VM
	- Download newest version of ubuntu desktop and install it onto a VM.

- **Create Shared Drive**
	- On the Plex VM we will create a shared drive that our bot will write our media to.
	- Install Samab
		- `sudo apt update`
		- `sudo apt install samba`
	- create shared folder
		- `mkdir /home/username/plex`
		- Create 2 sub directories named movies and tv-shows
			- `mkdir /home/username/plex/Movies`
			- `mkdir /home/username/plex/TV`
	- configure smaba config
		- `sudo nano /etc/smaba/smb.conf`
			- Add the following lines at the bottom
			- `[plex]`
				- `comment = plex share`
				- `path = /home/username/plex`
				- `read only = no`
				- `browsable = yes`
		- Restart the samba service
			- `sudo service smbd restart`
		- Configure firewall
			- `sudo ufw allow samba`
		- Add samba user
			- `sudo smbpasswd -a plex`

- **Mount Shared Drive**
	- On the discord bot VM, we will need to mount the shared drive
	- Install cifs
		- `sudo apt-get install cifs-utils`
	- Create mount point
		- `mkdir /mnt/plex`
	- Configure /etc/fstab to mount the share on restart
		- `sudo nano /etc/fstab`
			- Add a line
			- `//ip-address/plex /mnt/plex cifs user=plex,pass=SambaPlexPassword,uid=1000,gid=1000 0 0`

- **Register Bot Application with Discord**
	- https://www.digitaltrends.com/gaming/how-to-make-a-discord-bot/
	- Only do steps 1 - 4, do not do 5.

- **Pull down code from github**
	- https://github.com/JesseObvious/DiscordProject
	- Move and rename
		- `cd /home/user/downloads`
		- `git clone https://github.com/JesseObvious/DiscordProject`
		- `mvdir DiscordPoject-Master DiscordProject`

- **Install Node JS**
	- `cd /home/username`
	- `sudo apt update`
	- `sudo apt install nodejs npm`
	- check the version
		- `nodejs --version`

- **Install Transmission-cli**
	- `sudo add-apt-repository ppa:transmissionbt/ppa`
	- `sudo apt-get update`
	- `sudo apt-get install transmission-gtk transmission-cli transmission-common transmission-daemon`

- **Install PM2**
	- `npm -l pm2 -g`

- **Fill in information**
	- Discord Bot token
		- `sudo nano /DiscordBot/BotFiles/auth.json`
		- Add your bot token
	- DiscordProject/.env
		- `sudo nano /DiscordBot/.env`
		- Fille in your username
	- DiscordProject/PythonPlex/VpnStuff
		- edit login.txt for you username and password for your open vpn
			- `nano login.txt`
		- place your .ovpn configuration file here and name it `torrent.ovpn`
	- Update Connect.sh
		- `sudo nano /DiscordProject/PythonPlex/VpnStuff/connect.sh`
		- Change the path to fit your username ie `/home/USERNAME/DiscordProject/`
		- Change for both paths

- **Install requirements**
	- `pip3 install -r /DiscordProject/requirements.txt`
	- If you don't have pip installed
		- `sudo apt install python3-pip`

- **Edit /etc/sudoers config**
	- `sudo nano /etc/sudoers`
	- add 3 entries
		- ALL ALL = (root) NOPASSWD: /home/username/DiscordProject/PythonPlex/VpnStuff/kill.sh
		- ALL ALL = (root) NOPASSWD: /home/username/DiscordProject/PythonPlex/VpnStuff/connect.sh
		- ALL ALL = (root) NOPASSWD: /home/username/DiscordProject/PythonPlex/VpnStuff/disconnect.sh


- **Give bot permission in your discord server**s
	- Create plex role 
		- Permissions
			- view channels
			- Send messages
			- create posts
			- read message history
	- Give bot the role
	- In the discord.com/developers/
		- Choose your application, then your bot
		- tick the slider for message content intent setting

- **Start the bot with PM2**
	- run `cd DiscordProject/DiscordBot/BotFiles`
		- run `pm2 start bot.js --watch`

- **Test your first download**
	- You can check the logs from the bot by doing the following
		- `pm2 logs`
	- Go into your discord in the channel the Bot is apart of and download a movie `!moviename`
		- Confirm that is the movie you want with `!yes`
		- Start the download after it prompts you with `!download`
	- Back in the logs you should see things start to kick off. Mianly being the VPN connection then the torrent download. 
	- Some important things to note about the torrent are the stages in which it downloads.
		- It will go from Not forward to starting
			- There will be no progress
		- It will then go from Starting to ???
			- No progress will be made
		- The final stage it will say Starting IPv4 DHT announce
			- It will pull in the movie name and should start showing peers
			- The download will actually start then

**FAQ**
- If your downloads are not actually downloading and are stuck at 0 peers, try the following
	- **Kill exisiting bot process**
		- `sudo service transmission-daemon stop`
		- `sudo service killall openvpn`
		- `sudo service killall transmission-cli`
	- **Edit config**
		- `sudo nano /etc/transmission-daemon/settings.json`
			- Set `rpc-authentication-required: false`
			- Set `rpc-whitelist: 127.0.0.1`
			- Set `peer-port-random-on-start: true`
			- Set `peer-port-random-high: 65535`
			- Set `peer-port-random-low: 49152 `
	- **Restart the service**
		- `sudo service transmission-daemon start`