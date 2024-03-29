import json
import os
import time
from copy import deepcopy

from utils.general.common import write_todo
from utils.universal import Color as c, interact_cmd_history, replace_char_at_index, split_if_slash, print_inflections, \
    print_in_multiples, strip_accents


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


def is_it_the_same_meaning(lobj_1, lobj_2, input_counter, matches_record, total_anticipated, input_override, save_fxn,
                           target_lang):
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

    for x in [a_tags, a_topics]:
        if x is None:
            c.print_red("Doesn't have both tags and topics?")
            print(a_topics, a_tags, lobj_1)
            raise Exception("Stop")

    for x in [b_tags, b_topics]:
        if x is None:
            c.print_red("Doesn't have both tags and topics?")
            print(b_topics, b_tags, lobj_2)
            raise Exception("Stop")

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
                time.sleep(0.8)
                return is_it_the_same_meaning(lobj_1, lobj_2, input_counter, matches_record, total_anticipated,
                                              input_override, save_fxn, target_lang)
            else:
                confirmation = False

            interval = 0.4

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


def add_signalword_automatically(lobj_A, trans_for_lobj_A, trans_of_lobj_B):
    def _get_signalword_automatically():
        for w in trans_for_lobj_A:
            if w not in trans_of_lobj_B:
                return w
        return "⛳"

    signal_word = _get_signalword_automatically()
    lobj_A["id"] += f"({signal_word})"


