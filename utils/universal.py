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
