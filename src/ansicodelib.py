"""
basic functions for showing colors, moving the cursor,
and working with the screen buffer.
"""

import sys
from typing import Any


class ANSICursor:
    @staticmethod
    def cur_up(rows: int = 1):
        sys.stdout.write(f"\033[{rows}A")

    @staticmethod
    def cur_dn(rows: int = 1):
        sys.stdout.write(f"\033[{rows}B")

    @staticmethod
    def cur_fwd(cols: int = 1):
        sys.stdout.write(f"\033[{cols}C")

    @staticmethod
    def cur_bwd(cols: int = 1):
        sys.stdout.write(f"\033[{cols}D")

    @staticmethod
    def cur_goto(col: int = 1, row: int = 1):
        sys.stdout.write(f"\033[{row};{col}H")

    @staticmethod
    def cur_reset():
        sys.stdout.write(f"\033[1;1H")

    @staticmethod
    def cur_hide():
        sys.stdout.write("\033[?25l")

    @staticmethod
    def cur_show():
        sys.stdout.write(f"\033[?25h")

class ANSIBuffer:
    @staticmethod
    def buf_flush():
        sys.stdout.flush()

    @staticmethod
    def buf_clear():
        sys.stdout.write("\033[2J")

    @staticmethod
    def buf_write(*s: Any, sep: str = " "):
        sys.stdout.write(sep.join(map(str, s)))

    @staticmethod
    def buf_scroll_up(lines: int = 1):
        sys.stdout.write(f"\033[{lines}S")

    @staticmethod
    def buf_scroll_dn(lines: int = 1):
        sys.stdout.write(f"\033[{lines}T")

    @staticmethod
    def buf_enable_alt():
        sys.stdout.write(f"\033[?1049h")

    @staticmethod
    def buf_disable_alt():
        sys.stdout.write(f"\033[?1049l")

    @staticmethod
    def buf_set_title(title: str):
        sys.stdout.write(f"\033]0;{title}\033\\\\")

    @staticmethod
    def buf_get_hypr(url: str, label: str = "") -> str:
        return f"\033]8;;{url}\033\\\\{label}\033]8;;\033\\\\"

class ANSIStyles:
    RESET = "\033[0m"
    RESET_BOLD_DIM = "\033[22m"
    RESET_ITALIC = "\033[23m"
    RESET_UNDERLINE = "\033[24m"
    RESET_BLINK = "\033[25m"
    RESET_REVERSE = "\033[27m"
    RESET_HIDDEN = "\033[28m"
    RESET_STRIKE = "\033[29m"

    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKE = "\033[9m"

class ANSIForeground:
    FG_DARK = "\033[30m"
    FG_RED = "\033[31m"
    FG_GREEN = "\033[32m"
    FG_YELLOW = "\033[33m"
    FG_BLUE = "\033[34m"
    FG_MAGENTA = "\033[35m"
    FG_CYAN = "\033[36m"
    FG_WHITE = "\033[37m"

    FG_DARK_EX = "\033[90m"
    FG_RED_EX = "\033[91m"
    FG_GREEN_EX = "\033[92m"
    FG_YELLOW_EX = "\033[93m"
    FG_BLUE_EX = "\033[94m"
    FG_MAGENTA_EX = "\033[95m"
    FG_CYAN_EX = "\033[96m"
    FG_WHITE_EX = "\033[97m"

class ANSIBackground:
    BG_DARK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    BG_DARK_EX = "\033[100m"
    BG_RED_EX = "\033[101m"
    BG_GREEN_EX = "\033[102m"
    BG_YELLOW_EX = "\033[103m"
    BG_BLUE_EX = "\033[104m"
    BG_MAGENTA_EX = "\033[105m"
    BG_CYAN_EX = "\033[106m"
    BG_WHITE_EX = "\033[107m"

class ANSIColors(ANSIStyles, ANSIForeground, ANSIBackground):
    @staticmethod
    def get_ansi_code(r: int, g: int, b: int, *, is_bg: bool = False) -> str:
        if is_bg:
            return f"\033[48;2;{r};{g};{b}m"
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def apply_styles(text: str, *styles: str, reset: bool|str = True) -> str:
        prefix = ""
        suffix = ANSIStyles.RESET if reset == True else ""
        for color in styles:
            if reset != True:
                if color != "apply_colors" and hasattr(ANSIColors, color):
                    color = getattr(ANSIColors, color)
                    if hasattr(ANSIStyles, color):
                        if color in ("BOLD", "DIM"):
                            suffix += ANSIStyles.RESET_BOLD_DIM
                        else:
                            suffix += getattr(ANSIStyles, f"RESET_{color}")
            prefix += color
        if isinstance(reset, bool):
            if not reset:
                suffix = ""
        elif isinstance(reset, str):
            if hasattr(ANSIStyles, reset):
                suffix  = getattr(ANSIStyles, reset)
            else:
                suffix = reset
        else:
            suffix = reset

        return f"{prefix}{text}{suffix}"