def user_validate_translations(src_lobj_index, lobj, res, save_fxn, target_lang, cmd_history):
    def restart():
        return user_validate_translations(src_lobj_index, lobj, res, save_fxn, target_lang, cmd_history)

    def show_helptext():
        print("")
        c.print_teal("--------------------------------------------------------------------")
        print("")
        c.print_teal("Enter  : This lobj is OK.")
        print("")
        c.print_teal("h      : Help.")
        c.print_teal("qq     : Show COMMAND history.")
        c.print_teal("q1     : Repeat last COMMAND.")
        print("")
        c.print_teal("D      : DELETE lobj.")
        c.print_teal("w      : WRITE current res array to temporary file.")
        print("")
        c.print_teal("fHello : Add custom FLAG to lobj for later attention with any string eg 'Hello'.")
        c.print_teal("FHello : Add custom FLAG to previous lobj.")
        c.print_teal("xf     : REMOVE FLAGS from lobj.")
        print("")
        c.print_teal('a tin  : ADD translations eg "tin".')
        c.print_teal('a hue +color  : ADD translations eg "hue" and add additionalSpelling eg "color".')
        c.print_teal('a table.tennis  : ADD translations eg "table tennis".')
        c.print_teal("d24    : DELETE translations at eg indexes 2 and 4.")
        c.print_teal("s24    : SPLIT translations at eg indexes 2 and 4 to a new lobj for this lemma.")
        c.print_teal(
            "S24    : SPLIT translations at eg indexes 2 and 4 to a new lobj for this lemma but keep them in original lobj also.")
        c.print_teal(
            "s24S3  : Translations at eg indexes 2 and 4 are for new lobj, at index 3 is for both original and new lobjs.")
        c.print_teal("s      : SPLIT each translation to a new lobj for this lemma.")
        c.print_teal(
            "$ [1,2] [1,2,3] [2,3]      : SPLIT these numbered translations into these new lobjs for this lemma.")
        print("--------------------------------------------------------------------")
        print("")
        restart()

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
        time.sleep(0.8)
        res.append(dupe)

    if src_lobj_index % 10 == 0:
        save_fxn(res, True)

    show1(lobj, target_lang)
    user_input = input(
        "OK?   Enter for yes   Any key for no   a for Add   a then + for additional spellings   h for help\n")

    if not user_input:
        add_to_res(lobj)
        return

    if user_input == "h":
        show_helptext()
        return

    cmd_history_interaction = interact_cmd_history(user_input, cmd_history)
    if cmd_history_interaction == True:
        return restart()
    if type(cmd_history_interaction) is str:
        user_input = cmd_history_interaction

    if user_input[0] not in "fFa$":
        for char in user_input:
            if char not in "123456789dDfFwSsx":
                c.print_red("         Did not recognise user input. Options are:")
                time.sleep(0.8)
                show_helptext()
                return

    if user_input[0] in "sd":
        for char in user_input[1:]:
            if char not in "123456789":
                c.print_red("         Did not recognise user input. Options are:")
                time.sleep(0.8)
                show_helptext()
                return

    cmd_history.append(user_input)

    if user_input[0] == "D":
        print("🔥🔥 DELETED LOBJ")
        time.sleep(0.8)
        return

    elif user_input[0] == "d":
        print("DELETING SOME TRANS...")
        indexes_trans_to_delete = [int(n) - 1 for n in user_input[1:]]
        trans_to_keep = []
        for tindex, tran in enumerate(lobj["translations"][target_lang]):
            if tindex not in indexes_trans_to_delete:
                trans_to_keep.append(tran)
        lobj["translations"][target_lang] = trans_to_keep
        restart()
        return

    elif user_input[0] == "a" and " " in user_input:
        print("ADDING TRANS...")
        new_trans = user_input.split(" ")[1:]
        new_trans = [tr.replace(".", " ") for tr in new_trans]
        lobj["translations"][target_lang].extend(new_trans)
        restart()
        return

    elif user_input[0] in ["s", "S", "$"]:
        print("SWITCHING SOME TRANS TO NEW LOBJ...")

        if user_input == "s":
            user_input = "$"
            for i in range(len(lobj["translations"][target_lang])):
                user_input += f" [{i + 1}]"

        if user_input[0] == "$":
            new_index_sets_per_lobj = []
            user_input = user_input[2:].split(" ")
            for indices_string in user_input:
                indices = [int(char) - 1 for char in indices_string[1:-1].split(",")]
                new_index_sets_per_lobj.append(indices)
            print("new_index_sets_per_lobj", new_index_sets_per_lobj)
            new_trans_sets_per_lobj = [[lobj["translations"][target_lang][index] for index in new_index_set_per_lobj]
                                       for new_index_set_per_lobj in new_index_sets_per_lobj]
            print("new_trans_sets_per_lobj", new_trans_sets_per_lobj)

            print("")
            print("For lobj", c.blue(lobj["id"]))
            print("")
            print("EACH duplicate lobj will have")
            for new_tran_set_per_lobj in new_trans_sets_per_lobj:
                print("")
                print(new_tran_set_per_lobj)
            print("")
            confirm = not input("OK?   Enter for yes   Any key for no ")

            if confirm:
                clone_seed_lobj = deepcopy(lobj)

                lobj["translations"][target_lang] = new_trans_sets_per_lobj[0]
                add_signalword_automatically(lobj, new_trans_sets_per_lobj[0], [])
                add_to_res(lobj)

                for new_tran_set_per_lobj in new_trans_sets_per_lobj[1:]:
                    duplicated_lobj = deepcopy(clone_seed_lobj)

                    duplicated_lobj["translations"][target_lang] = new_tran_set_per_lobj
                    add_signalword_automatically(duplicated_lobj, new_tran_set_per_lobj, [])
                    duplicated_lobj["tags"] = "🏁"  # Add tags and topics manully before next stage.
                    duplicated_lobj["topics"] = None

                    add_to_res(duplicated_lobj)

                return
            else:
                print("🔄 RESTARTING...")
                restart()
                return
        else:
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

            if len(trans_for_new_lobj) and confirm:
                duplicated_lobj = deepcopy(lobj)

                duplicated_lobj["translations"][target_lang] = trans_for_new_lobj
                add_signalword_automatically(duplicated_lobj, trans_for_new_lobj, trans_for_original_lobj)

                duplicated_lobj["tags"] = "🏁"  # Add tags and topics manully before next stage.
                duplicated_lobj["topics"] = None

                lobj["translations"][target_lang] = trans_for_original_lobj
                add_signalword_automatically(lobj, trans_for_original_lobj, trans_for_new_lobj)

                add_to_res(lobj)
                add_to_res(duplicated_lobj)

                return

            print("🔄 RESTARTING...")
            restart()
            return

    elif user_input == "w":
        save_fxn(res, True)
        restart()
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
        restart()
        return

    elif user_input == "xf":
        if "🚩" in res[-1]["id"]:
            print("❌", c.blue(res[-1]["id"]), "will be UNFLAGGED")
            res[-1]["id"] = res[-1]["id"][:res[-1]["id"].index("🚩")]
            print("❌", c.green(res[-1]["id"]))
        else:
            print(c.green(res[-1]["id"]), "DOESN'T HAVE ANY FLAGS")
        restart()
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
            c.print_bold("DELETING " + lobj_to_delete["id"])
            print("")
            time.sleep(0.8)
            sibling_set.remove(lobj_to_delete)

        if len(sibling_set) == 1:
            only_sibling = sibling_set[0]
            only_sibling["id"] = only_sibling["id"][:only_sibling["id"].index("(")]
            print("Is only sibling so have removed signalword.")
            print(c.green(only_sibling["id"]))
            time.sleep(0.8)

        return

    add_signalwords(sibling_set)


