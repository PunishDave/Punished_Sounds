from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from uuid import UUID
from playsound import playsound
import os
import random
import re
import math
from decouple import config

# Creating list of files
sounds = os.listdir()
# Checking for .env file, create if not there
print("Checking for .env settings file \n")
if '.env' in sounds:
    print(".env file detected")
else:
    with open('.env', 'w') as f:
        f.write('APP_ID = \n')
        f.write('SECRET = \n')
        f.write('CHANNEL_ID = \n')
    print(".env file created, please fill in keys \n")
    exit()

played_sounds = {}
def callback_redemptions(uuid: UUID, data: dict) -> None:
    global played_sounds
    redeemed = data["data"]["redemption"]["reward"]["title"] + "*"
    # Grabbing the files that start with the redeem name
    results = [file for file in sounds if re.search(redeemed, file)]
    g = random.choice(results)
    # If multiple options
    if len(results)>1:
        if redeemed in played_sounds:
            # Checking if the random sound has been played recently
            while g in played_sounds[redeemed]:
                g = random.choice(results)
        # Added played file to directory
        played_sounds = add_value(played_sounds, redeemed, g)
        # Remove expired knockout
        if len(played_sounds[redeemed])>(math.ceil(len(results)/3)):
            played_sounds[redeemed].pop(0)
    print(f"Played: {g}" "\n")
    playsound(g)

def add_value(dict, key, newEntry):
# Add redeem name to dictionary and add sound to its list
    if key not in dict:
        dict[key] = list()
    dict[key].append(newEntry)
    return dict

# Setting up Authentication and getting your user id
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
# Logic to quit script
input('You can press ENTER in order to close script\n\n')
pubsub.unlisten(uuid)
pubsub.stop()
exit()
