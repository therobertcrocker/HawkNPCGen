import json
import random
import requests
import os

with open('data_lists.json') as f:
    data = json.load(f)


class NPC:

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
        self.data = {}

    def load(self, file):
        with open(file) as g:
            npc = json.load(g)
        if "base" in npc:
            self.culture = npc["base"].split(" | ")[1].split(" - ")[0]
            self.race = npc["base"].split(" | ")[1].split(" - ")[1]
            self.gender = npc["base"].split(" | ")[0]
            self.name = npc["Full Name"].split(", ")[0]
            self.surname = npc["Full Name"].split(", ")[1]
        if "traits" in npc:
            self.appearance = npc["traits"]["appearance"]
            if "high ability" in npc["traits"]:
                self.ability = npc["traits"]["high ability"] + ", " + npc["traits"]["low ability"]
            elif "abilities" in npc["traits"]:
                self.ability = npc["traits"]["abilities"]
        if "personality" in npc:
            self.talent = npc["personality"]["talent"]
            self.mannerism = npc["personality"]["mannerism"]
            self.interaction = npc["personality"]["interaction"]
        self.make_data()

    def quick_gen(self, **traits):
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
                self.set_culture(traits['culture'])
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
            self.full_gen()
        self.gen_traits()
        self.make_data()

    def make_data(self):
        self.data = {
            "Full Name": self.name + ", " + self.surname,
            "base": self.gender + " | " + self.culture + " - " + self.race,
            "traits": {
                "appearance":self.appearance,
                "abilities": self.ability
            },
            "personality": {
                "talent": self.talent,
                "mannerism": self.mannerism,
                "interaction": self.interaction
            }
        }

    def set_culture(self, culture):
        self.culture = culture

    def gen_culture(self):
        self.culture = random.choice(data["cultures"])

    def gen_gender(self):
        self.gender = random.choice(data["genders_full"])

    def set_gender(self, gender):
        self.gender = gender

    def gen_race(self):
        self.race = random.choice(data["races"][self.culture])

    def set_race(self, race):
        self.race = race

    def gen_traits(self):
        self.appearance = random.choice(data["traits"]["appearance"])
        ability_list = [0, 1, 2, 3, 4, 5]
        talent = random.randrange(2)
        high_pick = random.choice(ability_list)
        low_pick = random.choice(ability_list)
        while high_pick == low_pick:
            low_pick = random.choice(ability_list)
        self.ability = data["traits"]["high ability"][high_pick] + ", " + data["traits"]["low ability"][low_pick]
        if talent == 1:
            self.talent = random.choice(data["traits"]["talent"])
        else:
            self.talent = "None"
        self.mannerism = random.choice(data["traits"]["mannerism"])
        self.interaction = random.choice(data["traits"]["interaction"])

    def full_gen(self):
        self.gen_culture()
        self.gen_race()
        self.gen_gender()
        self.get_name()
        self.get_surname()

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

    def show_data(self):
        print(json.dumps(self.data, indent=4, ensure_ascii=False))

    def save_data(self):
        filename = self.race + " - " + self.name + "_" + self.surname
        parent = "npcs"
        path = os.path.join(parent, self.culture, self.gender)
        h = open(path + "/" + filename + '.json', "w")
        json.dump(self.data, h, indent=4, ensure_ascii=False)
        print("Sucess! saved: " + self.gender + " " + self.culture + " - created: " + self.name + " " + self.surname)

