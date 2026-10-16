import curses
import textwrap
from pathlib import Path

base_dir = Path(__file__).parent



def setup_colors():
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    curses.init_pair(5, curses.COLOR_RED, -1)


def safe_addstr(win, y, x, text, attr=0):
    """Write text without crashing at terminal boundaries."""
    height, width = win.getmaxyx()

    if 0 <= y < height and 0 <= x < width:
        try:
            win.addnstr(y, x, str(text), max(0, width - x - 1), attr)
        except curses.error:
            pass


def draw_frame(stdscr, title):
    stdscr.erase()
    height, width = stdscr.getmaxyx()

    if height < 12 or width < 45:
        safe_addstr(
            stdscr, 1, 2,
            "Please enlarge your terminal to at least 45x12.",
            curses.A_BOLD,
        )
        safe_addstr(stdscr, 3, 2, "Press Q to quit.")
        stdscr.refresh()
        return False

    stdscr.attron(curses.color_pair(1))
    stdscr.box()
    stdscr.attroff(curses.color_pair(1))

    safe_addstr(
        stdscr, 1, 3, f" UNMEI // {title.upper()} ",
        curses.color_pair(1) | curses.A_BOLD,
    )

    safe_addstr(
        stdscr, height - 2, 2,
        " [UP/DOWN] Navigate   [ENTER] Select   [Q] Quit ",
        curses.color_pair(3),
    )

    return True


def draw_centered(stdscr, y, text, attr=0):
    _, width = stdscr.getmaxyx()
    x = max(2, (width - len(text)) // 2)
    safe_addstr(stdscr, y, x, text, attr)


def show_menu(stdscr):
    while True:
        if not draw_frame(stdscr, "Main Menu"):
            key = stdscr.getch()
            if key in (ord("q"), ord("Q")):
                return "Quit"
            continue

        # Load the ASCII art from your assets directory
        filepath = base_dir / "assets" / "ascii" / "intro_banner.txt"

        try:
            with filepath.open("r", encoding="utf-8") as file:
                lines = file.read().splitlines()
        except FileNotFoundError:
            lines = ["Main menu ASCII art not found."]

        height, width = stdscr.getmaxyx()
        start_y = max(3, (height - len(lines)) // 2)

        for i, line in enumerate(lines):
            if start_y + i >= height - 3:
                break

            x = max(1, (width - len(line)) // 2)
            safe_addstr(
                stdscr,
                start_y + i,
                x,
                line,
                curses.color_pair(1) | curses.A_BOLD,
            )

        stdscr.refresh()

        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            return "Quit"

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    setup_colors()

    choice = show_menu(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)


