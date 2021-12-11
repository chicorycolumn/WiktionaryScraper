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
    "!!": {
        "tags": ["noise", "aa"],
        "topics": ["sense and perception"],
    },
    "!": {
        "tags": ["perception", "aa"],
        "topics": ["sense and perception"],
    },
    "o": {
        "tags": ["speech", "aa"],
        "topics": ["mental world"],
    },
    "e": {
        "tags": ["emotion", "aa"],
        "topics": ["mental world"],
    },
    "€": {
        "tags": ["thought", "aa"],
        "topics": ["mental world"],
    },
    "ee": {
        "tags": ["aa"],
        "topics": ["mental world"],
    },
    "v": {
        "tags": ["movement"],
        "topics": [],
    },
    "bb": {
        "tags": ["body", "concrete"],
        "topics": ["at the doctor", "basic", "body"],
    },
    "bp": {
        "tags": ["bb", "bodypart"],
        "topics": ["at the doctor", "basic", "body"],
    },
    
    ############### 3) Miscellaneous
    "k": {
        "tags": ["colour"],
        "topics": ["basic"],
    },
    "z": {
        "tags": ["dimension"],
        "topics": ["basic"],
    },
    "$": {
        "tags": ["money"],
        "topics": ["shopping", "math", "travel"],
    },
    "@": {
        "tags": ["measurement"],
        "topics": ["math"],
    },
    "@@": {
        "tags": ["container", "h"],
        "topics": [],
    },
    "g": {
        "tags": ["clothes", "h"],
        "topics": ["basic"],
    },
    "c": {
        "tags": ["material", "uncountable", "concrete"],
        "topics": ["basic"],
    },
    "¢": {
        "tags": ["chemical", "c"],
        "topics": ["science"],
    },
    "ß": {
        "tags": ["school subject", "aa"],
        "topics": ["school"],
    },
    "ł": {
        "tags": ["weather", "aa"],
        "topics": ["basic", "outdoor"],
    },

    ############### 4) Abstract
    "aa": {
        "tags": ["abstract"],
        "topics": [],
    },
    "at": {
        "tags": ["aa", "time"],
        "topics": ["travel", "math"],
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
        "topics": ["geometry", "math"],
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
        "tags": ["work"],
        "topics": [],
    },
    "s": {
        "tags": ["school"],
        "topics": [],
    },
    "x": {
        "tags": ["computing"],
        "topics": [],
    },
    "y": {
        "tags": ["sport"],
        "topics": [],
    },
    "l": {
        "tags": ["law"],
        "topics": [],
    },
    "µ": {
        "tags": ["medicine"],
        "topics": [],
    },
    "i": {
        "tags": ["tech"],
        "topics": [],
    },
    "¶": {
        "tags": ["religion"],
        "topics": [],
    },
    "ĸ": {
        "tags": ["curseword"],
        "topics": [],
    },
    "ŧ": {
        "tags": ["transport"],
        "topics": ["travel"],
    },
    "ø": {
        "tags": ["love"],
        "topics": ["relationship"],
    },
    "£": {
        "tags": ["language"],
        "topics": [],
    },
    "¬": {
        "tags": ["violence"],
        "topics": [],
    },
    "¬¬": {
        "tags": ["entertainment"],
        "topics": [],
    },
    "þ": {
        "tags": ["slang"],
        "topics": [],
    },
    "ŋ": {
        "tags": ["holiday"],
        "topics": [],
    }

    # # # # # # # # # # #





}