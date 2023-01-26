# Stalcraft-Wrapper-and-Disscord-Bot
Just a simple python wrapper and a discord bot that checks when the last emission is for Stalcraft using there new API.

## Hosting Instructions ##
1) git clone https://github.com/NotTheNobleSavage/Stalcraft-Wrapper-and-Disscord-Bot.git
2) pip install -r requirements.txt
3) copy your discord auth and token stalcraft auth to the auth.py
3) python3 bot.py

## Lazy People ##
just invite the public bot to your server.
https://discord.com/oauth2/authorize?client_id=1067745335860023297&permissions=8&scope=bot%20applications.commands

## How to use the bot ##
/emission region:
This will allow you to view when the last emission happened in the region of choice.

The features below deal with how you want to be alerted when an emission occurs.
These commands can only be run by admins!

/add_alert region:
This creates an alert for the region in the current channel in which the command is run.
You can set the region to a specific region or can enter “all” to get alerts for all regions.

/view_alert:
This views all the current alerts that are set up in this channel.

/remove_alert region:
This command is used to remove an alert for region specified in the current channel
