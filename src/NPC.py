import json
import random
import requests
import os

with open('src/data_lists.json') as f:
    data = json.load(f)

# --------------------------------- CONSTANTS ------------------------------------------------------------

# Cultures
AKTI = "Akti"
ARIDO = "Arido"
HURON_MAER = "Huron (Maer)"
HURON_URN = "Huron (Urn)"
ISFOLK = "Isfolk"
LOCHMOOR = "Lochmoor"
USUHAN = "Usuhan"

# Datalists
NAMES = "names"
NAMEBASES = "nambases"
SURNAMES = "surnames"
GENDERS = "genders"
GENDERS_FULL = "genders_full"
# Genders
ENBY = "Enby"
MALE = "Male"
FEMALE = "Female"
RACES = "races"
CULTURES = "cultures"
TRAITS = "traits"
APPEARANCES = "appearances"
HIGH_ABILITY = "high ability"
LOW_ABILITY = "low ability"
TALENTS = "talents"
MANNERISMS = "mannerisms"
INTERACTIONS = "interactions"
VOICES = "voices"
ACCENTS = "accents"
SPEED = "speed"
PITCH = "pitch"
TEXTURES = "textures"
QUIRKS = "quirks"

# NPC
NAME = "name"
BASE = "base"
RACE = "race"
CULTURE = "culture"
GENDER = "gender"
TRAITS = "traits"
APPEARANCE = "appearance"
ABILITIES = "abilities"
PERSONALITY = "personality"
TALENT = "talent"
MANNERISM = "mannerism"
INTERACTION = "interaction"
VOICE = "voice"
ACCENT = "accent"
VOCALS = 'vocals'
TEXTURE = "texture"
QUIRK = "quirk"


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
        self.culture = random.choice(data[CULTURES])

    def gen_race(self):
        self.race = random.choice(data[RACES][self.culture])

    def gen_gender(self):
        self.gender = random.choice(data[GENDERS_FULL])

    def gen_appearance(self):
        self.appearance = random.choice(data[TRAITS][APPEARANCES])

    def gen_ability(self):
        ability_list = [0, 1, 2, 3, 4, 5]
        high_pick = random.choice(ability_list)
        low_pick = random.choice(ability_list)
        while high_pick == low_pick:
            low_pick = random.choice(ability_list)
        self.ability = data[TRAITS][HIGH_ABILITY][high_pick] + ", " \
                       + data[TRAITS][LOW_ABILITY][low_pick]

    def gen_talent(self):
        talent = random.randrange(2)
        if talent == 1:
            self.talent = random.choice(data[TRAITS][TALENTS])
        else:
            self.talent = "None"

    def gen_manner(self):
        self.mannerism = random.choice(data[TRAITS][MANNERISMS])

    def gen_interact(self):
        self.interaction = random.choice(data[TRAITS][INTERACTIONS])

    def gen_accent(self):
        pick = random.randrange(0, 5)
        if pick < 2:
            self.accent = "None"
        else:
            self.accent = random.choice(data[VOICES][ACCENTS][self.culture])

    def gen_vocals(self):
        self.vocals = "Speaks " + random.choice(data[VOICES][SPEED]) + \
                      ", at a " + random.choice(data[VOICES][PITCH]) + " pitch."

    def gen_texture(self):
        self.texture = "Has a " + random.choice(data[VOICES][TEXTURES]) + " voice."

    def gen_quirk(self):
        self.quirk = random.choice(data[VOICES][QUIRKS])

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
            is_racial = RACE in traits
            is_cultural = CULTURE in traits
            is_gendered = GENDER in traits

            if is_racial and is_cultural:
                self.culture = traits[CULTURE]
                self.race = traits[RACE]

            elif is_racial and not is_cultural:
                self.race = traits[RACE]
                for i in data[RACES]:
                    if traits[RACE] in data[RACES][i]:
                        self.culture = i

            elif not is_racial and is_cultural:
                self.culture = traits[CULTURE]
                self.gen_race()

            elif not is_racial and not is_cultural:
                self.culture = traits[CULTURE]
                self.race = random.choice(data[RACES][self.culture])

            if is_gendered:
                self.gender = traits[GENDER]
            else:
                self.gender = random.choice(data[GENDERS_FULL])

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
        REQ_GENDER = "&gender=" + data[GENDERS][data[GENDERS_FULL].index(self.gender)]
        REQ_NUMBER = "&number=" + NUMBER
        if self.gender == data[GENDERS][2]:
            FULL_REQ = REQ_BASE + REQ_NUMBER + REQ_USAGE
        else:
            FULL_REQ = REQ_BASE + REQ_NUMBER + REQ_USAGE + REQ_GENDER

        name = requests.get(FULL_REQ).json()
        try:
            text = name[NAMES][0]
            text.encode('utf-8','replace')
            self.name = text
        except:
            if self.gender != ENBY:
                text = random.choice(data[NAMES][self.culture][self.gender])
                text.encode('utf-8', 'replace')
                self.name = text
            else:
                text = random.choice(
                    data[NAMES][self.culture][random.choice([MALE, FEMALE])])
                text.encode('utf-8', 'replace')
                self.name = text

    def get_surname(self):
        if self.culture in [AKTI, HURON_URN, ISFOLK]:
            surname = random.choice(data[SURNAMES][self.culture][self.gender])
        else:
            surname = random.choice(data[SURNAMES][self.culture])
        surname.encode('utf-8', 'replace')
        self.surname = surname

    # -------------------------------------------- Data Handling ----------------------------------

    def make_data(self):
        self.data = {
            NAME: self.name + ", " + self.surname,
            BASE: self.gender + " | " + self.culture + " - " + self.race,
            TRAITS: {
                APPEARANCE: self.appearance,
                ABILITIES: self.ability
            },
            PERSONALITY: {
                TALENT: self.talent,
                MANNERISM: self.mannerism,
                INTERACTION: self.interaction
            },
            VOICE: {
                ACCENT: self.accent,
                VOCALS: self.vocals,
                TEXTURE: self.texture,
                QUIRK: self.quirk
            }
        }

    def show_data(self):
        print(json.dumps(self.data, indent=4, ensure_ascii=False))

    def load(self, file):
        with open(file) as g:
            npc = json.load(g)
        if BASE in npc:
            self.culture = npc[BASE].split(" | ")[1].split(" - ")[0]
            self.race = npc[BASE].split(" | ")[1].split(" - ")[1]
            self.gender = npc[BASE].split(" | ")[0]
            self.name = npc[NAME].split(", ")[0]
            self.surname = npc[NAME].split(", ")[1]
        else:
            self.gen_base()
        if TRAITS in npc and PERSONALITY in npc:
            self.appearance = npc[TRAITS][APPEARANCE]
            if HIGH_ABILITY in npc[TRAITS]:
                self.ability = npc[TRAITS][HIGH_ABILITY] + ", " + npc[TRAITS][LOW_ABILITY]
            elif ABILITIES in npc[TRAITS]:
                self.ability = npc[TRAITS][ABILITIES]
            self.talent = npc[PERSONALITY][TALENT]
            self.mannerism = npc[PERSONALITY][MANNERISM]
            self.interaction = npc[PERSONALITY][INTERACTION]
        else:
            self.gen_traits()
        if VOICE in npc:
            self.accent = npc[VOICE][ACCENT]
            self.vocals = npc[VOICE][VOCALS]
            self.texture = npc[VOICE][TEXTURE]
            self.quirk = npc[VOICE][QUIRK]
        else:
            self.gen_voice()
        self.make_data()

    def save_data(self):
        filename = self.race + " - " + self.name + "_" + self.surname
        parent = "npcs"
        path = os.path.join(parent, self.culture, self.gender)
        h = open(path + "/" + filename + '.json', "w")
        json.dump(self.data, h, indent=4, ensure_ascii=False)
        print("Sucess! saved: " + self.gender + " " + self.culture + " - created: " + self.name + " " + self.surname)
