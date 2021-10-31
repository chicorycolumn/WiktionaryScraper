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
    "v": {
        "tags": ["movement"],
        "topics": [],
    },
    "k": {
        "tags": ["colour"],
        "topics": ["basic"],
    },
    "z": {
        "tags": ["dimensions"],
        "topics": ["basic"],
    },

    # # # # # # # # # # #

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
    "s": {
        "tags": ["school"],
        "topics": [],
    },
    "w": {
        "tags": ["work"],
        "topics": [],
    },

    # # # # # # # # # # #

    "c": {
        "tags": ["material", "uncountable", "concrete"],
        "topics": ["basic"],
    },
    "¢": {
        "tags": ["chemical", "c"],
        "topics": ["science"],
    },
    "b": {
        "tags": ["bodypart", "concrete"],
        "topics": ["at the doctor", "basic", "body"],
    },
    "ß": {
        "tags": ["schoolsubject", "abstract"],
        "topics": ["school"],
    },
    "ł": {
        "tags": ["weather", "abstract", "uncountable"],
        "topics": ["basic", "outdoor"],
    },
    "!!": {
        "tags": ["noise", "abstract"],
        "topics": ["sense and perception"],
    },
    "!": {
        "tags": ["perception", "abstract"],
        "topics": ["sense and perception"],
    },
    "e": {
        "tags": ["emotion", "abstract"],
        "topics": ["inside your head"],
    },
    "$": {
        "tags": ["money"],
        "topics": ["shopping", "maths", "travel"],
    },
    "@": {
        "tags": ["measurement"],
        "topics": ["maths"],
    },
    "at": {
        "tags": ["abstract", "time"],
        "topics": ["travel", "maths"],
    },
    "as": {
        "tags": ["abstract"],
        "topics": ["school"],
    },
    "aw": {
        "tags": ["abstract"],
        "topics": ["work"],
    },
    "ag": {
        "tags": ["abstract"],
        "topics": ["geometric", "maths"],
    },
    "aa": {
        "tags": ["abstract"],
        "topics": [],
    },
    "r": {
        "tags": ["relative", "person", "living", "concrete"],
        "topics": ["relationships"],
    },
    "j": {
        "tags": ["profession", "person", "living", "concrete"],
        "topics": ["work"],
    },
    "a": {
        "tags": ["animal", "living", "concrete"],
        "topics": ["outside"],
    },
    "æ": {
        "tags": ["pet", "animal", "living", "concrete"],
        "topics": ["home", "inside"],
    },
    "t": {
        "tags": ["title", "person", "living", "concrete"],
        "topics": [],
    },
    "p": {
        "tags": ["person", "living", "concrete"],
        "topics": [],
    },
    "f": {
        "tags": ["food", "h"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "fw": {
        "tags": ["sweet", "f"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "fv": {
        "tags": ["savoury", "f"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "ffr": {
        "tags": ["fruit", "f"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "fve": {
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
    "g": {
        "tags": ["clothes", "h"],
        "topics": ["basic"],
    },
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
        "tags": ["special location", "abstract"],
        "topics": ["religion"],
    },
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
    }
}