import curses
import textwrap
from PIL import Image
import time



def setup_colors():
    curses.start_color()

    with open("/tmp/unmei_colors.log", "w") as log:
        log.write(f"Can change colors: {curses.can_change_color()}\n")
        log.write(f"Available colors: {curses.COLORS}\n")
        log.write(f"Color pairs: {curses.COLOR_PAIRS}\n")

    if curses.can_change_color() and curses.COLORS > 11:
        curses.init_color(10, 1000, 1000, 1000)  # White
        curses.init_color(11, 0, 0, 0)            # Black
        curses.init_pair(3, 10, 11)               # White on black
    else:
        curses.init_pair(
            3,
            curses.COLOR_WHITE,
            curses.COLOR_BLACK
        )



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

def centered_cords(height, obj_h, width, obj_w):
    x = (width - obj_w) // 2
    y = (height - obj_h) // 2
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
        draw_text(window, 0, 2, f" {title } ", width - 4, curses.A_BOLD,)

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

def draw_typing(window, y, x, text, delay):
    for char in text:
        window.addstr(y, x, char)
        window.refresh()
        time.sleep(delay)
        x += 1

def draw_description(window, description, title):
    draw_clear_panel(window, title)
    height, width = window.getmaxyx()
    paragraphs = description.splitlines()
    y=1
    for paragraph in paragraphs:
        if not paragraph.strip():
            y += 1
            continue

        lines = textwrap.wrap(
            paragraph.strip(),
            width=max(1, width - 4)
        
        )
        for line in lines:
            if y >= height - 1:
                break
            draw_typing(window, y, 2, line,  0.001) #0.02)
            y += 1
        if y >= height - 1:
            break
    window.noutrefresh()

def draw_action(window, actions, actions_btn):
    draw_clear_panel(window, "ACTIONS")
    height, width = window.getmaxyx()
    column_width = max(1, (width - 4) // 2)
    for index, val in enumerate(actions):
        row = 1 + index // 2
        column = 2 + (index % 2) * column_width
        if row >= height - 1:
            break
        draw_text(window, row, column,f"[{actions_btn[index]}] {val}", column_width-1,)
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
        Image.Resampling.LANCZOS
    )

    # Center the image inside the available area
    offset_x = max(0, (max_width - width) // 2)
    offset_y = max(0, (max_height - height // 2) // 2)

    left += offset_x
    top += offset_y

    pixels = image.load()

    pair_ids = {}
    next_pair = 4
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

def draw_bar(window, y, x, current, maximum, width, color):
    if maximum <= 0:
        ratio = 0
    else:
        ratio = max(0, min(1, current / maximum))
    filled = int(ratio * width)
    empty = width - filled
    window.addstr(y, x, "█" * filled, color)
    window.addstr(y, x + filled, "░" * empty)

def draw_enemy_info(window, enemy_info_pack):
    draw_clear_panel(window, 'ENEMY INFO')
    height, width = window.getmaxyx()
    size_enemy_col1 = len(enemy_info_pack['enemy_name'])
    column_width = max(1, (width-4) // 2)
    draw_text(window, 1, 2, enemy_info_pack['enemy_name'], column_width)
    draw_bar(window, 1, column_width + 2, enemy_info_pack['current_health'], enemy_info_pack['max_health'], column_width, curses.color_pair(3))
    draw_text(window, 2, 1, '-' * width, width)
    draw_text(window, 3, 2, 'Enemy Type', column_width)
    draw_text(window, 3, column_width + 2, enemy_info_pack['enemy_type'], column_width)
    draw_text(window, 4, 1, '-' * width, width)
    draw_text(window, 5, 2, 'Attack Style', column_width)
    draw_text(window, 5, column_width + 2, enemy_info_pack['attack_style'], column_width)

    draw_text(window, 7, 2, 'Enemy Lvl', column_width)
    draw_text(window, 7, column_width + 2, enemy_info_pack['enemy_lvl'], column_width)

def draw_enemy_status(window, enemy_status_pack):
    draw_clear_panel(window, 'ENEMY STATUS')
    height, wdith = window.getmaxyx()
    #not sure what to do yet for this

def draw_character_info(window, hero_info_pack):
    draw_clear_panel(window, 'HERO INFO')
    height, width = window.getmaxyx()
    column_width = max(1, (width-4) // 2)
    draw_text(window, 1, 2, 'Health', column_width)
    draw_bar(window, 2, 3, hero_info_pack['health'], hero_info_pack['max_health'], column_width, curses.color_pair(3))
    draw_text(window, 4, 2, 'Mana', column_width)
    draw_bar(window, 5, 3, hero_info_pack['mana'], hero_info_pack['max_mana'], column_width, curses.color_pair(3))
    i = 1
    col_gap = int(column_width * 0.33)
    for name, val in hero_info_pack['attributes'].items():
        draw_text(window, i, column_width + col_gap, f'{name}: {val}', column_width)
        i += 1

def change_imDescActScene(Scenes, imagePath, message, action_packet):
    image_win = Scenes.image_window
    image_win.erase()
    height, width = image_win.getmaxyx()
    draw_clear_panel(image_win, "SCENE ART")
    draw_image(image_win, imagePath, 1, 1, width - 2, height - 2)
    image_win.noutrefresh()
    action_win = Scenes.actions_window
    action_win.erase()
    draw_clear_panel(action_win, 'ACTIONS')
    draw_action(action_win, action_packet['actions'], action_packet['act_btn'])
    action_win.noutrefresh()
    desc_win = Scenes.desc_window
    desc_win.erase()
    draw_description(desc_win, message, 'DESCRIPTION')
    desc_win.noutrefresh()
    curses.doupdate()

def changeDesc(Scenes, message, title):
    desc_win = Scenes.desc_window
    desc_win.erase()
    draw_description(desc_win, message, title)
    desc_win.noutrefresh()
    curses.doupdate()

def changeActs(Scenes, act_packet):
    act_win = Scenes.actions_window
    act_win.erase()
    draw_clear_panel(act_win, 'ACTIONS')
    draw_action(act_win, act_packet['actions'], act_packet['act_btns'])
    act_win.noutrefresh()
    curses.doupdate()

def inspect_window(window, name="window"):
    height, width = window.getmaxyx()

    with open("/tmp/unmei_screen_inspect.log", "a") as log:
        log.write(f"\n--- {name} ---\n")
        log.write(f"Dimensions: {height}x{width}\n")

        for y in range(height):
            try:
                line = window.instr(y, 0, width - 1)
                log.write(f"{y:03}: {line!r}\n")
            except curses.error as exc:
                log.write(f"{y:03}: ERROR {exc}\n")
