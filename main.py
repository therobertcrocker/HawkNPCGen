import json
from NPC import NPC
import time
import random

with open('data_lists.json') as f:
    data = json.load(f)


def make_many_npcs(num):
    for i in data["cultures"]:
        for x in range(num):
            try:
                npc = NPC(culture=i)
                print("Sucess! created: " + npc.name + " " + npc.surname)
                npc.save_data()
            except:
                print("Something went wrong")
            finally:
                time.sleep(1)


for i in range(5):
    print(random.randrange(2))




