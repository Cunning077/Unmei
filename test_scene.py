
import curses
from pathlib import Path

from imagetester import draw_image


BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "assets" / "art" / "dungeon.png"


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    try:
        curses.start_color()
        curses.use_default_colors()
    except curses.error:
        pass

    while True:
        stdscr.erase()

        height, width = stdscr.getmaxyx()

        # Upper half: artwork.
        art_height = height // 2 - 1
        art_width = width - 2

        draw_image(
            stdscr,
            IMAGE_PATH,
            top=1,
            left=1,
            max_width=art_width,
            max_height=art_height * 2,
        )

        # Lower half: dialogue and actions.
        dialogue_y = height // 2 + 1

        if dialogue_y < height - 3:
            stdscr.addstr(
                dialogue_y,
                2,
                "The ancient dungeon lies before you.",
            )

        if dialogue_y + 2 < height:
            stdscr.addstr(
                dialogue_y + 2,
                2,
                "[E] Enter dungeon    [Q] Quit",
            )

        stdscr.refresh()

        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            break

        # E is a placeholder for future scene-transition logic.
        if key in (ord("e"), ord("E")):
            break


if __name__ == "__main__":
    curses.wrapper(main)