def get_signalwords(lobjs):
    def restart():
        return get_signalwords(lobjs)

    if len(lobjs) < 2:
        print("NO LONGER SIBLINGS")
        for lobj in lobjs:
            print(lobj["id"], lobj["»trans"])
        return

    print("")
    print("* * * * * * * * * * * * * * *")
    for lobj in lobjs:
        if "»trans" not in lobj:
            print(c.red('No "»trans" key found on lobj'), lobj)
            raise Exception("Stop")
        print(c.purple(lobj["id"]), lobj["»trans"])
    print("* * * * * * * * * * * * * * *")
    print("")

    user_input = input('Enter signalwords   m to merge lobjs   x to delete   h for help\n')

    if user_input == "h":
        c.print_teal("*  -  *  -  *  -  *  -  *  -  *  -  *  -  *")
        c.print_teal("Please enter signalwords separated by a space.")
        c.print_teal('You can merge lobjs by specifying indexes eg "m01" will merge lobj 0 and lobj 1.')
        c.print_teal('Or merge all given lobjs by giving no indexes "m".')
        c.print_teal('You can delete lobjs by giving "x" as the signalword.')
        c.print_teal("*  -  *  -  *  -  *  -  *  -  *  -  *  -  *")
        return restart()

    if not user_input:
        c.print_red("Did not recognise input. Please type signalwords separated by a space.")
        time.sleep(0.8)
        return restart()

    failed_character_check = False
    indexes_of_lobjs_to_merge = []

    if user_input[0:5] == "merge" or user_input in ["m", "merge"] or (
            user_input[0] == "m" and user_input[1] in "1234567890"):
        if user_input == "m":
            if len(lobjs):
                num = 0
                while num < len(lobjs):
                    indexes_of_lobjs_to_merge.append(num)
                    num += 1
        else:
            indexes_of_lobjs_to_merge = [int(char) for char in user_input[1:]]
            failed_index_validation = False
            if len(indexes_of_lobjs_to_merge) < 2:
                failed_index_validation = True
            for index_of_lobj in indexes_of_lobjs_to_merge:
                if index_of_lobj > (len(lobjs) - 1):
                    failed_index_validation = True
            if failed_index_validation:
                print(c.red("Invalid indexes"), user_input, indexes_of_lobjs_to_merge)
                time.sleep(0.8)
                return restart()
    else:
        for char in user_input:
            if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !":
                failed_character_check = True

    if failed_character_check:
        c.print_red("Invalid input")
        time.sleep(0.8)
        return restart()

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

        return restart()

    signalwords = user_input.strip().split(" ")

    for signalword in signalwords:
        if len(signalword) < 2 and signalword != "x":
            c.print_red("Signalwords must be more than one character each, separated by a space.")
            time.sleep(0.8)
            return restart()

    if len(signalwords) != len(lobjs):
        c.print_red(f"Expected {len(lobjs)} signalwords but got {len(signalwords)}.")
        time.sleep(0.8)
        return restart()

    if len(list(set(signalwords))) != len(signalwords) or lobjs[0]["lemma"] in signalwords:
        c.print_red(f"Signalwords must be unique.")
        time.sleep(0.8)
        return restart()

    failed_signalword_check = False
    for signalword in signalwords:
        if not len(signalword):
            failed_signalword_check = True
    if failed_signalword_check:
        c.print_red("Invalid signalwords")
        time.sleep(0.8)
        return restart()

    signalwords = [sw.replace(".", " ") for sw in signalwords]

    return signalwords


def get_signalword(id):
    if "(" in id:
        ending = id[id.index("(") + 1:]
        signalword = ending[:ending.index(")")]
        if signalword[0] == "*":
            return signalword[1:]
        return signalword


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


def get_freq(lobj, prompt=None, allow_null: bool = False):
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
    def restart():
        return get_new_freqs(holder)

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
        return restart()

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
            return restart()
        for new_freq_instructions in user_input_split:
            new_freq_instructions_split = new_freq_instructions.split("-")
            if len(new_freq_instructions_split) != 2:
                print(c.red("Invalid input B"), new_freq_instructions)
                return restart()
            else:
                for char in new_freq_instructions_split[0]:
                    if char not in "1234567890":
                        print(c.red("Invalid input C"), new_freq_instructions)
                        return restart()
                if int(new_freq_instructions_split[0]) not in indexes:
                    print(c.red("Invalid input D"), new_freq_instructions)
                    return restart()
                for char in new_freq_instructions_split[1]:
                    if char not in "12345":
                        print(c.red("Invalid input E"), new_freq_instructions)
                        return restart()
        for new_freq_instructions in user_input_split:
            new_freq_instructions_split = new_freq_instructions.split("-")
            index_to_modify = int(new_freq_instructions_split[0])
            new_freq = int(new_freq_instructions_split[1])
            for item in holder:
                if item[0] == index_to_modify:
                    changes.append([new_freq, item[1]["id"]])
    return changes


def compare_lobj_id_root(id1, id2):
    if "(" in id1:
        id1 = "".join(id1[:id1.index("(")])

    if "(" in id2:
        id2 = "".join(id2[:id2.index("(")])

    return id1 == id2


allohom_info_template = {
    "singleWordtype": True,
    "text": "",
    "emoji": ""
}

