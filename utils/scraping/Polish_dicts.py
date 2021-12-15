aspect_ref = {
    "impf": "imperfective",
    "im": "imperfective",
    "imperfective": "imperfective",
    "pf": "perfective",
    "perfective": "perfective",
}

gender_translation_ref = {
    "pl": "nonvirile",
    "plural": "nonvirile",
    "nvir": "nonvirile",
    "nonvirile": "nonvirile",
    "non virile": "nonvirile",
    "m": "m3",
    "m inan": "m3",
    "m anim": "m2",
    "m pers": "m1",
    "f": "f",
    "n": "n"
}

gender_to_tags_ref = {
    "m1": ["person"],
    "m2": ["animal"],
    "m3": ["inanimate"],
    "n": ["inanimate"],
}

case_ref = {
    "nominative": "nom",
    "genitive": "gen",
    "dative": "dat",
    "accusative": "acc",
    "instrumental": "ins",
    "locative": "loc",
    "vocative": "voc",
}

shorthand_tag_refs = {
    ############### 1) Foundation
    "u": {
        "tags": ["uncountable"],
        "topics": [],
    },
    "h": {
        "tags": ["holdable", "concrete"],
        "topics": [],
    },
    "m": {
        "tags": ["manmade", "concrete"],
        "topics": [],
    },
    "n": {
        "tags": ["natural", "concrete"],
        "topics": ["outside"],
    },
    "0": {
        "tags": ["FREQ0"],
        "topics": [],
    },
    "1": {
        "tags": ["FREQ1"],
        "topics": [],
    },
    "2": {
        "tags": ["FREQ2"],
        "topics": [],
    },
    "3": {
        "tags": ["FREQ3"],
        "topics": [],
    },
    "4": {
        "tags": ["FREQ4"],
        "topics": [],
    },
    "5": {
        "tags": ["FREQ5"],
        "topics": [],
    },

    ############### 2) Mind and Body
    "!": {  # bang crash boom
        "tags": ["noise", "aa"],
        "topics": ["sense and perception"],
    },
    "~": {  # sight sound smell
        "tags": ["perception", "aa"],
        "topics": ["sense and perception"],
    },
    "o": {  # noun verb swear-word
        "tags": ["wordtype", "aa"],
        "topics": ["language"],
    },
    "e": {  # anger happiness sadness
        "tags": ["emotion", "aa"],
        "topics": ["mental"],
    },
    "€": {  # idea realisation
        "tags": ["thought", "aa"],
        "topics": ["mental"],
    },
    "ee": {
        "tags": ["aa"],
        "topics": ["mental"],
    },
    "v": {  # kick jump roll
        "tags": ["movement"],
        "topics": ["body"],
    },
    "bb": {  # sneeze snot ache
        "tags": [],
        "topics": ["at the doctor", "body"],
    },
    "bp": {  # toe eye skin
        "tags": ["bodypart"],
        "topics": ["at the doctor", "body"],
    },

    ############### 3) Miscellaneous
    "k": {  # red yellow
        "tags": ["colour"],
        "topics": ["sense and perception"],
    },
    "ð": {  # spiky smooth hot cold
        "tags": ["texture"],
        "topics": ["sense and perception"],
    },
    "đ": {  # sour sweet
        "tags": ["flavour"],
        "topics": ["sense and perception"],
    },
    "z": {  # big small wide
        "tags": ["dimension"],
        "topics": ["sense and perception"],
    },
    "$": {  # cheap expensive buy sell cost
        "tags": ["money"],
        "topics": ["shopping"],
    },
    "@": {  # inch metre litre
        "tags": ["measurement"],
        "topics": ["math"],
    },
    "@@": {  # cup fistful load
        "tags": ["container", "h"],
        "topics": [],
    },
    "g": {  # scarf tie shoe
        "tags": ["clothes", "h"],
        "topics": ["fashion"],
    },
    "gg": {  # scarf tie shoe
        "tags": [],
        "topics": ["fashion"],
    },
    "c": {  # cotton steel cardboard
        "tags": ["material", "uncountable", "concrete"],
        "topics": ["engineering"],
    },
    "¢": { # hydrogen helium lithium
        "tags": ["chemical", "c"],
        "topics": ["science"],
    },
    "ß": { # biology chemistry physics
        "tags": ["school subject", "aa"],
        "topics": ["school"],
    },
    "ł": { # rainy sunny windy
        "tags": ["weather type", "aa"],
        "topics": ["outdoor"],
    },
    "łł": { # climate albedo humidity
        "tags": ["weather", "aa"],
        "topics": ["outdoor"],
    },

    ############### 4) Abstract
    "aa": {
        "tags": ["abstract"],
        "topics": [],
    },
    "at": {
        "tags": ["aa"],
        "topics": ["time"],
    },
    "as": {
        "tags": ["aa"],
        "topics": ["school"],
    },
    "aw": {
        "tags": ["aa"],
        "topics": ["work"],
    },
    "ag": {
        "tags": ["aa"],
        "topics": ["geometry"],
    },

    ############### 5) People
    "p": {
        "tags": ["person", "living", "concrete"],
        "topics": [],
    },
    "r": {
        "tags": ["relative", "p"],
        "topics": ["relationship"],
    },
    "j": {
        "tags": ["profession", "p"],
        "topics": ["work"],
    },
    "a": {
        "tags": ["animal", "living", "concrete"],
        "topics": ["outside"],
    },
    "æ": {
        "tags": ["pet", "a"],
        "topics": ["home", "inside"],
    },
    "t": {
        "tags": ["title", "p"],
        "topics": [],
    },

    ############### 6) Food
    "f": {
        "tags": ["food", "h"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "sw": {
        "tags": ["sweet", "f"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "sv": {
        "tags": ["savoury", "f"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "fr": {
        "tags": ["fruit", "f"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "vg": {
        "tags": ["vegetable", "f"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "d": {
        "tags": ["drink", "h"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "da": {
        "tags": ["alcoholic", "d"],
        "topics": ["kitchen", "restaurant", "nightclub", "inside"],
    },

    ############### 7) Location
    "ll": {
        "tags": ["location", "concrete"],
        "topics": [],
    },
    "lb": {
        "tags": ["ll", "building"],
        "topics": ["inside"],
    },
    "lr": {
        "tags": ["ll", "room"],
        "topics": ["inside"],
    },
    "ln": {
        "tags": ["ll", "natural"],
        "topics": ["outside"],
    },
    "ls": {
        "tags": ["special location", "aa"],
        "topics": [],
    },

    ############### 8) House
    "hhf": {
        "tags": ["furniture", "concrete"],
        "topics": ["home", "inside"],
    },
    "hh": {
        "tags": ["household object", "h"],
        "topics": ["home", "inside"],
    },
    "hbf": {
        "tags": ["hhf"],
        "topics": ["home", "inside", "bedroom"],
    },
    "hb": {
        "tags": ["hh"],
        "topics": ["home", "inside", "bedroom"],
    },
    "hkf": {
        "tags": ["hhf"],
        "topics": ["home", "inside", "kitchen"],
    },
    "hk": {
        "tags": ["hh"],
        "topics": ["home", "inside", "kitchen"],
    },
    "hwf": {
        "tags": ["hhf"],
        "topics": ["home", "inside", "washroom"],
    },
    "hw": {
        "tags": ["hh"],
        "topics": ["home", "inside", "washroom"],
    },
    "hp": {
        "tags": ["part of house", "concrete"],
        "topics": ["home", "inside"],
    },

    ############### 9) Fields
    "q": {
        "tags": ["hobby"],
        "topics": [],
    },
    "w": {
        "tags": [],
        "topics": ["work"],
    },
    "s": {
        "tags": [],
        "topics": ["school"],
    },
    "x": {
        "tags": ["computer part"],
        "topics": ["computing"],
    },
    "xx": {
        "tags": [],
        "topics": ["computing"],
    },
    "y": {
        "tags": ["sport"],
        "topics": ["sport"],
    },
    "yy": {
        "tags": [],
        "topics": ["sport"],
    },
    "l": {
        "tags": [],
        "topics": ["law"],
    },
    "µ": {
        "tags": [],
        "topics": ["medicine"],
    },
    "i": {
        "tags": [],
        "topics": ["tech"],
    },
    "¶": {
        "tags": ["religion"],
        "topics": ["religion"],
    },
    "¶¶": {
        "tags": [],
        "topics": ["religion"],
    },
    "ĸ": {
        "tags": ["curseword"],
        "topics": [],
    },
    "ŧ": {
        "tags": ["transport"],
        "topics": ["travel"],
    },
    "ŧŧ": {
        "tags": [],
        "topics": ["travel"],
    },
    "ø": {
        "tags": [],
        "topics": ["love", "relationship"],
    },
    "£": {
        "tags": ["language"],
        "topics": ["language"],
    },
    "££": {
        "tags": [],
        "topics": ["language"],
    },
    "|": {
        "tags": [],
        "topics": ["violence"],
    },
    "¬": {
        "tags": [],
        "topics": ["entertainment"],
    },
    "þ": {
        "tags": ["holiday"],
        "topics": ["holiday"],
    },
    "þþ": {
        "tags": [],
        "topics": ["holiday"],
    },
    "ŋ": {
        "tags": ["slang"],
        "topics": [],
    },
    "art": {
        "tags": [],
        "topics": ["art"],
    },
    "bio": {
        "tags": [],
        "topics": ["biology"],
    },
    "bus": {
        "tags": [],
        "topics": ["business"],
    },
    "che": {
        "tags": [],
        "topics": ["chemistry"],
    },
    "dan": {
        "tags": [],
        "topics": ["dance"],
    },
    "eng": {
        "tags": [],
        "topics": ["engineering"],
    },
    "his": {
        "tags": [],
        "topics": ["history"],
    },
    "the": {
        "tags": [],
        "topics": ["theatre"],
    },
    "geo": {
        "tags": [],
        "topics": ["geography"],
    },
    "coo": {
        "tags": [],
        "topics": ["cooking"],
    },
    "ene": {
        "tags": [],
        "topics": ["energy and sustainability"],
    },
    "jou": {
        "tags": [],
        "topics": ["journalism"],
    },
    "mat": {
        "tags": [],
        "topics": ["math"],
    },
    "mus": {
        "tags": [],
        "topics": ["music"],
    },
    "phy": {
        "tags": [],
        "topics": ["physics"],
    },
    "phi": {
        "tags": [],
        "topics": ["philosophy and ethics"],
    },
    "soc": {
        "tags": [],
        "topics": ["sociology"],
    },

    # # # # # # # # # # #

}
