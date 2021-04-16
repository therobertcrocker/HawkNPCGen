import json
from NPC import NPC
import time
from npcs import walk_dir
import random
import os

with open('data_lists.json') as f:
    data = json.load(f)


def make_many_npcs(num):
    genders = ["Male", "Female", "Enby"]
    for i in data["cultures"]:
        for y in range(3):
            for x in range(num):
                try:
                        npc = NPC()
                        npc.quick_gen(culture=i, gender=genders[y])
                        npc.save_data()
                except:
                    print("Something went wrong")
                finally:
                    time.sleep(3)


def make_many_culture(num, culture):
    genders = ["Male", "Female", "Enby"]
    for x in range(num):
        for y in genders:
            try:
                npc = NPC()
                npc.quick_gen(culture= culture, gender= y)
                npc.save_data()
            except:
                print("Something went wrong")
            finally:
                time.sleep(3)


def make_many_race(num, race):
    genders = ["Male", "Female", "Enby"]
    for x in range(num):
        for y in genders:
            try:
                npc = NPC()
                npc.quick_gen(race=race, gender=y)
                npc.save_data()
            except:
                print("Something went wrong")
            finally:
                time.sleep(3)