allohom_infos = {
    "ab": {"singleWordtype": True, "text": "abstract", "emoji": "💭"},
    "ph": {"singleWordtype": True, "text": "physical", "emoji": "🪨"},
    "pe": {"singleWordtype": True, "text": "person", "emoji": "🏃"},
    "ob": {"singleWordtype": True, "text": "object", "emoji": "📦"},
    "fo": {"singleWordtype": True, "text": "food", "emoji": "🍲"},
    "me": {"singleWordtype": True, "text": "medical", "emoji": "🩺"},
    "qu": {"singleWordtype": True, "text": "quality", "emoji": "✅"},
    "ma": {"singleWordtype": True, "text": "mathematical", "emoji": "🧮"},
    "di": {"singleWordtype": True, "text": "direction", "emoji": "📍"},
    "lo": {"singleWordtype": True, "text": "location", "emoji": "📍"},
    "ti": {"singleWordtype": True, "text": "time", "emoji": "🕒"},
    "fr": {"singleWordtype": True, "text": "frequency", "emoji": "📅"},
    "mo": {'singleWordtype': True, 'text': 'money', 'emoji': '💵'},
    "ge": {'singleWordtype': True, 'text': 'general', 'emoji': '🔲'},
    "tx": {'singleWordtype': True, 'text': 'texture', 'emoji': '🪨'},
    "th": {'singleWordtype': True, 'text': 'temperature', 'emoji': '🌡️'},
    "cu": {'singleWordtype': True, 'text': 'curseword', 'emoji': '🤬️'},
    "li": {'singleWordtype': True, 'text': 'linguistics', 'emoji': '🔤'},
    "ps": {'singleWordtype': True, 'text': 'psychological', 'emoji': '🧠'},
    "py": {'singleWordtype': True, 'text': 'personality', 'emoji': '🧠'},
    "ma": {"singleWordtype": True, "text": "mathematical", "emoji": "🧮"},
    "tr": {"singleWordtype": True, "text": "truthiness", "emoji": "💬"},
    "ac": {"singleWordtype": True, "text": "accuracy", "emoji": "✅"},
    "ea": {"singleWordtype": True, "text": "ease", "emoji": "🤔"},
    "po": {"singleWordtype": True, "text": "politics", "emoji": "🗽"},
    "lj": {"singleWordtype": True, "text": "law/justice", "emoji": "⚖️"},
    "sp": {"singleWordtype": True, "text": "speech", "emoji": "💬"},
    "ap": {"singleWordtype": True, "text": "appearance", "emoji": "🧍"},
    "bo": {"singleWordtype": True, "text": "body", "emoji": "🧍"},
    "an": {"singleWordtype": True, "text": "animal", "emoji": "🐕"},
    "co": {"singleWordtype": True, "text": "computing", "emoji": "💻"},
    "te": {"singleWordtype": True, "text": "technology", "emoji": "💻"},
    "sc": {"singleWordtype": True, "text": "school", "emoji": "🎒"},
    "ga": {"singleWordtype": True, "text": "games/sports", "emoji": "🎲"},
    "mt": {"singleWordtype": True, "text": "material", "emoji": "👚"},
    "pu": {"singleWordtype": True, "text": "punctuation", "emoji": "❕"},
    "ey": {"singleWordtype": True, "text": "employment", "emoji": "🏢"},
    "ro": {"singleWordtype": True, "text": "romantic", "emoji": "💕"},
    "dr": {"singleWordtype": True, "text": "driving", "emoji": "🚗"},
    "si": {"singleWordtype": True, "text": "science", "emoji": "🧫"},
    "ch": {"singleWordtype": True, "text": "chemical", "emoji": "🧪"},
    "bi": {"singleWordtype": True, "text": "biology", "emoji": "🧬"},
    "pc": {"singleWordtype": True, "text": "physics", "emoji": "☄️"},
    "we": {"singleWordtype": True, "text": "weather", "emoji": "☀️️"},
    "tt": {"singleWordtype": True, "text": "transport", "emoji": "🚢️️"},
    "fu": {"singleWordtype": True, "text": "furniture", "emoji": "🛋️️️"},
    "dg": {"singleWordtype": True, "text": "drug", "emoji": "🚬️️️"},
    "cr": {"singleWordtype": True, "text": "crafts", "emoji": "🧵️️"},
    "na": {"singleWordtype": True, "text": "nature", "emoji": "🌳️"},
    "ev": {"singleWordtype": True, "text": "event", "emoji": "📅️"},
    "tl": {"singleWordtype": True, "text": "title", "emoji": "🙇"},
    "fm": {"singleWordtype": True, "text": "form of address", "emoji": "👋"},
    "wr": {"singleWordtype": True, "text": "writing", "emoji": "📖"},
    "im": {"singleWordtype": True, "text": "importance", "emoji": "❗"},
    "pm": {"singleWordtype": True, "text": "permission", "emoji": "🚫"},
    "bb": {"singleWordtype": True, "text": "ability", "emoji": "🏃"},
    "pb": {"singleWordtype": True, "text": "possibility", "emoji": "❓"},
    "nj": {"singleWordtype": True, "text": "negative judgement", "emoji": "👎"},
    "pj": {"singleWordtype": True, "text": "positive judgement", "emoji": "👍"},
    "cl": {"singleWordtype": True, "text": "clothes", "emoji": "👚"},
    "mi": {"singleWordtype": True, "text": "military", "emoji": "🪖"},
    "mu": {"singleWordtype": True, "text": "music", "emoji": "🎵"},
    "iv": {"singleWordtype": True, "text": "intransitive", "emoji": "🇮"},
    "tv": {"singleWordtype": True, "text": "transitive", "emoji": "🇹"},
    "pv": {"singleWordtype": True, "text": "plus verb", "emoji": "🇻"},
    "pn": {"singleWordtype": True, "text": "plus noun", "emoji": "🇳"},
    "so": {"singleWordtype": True, "text": "sound", "emoji": "🔊"},
    "xs": {"singleWordtype": True, "text": "small", "emoji": "🔹"},
    "xl": {"singleWordtype": True, "text": "large", "emoji": "🔷"},
    "ns": {"singleWordtype": True, "text": "single", "emoji": "1"},
    "nm": {"singleWordtype": True, "text": "many", "emoji": "2"},
    "tc": {"singleWordtype": True, "text": "theatre", "emoji": "🎭"},
    "em": {"singleWordtype": True, "text": "emotion", "emoji": "🤪"},
}


