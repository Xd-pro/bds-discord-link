# BDS Discord Link
Wrapper for BDS that enables Discord linking.
## Features
Role rewards for linking

In-game rewards for linking (tag "linked" added when you link your account, so that this can be automated via command blocks/functions)

Change nicknames to Minecraft usernames

Pickle data format

## How to use

Download main.py

(Windows

Open cmd (Win+R)

Type python and press enter

Install python from the Microsoft store page that pops up)

(Linux

Install python 3 from ```apt-get python3```

Install pip 3 from ```apt-get python3-pip```

)

Move your BDS server to a folder named bds, in the same folder as main.py

Type ```pip install discord.py``` or ```pip3 install discord.py``` on Linux

![image](https://user-images.githubusercontent.com/62808970/111223661-58d7d480-85d5-11eb-8f30-2757dfef3643.png)


Open main.py with a text editor

Go to line 8

Change the number after the = sign to the role ID for the reward once you've linked your account

Go to line 122

Create a discord application and bot (https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/, stop at "Install Node.js and Get Coding")

Enable members intent on your Discord bot page

Change the number inside the ()s and ""s to your Discord bot's token

Run main.py to start the server

## Discord commands

!linkaccount - link your Discord account to your Minecraft account

!unlinkaccount - unlink your Discord account to your Minecraft account

!check <@user> - check who a Discord account is linked to
