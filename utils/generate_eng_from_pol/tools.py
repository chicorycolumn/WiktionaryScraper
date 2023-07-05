import json
import os
import time
from copy import deepcopy

from utils.general.common import write_todo


def show1(lobj):
    print("")
    print(lobj["id"])
    for tindex, tran in enumerate(lobj["translations"]["ENG"]):
        print("")
        print(tindex, tran)

def q(s):
    return f'"{s}"'


def print_conf_yes():
    print("**********************************")
    print("")
    print("  💚  💚  💚  💚  💚  💚  💚  💚")
    print("    💚  💚  💚  💚  💚  💚  💚")
    print("  💚  💚  💚  💚  💚  💚  💚  💚")
    print("    💚  💚  💚  💚  💚  💚  💚")
    print("  💚  💚  💚  💚  💚  💚  💚  💚")
    print("    💚  💚  💚  💚  💚  💚  💚")
    print("  💚  💚  💚  💚  💚  💚  💚  💚")
    print("")
    print("**********************************")
    print("")
    print("")


def print_conf_no():
    print("**********************************")
    print("")
    print("  🟥  🟥  🟥  🟥  🟥  🟥  🟥  🟥")
    print("    🟥  🟥  🟥  🟥  🟥  🟥  🟥")
    print("  🟥  🟥  🟥  🟥  🟥  🟥  🟥  🟥")
    print("    🟥  🟥  🟥  🟥  🟥  🟥  🟥")
    print("  🟥  🟥  🟥  🟥  🟥  🟥  🟥  🟥")
    print("    🟥  🟥  🟥  🟥  🟥  🟥  🟥")
    print("  🟥  🟥  🟥  🟥  🟥  🟥  🟥  🟥")
    print("")
    print("**********************************")
    print("")
    print("")


def is_it_the_same_meaning(lobj_1, lobj_2, input_counter, matches_record, total_anticipated, input_override):
    for match_record in matches_record["YES"]:
        if len(match_record) == 2 and lobj_1["id"] in match_record and lobj_2["id"] in match_record:
            return "ALREADY CONFIRMED"
    for match_record in matches_record["NO"]:
        if len(match_record) == 2 and lobj_1["id"] in match_record and lobj_2["id"] in match_record:
            return False

    def record_it(bool):
        matches_record["YES" if bool else "NO"].append([lobj_1["id"], lobj_2["id"]])

    a_topics = lobj_1["topics"]
    b_topics = lobj_2["topics"]
    a_tags = [y for y in lobj_1["tags"] if y[:4] != "FREQ"]
    b_tags = [y for y in lobj_2["tags"] if y[:4] != "FREQ"]

    if "extra" in lobj_2:
        if "synonyms" in lobj_2["extra"]:
            if lobj_1["lemma"] in lobj_2["extra"]["synonyms"]:
                record_it(True)
                return "LISTED SYNONYM"

    if "extra" in lobj_1:
        if "synonyms" in lobj_1["extra"]:
            if lobj_2["lemma"] in lobj_1["extra"]["synonyms"]:
                record_it(True)
                return "LISTED SYNONYM"

    topics_match = False
    tags_match = False

    if not len(a_topics) and not len(b_topics):
        topics_match = True

    if not len(a_tags) and not len(b_tags):
        tags_match = True

    if topics_match and tags_match:
        write_todo(
            f"I made a nexus where I think {lobj_1['id']} and {lobj_2['id']} have same meaning, but only because both have no tags and topics. Can you check that please?")
        record_it(True)
        return "NO TAGS OR TOPICS"

    if not topics_match:
        if len(list(set(a_topics) & set(b_topics))):
            topics_match = True

    if not tags_match:
        if len(list(set(a_tags) & set(b_tags))):
            tags_match = True

    if topics_match and tags_match:
        print("")
        print("**********************************")
        print("")
        print(lobj_1["id"], "", lobj_1["translations"]["ENG"])
        print(a_tags)
        print(a_topics)
        print("")
        print(lobj_2["id"], "", lobj_2["translations"]["ENG"])
        print(b_tags)
        print(b_topics)
        print("")
        print("**********************************")
        print("")

        input_counter["num"] += 1

        confirmation = True
        interval = 0

        if not input_override:
            confirmation = input(f"{input_counter['num']}/{total_anticipated} same?\n")
            interval = 0.1

        if confirmation:
            print_conf_yes()
            record_it(True)
            time.sleep(interval)
            return "TAGS AND TOPICS MATCH"
        else:
            print_conf_no()
            time.sleep(interval)

    record_it(False)


def user_validate_translations(lobj, res):
    show1(lobj)
    input_num = input("OK?")

    if not input_num:
        print("💚")
        res.append(lobj)

    elif input_num[0] == "d":
        print("DELETING SOME TRANS...")
        indexes_trans_to_delete = [int(n) for n in input_num[1:].split("")]
        trans_to_keep = []
        for tindex, tran in enumerate(lobj["translations"]["ENG"]):
            if tindex not in indexes_trans_to_delete:
                trans_to_keep.append(tran)
        lobj["translations"]["ENG"] = trans_to_keep
        user_validate_translations(lobj, res)

    elif input_num[0] in ["s","S"]:
        print("SWITCHING SOME TRANS TO NEW LOBJ...")
        indexes_trans_to_move = [int(n) for n in input_num[1:]]
        trans_to_keep = []
        trans_to_move = []
        for tindex, tran in enumerate(lobj["translations"]["ENG"]):
            if tindex not in indexes_trans_to_move:
                trans_to_keep.append(tran)
            else:
                trans_to_move.append(tran)
        lobj["translations"]["ENG"] = trans_to_keep
        print("")
        print("ORIGINAL:")
        user_validate_translations(lobj, res)

        if len(trans_to_move):
            duplicated_lobj = deepcopy(lobj)
            duplicated_lobj["id"] += f"({trans_to_move[0]})"
            duplicated_lobj["translations"]["ENG"] = trans_to_move
            print("")
            print("NEW:")
            user_validate_translations(duplicated_lobj, res)

    elif input_num == "f":
        print("ADDED FLAG FOR ATTENTION")
        print("🚩")
        lobj["flag"] = "đ"
        res.append(lobj)

    else:
        print("Did not recognise user input. Options are:")
        print("Enter: This lobj is OK.")
        print("d245 : DELETE translations at indexes 2, 4, and 5.")
        print("s245 : SWITCH translations at indexes 2, 4, and 5 to a new lobj for this lemma.")
        print("f    : Let this lobj through, but FLAG for later attention.")
        user_validate_translations(lobj, res)
