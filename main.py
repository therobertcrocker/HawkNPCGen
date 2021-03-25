import json
from NPC import NPC
import time
import random
import os

with open('data_lists.json') as f:
    data = json.load(f)


def make_many_npcs(num):
    for i in data["cultures"]:
        for x in range(num):
            try:
                npc = NPC()
                npc.quick_gen(culture=i)
                print("Sucess! created: " + npc.name + " " + npc.surname)
                npc.save_data()
            except:
                print("Something went wrong")
            finally:
                time.sleep(3)


def make_many_culture(num, culture):
    for x in range(num):
        try:
            npc = NPC()
            npc.quick_gen(culture= culture)
            print("Sucess! created: " + npc.name + " " + npc.surname)
            npc.save_data()
        except:
            print("Something went wrong")
        finally:
            time.sleep(3)
