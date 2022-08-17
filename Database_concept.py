from tinydb import TinyDB, Query, __all__
from tinydb.operations import delete
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from pprint import pprint
from uuid import UUID
from playsound import playsound
import json
import random
import re
import os
import fnmatch
import time
from decouple import config

# Checking for .env file, create if not there
print("Checking for .env settings file")
cwd = os.getcwd()
sounds = os.listdir(cwd)
if '.env' in sounds:
    time.sleep(1)
    print(".env file detected")
else:
    with open('.env', 'w') as f:
        f.write('APP_ID = \n')
        f.write('SECRET = \n')
        f.write('CHANNEL_ID = \n')
        time.sleep(1)
    print(".env file created, please fill in keys")
    exit()

print("Checking database exists...")
# Build the  DB
db = TinyDB('db.json', encoding = "utf8")
Punished_Sounds = db.table('FILES')
File = Query()
if len(Punished_Sounds) == 0:
    for x in sounds:
        Punished_Sounds.insert({
        'File': x,
        'Playcount': int(1)
        })
    print(f"Inserted {len(Punished_Sounds)} rows into your database")
    time.sleep(2)
    print("Please restart application to use your new database" "\n")
    exit()
else:
    print(f"Database found with {len(Punished_Sounds)} rows")

# Database refresh function, adding only differences in files
def database_check():
    item = Punished_Sounds.all()
    file = [row['File'] for row in item]
    check_differences = [x for x in sounds + file if x not in sounds or x not in file]
    for sound in check_differences:
        Punished_Sounds.insert({
        'File': sound,
        'Playcount': int(1)
        })
    print("Database refresh has been completed \n")

def callback_redemptions(uuid: UUID, data: dict) -> None:
    # Grabbing title
    redeemed = data["data"]["redemption"]["reward"]["title"]
    redeemed += '*'
    # Searching for all files
    sound_search = Punished_Sounds.search(File.File.search(redeemed))
    # Getting length to check if random or not
    range = len(sound_search)
    if range == 1:
        searchpop = sound_search.pop(0)
        filepop = searchpop.get("File")
        # Playsound here
        print(f"Redeemed non-random sound played {filepop}""\n")
        playsound(filepop)
        # Increasing playcount
        playcountpop = int(searchpop.get("Playcount"))
        newplay = playcountpop +1
        Punished_Sounds.upsert({'Playcount': newplay}, File.File == filepop)
    else:
        # Temp table of search results
        Search_Results = db.table('SEARCH_RESULTS')
        for results in sound_search:
            Search_Results.insert({
            'File': results.get("File"),
            'Playcount': results.get("Playcount")
            })
        # Logic to get the least played from temp table
        all_playcount = Search_Results.all()
        playcount = {row['Playcount'] for row in all_playcount}
        try:
            minplay = min(playcount)
        except ValueError as e:
            minplay = 1
        least_played = Search_Results.search(File.Playcount == minplay)
        # Setting random here, in case playcount matches multiple files
        randomfile = random.sample(least_played, 1)
        filepop = randomfile.pop(0)
        thefile = filepop.get("File")
        # Playsound here
        print(f"Redeemed random sound played {thefile}""\n")
        playsound(thefile)
        # Drop temp table
        db.drop_table('SEARCH_RESULTS')
        # Increasing playcount
        newplay = minplay +1
        Punished_Sounds.upsert({'Playcount': newplay}, File.File == thefile)

# setting up Authentication and getting your user id
twitch = Twitch(config('APP_ID'), config('SECRET'))
twitch.authenticate_app([])
target_scope = [AuthScope.CHANNEL_READ_REDEMPTIONS]
auth = UserAuthenticator(twitch, target_scope, force_verify=False)
token, refresh_token = auth.authenticate()
twitch.set_user_authentication(token, target_scope, refresh_token)
channel_id = config('CHANNEL_ID')
# Starting up PubSub
pubsub = PubSub(twitch)
pubsub.start()
uuid = pubsub.listen_channel_points(channel_id, callback_redemptions)
# Checking for input if database check is required
value = input("Please type R to check the db:\n")
v = value
if value == 'R':
    database_check()
