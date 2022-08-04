# Punished_Sounds
Python script for setting up a pubsub subscription

Punished Sounds (Windows setup)

- Getting your client secret and ID
Both are needed for authorising with Twitch

1. Visit https://dev.twitch.tv/ and follow the signup process
2. Goto your console (top right)
3. Register your application
4. Fill in the name (doesn't matter what)
5. Select the category (chatbot)
6. Use the local host as http://localhost:17563 (this is for client auth, when the script runs)
7. Copy your client ID
8. Select new secret, copy it also

- Getting your channel ID
This is needed to point your event subscription to

1. Visit https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
2. Input your channel name and convert to an ID
3. Copy your channel ID

- Installing Python
Script is written in Pyton, you'll need this to execute it

1. Visit https://www.python.org/downloads/windows/
2. Select latest Python 3 release
3. Scroll to the bottom and select Windows installer
4. Follow the install process (make sure to select 'add python.exe to PATH' when you are on the customise Python screen)

- Installing PIP
PIP is a Python package manager, you'll need this to install the additional files for using the script

1. Open up the command prompt
2. Run curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
3. To install PIP run python get-pip.py (note, you'll have to be in the same directory as the file you just curled, to check you are run dir)
4. Check it's installed run pip help
5. Open Control Panel
6. Open 'System'
7. Select 'Advanced System Settings'
8. Select 'Environment Variables'
9. Select 'New'
10. Select 'Browse Directory' and ensure to navigate to where you installed PIP
11. Input the name as pip if it's not already filled in

- Installing required packages
Additional useful packages that the script relies on

1. Open up the command prompt

~ Note: For the next steps, some packages might already be on your system, if you see an error suggesting this is the case just move onto the next package

3. Run pip install twitchAPI
4. Run pip install pprint
5. Run pip install UUID
6. Run pip install playsound
7. Run pip install os
8. Run pip install random
9. Run pip install fnmatch

- Installing Punished Sounds
Basically downloading the script

1. Visit https://github.com/PunishDave/Punished_Sounds
2. Select the green 'Code' button
3. Select 'Download ZIP'
4. Extract the files to your sounds directory
5. Open 'Punished_Sounds.py' after extraction with notepad or notepad++
6. Edit line 26 and input your client ID and client secret
7. Edit line 33 and input your channel ID
8. Save

- Running the program
To actually start Punished Sounds

1. Open up cmd
2. Change the directory to where your script/sounds are (via cd path\to\where\it\is)
3. Type python PunishedSounds.py press enter
4. If it's connected and works, you'll see "You can press ENTER in order to close script")