def get_allohom_info(cmd_history):
    def restart():
        return get_allohom_info(cmd_history)

    template_keys = [k + allohom_infos[k]["text"][2:] for k in allohom_infos]
    template_keys.sort()

    index = 10
    while index < len(template_keys):
        print(", ".join([c.blue(t[:2]) + t[2:] for t in template_keys[index - 10:index]]))
        index = index + 10
    print(", ".join([c.blue(t[:2]) + t[2:] for t in template_keys[index - 10:index]]))

    user_input = input("Use first two letters of existing templates above, or enter new like so 'activity.🏕'\n")

    cmd_history_interaction = interact_cmd_history(user_input, cmd_history)
    if cmd_history_interaction == True:
        return restart()
    if type(cmd_history_interaction) is str:
        user_input = cmd_history_interaction

    if user_input in allohom_infos:
        cmd_history.append(user_input)
        return allohom_infos[user_input]

    if "." not in user_input:
        return restart()

    user_input_split = user_input.split(".")
    allohom_info = deepcopy(allohom_info_template)
    allohom_info["text"] = user_input_split[0]
    allohom_info["emoji"] = user_input_split[1]

    cmd_history.append(user_input)
    return allohom_info


def add_allohom_info(cmd_history, lobj, following_lobjs):
    print("")
    c.print_bold(f'CURRENT is             {lobj["id"]}')
    for following_lobj in following_lobjs:
        c.print_purple(f'                       {following_lobj}')
    print("")

    allohom_info = get_allohom_info(cmd_history)
    print(c.green(allohom_info["text"]), allohom_info)
    print("")
    lobj["allohomInfo"] = allohom_info
    if lobj['id'].endswith('(þ)'):
        lobj['id'] = lobj['id'][0:-3]
    time.sleep(0.8)


reg_refs = [
    {"tag": "fancy", "num": 1},
    {"tag": "slang", "num": 6},
    {"tag": "insult", "num": 7},
    {"tag": "curseword", "num": 8},
]


def run_sanhedrin(fxn, wordtypes, additional_args=[]):
    if not len(wordtypes):
        wordtypes = ["adj", "nco", "npe", "ver"]
    print(c.purple('Running for wordtypes:'), wordtypes)
    for w in wordtypes:
        print("")
        print(c.purple("Running for wordtype:"), w)
        fxn(w, *additional_args)
        time.sleep(1)


def run_sanhedrin_with_suffixes(fxn, wordtypes, suffixes, additional_args=[]):
    if not len(suffixes):
        suffixes = ['SRC', 'TGT']
    for suffix in suffixes:
        addition_args = [suffix] + additional_args
        run_sanhedrin(fxn, wordtypes, addition_args)


def get_unused(lobjs, nex, lang):
    unused = []
    for lob in [l for l in lobjs if not l.get("_untranslated")]:
        found = False
        for nobj in nex:
            if lob["id"] in nobj["traductions"][lang]:
                found = True
                break
        if not found:
            unused.append(lob["id"])
    return unused


def get_nonexisting(lobjs, nex, lang):
    nonexisting = []
    for nobj in nex:
        for lobj_id in nobj["traductions"][lang]:
            existing = False
            for lob in lobjs:
                if lob["id"] == lobj_id:
                    existing = True
                    break
            if not existing:
                nonexisting.append(lobj_id)
    return nonexisting


def get_inflections_eng_ver(lemma, cmd_history, manually_entered_inflections: [str] = None, reconfirming: bool = False):
    def restart():
        return get_inflections_eng_ver(lemma, cmd_history)

    if manually_entered_inflections:
        v2, v3, gerund, thirdPS = manually_entered_inflections
    else:
        remaining_words = None
        split_char = None

        if ' ' in lemma:
            split_char = ' '
            split = lemma.split(' ')
            lemma = split[0]
            remaining_words = split[1:]
        elif '-' in lemma:
            split_char = '-'
            split = lemma.split('-')
            lemma = split[0]
            remaining_words = split[1:]

        v2 = lemma + ("ed" if not lemma.endswith('e') else 'd')
        v3 = v2
        thirdPS = lemma + ("s" if (lemma[-1] not in 'hxsy' or lemma.endswith('th')) else "es")

        if lemma.endswith('y'):
            thirdPS = replace_char_at_index(thirdPS, -3, 'i')
            v2 = replace_char_at_index(v2, -3, 'i')
            v3 = replace_char_at_index(v3, -3, 'i')
        gerund = lemma + "ing"

        if lemma.endswith('e'):
            gerund = replace_char_at_index(gerund, -4, '')

        if remaining_words:
            print('remaining_words', remaining_words)
            v2 = split_char.join([v2, *remaining_words])
            v3 = split_char.join([v3, *remaining_words])
            thirdPS = split_char.join([thirdPS, *remaining_words])
            gerund = split_char.join([gerund, *remaining_words])

    print("")
    print_function = c.print_blue if reconfirming else c.print_bold
    print_function(f"yesterday I {v2},    I've already {v3}")
    print("")
    print_function(f'     yo we {gerund},      she {thirdPS}')
    print("")
    user_input = input(
        'Enter YES\nAny   NO\nd     to double final consonant\ne     to keep terminal "y"\nOr type in manually and press enter (add semicolon after v2 if v3 is same)\n: ')

    if not user_input or user_input == 'y':
        return [{
            "infinitive": lemma,
            "verbal": {},
            "v2": split_if_slash(v2),
            "v3": split_if_slash(v3),
            "thirdPS": split_if_slash(thirdPS),
            "gerund": split_if_slash(gerund)
        }, False]

    cmd_history_interaction = interact_cmd_history(user_input, cmd_history)
    if cmd_history_interaction == True:
        return restart()
    if type(cmd_history_interaction) is str:
        user_input = cmd_history_interaction
    cmd_history.append(user_input)

    if len(user_input) == 1:
        if user_input == 'e':
            v2 = replace_char_at_index(v2, -3, 'y')
            v3 = replace_char_at_index(v3, -3, 'y')
            thirdPS = replace_char_at_index(thirdPS, -3, 'y')
            thirdPS = replace_char_at_index(thirdPS, -2, '')
            return get_inflections_eng_ver(lemma, cmd_history, [v2, v3, gerund, thirdPS])
        if user_input == 'd':
            v2 = v2[0:-2] + v2[-3] + v2[-2:]
            v3 = v2
            gerund = gerund[0:-3] + gerund[-4] + gerund[-3:]
            return get_inflections_eng_ver(lemma, cmd_history, [v2, v3, gerund, thirdPS])
        return restart()

    else:
        split = user_input.split(",")

        if split[0][-1] == ';':
            v2 = split[0][0:-1]
            split[0] = v2
            split.insert(0, v2)

        if len(split) == 1:
            split.append(v3)
            split.append(gerund)
            split.append(thirdPS)
        if len(split) == 2:
            split.append(gerund)
            split.append(thirdPS)
        if len(split) == 3:
            split.append(thirdPS)

        split = [False if el == 'no' else el for el in split]
        return get_inflections_eng_ver(lemma, cmd_history, split, reconfirming)


