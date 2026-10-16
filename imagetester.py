import curses
import textwrap
from pathlib import Path
from PIL import Image
import time


# ============================================================
# IMAGE RENDERER
# ============================================================

def draw_image(stdscr, image_path, top, left, max_width, max_height):
    """
    Render a PNG using colored terminal half-block characters.
    Each terminal character represents two vertically stacked pixels.
    The original image is never modified.
    """
    with Image.open(image_path) as source:
        image = source.convert("RGB")

    image_width, image_height = image.size

    if image_width == 0 or image_height == 0:
        return

    scale = min(
        max_width / image_width,
        (max_height * 2) / image_height,
    )

    width = max(1, int(image_width * scale))
    height = max(2, int(image_height * scale))

    if height % 2:
        height -= 1

    if width < 1 or height < 2:
        return

    image = image.resize(
        (width, height),
        Image.Resampling.LANCZOS,
    )
    pixels = image.load()

    try:
        curses.start_color()
        curses.use_default_colors()
    except curses.error:
        return

    def rgb_to_256(r, g, b):
        """Approximate an RGB color using the xterm-256 palette."""
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

    # Reuse color pairs when the same combination appears.
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
                    "\u2580",  # Upper half-block: ▀
                    curses.color_pair(pair),
                )
            except curses.error:
                # Ignore terminal boundary and unsupported-character errors.
                pass


# ============================================================
# LAYOUT SETTINGS
# ============================================================

HEADER_HEIGHT = 3
DESCRIPTION_HEIGHT = 5
ACTIONS_HEIGHT = 5

MIN_WIDTH = 72
MIN_HEIGHT = 20


# ============================================================
# SHARED DRAWING HELPERS
# ============================================================

def draw_text(window, y, x, text, max_width, style=0):
    """Draw text without writing beyond the window."""
    height, width = window.getmaxyx()

    if y < 0 or y >= height or x < 0 or x >= width:
        return

    available = min(max_width, width - x - 1)

    if available <= 0:
        return

    try:
        window.addnstr(y, x, str(text), available, style)
    except curses.error:
        pass


def draw_panel(window, title):
    """Clear a window and draw its border and title."""
    window.erase()
    window.box()

    height, width = window.getmaxyx()

    if width > len(title) + 4 and height >= 2:
        draw_text(
            window,
            0,
            2,
            f" {title} ",
            width - 4,
            curses.A_BOLD,
        )


# ============================================================
# INDIVIDUAL PANELS
# ============================================================

def draw_header(window, title):
    draw_panel(window, "UNMEI")

    height, width = window.getmaxyx()

    if height > 1:
        draw_text(
            window,
            1,
            2,
            title,
            width - 4,
            curses.A_BOLD,
        )

    window.noutrefresh()


def draw_location(window, scene):
    draw_panel(window, "LOCATION")

    height, width = window.getmaxyx()

    lines = [
        scene.get("location", "Unknown"),
        scene.get("sub_location", ""),
        "",
        f"Region: {scene.get('region', 'Unknown')}",
    ]

    for y, line in enumerate(lines, start=2):
        if y >= height - 1:
            break

        draw_text(window, y, 2, line, width - 4)

    window.noutrefresh()


def draw_attributes(window, attributes):
    draw_panel(window, "ATTRIBUTES")

    height, width = window.getmaxyx()
    y = 2

    for name, value in attributes.items():
        if y >= height - 1:
            break

        if isinstance(value, tuple) and len(value) == 2:
            current, maximum = value
            line = f"{name}: {current}/{maximum}"
        else:
            line = f"{name}: {value}"

        draw_text(window, y, 2, line, width - 4)
        y += 1

    window.noutrefresh()


def draw_description(window, description):
    draw_panel(window, "SCENE DESCRIPTION")

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


