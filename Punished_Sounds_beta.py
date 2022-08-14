from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from pprint import pprint
from uuid import UUID
from playsound import playsound
import os
import random
import fnmatch
import re
from decouple import config

played_sounds = {}
def callback_redemptions(uuid: UUID, data: dict) -> None:
    global played_sounds
    redeemed = data["data"]["redemption"]["reward"]["title"]
    redeemed += "*"
    #setting path
    cwd = os.getcwd()
    sounds = os.listdir(cwd)
    #setting up a new result array
    results = []
    #walk the dir to pull the only result
    for x in range(len(sounds)):
        if fnmatch.fnmatch(sounds[x], redeemed):
            p=sounds[x]
            results.append(p)
    g = random.choice(results)
    #if multiple options
    if len(results)>1:
        #create dictionary call
        played_sounds = add_value(played_sounds, redeemed, None)
        #remove eronius "None" from addition
        played_sounds[redeemed].pop(len(played_sounds[redeemed])-1)
        #if more than 2 option and both specific knockouts occupied, try until knockouts satisfied
        if len(results) > 2 and len(played_sounds[redeemed]) > 1:
            while g == played_sounds[redeemed][0] or g == played_sounds[redeemed][1]:
                g = random.choice(results)
        else:
            #if more than 2 option and only specific knockout occupied, try until knockout satisfied
            if len(results) > 2 and len(played_sounds[redeemed]) == 1:
                while g == played_sounds[redeemed][0]:
                    g = random.choice(results)
            else:
                #if first entry of multiple options
                if len(played_sounds[redeemed]) == 0:
                    g = random.choice(results)
                else:
                    #if only 2 options
                    while g == played_sounds[redeemed][0]:
                        g = random.choice(results)
        #added played file to directory
        played_sounds = add_value(played_sounds, redeemed, g)
        #remove expired knockout
        if len(played_sounds[redeemed])>2:
            played_sounds[redeemed].pop(0)
    playsound(g)
    print(f"Played: {g}" "\n")


def add_value(sample_dict, key, newEntry):
#add redeem name to dictionary and add sound to its list
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].append(newEntry)
    return sample_dict



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
