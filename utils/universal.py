import json
import os
import time
from math import floor


class Colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    TEAL = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Color:
    def bold(s: str):
        return Colors.BOLD + s + Colors.END

    def purple_light(s: str):
        return Colors.PURPLE + s + Colors.END

    def cyan_light(s: str):
        return Colors.CYAN + s + Colors.END

    def teal_light(s: str):
        return Colors.TEAL + s + Colors.END

    def blue_light(s: str):
        return Colors.BLUE + s + Colors.END

    def green_light(s: str):
        return Colors.GREEN + s + Colors.END

    def yellow_light(s: str):
        return Colors.YELLOW + s + Colors.END

    def red_light(s: str):
        return Colors.RED + s + Colors.END

    def underline_light(s: str):
        return Colors.UNDERLINE + s + Colors.END

    #

    def purple(s: str):
        return Color.bold(Colors.PURPLE + s + Colors.END)

    def cyan(s: str):
        return Color.bold(Colors.CYAN + s + Colors.END)

    def teal(s: str):
        return Color.bold(Colors.TEAL + s + Colors.END)

    def blue(s: str):
        return Color.bold(Colors.BLUE + s + Colors.END)

    def green(s: str):
        return Color.bold(Colors.GREEN + s + Colors.END)

    def yellow(s: str):
        return Color.bold(Colors.YELLOW + s + Colors.END)

    def red(s: str):
        return Color.bold(Colors.RED + s + Colors.END)

    def underline(s: str):
        return Color.bold(Colors.UNDERLINE + s + Colors.END)

    #

    def print_purple(s: str):
        print(Color.purple(s))

    def print_cyan(s: str):
        print(Color.cyan(s))

    def print_teal(s: str):
        print(Color.teal(s))

    def print_blue(s: str):
        print(Color.blue(s))

    def print_green(s: str):
        print(Color.green(s))

    def print_yellow(s: str):
        print(Color.yellow(s))

    def print_red(s: str):
        print(Color.red(s))

    def print_underline(s: str):
        print(Color.underline(s))

    def print_bold(s: str):
        print(Color.bold(s))

    def print_inside_rainbow(input):
        print("")
        print("")
        Color.print_red("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_yellow("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_green("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_cyan("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_blue("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_purple("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        print(input)
        Color.print_purple("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_blue("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_cyan("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_green("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_yellow("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        Color.print_red("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")


def get_curried_save(output_path: str, tempsave_path: str):
    def curried_save(data: any, temp: bool = False):
        print(f"📀 {'SAVING PROGRESS' if temp else 'SAVING FINAL'}")

        _output_path = tempsave_path if temp else output_path

        with open(_output_path + ".json", "w") as outfile:
            print(f'Writing {len(data)} results.')
            data_json = json.dumps(data, indent=2, ensure_ascii=False)
            outfile.write(data_json)
            outfile.close()
        print("Done")

    return curried_save


def save(output_path: str, tempsave_path: str, data: any, temp: bool = False):
    print(f"📀 {'SAVING PROGRESS' if temp else 'SAVING FINAL'}")

    _output_path = tempsave_path if temp else output_path

    with open(_output_path + ".json", "w") as outfile:
        print(f'Writing {len(data)} results.')
        data_json = json.dumps(data, indent=2, ensure_ascii=False)
        outfile.write(data_json)
        outfile.close()


def load_data(input_path):
    with open(input_path + ".json", "r") as f:
        loaded = json.load(f)
        print("Loaded", len(loaded), "items from input.")
        f.close()
    return loaded if loaded else []


def load_tempsave_if_exists(tempsave_path, input_path: str = None):
    if os.path.isfile(tempsave_path + ".json"):
        with open(tempsave_path + ".json", "r") as f:
            loaded = json.load(f)
            Color.print_teal("Loaded " + str(len(loaded)) + " items from tempsave.")
            f.close()
        return loaded
    else:
        if not input_path:
            Color.print_teal("No tempsave_path file found, I assume you're at the start of this batch?")
            return []
        else:
            Color.print_teal(f'No tempsave_path file found, loading input "{input_path}".')
            with open(input_path + ".json", "r") as f:
                loaded = json.load(f)
                Color.print_teal("Loaded " + str(len(loaded)) + " items from input.")
                f.close()
            return loaded


def deepequals(obj1, obj2):
    def _deepequals(item1, item2):
        if type(item1) is not type(item2):
            return False

        if type(item1) in [str, int, float, complex, bool]:
            return item1 == item2

        if item1 is None:
            return item1 == item2

        if type(item1) in [list, tuple, set, frozenset]:

            if len(item1) != len(item2):
                return False

            for index, item_from_1 in enumerate(item1):
                item_from_2 = item2[index]
                return _deepequals(item_from_1, item_from_2)

        if type(item1) is dict:
            keys_from_1 = [k for k in item1]
            keys_from_2 = [k for k in item2]
            if not _deepequals(keys_from_1, keys_from_2):
                return False
            for key in item1:
                return _deepequals(item1[key], item2[key])

        return True

    return _deepequals(obj1, obj2)


def interact_cmd_history(user_input, cmd_history):
    if user_input[0] == "q":
        if user_input[1] == "q":
            Color.print_yellow("COMMAND HISTORY")
            for ind in range(1, 5):
                if len(cmd_history) >= ind:
                    print(f"q{ind}", Color.yellow(cmd_history[-ind]))
            time.sleep(0.8)
            return True

        else:
            index_of_cmd_to_repeat = int(user_input[1])
            if len(cmd_history) < index_of_cmd_to_repeat:
                Color.print_red("History does not go back that far.")
                return True
            cmd_to_repeat = cmd_history[-index_of_cmd_to_repeat]
            Color.print_yellow(cmd_to_repeat)
            confirmed = not input("Repeat cmd?   Enter for yes   Any key for no")
            if confirmed:
                return cmd_to_repeat
            else:
                return True


def replace_char_at_index(s, index, new_char):
    split = [char for char in s]
    split[index] = new_char
    return ''.join(split)


def progress_bar(index, total, use_emojis: bool = False):
    height = 50
    emojis_1 = '🎷🌇🏐🏔🎵🏈🎣🏀🎼🎁🏰️💃🌃🎃🌋🥋🎺🎂🏜🪅🏸🎹🎊🎳⚽🕺🏝🎈🎻🎸🎋🥅🎄🏏🎏🏕🥊🎆🗻🏉🎾🥌🎿🏓⛸🎅🎶🥎🏖'
    emojis_2 = "🍓👹💃🍊🐯🎃🦁🐈⭐🌻🌝🐝🍌🐠🍋🧀🌽🍀🌲🌴🐍🐢🌱🥑🦖🫑🎋🥶🧢🐬🚙🐳👖🌀📘🙆‍♀️💟😈🍆👾🍇💜"


    if use_emojis:
        height = len(emojis_2)
        progress = floor((index / total) * height)
        emoji_string = emojis_2[0:progress]
        print(f'[{emoji_string}{("-" if not use_emojis else "--") * (height - progress)}]')
        if (len(emoji_string)):
            print(("   " + emoji_string[-1]) * 5)
    else:
        progress = floor((index / total) * height)
        Color.print_purple(f'[{"#" * progress}{"-" * (height - progress)}]')
