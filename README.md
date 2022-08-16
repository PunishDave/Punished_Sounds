# Punished_Sounds
Using Punished Sounds!

After following the install guide, just setup channel rewards with the EXACT same name as the sound you want to play, when a chatter redeems that reward the file will dynamically search for the relevant sound and play it.

~ Note! : Occasionally Twitch might dc the subscription to channel events, it's happened to me a couple of times overnight - just stop the script with CTRL + D or C (or just close the cmd prompt down) and start it up again.

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
4. Open Control Panel
5. Open 'System'
6. Select 'Advanced System Settings'
7. Select 'Environment Variables'
8. Select the system variable for PATH
9. Select 'Edit'
10. Select 'New'
11. Select 'Edit'
12. Select 'Browse' and navigate to the folder in which Python is installed
~ NOTE! : If you are unsure where it installed, try typing in python after pressing the Windows key and opening the file location (might be a shortcut, so right click the shortcut and find the path that way)
13. Select 'New' for a new System Environment Variable
14. Input the name as PYTHONPATH
15. Press browse and input the path where Python is installed
~ NOTE! : Make sure when inputting the path you do not include the full path, you just need the directory
16. Test python is installed via typing in the cmd prompt python --version

- Installing required packages

Additional useful packages that the script relies on

1. Open up the command prompt

~ NOTE! : For the next steps, some packages might already be on your system, if you see an error suggesting this is the case just move onto the next package

2. python -m pip install twitchAPI
3. python -m pip install UUID
5. python -m pip install playsound==1.2.2
6. python -m pip install os

- Installing Punished Sounds

Basically downloading the script

1. Select the green 'Code' button
2. Select 'Download ZIP'
3. Extract the files to your sounds directory
4. Open '.env' after extraction with notepad or notepad++
5. Replace the relevant values gained from above
6. Save
~ NOTE! : Windows has an annoying habbit of trying to make you save the file as a .txt or similar, make sure that it is still saved as a .env file

- Running the program
To actually start Punished Sounds

1. Open up .bat file
2. Change the directory to where your script/sounds are (i.e. "cd C:\Users\Username\Desktop\TwitchSounds")
3. Change the 2nd line to the file name of whichever form of the bot you wish to use (i.e. Punished_Sounds.py, Database_concept.py)
4. Place the batch file where its easy to get access (such as your desktop) and double-click to launch the bot.
5. Close the command prompt window or press enter to end the script
Note: You may close the web browser it opens and the bot will still work
