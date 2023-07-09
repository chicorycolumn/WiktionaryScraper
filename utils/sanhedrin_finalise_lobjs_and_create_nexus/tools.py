import json
import os
import time
from copy import deepcopy

from utils.general.common import write_todo
from utils.universal import color as c


def show1(lobj, target_lang):
    print("")
    print(c.blue(lobj["id"]), f'({len(lobj["translations"][target_lang])} trans)')
    for tindex, tran in enumerate(lobj["translations"][target_lang]):
        print("     ", tindex + 1, c.blue(tran))
    print("")


def q(s):
    return f'"{s}"'


def print_conf_yes():
    print("**********************************")
    print("")
    print("")
    print("")
    print("")
    print("             💚  💚  💚")
    print("")
    print("")
    print("")
    print("")
    print("**********************************")
    print("")
    print("")


def print_conf_no():
    print("**********************************")
    print("")
    print("")
    print("")
    print("")
    print("             🟥  🟥  🟥")
    print("")
    print("")
    print("")
    print("")
    print("**********************************")
    print("")
    print("")


def is_it_the_same_meaning(lobj_1, lobj_2, input_counter, matches_record, total_anticipated, input_override, save_fxn, target_lang):
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
        print(c.purple(lobj_1["id"]), "", lobj_1["translations"][target_lang])
        print(a_tags)
        print(a_topics)
        print("")
        print(c.purple(lobj_2["id"]), "", lobj_2["translations"][target_lang])
        print(b_tags)
        print(b_topics)
        print("")
        print("**********************************")
        print("")

        confirmation = True
        interval = 0

        if not input_override:
            user_input = input(f"{input_counter['num'] + 1}/{total_anticipated} same meaning?\n"
                               f"ENTER for yes   ANY KEY for no   w for tempsave ")

            if not user_input:
                confirmation = True
            elif user_input == "w":
                save_fxn(True)
                time.sleep(0.2)
                return is_it_the_same_meaning(lobj_1, lobj_2, input_counter, matches_record, total_anticipated,
                                              input_override, save_fxn, target_lang)
            else:
                confirmation = False

            interval = 0.2

        input_counter["num"] += 1

        if confirmation:
            print_conf_yes()
            record_it(True)
            time.sleep(interval)
            return "TAGS AND TOPICS MATCH"
        else:
            print_conf_no()
            time.sleep(interval)

    record_it(False)


