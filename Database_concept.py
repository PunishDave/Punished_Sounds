from tinydb import TinyDB, Query, __all__
from tinydb.operations import delete
import json
import random
import re
import os

redeemed = "Oh_mike"
print(f"Searching for {redeemed}")
db = TinyDB('db.json', encoding = "utf8")
Punished_Sounds = db.table('FILES')


#Build the  DB
# path = "/home/d-berry/github/db/python/twitchbot/SoundClips"
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
    for results in sound_search:
        Search_Results = db.table('SEARCH_RESULTS')
        Search_Results.insert({
            'Name': results.get("Name"),
            'File': results.get("File"),
            'Playcount': results.get("Playcount")
            })
    #Logic to get the least played from temp table
    Search_Results = db.table('SEARCH_RESULTS')
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
