import curses
import textwrap
from PIL import Image

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

def centered_cords(height, o_h, width, o_w):
    x = (width - o_w) // 2
    y = (height - o_h) // 2
    return x, y

def debug_message(stdscr, message, row=0):
    height, width = stdscr.getmaxyx()

    if 0 <= row < height:
        stdscr.addnstr(row, 0, f"DEBUG: {message}", width - 1)
        stdscr.refresh()

def draw_text(window, y, x, text, max_width, style=0):
    height, width = window.getmaxyx()
    if y < 0 or y >= height or x <0 or x >= width:
        return
    available = min(max_width, width - x - 1)
    if available <= 0:
        return
    try:
        window.addnstr(y, x, str(text), available, style)
    except curses.error:
        pass

def draw_clear_panel(window, title):
    window.erase()
    window.box()
    height, width = window.getmaxyx()
    if width > len(title) + 4 and height >= 2:
        draw_text(window, 0, 2, f" {title }", width - 4, curses.A_BOLD,)

def draw_location(window, scene):
    draw_clear_panel(window, 'LOCATION')
    height, width = window.getmaxyx()
    lines = [
            scene.get("location", "ERR"),
            scene.get("sub_location", "ERR"),
            "",
            f"Region: {scene.get('region', 'ERR')}",
    ]
    for y, line in enumerate(lines, start=2):
        if y >= height - 1:
            break
        draw_text(window, y, 2, line, width - 4)
    window.noutrefresh()

def draw_attributes(window, attributes):
    draw_clear_panel(window, 'ATTRIBUTES')
    height, width = window.getmaxyx()
    y = 2
    for name, value in attributes.items():
        if y >= height - 1:
            break
        if isinstance(value, int):
            line = f"{name}: {value}"
            draw_text(window, y, 2, line, width - 4)
            y += 1
    window.noutrefresh()

def draw_description(window, description):
    draw_clear_panel(window, "SCENE DESCRIPTION")
    height, width = window.getmaxyx()
    wrapped = textwrap.wrap(
        str(description),
        width=max(1, width - 4),
    )
    for y, line in enumerate(wrapped, start=2):
        if y >= height - 1:
            break
        draw_text(window, y, 2, line, width - 4)
    window.noutrefresh()

def draw_action(window, actions):
    draw_clear_panel(window, "ACTIONS")
    height, width = window.getmaxyx()
    column_width = max(1, (width - 4) // 2)
    for index, val in enumerate(actions):
        row = 1 + index // 2
        column = 2 + (index % 2) * column_width
        if row >= height - 1:
            break
        draw_text(window, row, column,f"{val}", column_width-1,)
    window.noutrefresh()

def draw_image(stdscr, imagePath, top, left, max_width, max_height):
    with Image.open(imagePath) as source:
        image = source.convert("RGB")

    image_w, image_h = image.size

    if image_w == 0 or image_h == 0 or max_width <= 0 or max_height < 2:
        return

    scale = min(
        max_width / image_w,
        (max_height * 2) / image_h,
    )

    width = max(1, int(image_w * scale))
    height = max(2, int(image_h * scale))

    if height % 2:
        height -= 1

    if width < 1 or height < 2:
        return

    image = image.resize(
        (width, height),
        Image.Resampling.LANCZOS,
    )

    pixels = image.load()

    pair_ids = {}
    next_pair = 1
    max_pairs = curses.COLOR_PAIRS - 1

    def get_pair(fg, bg):
        nonlocal next_pair

        key = (fg, bg)

        if key in pair_ids:
            return pair_ids[key]

        if next_pair > max_pairs:
            return 0

        try:
            curses.init_pair(next_pair, fg, bg)
        except curses.error:
            return 0

        pair_ids[key] = next_pair
        next_pair += 1

        return pair_ids[key]

    for y in range(0, height, 2):
        screen_y = top + y // 2

        for x in range(width):
            r1, g1, b1 = pixels[x, y]
            r2, g2, b2 = pixels[x, y + 1]

            fg = rgb_to_256(r1, g1, b1)
            bg = rgb_to_256(r2, g2, b2)

            pair = get_pair(fg, bg)

            try:
                stdscr.addstr(
                    screen_y,
                    left + x,
                    "\u2580",
                    curses.color_pair(pair),
                )
            except curses.error:
                pass

    stdscr.noutrefresh()


def rgb_to_256(r, g, b):
    def channel(v):
        if v < 48:
            return 0
        if v < 115:
            return 1
        return min(5, (v - 35) // 40)

    if max(r, g, b) < 8:
        return 16

    if min(r, g, b) > 248:
        return 231

    return (
        16
        + 36 * channel(r)
        + 6 * channel(g)
        + channel(b)
    )