def user_validate_translations(lobj, res, save_fxn, target_lang):
    def show_helptext():
        print("")
        c.print_teal("--------------------------------------------------------------------")
        print("")
        c.print_teal("Enter  : This lobj is OK.")
        print("")
        c.print_teal("D      : DELETE lobj.")
        c.print_teal("w      : WRITE current res array to temporary file.")
        print("")
        c.print_teal("fHello : FLAG lobj for later attention with any string eg 'Hello'.")
        c.print_teal("FHello : FLAG the previous lobj.")
        c.print_teal("xf     : REMOVE FLAGS from lobj.")
        print("")
        c.print_teal("d24    : DELETE translations at eg indexes 2 and 4.")
        c.print_teal("s24    : SWITCH translations at eg indexes 2 and 4 to a new lobj for this lemma.")
        c.print_teal(
            "s24S3  : Translations at eg indexes 2 and 4 are for new lobj, at index 3 is for both original and new lobjs.")
        print("--------------------------------------------------------------------")
        print("")
        user_validate_translations(lobj, res, save_fxn, target_lang)

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
        time.sleep(0.25)
        res.append(dupe)

    if int(lobj["id"].split("-")[2]) % 10 == 1:
        save_fxn(res, True)

    show1(lobj, target_lang)
    user_input = input("OK?   Enter for yes   Any key for no   h for help ")

    if not user_input:
        add_to_res(lobj)
        return

    if user_input == "h":
        show_helptext()
        return

    if user_input[0] not in ["f", "F"]:
        for char in user_input:
            if char not in "123456789dDfFwSsx":
                c.print_red("         Did not recognise user input. Options are:")
                time.sleep(0.5)
                show_helptext()
                return

    if user_input[0] == "D":
        print("🔥 DELETED LOBJ")
        time.sleep(0.25)
        return

    elif user_input[0] == "d":
        print("DELETING SOME TRANS...")
        indexes_trans_to_delete = [int(n) - 1 for n in user_input[1:]]
        trans_to_keep = []
        for tindex, tran in enumerate(lobj["translations"][target_lang]):
            if tindex not in indexes_trans_to_delete:
                trans_to_keep.append(tran)
        lobj["translations"][target_lang] = trans_to_keep
        user_validate_translations(lobj, res, save_fxn, target_lang)
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

        for tindex, tran in enumerate(lobj["translations"][target_lang]):
            if tindex in indexes_trans_to_move:
                trans_for_new_lobj.append(tran)
            elif tindex in indexes_trans_to_copy:
                trans_for_new_lobj.append(tran)
                trans_for_original_lobj.append(tran)
            else:
                trans_for_original_lobj.append(tran)

        print("")
        print("For lobj", c.blue(lobj["id"]))
        print("")
        print("ORIGINAL lobj will have")
        print(trans_for_original_lobj)
        print("")
        print("NEW lobj will have")
        print(trans_for_new_lobj)
        print("")
        confirm = not input("OK?   Enter for yes   Any key for no ")

        if confirm:
            lobj["translations"][target_lang] = trans_for_original_lobj
            add_to_res(lobj)

            if len(trans_for_new_lobj):
                duplicated_lobj = deepcopy(lobj)

                signal_word = None
                for w in trans_for_new_lobj:
                    if not signal_word and w not in lobj["translations"][target_lang]:
                        signal_word = w
                if not signal_word:
                    signal_word = "⛳"

                duplicated_lobj["id"] += f"({signal_word})"
                duplicated_lobj["tags"] = "🏁"  # Add tags and topics manully before next stage.
                duplicated_lobj["topics"] = None
                duplicated_lobj["translations"][target_lang] = trans_for_new_lobj
                add_to_res(duplicated_lobj)

                if "(" not in lobj["id"]:
                    lobj["id"] += f'({lobj["translations"][target_lang][0]})'

            return

        else:
            print("🔄 RESTARTING...")
            user_validate_translations(lobj, res, save_fxn, target_lang)
            return

    elif user_input == "w":
        save_fxn(res, True)
        user_validate_translations(lobj, res, save_fxn, target_lang)
        return

    elif user_input[0] == "f":
        flag = "🚩" + user_input[1:]
        print(c.blue(lobj["id"]), "will be FLAGGED")
        lobj["id"] += flag
        print(c.green(lobj["id"]))
        add_to_res(lobj)
        return

    elif user_input[0] == "F":
        flag = "🚩" + user_input[1:]
        print("⬆️", c.blue(res[-1]["id"]), "will be FLAGGED")
        res[-1]["id"] += flag
        print("⬆️", c.green(res[-1]["id"]))
        user_validate_translations(lobj, res, save_fxn, target_lang)
        return

    elif user_input == "xf":
        if "🚩" in res[-1]["id"]:
            print("❌", c.blue(res[-1]["id"]), "will be UNFLAGGED")
            res[-1]["id"] = res[-1]["id"][:res[-1]["id"].index("🚩")]
            print("❌", c.green(res[-1]["id"]))
        else:
            print(c.green(res[-1]["id"]), "DOESN'T HAVE ANY FLAGS")
        user_validate_translations(lobj, res, save_fxn, target_lang)
        return

    show_helptext()


def add_signalwords(sibling_set):
    signalwords = get_signalwords(sibling_set)

    if not signalwords:
        print("NO SIGNALWORDS")
        return

    lobjs_with_signalwords = []
    lobjs_to_delete = []

    for signalword_index, signalword in enumerate(signalwords):

        sib_lobj = sibling_set[signalword_index]

        if signalword == "x":
            lobjs_to_delete.append(sib_lobj)
        else:
            new_id = sib_lobj["id"]
            if "(" in new_id:
                new_id = new_id[:new_id.index("(")]
            new_id += f"({signalword})"

            lobjs_with_signalwords.append([sib_lobj, new_id])

    for lobj_with_signalword in lobjs_with_signalwords:
        print(">>", c.green(lobj_with_signalword[1]), lobj_with_signalword[0]["»trans"])
    print("")

    user_input = input("OK?   Enter for yes   Any key for no ")
    confirmation = not user_input

    if confirmation:
        for lobj_with_signalword in lobjs_with_signalwords:
            lobj_with_signalword[0]["id"] = lobj_with_signalword[1]

        for lobj_to_delete in lobjs_to_delete:
            c.print_bold("DELETING", lobj_to_delete["id"])
            print("")
            time.sleep(0.5)
            sibling_set.remove(lobj_to_delete)

        if len(sibling_set) == 1:
            only_sibling = sibling_set[0]
            only_sibling["id"] = only_sibling["id"][:only_sibling["id"].index("(")]
            print("Is only sibling so have removed signalword.")
            print(c.green(only_sibling["id"]))
            time.sleep(0.5)

        return

    add_signalwords(sibling_set)