def get_inflections_eng_nou(
        lemma,
        cmd_history,
        manually_entered_inflections: [str] = None,
        reconfirming: bool = False,
        keep_terminal_y: bool = False,
        flag: bool = False,
):
    def restart():
        return get_inflections_eng_nou(lemma, cmd_history)

    if manually_entered_inflections:
        plur_nom, sing_gen, plur_gen = manually_entered_inflections
    else:
        sing_gen = lemma + "'s"
        plur_nom = lemma + ("s" if (keep_terminal_y or lemma[-1] not in 'hxsy' or lemma.endswith('th')) else "es")
        if lemma.endswith('y') and not keep_terminal_y:
            plur_nom = replace_char_at_index(plur_nom, -3, 'i')
        plur_gen = plur_nom + "'"

    print("")
    print_function = c.print_blue if reconfirming else c.print_bold
    print_function(f'{lemma}, {plur_nom}')
    print_function(f'{sing_gen}, {plur_gen}')
    print("")
    user_input = input(
        'Enter for YES / Any for NO\nq     Keep terminal y\nw     Plural same as singular\ns     Tantum singulare\np     Tantum plurale\nOr type in irregular plural eg "men" and press Enter\n: ')

    cmd_history_interaction = interact_cmd_history(user_input, cmd_history)
    if cmd_history_interaction == True:
        return restart()
    if type(cmd_history_interaction) is str:
        user_input = cmd_history_interaction
    cmd_history.append(user_input)

    if user_input and user_input[0] == 'x':
        flag = '🚩'
        user_input = user_input[1:]

    if not user_input or user_input == 'y':
        return [{
            "singular": {
                "nom": lemma,
                "gen": split_if_slash(sing_gen)
            },
            "plural": {
                "nom": split_if_slash(plur_nom),
                "gen": split_if_slash(plur_gen)
            }
        }, flag]

    if user_input == 's':
        inflections = {
            "singular": {
                "nom": lemma,
                "gen": lemma + "'s",
                "lacking": True,
                "tantumSingulare": True,
            }
        }

        print_inflections(inflections)

        return [inflections, flag]

    if user_input == 'p':
        inflections = {
            "plural": {
                "nom": lemma,
                "gen": False,
                "lacking": True,
                "tantumPlurale": True,
            }
        }

        print_inflections(inflections)

        return [inflections, flag]

    if user_input == 'q':
        return get_inflections_eng_nou(lemma, cmd_history, None, True, True, flag=flag)

    if user_input == 'w':
        plur_nom = lemma
        sing_gen = lemma + "'s"
        plur_gen = sing_gen
        return get_inflections_eng_nou(lemma, cmd_history, [plur_nom, sing_gen, plur_gen], True, flag=flag)

    if len(user_input) == 1:
        return restart()

    else:
        if len(user_input) < 2 or "," in user_input:
            c.print_red("You must type one string: nominative plural")
            return restart()

        plur_nom = user_input
        sing_gen = lemma + "'s"

        if type(plur_nom) is str:
            if '/' in plur_nom:
                plur_nom = plur_nom.split('/')
            else:
                plur_nom = [plur_nom]
        else:
            plur_nom = plur_nom.split('/')

        if plur_nom[0].endswith('s'):
            plur_gen = [plur_nom_str + "'" for plur_nom_str in plur_nom]
        else:
            plur_gen = [plur_nom_str + "'s" for plur_nom_str in plur_nom]

        return get_inflections_eng_nou(lemma, cmd_history, [plur_nom, sing_gen, plur_gen], True, flag=flag)


