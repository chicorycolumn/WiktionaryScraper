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
    ############### 0) Foundation
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
        "topics": [],
    },
    
    ############### 1) Mind and Body
    "!!": {
        "tags": ["noise", "aa"],
        "topics": ["sense and perception"],
    },
    "!": {
        "tags": ["perception", "aa"],
        "topics": ["sense and perception"],
    },
    "ø": {
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
    "b": {
        "tags": ["bodypart", "concrete"],
        "topics": ["at the doctor", "basic", "body"],
    },
    "bb": {
        "tags": ["b"],
        "topics": ["at the doctor", "basic", "body"],
    },
    
    ############### 2) Appearance
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
        "topics": ["shopping", "maths", "travel"],
    },
    "@": {
        "tags": ["measurement"],
        "topics": ["maths"],
    },
    "@@": {
        "tags": ["container", "h"],
        "topics": [],
    },
    "g": {
        "tags": ["clothes", "h"],
        "topics": ["basic"],
    },

    ############### 3) Miscellaneous
    "c": {
        "tags": ["material", "uncountable", "concrete"],
        "topics": ["basic"],
    },
    "¢": {
        "tags": ["chemical", "c"],
        "topics": ["science"],
    },
    "ß": {
        "tags": ["schoolsubject", "aa"],
        "topics": ["school"],
    },
    "ł": {
        "tags": ["weather", "aa"],
        "topics": ["basic", "outdoor"],
    },

    ############### 4) Abstract
    "at": {
        "tags": ["aa", "time"],
        "topics": ["travel", "maths"],
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
        "topics": ["geometric", "maths"],
    },
    "aa": {
        "tags": ["abstract"],
        "topics": [],
    },

    ############### 5) People
    "r": {
        "tags": ["relative", "p"],
        "topics": ["relationships"],
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
    "p": {
        "tags": ["person", "living", "concrete"],
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
    "ve": {
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

    ############### 7A) Location
    "lg": {
        "tags": ["location", "concrete"],
        "topics": [],
    },
    "lb": {
        "tags": ["location", "building", "concrete"],
        "topics": ["inside"],
    },
    "lr": {
        "tags": ["location", "room", "concrete"],
        "topics": ["inside"],
    },
    "ln": {
        "tags": ["location", "natural", "concrete"],
        "topics": ["outside"],
    },
    "ls": {
        "tags": ["special location", "aa"],
        "topics": ["religion"],
    },

    ############### 7B) House
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

    ############### 8) Fields
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

    # # # # # # # # # # #





}