def get_signalwords(lobjs):
    if len(lobjs) < 2:
        print("NO LONGER SIBLINGS")
        for lobj in lobjs:
            print(lobj["id"], lobj["»trans"])
        return

    print("")
    print("* * * * * * * * * * * * * * *")
    for lobj in lobjs:
        print(c.purple(lobj["id"]), lobj["»trans"])
    print("* * * * * * * * * * * * * * *")
    print("")

    user_input = input('Enter signalwords   h for help   ')

    if user_input == "h":
        c.print_teal("*  -  *  -  *  -  *  -  *  -  *  -  *  -  *")
        c.print_teal("Please enter signalwords separated by a space.")
        c.print_teal('You can merge lobjs by specifying indexes eg "merge 0 1".')
        c.print_teal('Or merge all given lobjs by giving no indexes "m".')
        c.print_teal('You can delete lobjs by giving "x" as the signalword.')
        c.print_teal("*  -  *  -  *  -  *  -  *  -  *  -  *  -  *")
        return get_signalwords(lobjs)

    if not user_input:
        c.print_red("Did not recognise input. Please type signalwords separated by a space.")
        time.sleep(0.5)
        return get_signalwords(lobjs)

    failed_character_check = False
    indexes_of_lobjs_to_merge = []

    if user_input[0:5] == "merge" or user_input in ["m", "merge"]:
        if user_input == "m":
            if len(lobjs):
                num = 0
                while num < len(lobjs):
                    indexes_of_lobjs_to_merge.append(num)
                    num += 1
        else:
            indexes_of_lobjs_to_merge = [int(char) for char in user_input.split(" ")[1:]]
            failed_index_validation = False
            if len(indexes_of_lobjs_to_merge) < 2:
                failed_index_validation = True
            for index_of_lobj in indexes_of_lobjs_to_merge:
                if index_of_lobj > (len(lobjs) - 1):
                    failed_index_validation = True
            if failed_index_validation:
                c.print_red("Invalid indexes")
                time.sleep(0.5)
                return get_signalwords(lobjs)
    else:
        for char in user_input:
            if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !":
                failed_character_check = True

    if failed_character_check:
        c.print_red("Invalid input")
        time.sleep(0.5)
        return get_signalwords(lobjs)

    if len(indexes_of_lobjs_to_merge):
        lobjs_to_merge = [lobjs[index_m] for index_m in indexes_of_lobjs_to_merge]
        print("")
        print("WILL MERGE")
        for lo in lobjs_to_merge:
            print(c.blue(lo["id"]), lo["»trans"])
        print("")
        conf = not input("OK?   Enter for yes   Any key for no ")
        if conf:
            base_lobj = lobjs_to_merge[0]

            for additive_lobj in lobjs_to_merge[1:]:
                for tran in additive_lobj["»trans"]:
                    if tran not in base_lobj["»trans"]:
                        base_lobj["»trans"].append(tran)
                lobjs.remove(additive_lobj)

            print("")
            print("MERGED into", c.green(base_lobj["id"]), base_lobj["»trans"])

        return get_signalwords(lobjs)

    signalwords = user_input.strip().split(" ")

    for signalword in signalwords:
        if len(signalword) < 2 and signalword != "x":
            c.print_red("Signalwords must be more than one character each, separated by a space.")
            time.sleep(0.5)
            return get_signalwords(lobjs)

    if len(signalwords) != len(lobjs):
        c.print_red(f"Expected {len(lobjs)} signalwords but got {len(signalwords)}.")
        time.sleep(0.5)
        return get_signalwords(lobjs)

    if len(list(set(signalwords))) != len(signalwords) or lobjs[0]["lemma"] in signalwords:
        c.print_red(f"Signalwords must be unique.")
        time.sleep(0.5)
        return get_signalwords(lobjs)

    failed_signalword_check = False
    for signalword in signalwords:
        if not len(signalword):
            failed_signalword_check = True
    if failed_signalword_check:
        c.print_red("Invalid signalwords")
        time.sleep(0.5)
        return get_signalwords(lobjs)

    return signalwords


