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

    ############### 1) Mind and Body
    "!": {  # bang crash boom
        "tags": ["noise", "aa"],
        "topics": ["sense and perception"],
    },
    "Q": {  # sight sound smell
        "tags": ["perception", "aa"],
        "topics": ["sense and perception"],
    },
    "o": {  # noun verb swear-word
        "tags": ["wordtype", "aa"],
        "topics": ["language"],
    },
    "oo": {  # noun verb swear-word
        "tags": ["punctuation", "aa"],
        "topics": ["language", "writing"],
    },
    "e": {  # anger happiness sadness
        "tags": ["emotion", "aa"],
        "topics": ["mental"],
    },
    "Y": {  # idea realisation
        "tags": ["thought", "aa"],
        "topics": ["mental"],
    },
    "sr": {  # idea realisation
        "tags": ["speech", "aa"],
        "topics": ["mental"],
    },
    "QQ": {  # phone, post, signal
        "tags": [],
        "topics": ["communications"],
    },
    "ee": {
        "tags": ["aa"],
        "topics": ["mental"],
    },
    "eee": {
        "tags": [],
        "topics": ["knowledge and existence"],
    },
    "v": {  # kick jump roll
        "tags": ["movement"],
        "topics": ["body"],
    },
    "vv": {  # walk run sail swim
        "tags": ["locomotion"],
        "topics": [],
    },
    "bb": {
        "tags": [],
        "topics": ["body"],
    },
    "b": {  # toe eye skin
        "tags": ["bodypart"],
        "topics": ["medicine", "body"],
    },
    "ba": {  # toe eye skin
        "tags": ["bodypart animal"],
        "topics": [],
    },
    "dr": {  # toothbrush, wake, wash
        "tags": [],
        "topics": ["daily routine"],
    },

    ############### 2) Miscellaneous
    "kk": {  # tall short light dark
        "tags": [],
        "topics": ["sense and perception", "appearance"],
    },
    "k": {  # red yellow
        "tags": ["colour"],
        "topics": ["sense and perception", "appearance"],
    },
    "D": {  # spiky smooth hot cold
        "tags": ["texture"],
        "topics": ["sense and perception"],
    },
    "F": {  # sour sweet
        "tags": ["flavour"],
        "topics": ["sense and perception", "kitchen", "restaurant", "inside"],
    },
    "z": {  # big small wide
        "tags": ["dimension"],
        "topics": ["sense and perception", "appearance"],
    },
    "$": {  # cheap expensive buy sell cost
        "tags": ["money"],
        "topics": ["shopping", "business"],
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
    "gg": {  #
        "tags": [],
        "topics": ["fashion"],
    },
    "ggg": {  #
        "tags": ["h"],
        "topics": ["cosmetics"],
    },
    "c": {  # cotton steel cardboard
        "tags": ["material", "uncountable", "concrete"],
        "topics": ["engineering"],
    },
    "C": {  # hydrogen helium lithium
        "tags": ["chemical", "c"],
        "topics": ["chemistry"],
    },
    "S": {  # biology chemistry physics
        "tags": ["school subject", "aa"],
        "topics": ["school"],
    },
    "L": {  # rainy sunny windy
        "tags": ["weather type"],
        "topics": ["outdoor", "geography"],
    },
    "LL": {  # climate albedo humidity
        "tags": ["weather"],
        "topics": ["outdoor", "geography"],
    },
    "H": {  # hot cold cool
        "tags": ["temperature", "weather"],
        "topics": ["outdoor", "geography"],
    },
    "fq": {  # often sometimes custom
        "tags": ["frequency", "aa"],
        "topics": [],
    },

    ############### 3) Abstract
    "aa": {
        "tags": ["abstract"],
        "topics": [],
    },
    "at": {
        "tags": ["aa"],
        "topics": ["time"],
    },
    "tt": {
        "tags": [],
        "topics": ["time"],
    },
    "ttt": {
        "tags": ["event"],
        "topics": ["time"],
    },
    "ss": {
        "tags": [],
        "topics": ["spatial"],
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
    "an": {
        "tags": ["aa", "abstract noun"],
        "topics": [],
    },
    "pr": {
        "tags": ["aa"],
        "topics": ["probability"],
    },

    ############### 4) People
    "py": {
        "tags": ["personality"],
        "topics": ["people"],
    },
    "p": {
        "tags": ["person", "living", "concrete"],
        "topics": ["people"],
    },
    "r": {
        "tags": ["relative", "p"],
        "topics": ["people"],  # ie relationships / friendships / people descriptions
    },
    "pp": {
        "tags": [],
        "topics": ["people"],
    },
    "ppp": {
        "tags": ["physical personal description", "kk", "bb"], # tall handsome fat
        "topics": ["sense and perception", "appearance", "body"],
    },
    "j": {
        "tags": ["profession", "p"],
        "topics": ["work", "people"],
    },
    "a": {
        "tags": ["animal", "living", "concrete"],
        "topics": ["outside"],
    },
    "A": {
        "tags": ["pet", "a"],
        "topics": ["home", "inside"],
    },
    "ai": {
        "tags": ["insect", "a"],
        "topics": ["outside"],
    },
    "t": {
        "tags": ["title", "p"],
        "topics": ["people"],
    },

    ############### 5) Food
    "f": {
        "tags": ["food", "h"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "fc": {
        "tags": ["condiment", "f"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "fi": {
        "tags": ["ingredient", "f"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "ff": {
        "tags": [],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "fff": {
        "tags": ["eating utensil"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "coo": {  # duplicate for mental ease
        "tags": [],
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

    ############### 6) Location
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
        "topics": ["outside", "geography"],
    },
    "lc": {
        "tags": ["ll", "nation"],
        "topics": ["outside", "geography"],
    },
    "ls": {
        "tags": ["special location", "aa"],
        "topics": [],
    },

    ############### 7) House
    "HH": {
        "tags": ["furniture", "concrete"],
        "topics": ["home", "inside"],
    },
    "hh": {
        "tags": ["household object", "h"],
        "topics": ["home", "inside"],
    },
    "HB": {
        "tags": ["HH"],
        "topics": ["home", "inside", "bedroom"],
    },
    "hb": {
        "tags": ["hh"],
        "topics": ["home", "inside", "bedroom"],
    },
    "HK": {
        "tags": ["HH"],
        "topics": ["home", "inside", "kitchen"],
    },
    "hk": {
        "tags": ["hh"],
        "topics": ["home", "inside", "kitchen"],
    },
    "HW": {
        "tags": ["HH"],
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
        "tags": ["hobby"], #eg knit painting
        "topics": [],
    },
    "qqq": {
        "tags": ["tool"],
        "topics": [],
    },
    "qq": { # eg try skill
        "tags": [],
        "topics": ["hobbies"],
    },
    "w": {
        "tags": [],
        "topics": ["work"],
    },
    "jj": {  # duplicate for mental ease
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
    "M": {
        "tags": ["game"],
        "topics": ["game"],
    },
    "MM": {
        "tags": [],
        "topics": ["game"],
    },
    "l": {
        "tags": [],
        "topics": ["law"],
    },
    "law": { # Duplicate for mental ease.
        "tags": [],
        "topics": ["law"],
    },
    "i": {
        "tags": ["device"],
        "topics": ["tech"],
    },
    "ii": {
        "tags": [],
        "topics": ["tech"],
    },
    "R": {
        "tags": ["religion"],
        "topics": ["religion"],
    },
    "RR": {
        "tags": [],
        "topics": ["religion"],
    },
    "RRR": {
        "tags": [],
        "topics": ["fantasy"],
    },
    "K": {
        "tags": ["curseword"],
        "topics": [],
    },
    "KK": {
        "tags": ["insult"],
        "topics": [],
    },
    "T": {
        "tags": ["transport"],
        "topics": ["travel"],
    },
    "TT": {
        "tags": [],
        "topics": ["travel"],
    },
    "TTT": {
        "tags": [],
        "topics": ["travel", "car"],
    },
    "Z": {
        "tags": [],
        "topics": ["love", "people"],
    },
    "£": {
        "tags": ["language"],
        "topics": ["language"],
    },
    "££": {
        "tags": ["aa"],
        "topics": ["language"],
    },
    "X": {
        "tags": ["weapon"],
        "topics": ["violence"],
    },
    "XX": {
        "tags": [],
        "topics": ["violence"],
    },
    "XXX": {
        "tags": [],
        "topics": ["war"],
    },
    "J": {
        "tags": ["natural", "natural disaster"],
        "topics": ["danger"],
    },
    "JJ": {
        "tags": [],
        "topics": ["danger"],
    },
    "V": {
        "tags": [],
        "topics": ["entertainment"],
    },
    "VV": {
        "tags": [],
        "topics": ["possession"],
    },
    "P": {
        "tags": ["holiday"],
        "topics": ["holiday"],
    },
    "PP": {
        "tags": [],
        "topics": ["holiday"],
    },
    "G": {
        "tags": ["slang"],
        "topics": [],
    },
    "N": { # cocaine, weed, heroin
        "tags": ["drugs"],
        "topics": ["drugs"],
    },
    "NN": { # smoke, pipe, bong
        "tags": [],
        "topics": ["drugs"],
    },
    "B": { # robbery, robber, manslaughter
        "tags": ["crime"],
        "topics": ["crime", "law"],
    },
    "W": { # top bottom side centre
        "tags": ["part"],
        "topics": [],
    },
    "WW": { # cog board gear joint
        "tags": ["component"],
        "topics": [],
    },
    "agr": {
        "tags": [],
        "topics": ["agriculture"],
    },
    "gar": {  # duplicate for mental ease
        "tags": [],
        "topics": ["agriculture"],
    },
    "art": {
        "tags": [],
        "topics": ["art"],
    },
    "ast": {
        "tags": [],
        "topics": ["astronomy"],
    },
    "bio": {
        "tags": [],
        "topics": ["biology", "science"],
    },
    "bus": {
        "tags": [],
        "topics": ["business"],
    },
    "che": {
        "tags": [],
        "topics": ["chemistry", "science"],
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
    "mu": {
        "tags": ["musical instrument"],
        "topics": ["music"],
    },
    "mus": {
        "tags": [],
        "topics": ["music"],
    },
    "phy": {
        "tags": [],
        "topics": ["physics", "science"],
    },
    "nut": {
        "tags": [],
        "topics": ["nutrition"],
    },
    "nau": {
        "tags": [],
        "topics": ["nautical"],
    },
    "phi": {
        "tags": [],
        "topics": ["philosophy and ethics"],
    },
    "soc": {
        "tags": [],
        "topics": ["sociology"],
    },
    "sci": {
        "tags": [],
        "topics": ["science", "biology", "chemistry", "physics"],
    },
    "pol": {
        "tags": [],
        "topics": ["politics"],
    },
    "gem": {
        "tags": [],
        "topics": ["geometry"],
    },
    "med": {
        "tags": [],
        "topics": ["medicine"],
    },
    "U": {
        "tags": ["disease"],
        "topics": ["disease", "medicine"],
    },
    "UU": {
        "tags": [],
        "topics": ["disease", "medicine"],
    },
    "wri": {
        "tags": [],
        "topics": ["writing"],
    },
    "cel": {
        "tags": [],
        "topics": ["celebration"],
    },
    "pl": {
        "tags": [],
        "topics": ["planning"],
    },
    "sg": {
        "tags": [],
        "topics": ["social glue"],
    },
    "rp": {
        "tags": [],
        "topics": ["request and permission"],
    },

    ############### 9) Appraisal
    "+": {
        "tags": ["positive judgment"],
        "topics": ["judgment"],
    },
    "-": {
        "tags": ["negative judgment"],
        "topics": ["judgment"],
    },
    "=": {
        "tags": ["neutral judgment"],
        "topics": ["judgment"],
    },

    # # # # # # # # # # #

    "he": {
        "tags": ["helper"],
        "topics": [],
    },
}
