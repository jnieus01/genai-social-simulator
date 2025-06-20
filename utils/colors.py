RESET = "\033[0m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RED = "\033[91m"

BOT_COLORS = {"BOT1": BLUE, "BOT2": GREEN, "system": MAGENTA}


def colorize(bot_name, text):
    color = BOT_COLORS.get(bot_name, CYAN)
    return f"{color}{text}{RESET}"
