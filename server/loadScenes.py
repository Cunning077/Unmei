import curses
import textwrap
from pathlib import Path
import time


from imagetester import BASE_DIR
import utils.curses as cU
import utils.auth as uA
from dependencies.gamestate_log import gamestage_subchapters

base_dir = Path(__file__).resolve().parent.parent

class LoadScenes:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        stdscr.keypad(True)
        cU.setup_colors()

    def welcomeBoard(self):
        stdscr = self.stdscr
        stdscr.clear()

        filepath = base_dir / "assets" / "ascii" / "intro_banner.txt"

        try:
            lines = filepath.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            lines = ["Welcome Menu not found"]
        height, width = stdscr.getmaxyx()
        start_y = max(3, (height - len(lines)) // 2)

        for i, line in enumerate(lines):
            if start_y + i >= height - 3:
                break

            x = max(1, (width - len(line)) // 2)
            cU.safe_addstr(
                stdscr,
                start_y + i,
                x,
                line,
                curses.color_pair(1) | curses.A_BOLD,
            )
        stdscr.refresh()

    def logcreateMenu(self):
        stdscr = self.stdscr
        options = ["Login", "Create Account", "Exit"]
        selected = 0

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            title = "UNMEI - ACCOUNT"

            message = [
                    "The SSH key isnt linked to a Unmei account.",
                    'Log in to link it to an existing account',
                    'Or create a new account to get started'
            ]

            stdscr.addstr(2, max(0, (width - len(title)) // 2), title,
                          curses.color_pair(1) | curses.A_BOLD)
            
            message_y = height // 2 - len(message) - 2
            for i, line in enumerate(message):
                x = max(0, (width - len(line)) // 2)
                stdscr.addstr(message_y + i, x, line)

            options_y = message_y + len(message) + 2

            for i, option in enumerate(options):
                y = options_y + i
                x = max(0, (width - len(option)) // 2)

                if i == selected:
                    stdscr.addstr(y, x, f"> {option}",
                                  curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addstr(y, x, f"  {option}")

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected = (selected - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected = (selected + 1) % len(options)
            elif key in (curses.KEY_ENTER, 10, 13):
                return options[selected].lower().replace(" ", "_")

    def createAccMenu(self):
        stdscr = self.stdscr
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        win_h = 19
        win_w = 54

        if height < win_h or width < win_w:
            stdscr.addstr(0,0, "Terminal to small. Please resize it.")
            stdscr.refresh()
            stdscr.getch()
        startX, startY = cU.centered_cords(height, win_h, width, win_w)
        win = curses.newwin(win_h, win_w, startY, startX)
        win.keypad(True)
        win.box()
        title = " UNMEI CREATE ACCOUNT"
        win.addstr(2, (win_w - len(title)) // 2, title,
                   curses.color_pair(1) | curses.A_BOLD)
        win.addstr(4, 4, "Username")
        win.addstr(7, 4, "Passphrase")
        win.addstr(10, 4, "Confirm Passphrase")
        win.addstr(14, 4, "Enter: continue | Esc: cancel",
               curses.A_DIM)
        win.refresh()
        win.addstr(5, 4, "> ")
        win.refresh()
        username = self.read_field(win, 5, 6, 32)
        isValid = uA.usernameValid(username)
        while not isValid:
            win.addstr(13,4, "Username is taken or missing", curses.color_pair(5) | curses.A_BOLD)
            win.refresh()
            username = self.read_field(win, 5, 6, 32)
            isValid = uA.usernameValid(username)
        win.move(13,4)
        win.clrtoeol()
        win.refresh()
        win.addstr(8, 4, "> ")
        win.refresh()
        passphrase = self.read_field(win, 8, 6, 128, masked=True)
        isValid = uA.checkIfEmpty(passphrase)
        while not isValid:
            win.addstr(13, 4, "Passphrase is left empty", curses.color_pair(5) | curses.A_BOLD)
            win.refresh()
            passphrase = self.read_field(win, 8, 6, 128, masked=True)
            isValid = uA.checkIfEmpty(passphrase)
        win.move(13, 4)
        win.clrtoeol()
        win.refresh()
        win.addstr(11, 4, "> ")
        win.refresh()
        conpassphrase = self.read_field(win, 11, 6, 128, masked=True)
        isValid = uA.checkIfEmpty(passphrase)
        while not isValid or conpassphrase.strip() != passphrase.strip(): 
            if conpassphrase != passphrase:
                win.addstr(13, 4, "Passwords dont match", curses.color_pair(5) | curses.A_BOLD)
                win.refresh()
            conpassphrase = self.read_field(win, 11, 6, 128, masked=True)
            isValid = uA.checkIfEmpty(conpassphrase)
        win.move(13, 4)
        win.clrtoeol()
        win.refresh()
        win.addstr(13, 4, "Creating your account...", curses.color_pair(4) | curses.A_BOLD)
        win.refresh()
        return username, passphrase

    def loginMenu(self):
        stdscr = self.stdscr
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        win_h = 16
        win_w = 54

        if height < win_h or width < win_w:
            stdscr.addstr(0,0, "Terminal to small. Please resize it.")
            stdscr.refresh()
            stdscr.getch()

        startX, startY = cU.centered_cords(height, win_h, width, win_w)
        win = curses.newwin(win_h, win_w, startY, startX)
        win.keypad(True)
        win.box()
        title = " UNMEI LOGIN "
        win.addstr(2, (win_w - len(title)) // 2, title,
               curses.color_pair(1) | curses.A_BOLD)
        win.addstr(4, 4, "Username")
        win.addstr(7, 4, "Passphrase")
        win.addstr(13, 4, "Enter: continue | Esc: cancel",
               curses.A_DIM)
        win.refresh()
        win.addstr(5, 4, "> ")
        win.refresh()
        username = self.read_field(win, 5, 6, 32)
        isValid = uA.checkIfEmpty(username)
        while not isValid:
            win.addstr(12,4, "Username is missing", curses.color_pair(5) | curses.A_BOLD)
            win.refresh()
            username = self.read_field(win, 5, 6, 32)
            isValid = uA.checkIfEmpty(username)
        win.move(12, 4)
        win.clrtoeol()
        win.refresh()
        win.addstr(8, 4, "> ")
        win.refresh()
        passphrase = self.read_field(win, 8, 6, 128, masked=True)
        isValid = uA.checkIfEmpty(passphrase)
        while not isValid:
            win.addstr(12, 4, "Passphrase is left empty", curses.color_pair(5) | curses.A_BOLD)
            win.refresh()
            passphrase = self.read_field(win, 8, 6, 128, masked=True)
            isValid = uA.checkIfEmpty(passphrase)
        win.move(12, 4)
        win.clrtoeol()
        win.refresh()
        win.addstr(12, 4, 'Logging you in...', curses.color_pair(4) | curses.A_BOLD)
        win.refresh()
        return username, passphrase



    def read_field(self, win, y, x, max_length, masked=False):
        value = ""

        curses.curs_set(1)

        while True:
            win.move(y, x)
            win.clrtoeol()
            displayed = "*" * len(value) if masked else value
            win.addnstr(y, x, displayed, max_length)
            win.move(y, x + len(value))
            win.refresh()

            key = win.getch()

            if key in (10, 13, curses.KEY_ENTER):
                break

            if key == 27:  # Escape
                curses.curs_set(0)
                return None

            if key in (curses.KEY_BACKSPACE, 127, 8):
                value = value[:-1]

            elif 32 <= key <= 126 and len(value) < max_length:
                value += chr(key)

        curses.curs_set(0)
        return value

    def render_scene(self, gameState):
        min_width = 72
        min_height = 20
        description_h = 5
        actions_h = 5

        stdscr = self.stdscr
        stdscr.clear()
        stdscr.refresh()
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        if width < min_width or height < min_height:
            message = (
                f"Terminal too small ({width}x{height}). "
                f"Resize to at least {min_width}x{min_height}."
            )
            cU.draw_text(stdscr,height // 2,1,
                      message,max(1, width - 2),curses.A_BOLD,
            )
            stdscr.refresh()
            return

        content_y = 0
        left_width = width // 4
        right_width = width // 4
        center_width = width - left_width - right_width
        content_height = (
                height
                - description_h
                - actions_h
        )
        description_y = content_y + content_height
        actions_y = description_y + description_h
        gameStageParts = gameState['gamestage'].split('-')
        chapter = gameStageParts[0]
        subchapter = gameStageParts[1]
        loc_name = gamestage_subchapters[chapter][subchapter]['name']
        loc_packet = {
            'location': loc_name,
            'sub_location': '',
            'region': ''
        }
        location_win = curses.newwin(content_height, left_width, content_y, 0)
        center_win = curses.newwin(content_height, center_width, content_y, left_width)
        attributes_win = curses.newwin(content_height, right_width, content_y, left_width + center_width)
        cU.draw_location(location_win, loc_packet)

        cU.draw_attributes(attributes_win, gameState['attributes'])
        cU.draw_clear_panel(center_win, "SCENE ART")
        image_name = gamestage_subchapters[chapter][subchapter]['imagepath']
        imagePath = base_dir / 'assets' / 'art' / image_name
        if imagePath:
            try:
                cU.draw_image(center_win, imagePath, top=1, left=1, max_width=center_width - 2, max_height=content_height - 2,)
            except (OSError, ValueError) as error:
                cU.draw_text(
                    center_win,
                    2,
                    2,
                    f"Could not load image: {error}",
                    center_width - 4,
                )
        center_win.noutrefresh()

                

        description_win = curses.newwin(description_h, width, description_y, 0,)
        actions_win = curses.newwin(actions_h, width, actions_y, 0,)
        cU.draw_description = (description_win, gamestage_subchapters[chapter][subchapter]['desc'])
        cU.draw_action(actions_win, ['talk', 'open door'])
        curses.doupdate()


        
