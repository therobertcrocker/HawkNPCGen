import json
import random
import requests
import os

with open('data_lists.json') as f:
    data = json.load(f)


class NPC:
    # -------------------------------------------- Set Up -------------------------------------------------
    def __init__(self):
        self.culture = ""
        self.race = ""
        self.gender = ""
        self.name = ""
        self.surname = ""
        self.appearance = ""
        self.ability = ""
        self.talent = ""
        self.mannerism = ""
        self.interaction = ""
        self.accent = ""
        self.vocals = ""
        self.texture = ""
        self.quirk = ""
        self.data = {}

    # -------------------------------------------- Individual Generators  ----------------------------------

    def gen_culture(self):
        self.culture = random.choice(data["cultures"])

    def gen_race(self):
        self.race = random.choice(data["races"][self.culture])

    def gen_gender(self):
        self.gender = random.choice(data["genders_full"])

    def gen_appearance(self):
        self.appearance = random.choice(data["traits"]["appearance"])

    def gen_ability(self):
        ability_list = [0, 1, 2, 3, 4, 5]
        high_pick = random.choice(ability_list)
        low_pick = random.choice(ability_list)
        while high_pick == low_pick:
            low_pick = random.choice(ability_list)
        self.ability = data["traits"]["high ability"][high_pick] + ", " + data["traits"]["low ability"][low_pick]

    def gen_talent(self):
        talent = random.randrange(2)
        if talent == 1:
            self.talent = random.choice(data["traits"]["talent"])
        else:
            self.talent = "None"

    def gen_manner(self):
        self.mannerism = random.choice(data["traits"]["mannerism"])

    def gen_interact(self):
        self.interaction = random.choice(data["traits"]["interaction"])

    def gen_accent(self):
        self.accent = random.choice(data["voice"]["accents"][self.culture])

    def gen_vocals(self):
        self.vocals = "Speaks " + random.choice(data["voice"]["Speed"]) + \
                      ", at a " + random.choice(data["voice"]["Pitch"]) + " pitch."

    def gen_texture(self):
        self.texture = "Has a " + random.choice(data["voice"]["Texture"]) + " voice."

    def gen_quirk(self):
        self.quirk = random.choice(data["voice"]["Quirk"])

    # -------------------------------------------- Main Functions ----------------------------------

    def quick_gen(self, **traits):
        self.gen_base(traits)
        self.gen_traits()
        self.gen_voice()
        self.make_data()

    def full_base(self):
        self.gen_culture()
        self.gen_race()
        self.gen_gender()
        self.get_name()
        self.get_surname()

    def gen_base(self, traits):
        if traits:
            if 'race' in traits and 'culture' in traits:
                self.culture = traits['culture']
                self.race = traits['race']
            elif 'race' in traits and 'culture' not in traits:
                self.race = traits['race']
                for i in data["races"]:
                    if traits['race'] in data["races"][i]:
                        self.culture = i
            elif 'race' not in traits and 'culture' in traits:
                self.culture = traits['culture']
                self.gen_race()
            elif 'race' not in traits and 'culture' not in traits:
                self.culture = traits['culture']
                self.race = random.choice(data["races"][self.culture])
            if 'gender' in traits:
                self.gender = traits["gender"]
            else:
                self.gender = random.choice(data["genders_full"])
            self.get_name()
            self.get_surname()
        else:
            self.full_base()

    def gen_traits(self):
        self.gen_appearance()
        self.gen_ability()
        self.gen_talent()
        self.gen_manner()
        self.gen_interact()

    def gen_voice(self):
        self.gen_accent()
        self.gen_vocals()
        self.gen_texture()
        self.gen_quirk()

    # -------------------------------------------- Name Generation ----------------------------------
    def get_name(self):
        namebase = random.choice(data["namebases"][self.culture])
        key = "ro573598767"
        number = "1"
        req_base = "https://www.behindthename.com/api/random.json?key=" + key
        req_usage = "&usage=" + namebase
        req_gender = "&gender=" + data["genders"][data["genders_full"].index(self.gender)]
        req_number = "&number=" + number
        if self.gender == "o":
            full_req = req_base + req_number + req_usage
        else:
            full_req = req_base + req_number + req_usage + req_gender

        name = requests.get(full_req).json()
        try:
            self.name = name["names"][0]
        except:
            if self.gender != "Enby":
                self.name = random.choice(data["names"][self.culture][self.gender])
            else:
                self.name = random.choice(data["names"][self.culture][random.choice(["Male", "Female"])])

    def get_surname(self):
        if self.culture in ["Akti", "Huron (Urn)", "Isfolk"]:
            surname = random.choice(data["surnames"][self.culture][self.gender])
        else:
            surname = random.choice(data['surnames'][self.culture])

        self.surname = surname

    # -------------------------------------------- Saving, Making, and Loading ----------------------------------
    def load(self, file):
        with open(file) as g:
            npc = json.load(g)
        if "base" in npc:
            self.culture = npc["base"].split(" | ")[1].split(" - ")[0]
            self.race = npc["base"].split(" | ")[1].split(" - ")[1]
            self.gender = npc["base"].split(" | ")[0]
            self.name = npc["Full Name"].split(", ")[0]
            self.surname = npc["Full Name"].split(", ")[1]
        else:
            self.gen_base()
        if "traits" in npc and "personality" in npc:
            self.appearance = npc["traits"]["appearance"]
            if "high ability" in npc["traits"]:
                self.ability = npc["traits"]["high ability"] + ", " + npc["traits"]["low ability"]
            elif "abilities" in npc["traits"]:
                self.ability = npc["traits"]["abilities"]
            self.talent = npc["personality"]["talent"]
            self.mannerism = npc["personality"]["mannerism"]
            self.interaction = npc["personality"]["interaction"]
        else:
            self.gen_traits()
        if "voice" in npc:
            self.accent = npc["voice"]["accent"]
            self.vocals = npc["voice"]["vocals"]
            self.texture = npc["voice"]["texture"]
            self.quirk = npc["voice"]["quirk"]
        else:
            self.gen_voice()
        self.make_data()

    def make_data(self):
        self.data = {
            "name": self.name + ", " + self.surname,
            "base": self.gender + " | " + self.culture + " - " + self.race,
            "traits": {
                "appearance": self.appearance,
                "abilities": self.ability
            },
            "personality": {
                "talent": self.talent,
                "mannerism": self.mannerism,
                "interaction": self.interaction
            },
            "voice": {
                "accent": self.accent,
                "vocals": self.vocals,
                "texture": self.texture,
                "quirk": self.quirk
            }
        }

    def show_data(self):
        print(json.dumps(self.data, indent=4, ensure_ascii=False))

    def save_data(self):
        filename = self.race + " - " + self.name + "_" + self.surname
        parent = "npcs"
        path = os.path.join(parent, self.culture, self.gender)
        h = open(path + "/" + filename + '.json', "w")
        json.dump(self.data, h, indent=4, ensure_ascii=False)
        print("Sucess! saved: " + self.gender + " " + self.culture + " - created: " + self.name + " " + self.surname)