def draw_actions(window, actions):
    draw_panel(window, "ACTIONS")

    height, width = window.getmaxyx()
    column_width = max(1, (width - 4) // 2)

    for index, (key, label) in enumerate(actions):
        row = 1 + index // 2
        column = 2 + (index % 2) * column_width

        if row >= height - 1:
            break

        draw_text(
            window,
            row,
            column,
            f"[{key.upper()}] {label}",
            column_width - 1,
        )

    window.noutrefresh()


# ============================================================
# COMPLETE SCENE LAYOUT
# ============================================================

def render_layout(stdscr, scene):
    """Render all panels and the scene image."""
    stdscr.erase()

    height, width = stdscr.getmaxyx()

    if width < MIN_WIDTH or height < MIN_HEIGHT:
        message = (
            f"Terminal too small ({width}x{height}). "
            f"Resize to at least {MIN_WIDTH}x{MIN_HEIGHT}."
        )

        draw_text(
            stdscr,
            height // 2,
            1,
            message,
            max(1, width - 2),
            curses.A_BOLD,
        )

        stdscr.refresh()
        return

    # Calculate layout dimensions from the terminal size.
    content_y = HEADER_HEIGHT

    left_width = width // 4
    right_width = width // 4
    center_width = width - left_width - right_width

    content_height = (
        height
        - HEADER_HEIGHT
        - DESCRIPTION_HEIGHT
        - ACTIONS_HEIGHT
    )

    description_y = content_y + content_height
    actions_y = description_y + DESCRIPTION_HEIGHT

    # Header.
    header = curses.newwin(HEADER_HEIGHT, width, 0, 0)

    draw_header(
        header,
        scene.get("title", "The Forgotten Realm"),
    )

    # Main content panels.
    location_win = curses.newwin(
        content_height,
        left_width,
        content_y,
        0,
    )

    center_win = curses.newwin(
        content_height,
        center_width,
        content_y,
        left_width,
    )

    attributes_win = curses.newwin(
        content_height,
        right_width,
        content_y,
        left_width + center_width,
    )

    draw_location(location_win, scene)

    draw_attributes(
        attributes_win,
        scene.get("attributes", {}),
    )

    # Center panel: scene art.
    draw_panel(center_win, "SCENE ART")

    image_path = scene.get("image")

    if image_path:
        try:
            draw_image(
                center_win,
                image_path,
                top=1,
                left=1,
                max_width=center_width - 2,
                max_height=content_height - 2,
            )
        except (OSError, ValueError) as error:
            draw_text(
                center_win,
                2,
                2,
                f"Could not load image: {error}",
                center_width - 4,
            )

    center_win.noutrefresh()

    # Full-width description and action panels.
    description_win = curses.newwin(
        DESCRIPTION_HEIGHT,
        width,
        description_y,
        0,
    )

    actions_win = curses.newwin(
        ACTIONS_HEIGHT,
        width,
        actions_y,
        0,
    )

    draw_description(
        description_win,
        scene.get("description", ""),
    )

    draw_actions(
        actions_win,
        scene.get("actions", []),
    )

    curses.doupdate()


# ============================================================
# TEST SCENE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

SCENE = {
    "title": "The Forgotten Realm",
    "location": "Ashen Forest",
    "sub_location": "Northern Trail",
    "region": "Eldoria",
    "image": str(BASE_DIR / "assets" / "art" / "img2.png"),
    "attributes": {
        "Health": (80, 100),
        "Stamina": (60, 100),
        "Level": 3,
        "Gold": 125,
    },
    "description": (
        "A narrow trail winds between ancient trees. "
        "Something moves beyond the mist."
    ),
    "actions": [
        ("w", "Move forward"),
        ("e", "Interact"),
        ("i", "Inventory"),
        ("q", "Quit prototype"),
    ],
}


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    description = SCENE["description"]

    while True:
        current_scene = {
            **SCENE,
            "description": description,
        }

        render_layout(stdscr, current_scene)
        time.sleep(30)




if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception:
        import traceback

        traceback.print_exc()
        input("\nPress Enter to exit...")
