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

played_sounds = {}
def callback_redemptions(uuid: UUID, data: dict) -> None:
    global played_sounds
    redeemed = data["data"]["redemption"]["reward"]["title"] + "*"
    #creating list of files
    sounds = os.listdir()
    #grabbing the files that start with the redeem name
    results = [file for file in sounds if re.search(redeemed, file)]
    g = random.choice(results)
    #if multiple options
    if len(results)>1:
        if redeemed in played_sounds:
            #checking if the random sound has been played recently
            while g in played_sounds[redeemed]:
                g = random.choice(results)
        #added played file to directory
        played_sounds = add_value(played_sounds, redeemed, g)
        #remove expired knockout
        if len(played_sounds[redeemed])>(math.ceil(len(results)/3)):
            played_sounds[redeemed].pop(0)
    print(f"Played: {g}" "\n")
    playsound(g)


def add_value(dict, key, newEntry):
#add redeem name to dictionary and add sound to its list
    if key not in dict:
        dict[key] = list()
    dict[key].append(newEntry)
    return dict



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
input('You can press ENTER in order to close script\n\n')
# you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
pubsub.unlisten(uuid)
pubsub.stop()
