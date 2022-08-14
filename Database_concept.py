from tinydb import TinyDB, Query, __all__
from tinydb.operations import delete
import json
import random
import re
import os
import time
import keyboard
from decouple import config

def callback_redemptions(uuid: UUID, data: dict) -> None:
    #grabbing title
    redeemed = data["data"]["redemption"]["reward"]["title"]
    redeemed += '*'
    #Build the  DB
    db = TinyDB('db.json', encoding = "utf8")
    Punished_Sounds = db.table('FILES')
    File = Query()
    #get the working dir
    cwd = os.getcwd()
    sounds = os.listdir(cwd)
    print("Checking database exists...")
    if len(Punished_Sounds) == 0:
        for x in sounds:
            Punished_Sounds.insert({
            'File': x,
            'Playcount': int(1)
            })
        print(f"Inserted {len(Punished_Sounds)} rows into your database")
    time.sleep(2)
    print("Check completed, thanks for waiting" "\n")
    def  database_check():
        item = Punished_Sounds.all()
        file = [row['File'] for row in item]
        check_differences = [x for x in sounds + file if x not in sounds or x not in file]
        for sound in check_differences:
            Punished_Sounds.insert({
            'File': sound,
            'Playcount': int(1)
            })
    #Searching for all files
    sound_search = Punished_Sounds.search(File.File.search(redeemed))
    #Getting length
    range = len(sound_search)
    #Since lists start at index 0, need to add 0 and remove one from length
    rangecomprehension = [0]
    rangecomprehension.append(range - 1)
    if range == 1:
        print("Not Random")
        searchpop = sound_search.pop(0)
        filepop = searchpop.get("File")
        #Playsound here
        print(filepop)
        #Increasing playcount
        playcountpop = int(searchpop.get("Playcount"))
        newplay = playcountpop +1
        Punished_Sounds.upsert({'Playcount': newplay}, File.File == filepop)
    else:
        print("Random")
        # Temp table idea - need to drop this after
        Search_Results = db.table('SEARCH_RESULTS')
        for results in sound_search:
            Search_Results.insert({
            'File': results.get("File"),
            'Playcount': results.get("Playcount")
            })
            #Logic to get the least played from temp table
            all_playcount = Search_Results.all()
            playcount = {row['Playcount'] for row in all_playcount}
            minplay = min(playcount)
            least_played = Search_Results.search(File.Playcount == minplay)
            #Setting random here, in case playcount matches multiple files
            randomfile = random.sample(least_played, 1)
            filepop = randomfile.pop(0)
            thefile = filepop.get("File")
            #Playsound here
            print(thefile)
            #Drop temp table
            db.drop_table('SEARCH_RESULTS')
            #Increasing playcount
            newplay = minplay +1
            Punished_Sounds.upsert({'Playcount': newplay}, File.File == thefile)

    if keyboard.is_pressed("r"):
        database_check()
        print("Database refresh completed")
# setting up Authentication and getting your user id
twitch = Twitch(config('APP_ID'), config('SECRET'))
twitch.authenticate_app([])
# you can get your user auth token and user auth refresh token following the example in twitchAPI.oauth
target_scope = [AuthScope.CHANNEL_READ_REDEMPTIONS]
auth = UserAuthenticator(twitch, target_scope, force_verify=False)
token, refresh_token = auth.authenticate()
twitch.set_user_authentication(token, target_scope, refresh_token)
channel_id = config('CHANNEL_ID')
# starting up PubSub
pubsub = PubSub(twitch)
pubsub.start()
# you can either start listening before or after you started pubsub.
uuid = pubsub.listen_channel_points(channel_id, callback_redemptions)
input('You can press ENTER in order to close script')
# you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
pubsub.unlisten(uuid)
pubsub.stop()
