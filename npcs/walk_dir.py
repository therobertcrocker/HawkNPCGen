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
                npc.gen_traits()
                npc.make_data()
                npc.save_data()
                print("    - saved: " + str(file))
