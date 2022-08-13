from tinydb import TinyDB, Query, __all__
from tinydb.operations import delete
import json
import random
import re
import os

#Build the  DB

db = TinyDB('db.json', encoding = "utf8")
Punished_Sounds = db.table('FILES')

path = "C:\\Users\\insat\\Documents\\dev\\db\\python\\twitchbot\\SoundClips"
for root, dirs, files in os.walk(path):
    for name in files:
        Punished_Sounds.insert({
            'Name': name[:-4],
            'File': os.path.join(root,name),
            'Playcount': int(1)
            })