def get_inflections_eng_adj(lemma, cmd_history, manually_entered_inflections: [str] = None, reconfirming: bool = False):
    def restart():
        return get_inflections_eng_adj(lemma, cmd_history)

    if manually_entered_inflections:
        compar, superl, adverb = manually_entered_inflections
    else:
        compar = lemma + ("er" if not lemma.endswith('e') else 'r')
        superl = lemma + ("est" if not lemma.endswith('e') else 'st')
        adverb = lemma + ("ly" if not lemma.endswith('ll') else 'y')
        if lemma.endswith('y'):
            compar = replace_char_at_index(compar, -3, 'i')
            superl = replace_char_at_index(superl, -4, 'i')
            adverb = replace_char_at_index(adverb, -3, 'i')
        if lemma.endswith('le'):
            adverb = replace_char_at_index(adverb, -3, '')
            adverb = replace_char_at_index(adverb, -3, '')
        if lemma.endswith('ic'):
            adverb = replace_char_at_index(adverb, -3, 'cal')

    print("")
    print_function = c.print_blue if reconfirming else c.print_bold
    print_function(compar if compar else '(none)')
    print_function(superl if superl else '(none)')
    print_function(adverb if adverb else '(none)')
    if not compar and not superl and not adverb:
        c.print_bold(f'(lemma was {lemma})')
    else:
        print("")

    user_input = input(
        'Enter for YES / Any for NO / Or type in manually and press Enter\na     "more" and "most" plus adverb\ns     "more" and "most" but NO adverb\nd     double final consonant\nf     NO adverb\ng     adverb ONLY\nx     NO ANYTHING\n: ')

    if not user_input or user_input == 'y':
        return [{
            "simple": lemma,
            "comparative": split_if_slash(compar),
            "superlative": split_if_slash(superl),
            "adverb": split_if_slash(adverb)
        }, False]

    cmd_history_interaction = interact_cmd_history(user_input, cmd_history)
    if cmd_history_interaction == True:
        return restart()
    if type(cmd_history_interaction) is str:
        user_input = cmd_history_interaction
    cmd_history.append(user_input)

    if user_input == 'f':
        return get_inflections_eng_adj(lemma, cmd_history, [compar, superl, False], True)
    if user_input == 'g':
        return get_inflections_eng_adj(lemma, cmd_history, [False, False, adverb], True)
    if user_input == 'd':
        compar = compar[0:-2] + compar[-3] + compar[-2:]
        superl = superl[0:-3] + superl[-4] + superl[-3:]
        return get_inflections_eng_adj(lemma, cmd_history, [compar, superl, adverb], True)
    if user_input == 's':
        return get_inflections_eng_adj(lemma, cmd_history, [f'more {lemma}', f'the most {lemma}', False], True)
    if user_input == 'a':
        return get_inflections_eng_adj(lemma, cmd_history, [f'more {lemma}', f'the most {lemma}', adverb], True)
    if user_input in ['no', 'x']:
        return get_inflections_eng_adj(lemma, cmd_history, [False, False, False], True)

    if len(user_input) == 1:
        return restart()

    else:
        split = user_input.split(",")

        if len(split) != 3 or any(len(s) < 2 for s in split):
            c.print_red("You must type three strings: comparative, superlative, adverb. Type 'no' for any if none.")
            return restart()
        else:
            split = [False if el == 'no' else el for el in split]
            return get_inflections_eng_adj(lemma, cmd_history, split, True)


def add_uncountable_label(lobj, cmd_history):
    def restart():
        return add_uncountable_label(lobj, cmd_history)

    results = []

    if not lobj["inflections"].get('plural') or not lobj["inflections"].get('singular'):
        c.print_teal('LACKING')
        return

    print("")
    user_input = input(c.bold(f'a lot of {lobj["lemma"]} ') + 'is wrong, right? ')

    if not user_input or user_input == 'y':
        results.append(True)
        results.append(False)
    else:
        user_input = input(c.bold(f'Two {lobj["inflections"]["plural"]["nom"]}. ') + 'OK? ')

        if not user_input or user_input == 'y':
            results.append(True)
        elif user_input in ["'", "n"]:
            results.append(False)
        else:
            return restart()

        user_input = input(c.bold(f'A lot of {lobj["lemma"]}. ') + 'OK? ')
        if not user_input or user_input == 'y':
            results.append(True)
        elif user_input in ["'", "n"]:
            results.append(False)
        else:
            return restart()

        if len(results) != 2:
            return restart()

    if results[0] and not results[1]:
        c.print_green('COUNTABLE')
        return
    elif results[1] and not results[0]:
        c.print_purple('TYPE ONE')
        lobj["_uncountableType"] = 1
        return
    elif results[1] and results[0]:
        c.print_yellow('TYPE TWO')
        lobj["_uncountableType"] = 2
        return
    else:
        return restart()


