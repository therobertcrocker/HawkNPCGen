import json
import random
import requests
import os
from constants import cultures, lists, character

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
        self.culture = random.choice(data[lists.CULTURES])

    def gen_race(self):
        self.race = random.choice(data[lists.RACES][self.culture])

    def gen_gender(self):
        self.gender = random.choice(data[lists.GENDERS_FULL])

    def gen_appearance(self):
        self.appearance = random.choice(data[lists.TRAITS][lists.APPEARANCE])

    def gen_ability(self):
        ability_list = [0, 1, 2, 3, 4, 5]
        high_pick = random.choice(ability_list)
        low_pick = random.choice(ability_list)
        while high_pick == low_pick:
            low_pick = random.choice(ability_list)
        self.ability = data[lists.TRAITS][lists.HIGHABILITY][high_pick] + ", " \
                       + data[lists.TRAITS][lists.LOWABILITY][low_pick]

    def gen_talent(self):
        talent = random.randrange(2)
        if talent == 1:
            self.talent = random.choice(data[lists.TRAITS][lists.TALENT])
        else:
            self.talent = "None"

    def gen_manner(self):
        self.mannerism = random.choice(data[lists.TRAITS][lists.MANNERISM])

    def gen_interact(self):
        self.interaction = random.choice(data[lists.TRAITS][lists.INTERACTION])

    def gen_accent(self):
        pick = random.randrange(0, 5)
        if pick < 2:
            self.accent = "None"
        else:
            self.accent = random.choice(data[lists.VOICE][lists.ACCENT][self.culture])

    def gen_vocals(self):
        self.vocals = "Speaks " + random.choice(data[lists.VOICE][lists.SPEED]) + \
                      ", at a " + random.choice(data[lists.VOICE][lists.PITCH]) + " pitch."

    def gen_texture(self):
        self.texture = "Has a " + random.choice(data[lists.VOICE][lists.TEXTURE]) + " voice."

    def gen_quirk(self):
        self.quirk = random.choice(data[lists.VOICE][lists.QUIRK])

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
            # Defining the conditions for the parameters given in traits
            is_racial = character.RACE in traits
            is_cultural = character.CULTURE in traits
            is_gendered = character.GENDER in traits

            if is_racial and is_cultural:
                self.culture = traits[character.CULTURE]
                self.race = traits[character.RACE]
                
            elif is_racial and not is_cultural:
                self.race = traits[character.RACE]
                for i in data[lists.RACES]:
                    if traits[character.RACE] in data[lists.RACES][i]:
                        self.culture = i
                        
            elif not is_racial and is_cultural:
                self.culture = traits[character.CULTURE]
                self.gen_race()
                
            elif not is_racial and not is_cultural:
                self.culture = traits[character.CULTURE]
                self.race = random.choice(data[lists.RACES][self.culture])
                
            if is_gendered:
                self.gender = traits[character.GENDER]
            else:
                self.gender = random.choice(data[lists.GENDERS_FULL])
                
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
        KEY = "ro573598767"
        NUMBER = "1"
        REQ_BASE = "https://www.behindthename.com/api/random.json?key=" + KEY
        REQ_USAGE = "&usage=" + namebase
        REQ_GENDER = "&gender=" + data[lists.GENDERS][data[lists.GENDERS_FULL].index(self.gender)]
        REQ_NUMBER = "&number=" + NUMBER
        if self.gender == data[lists.GENDERS][2]:
            FULL_REQ = REQ_BASE + REQ_NUMBER + REQ_USAGE
        else:
            FULL_REQ = REQ_BASE + REQ_NUMBER + REQ_USAGE + REQ_GENDER

        name = requests.get(FULL_REQ).json()
        try:
            self.name = name[lists.NAMES][0]
        except:
            if self.gender != lists.GENDERS_ENBY:
                self.name = random.choice(data[lists.NAMES][self.culture][self.gender])
            else:
                self.name = random.choice(
                    data[lists.NAMES][self.culture][random.choice([lists.GENDERS_MALE, lists.GENDERS_FEMALE])])

    def get_surname(self):
        if self.culture in [cultures.AKTI, cultures.HURON_URN, cultures.ISFOLK]:
            surname = random.choice(data[lists.SURNAMES][self.culture][self.gender])
        else:
            surname = random.choice(data[lists.SURNAMES][self.culture])

        self.surname = surname

    # -------------------------------------------- Saving, Making, and Loading ----------------------------------
    def load(self, file):
        with open(file) as g:
            npc = json.load(g)
        if character.BASE in npc:
            self.culture = npc[character.BASE].split(" | ")[1].split(" - ")[0]
            self.race = npc[character.BASE].split(" | ")[1].split(" - ")[1]
            self.gender = npc[character.BASE].split(" | ")[0]
            self.name = npc[character.NAME].split(", ")[0]
            self.surname = npc[character.NAME].split(", ")[1]
        else:
            self.gen_base()
        if character.TRAITS in npc and character.PERSONALITY in npc:
            self.appearance = npc[character.TRAITS][character.APPEARANCE]
            if lists.HIGHABILITY in npc[character.TRAITS]:
                self.ability = npc[character.TRAITS][lists.HIGHABILITY] + ", " + npc[character.TRAITS][lists.LOWABILITY]
            elif character.ABILITIES in npc[character.TRAITS]:
                self.ability = npc[character.TRAITS][character.ABILITIES]
            self.talent = npc[character.PERSONALITY][character.TALENT]
            self.mannerism = npc[character.PERSONALITY][character.MANNERISM]
            self.interaction = npc[character.PERSONALITY][character.INTERACTION]
        else:
            self.gen_traits()
        if character.VOICE in npc:
            self.accent = npc[character.VOICE][character.ACCENT]
            self.vocals = npc[character.VOICE][character.VOCALS]
            self.texture = npc[character.VOICE][character.TEXTURE]
            self.quirk = npc[character.VOICE][character.QUIRK]
        else:
            self.gen_voice()
        self.make_data()

    def make_data(self):
        self.data = {
            character.NAME: self.name + ", " + self.surname,
            character.BASE: self.gender + " | " + self.culture + " - " + self.race,
            character.TRAITS: {
                character.APPEARANCE: self.appearance,
                character.ABILITIES: self.ability
            },
            character.PERSONALITY: {
                character.TALENT: self.talent,
                character.MANNERISM: self.mannerism,
                character.INTERACTION: self.interaction
            },
            character.VOICE: {
                character.ACCENT: self.accent,
                character.VOCALS: self.vocals,
                character.TEXTURE: self.texture,
                character.QUIRK: self.quirk
            }
        }

    def show_data(self):
        print(json.dumps(self.data, indent=4, ensure_ascii=False))

    def save_data(self):
        filename = self.race + " - " + self.name + "_" + self.surname
        parent = "npcs"
        path = os.path.join(parent, self.culture, self.gender)
        h = open(path + "/" + filename + '.json', "w")
        json.dump(self.data, h, indent=4, ensure_ascii=True)
        print("Sucess! saved: " + self.gender + " " + self.culture + " - created: " + self.name + " " + self.surname)
