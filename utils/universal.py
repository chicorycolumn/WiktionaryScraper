import json
import os


class colors:
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


class color:
    def bold(s):
        return colors.BOLD + s + colors.END

    def purple_light(s):
        return colors.PURPLE + s + colors.END

    def cyan_light(s):
        return colors.CYAN + s + colors.END

    def teal_light(s):
        return colors.TEAL + s + colors.END

    def blue_light(s):
        return colors.BLUE + s + colors.END

    def green_light(s):
        return colors.GREEN + s + colors.END

    def yellow_light(s):
        return colors.YELLOW + s + colors.END

    def red_light(s):
        return colors.RED + s + colors.END

    def underline_light(s):
        return colors.UNDERLINE + s + colors.END

    #

    def purple(s):
        return color.bold(colors.PURPLE + s + colors.END)

    def cyan(s):
        return color.bold(colors.CYAN + s + colors.END)

    def teal(s):
        return color.bold(colors.TEAL + s + colors.END)

    def blue(s):
        return color.bold(colors.BLUE + s + colors.END)

    def green(s):
        return color.bold(colors.GREEN + s + colors.END)

    def yellow(s):
        return color.bold(colors.YELLOW + s + colors.END)

    def red(s):
        return color.bold(colors.RED + s + colors.END)

    def underline(s):
        return color.bold(colors.UNDERLINE + s + colors.END)

    #

    def print_purple(s):
        print(color.purple(s))

    def print_cyan(s):
        print(color.cyan(s))

    def print_teal(s):
        print(color.teal(s))

    def print_blue(s):
        print(color.blue(s))

    def print_green(s):
        print(color.green(s))

    def print_yellow(s):
        print(color.yellow(s))

    def print_red(s):
        print(color.red(s))

    def print_underline(s):
        print(color.underline(s))

    def print_bold(s):
        print(color.bold(s))


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


def load_tempsave_if_exists(tempsave_path):
    if os.path.isfile(tempsave_path + ".json"):
        with open(tempsave_path + ".json", "r") as f:
            loaded = json.load(f)
            color.print_teal("Loaded " + str(len(loaded)) + " items from tempsave.")
            f.close()
        return loaded
    else:
        color.print_teal("No tempsave_path file found, I assume you're at the start of this batch?")
        return []