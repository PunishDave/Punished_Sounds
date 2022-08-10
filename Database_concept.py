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
path = "C:\\Users\\insat\\Documents\\dev\\db\\python\\twitchbot\\SoundClips"

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
search = Punished_Sounds.search(File.Name.search(redeemed))

print("\n")
searchpop = search.pop()
print(searchpop)
