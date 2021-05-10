# covind-bot
A bot to poll the cowin api to find vaccination slots and send notifications to a discord channel.

# covind-bot
A python bot to poll the cowin api to find vaccination slots and send notifications to a discord channel.
Uses the cowin API wrapper


Setup 
- Create a application on Discord (https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications)
  - create a bot for the application
  - make sure to set up OAuth2 for the bot (click on OAuth2, select bot and the copy the link thats generated. Paste on a new browser tab)
- set the environment variables 
    -create a .env in your working directory 
    - set the following varibale 
      1) DISCORD_TOKEN (the bot token from discord)
      2) DISCORD_CHANNEL (Channel ID: this is where the bot will ping your messages)
      3) DISCORD_ERROR_CHANNEL (Channel ID for error messages. This is where the bot will sending logs/errors) 
- run pip install -r requirements.txt 


Run:
- python discordBot.py 

Arguements(optional): 
  - age (minimum age to consider for the vaccination slot) #default=18
  - district (District ID for the vaccination centers. Can check the Arogya Sethu API for your district ID https://apisetu.gov.in/public/api/cowin#/) #default=269 (Dakshina Kannada)
  - poll (Time between polling the cowin API) #default=60
      


To run on cloud(AWS): 
  - Note: can only be run on servers located in India.(The cowin API has geofenced to accepet request coming from Indian servers only) 
  - An VM that is loacted in India can run this script. (I used AWS and choose the Mumbai region)
  - Steps to follow after launching a VM:
      - Install python (sudo yum install python36)
      - Install pip 
          -cd /tmp
          -curl -O https://bootstrap.pypa.io/get-pip.py
          -python3 get-pip.py --user
          -pip3 --version
      - Transfer the code (Use filezilla or winscp, based on os)
      - create a systemd service 
          - Create a service file like covind.service (script provided above)
          - Put it in /lib/systemd/system/
          - Reload systemd using command: systemctl daemon-reload
          - Enable auto start using command: systemctl enable covind.service
          - start service using: systemctl start covind
          - check status of service: systemctl status covind
