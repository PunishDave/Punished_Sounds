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

oldsound1 = ""
oldsound2 = ""
def callback_redemptions(uuid: UUID, data: dict) -> None:
    global oldsound1
    global oldsound2
    redeemed = data["data"]["redemption"]["reward"]["title"]
    #setting path
    path = "C:\Users\dmvh1\Desktop\TwitchSounds"
    cleaned = redeemed.replace('#', '')
    cleaned += "*"
    #setting up a new result array
    results = []
    #walk the dir to pull the only result
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, cleaned):
                 p = os.path.join(root, name)
                 results.append(p)
    g = random.choice(results)
    if re.search("[#]", redeemed):
        if len(results) > 2:
            while g == oldsound1 or g == oldsound2:
                 g = random.choice(results)
        else:
            while g == oldsound1:
                 g = random.choice(results)
    playsound(g)
    print(f"Played: {g}" "\n")
    oldsound2 = oldsound1
    oldsound1 = g
