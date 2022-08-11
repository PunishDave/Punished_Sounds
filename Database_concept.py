from tinydb import TinyDB, Query, __all__
from tinydb.operations import delete
import json
import random
import re
import os

redeemed = "Oh_mike"
results = {}
print(f"Searching for {redeemed}")
db = TinyDB('db.json', encoding = "utf8")
Punished_Sounds = db.table('FILES')
path = "/home/d-berry/github/db/python/twitchbot/SoundClips"

#Build the  DB
# for root, dirs, files in os.walk(path):
#     for name in files:
#         Punished_Sounds.insert({
#             'Name': name[:-4],
#             'File': os.path.join(root,name),
#             'Playcount': int(1)
#             })

#Search for the file
File = Query()
#Searching for all files
sound_search = Punished_Sounds.search(File.Name.search(redeemed))
#Getting length
range = len(sound_search)
#Since lists start at index 0, need to add 0 and remove one from length
rangecomprehension = [0]
rangecomprehension.append(range - 1)

if range == 1:
    print("Not Random")
    searchpop = sound_searchj.pop(0)
    filepop = searchpop.get('File')
    print(filepop)
else:
    print("Random")
    #get playcount
    for item in sound_search:
        The_file = item.get("File")
        The_playcount = item.get("Playcount")
        sound_dict = {The_file: The_playcount}
        minimum = sound_dict
    print(minimum)
    #pick the least

    #print
