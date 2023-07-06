import json
import os
import time
from copy import deepcopy

from utils.general.common import write_todo


def show1(lobj):
    print("")
    print(lobj["id"], f'({len(lobj["translations"]["ENG"])} trans)')
    for tindex, tran in enumerate(lobj["translations"]["ENG"]):
        print("     ", tindex + 1, tran)
    print("")


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

    def show_helptext():
        print("")
        print("--------------------------------------------------------------------")
        print("            Did not recognise user input. Options are:")
        print("     Enter: This lobj is OK.")
        print("     D    : DELETE lobj.")
        print("     f    : Okay this lobj but FLAG for later attention.")
        print("     F    : FLAG the lobj just gone.")
        print("     w    : WRITE current res array to temporary file.")
        print("     d24  : DELETE translations at indexes 2 and 4.")
        print("     s24  : SWITCH translations at indexes 2 and 4 to a new lobj for this lemma.")
        print(
            "     s24S3: Translations at indexes 2 and 4 are for new lobj, at index 3 is for both original and new lobjs.")
        print("--------------------------------------------------------------------")
        print("")
        user_validate_translations(lobj, res)

    def add_to_res(l):
        dupe = {}
        dupe["lemma"] = l["lemma"]
        dupe["id"] = l["id"]
        dupe["tags"] = l["tags"]
        dupe["topics"] = l["topics"]
        for k in l:
            if k not in ["lemma", "tags", "topics"]:
                dupe[k] = l[k]
        print("💚")
        res.append(dupe)

    def tempsave_res():
        print("")
        print(f"📀 SAVING current res ({len(res)} items).")
        print("")
        stem = "./../../output_saved/batches/"
        output_path = f"{stem}tempsave_doublecheck_trans_of_pol_lobjs.json"
        res_json = json.dumps(res, indent=2, ensure_ascii=False)
        with open(output_path, "w") as outfile:
            outfile.write(res_json)

    if int(lobj["id"].split("-")[2]) % 10 == 1:
        tempsave_res()

    show1(lobj)
    user_input = input("OK? (hit Enter)")

    if not user_input:
        add_to_res(lobj)
        return

    for char in user_input:
        if char not in "123456789dDfFwSs":
            show_helptext()
            return

    if user_input[0] == "D":
        print("🔥 DELETED LOBJ")
        return

    elif user_input[0] == "d":
        print("DELETING SOME TRANS...")
        indexes_trans_to_delete = [int(n) - 1 for n in user_input[1:]]
        trans_to_keep = []
        for tindex, tran in enumerate(lobj["translations"]["ENG"]):
            if tindex not in indexes_trans_to_delete:
                trans_to_keep.append(tran)
        lobj["translations"]["ENG"] = trans_to_keep
        user_validate_translations(lobj, res)
        return

    elif user_input[0] in ["s", "S"]:
        print("SWITCHING SOME TRANS TO NEW LOBJ...")
        if user_input == "s":
            user_input = "s2"
        if user_input == "S":
            user_input = "S2"

        move_these = user_input[user_input.index("s"): user_input.index("S") if (
                "S" in user_input and user_input.index("S") > user_input.index("s")) else len(user_input)][
                     1:] if "s" in user_input else ""
        copy_these = user_input[user_input.index("S"): user_input.index("s") if (
                "s" in user_input and user_input.index("s") > user_input.index("S")) else len(user_input)][
                     1:] if "S" in user_input else ""

        indexes_trans_to_move = [int(n) - 1 for n in move_these]
        indexes_trans_to_copy = [int(n) - 1 for n in copy_these]

        trans_for_original_lobj = []
        trans_for_new_lobj = []

        for tindex, tran in enumerate(lobj["translations"]["ENG"]):
            if tindex in indexes_trans_to_move:
                trans_for_new_lobj.append(tran)
            elif tindex in indexes_trans_to_copy:
                trans_for_new_lobj.append(tran)
                trans_for_original_lobj.append(tran)
            else:
                trans_for_original_lobj.append(tran)

        print("")
        print("For lobj", q(lobj["id"]))
        print("")
        print("ORIGINAL lobj will have")
        print(trans_for_original_lobj)
        print("")
        print("NEW lobj will have")
        print(trans_for_new_lobj)
        print("")
        confirm = input("OK? (hit Enter)")

        if not confirm:
            lobj["translations"]["ENG"] = trans_for_original_lobj
            add_to_res(lobj)

            if len(trans_for_new_lobj):
                duplicated_lobj = deepcopy(lobj)

                signal_word = None
                for w in trans_for_new_lobj:
                    if not signal_word and w not in lobj["translations"]["ENG"]:
                        signal_word = w
                if not signal_word:
                    signal_word = "🚩ß"

                duplicated_lobj["id"] += f"({signal_word})"
                duplicated_lobj["tags"] = []
                duplicated_lobj["topics"] = []
                duplicated_lobj["id"] += "🚩Ŧ"  # Need to add tags and topics
                duplicated_lobj["translations"]["ENG"] = trans_for_new_lobj
                add_to_res(duplicated_lobj)
            return

        else:
            print("Restarting...")
            user_validate_translations(lobj, res)
            return

    elif user_input == "w":
        tempsave_res()
        user_validate_translations(lobj, res)

    elif user_input == "f":
        print("ADDED FLAG FOR ATTENTION")
        print("🚩")
        lobj["id"] += "🚩"
        add_to_res(lobj)

    elif user_input == "F":
        print("ADDED FLAG TO", res[-1]["id"])
        print("⬅️🚩")
        res[-1]["id"] += "🚩"
        user_validate_translations(lobj, res)

    else:
        show_helptext()