def add_size_tag(lobj, cmd_history):
    def restart():
        return add_size_tag(lobj, cmd_history)

    def print_lobj_info():
        print('ENG:', lobj['traductions']['ENG'])
        print('POL:', lobj['traductions']['POL'])

    if 'concrete' not in lobj['papers']:
        if 'abstract' in lobj['papers']:
            c.print_yellow('IS ABSTRACT ONLY')
            print("")
            print("")
            print("")
            print("")
            return
        else:
            print_lobj_info()
            raise Exception('Not concrete or abstract?')
    else:
        if any(t in lobj['papers'] for t in ['building', 'nation']):
            user_input = '6'
        else:
            c.print_bold('1-Pocket, 2-OneHand, 3-BothArms, 4-Team, 5-Machine, 6-Immovable,    a-Abstract, z-Not applicable        ? for info')
            user_input = input('Enter digit 0-6: ')

    if not user_input:
        return restart()

    if user_input == '?':
        print_lobj_info()
        return restart()

    if user_input == 'a':
        if 'abstract' not in lobj['papers']:
            lobj['papers'].append('abstract')
        return

    if user_input == 'z':
        return

    print("WAS:", lobj['papers'])

    if user_input in 'qwe':
        translate_input_dict = {
            'q': '4',
            'w': '5',
            'e': '6',
        }
        user_input = translate_input_dict[user_input]

    if user_input == '0':
        lobj['papers'] = [t for t in lobj['papers'] if t not in ['concrete', 'holdable']]
    elif user_input in '123456':
        size_tag = 's' + user_input
        lobj['papers'] = [size_tag] + [t for t in lobj['papers'] if t not in ['holdable']]
    else:
        if user_input == 'h':
            c.print_bold('0  NOT actually concrete')
            c.print_bold('1  POCKETABLE     needle - booklet')
            c.print_bold('2  ONE HAND       book - racquet')
            c.print_bold('3  BOTHS HANDS    dog - armchair')
            c.print_bold('4  TEAM move      bed - car')
            c.print_bold('5  MACHINE move   lorry - ship')
            c.print_bold('6  IMMOVABLE      house - mountain - wall')
        return restart()

    print("NOW:", lobj['papers'])


def get_concrete_input_adjective(lem):
    added_tags = []

    user_input = input(f'{lem} man, {lem} ball?   ENTER for yes   ANY for no  ')
    if not user_input or user_input == 'y':
        added_tags.append('concrete')

    user_input = input(f'{lem} idea, {lem} action?   ENTER for yes   ANY for no  ')
    if not user_input or user_input == 'y':
        added_tags.append('abstract')

    return added_tags


def get_concrete_input_noun(lem):
    added_tags = []

    user_input = input(f'he touch {lem}, he watch {lem}?   ENTER for yes   ANY for no  ')
    if not user_input or user_input == 'y':
        added_tags.append('concrete')

    user_input = input(f'he experience {lem}, he formulate {lem}?   ENTER for yes   ANY for no  ')
    if not user_input or user_input == 'y':
        added_tags.append('abstract')

    return added_tags


def renumber_inflections_root(stage, src, save, src_input_path):
    remaining = []

    src_ids = [l['id'] for l in src]
    for src_lobj in src:
        if "_inflectionsRoot" in src_lobj:
            root_id = src_lobj["_inflectionsRoot"]
            if root_id not in src_ids:
                root_id_trimmed = root_id[12:]
                matching_ids = [id for id in src_ids if id != src_lobj['id'] and id[12:] == root_id_trimmed]

                if stage == 2 and len(matching_ids) == 1:
                    src_lobj["_inflectionsRoot"] = matching_ids[0]
                    print(c.green(src_lobj['id']))

                elif len(matching_ids) == 0:
                    more_matching_ids = []
                    for id in [sid for sid in src_ids if sid != src_lobj['id']]:
                        if "(" in id:
                            double_trimmed_id = id[12:id.index("(")]
                            if double_trimmed_id == root_id_trimmed:
                                more_matching_ids.append(id)
                    if stage == 2 and len(more_matching_ids) == 1:
                        src_lobj["_inflectionsRoot"] = more_matching_ids[0]
                        print(c.green(src_lobj['id']))
                    else:
                        remaining.append([src_lobj['id'], more_matching_ids])

                elif len(matching_ids) > 1:
                    remaining.append([src_lobj['id'], matching_ids])

    if len(remaining):
        c.print_red("REQUIRE MANUAL RESOLUTION:")
        for remaining_item in remaining:
            print(remaining_item[0])
            print(remaining_item[1])
            print("")

    if stage == 2:
        save(src_input_path, None, src)


def check_all_inflections_begin_with(lobj):
    inflections_obj = lobj['inflections']
    incorrect_values = []
    lemma_start = strip_accents(lobj['lemma'][0:2])
    acceptable_beginnings = [
        lemma_start,
        f'bardziej {lemma_start}',
        f'najbardziej {lemma_start}',
        f'naj{lemma_start}',
        f'more {lemma_start}',
        f'the most {lemma_start}',
    ]

    def check_function(inflection_value):
        if any(bad_char in inflection_value for bad_char in '(){}[]'):
            c.print_red(inflection_value)
        is_correct = any(strip_accents(inflection_value).startswith(acceptable_beginning) for acceptable_beginning in acceptable_beginnings)
        if not is_correct:
            incorrect_values.append(inflection_value)

    def recurse(inf):
        for k in inf:
            if type(inf[k]) is str:
                check_function(inf[k])
            elif type(inf[k]) is dict:
                recurse(inf[k])
            elif type(inf[k]) is list:
                for el in inf[k]:
                    check_function(el)

    recurse(inflections_obj)

    if len(incorrect_values):
        print('')
        c.print_bold(lobj['id'])
        print_in_multiples(incorrect_values)
        return False
    return True