def get_signalword(id):
    if "(" in id:
        ending = id[id.index("(") + 1:]
        return ending[:ending.index(")")]


def test_signalword(s):
    if not s:
        return False

    if not len(s):
        return False

    for flag_char in "🚩🏁⛳":
        if flag_char in s:
            return False

    for char in s:
        if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !,./-_":
            return False

    return True


def get_freq(lobj, prompt, allow_null: bool = False):
    if not prompt:
        prompt = f'Enter frequency 1-5 for {c.purple(lobj["lemma"])} {c.blue(lobj["id"])}\n'

    user_input = input(prompt)
    if not user_input:
        if allow_null:
            return
        return get_freq(lobj)
    if user_input not in "12345":
        return get_freq(lobj)

    return int(user_input)


def get_new_freqs(holder):

    changes = []

    indexes = [item[0] for item in holder]

    user_input = input("OK?   Enter for yes   Or type indexes and new frequencies   h for help\n\n")

    if not user_input:
        return []

    if user_input == "h":
        print("")
        c.print_teal("-  *  -  *  -  *  -  *  -  *  -  *  -")
        c.print_teal("You are shown 20 lobjs for the given frequency category.")
        c.print_teal("If you want to change any, type their index and new frequency category.")
        c.print_teal('eg "13-1 14-5 20-1"')
        c.print_teal('Or write as arrays:')
        c.print_teal('eg "3=[13,14,20] 4=[1,2,4,9]"')
        c.print_teal(
            "will set lobj at index 13 to be freq 1, lobj at index 14 to be freq 5, and lobj at index 20 to be freq 1.")
        c.print_teal("-  *  -  *  -  *  -  *  -  *  -  *  -")
        print("")
        return get_new_freqs(holder)

    user_input_split = user_input.strip().split(" ")

    if "[" in user_input:
        array_instructions = user_input.split(" ")
        for array_instruction in array_instructions:
            new_freq_requested = int(array_instruction[0])
            indexes_requested = array_instruction[3:-1].split(",")
            print("")
            print("new freq", int(new_freq_requested), "for indexes", [int(inde) for inde in indexes_requested])
            for index_requested in indexes_requested:
                for item in holder:
                    if int(item[0]) == int(index_requested):
                        changes.append([new_freq_requested, item[1]["id"]])
    else:
        if not len(user_input_split):
            c.print_red("Invalid input A")
            return get_new_freqs(holder)
        for new_freq_instructions in user_input_split:
            new_freq_instructions_split = new_freq_instructions.split("-")
            if len(new_freq_instructions_split) != 2:
                print(c.red("Invalid input B"), new_freq_instructions)
                return get_new_freqs(holder)
            else:
                for char in new_freq_instructions_split[0]:
                    if char not in "1234567890":
                        print(c.red("Invalid input C"), new_freq_instructions)
                        return get_new_freqs(holder)
                if int(new_freq_instructions_split[0]) not in indexes:
                    print(c.red("Invalid input D"), new_freq_instructions)
                    return get_new_freqs(holder)
                for char in new_freq_instructions_split[1]:
                    if char not in "12345":
                        print(c.red("Invalid input E"), new_freq_instructions)
                        return get_new_freqs(holder)
        for new_freq_instructions in user_input_split:
            new_freq_instructions_split = new_freq_instructions.split("-")
            index_to_modify = int(new_freq_instructions_split[0])
            new_freq = int(new_freq_instructions_split[1])
            for item in holder:
                if item[0] == index_to_modify:
                    changes.append([new_freq, item[1]["id"]])
    return changes

reg_refs = [
    {"tag": "fancy", "num": 1},
    {"tag": "slang", "num": 6},
    {"tag": "insult", "num": 7},
    {"tag": "curseword", "num": 8},
]