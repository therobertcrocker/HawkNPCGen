# Python code to search .mp3 files in current
# folder (We can change file type/name and path
# according to the requirements.
import os
from NPC import NPC

# This is to get the directory that the program
# is currently running in.
dir_path = os.path.dirname(os.path.realpath(__file__))


def rename():
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            npc = NPC()

        # change the extension from '.mp3' to
        # the one of your choice.
            if file.endswith('.json'):
                npc.load(root + '/' + str(file))
                new_name = npc.race + " - " + npc.name + "_" + npc.surname + ".json"
                os.rename(root + '/' + str(file), root + '/' + str(new_name))

def refactor():
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            npc = NPC()

        # change the extension from '.mp3' to
        # the one of your choice.
            if file.endswith('.json'):
                npc.load(root + '/' + str(file))
                print("loaded: " + str(file))
                npc.save_data()
                print("    - saved: " + str(file))

def pick_refactor(*changes):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            npc = NPC()

        # change the extension from '.mp3' to
        # the one of your choice.
            if file.endswith('.json'):
                npc.load(root + '/' + str(file))
                print("loaded: " + str(file))
                if 'culture' in changes:
                    npc.gen_culture()
                if 'race' in changes:
                    npc.gen_race()
                if 'gender' in changes:
                    npc.gen_gender()
                if 'appearance' in changes:
                    npc.gen_appearance()
                if 'ability' in changes:
                    npc.gen_ability()
                if 'talent' in changes:
                    npc.gen_talent()
                if 'mannerism' in changes:
                    npc.gen_manner()
                if 'interact' in changes:
                    npc.gen_interact()
                if 'accent' in changes:
                    npc.gen_accent()
                if 'vocals' in changes:
                    npc.gen_vocals()
                if 'texture' in changes:
                    npc.gen_texture()
                if 'quirk' in changes:
                    npc.gen_quirk()
                npc.make_data()
                npc.save_data()


