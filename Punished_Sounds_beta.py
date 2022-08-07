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

def callback_redemptions(uuid: UUID, data: dict) -> None:
    #grabbing title
    redeemed = data["data"]["redemption"]["reward"]["title"]
    #Taking off potential # and adding a wildcard for the search
    filename = re.sub(r"[^a-zA-Z-_]","",redeemed)
    filename += '*'
    #setting path
    path = "C:\\Path\\to\\where\\your\\sounds\\are"
    #Setting an array of results
    result = []
    #Walking the dir for the results
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, filename):
                d = os.path.join(root, name)
                result.append(d)
    #If # is detected, do a random result
    if re.search("[#]", redeemed):
        choice = random.choice(result)
        print(f'Random choice played: {choice}' '\n')
        playsound(choice)
    #If no # detected, just play the result since there should be one
    else:
        print(f'Played: {d}' '\n')
        playsound(d)

# setting up Authentication and getting your user id
twitch = Twitch('Client ID goes here', 'Client Secret goes here')
twitch.authenticate_app([])
# you can get your user auth token and user auth refresh token following the example in twitchAPI.oauth
target_scope = [AuthScope.CHANNEL_READ_REDEMPTIONS]
auth = UserAuthenticator(twitch, target_scope, force_verify=False)
token, refresh_token = auth.authenticate()
twitch.set_user_authentication(token, target_scope, refresh_token)
channel_id = 'Channel ID goes here'
# starting up PubSub
pubsub = PubSub(twitch)
pubsub.start()
# you can either start listening before or after you started pubsub.
uuid = pubsub.listen_channel_points(channel_id, callback_redemptions)
input('You can press ENTER in order to close script \n \n')
# you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
pubsub.unlisten(uuid)
pubsub.stop()
