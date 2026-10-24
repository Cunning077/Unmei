import utils.curses as cU
import utils.gen as gen
import dependencies.action_registry as ar

from pathlib import Path
import time
import textwrap
import curses

base_dir = Path(__file__).resolve().parent.parent

def speak0001(Scenes, gameState):
    action_key = {
            'status': False,
            'action_id': 'speak0001',
            'next_scene_pack': None,
            'state_changed': None
    }
    stdscr = Scenes.stdscr
    key = stdscr.getch()
    match chr(key):
        case "c":
            message = textwrap.dedent("""
                By the gods, my memory grows more treacherous by the day…
                I cannot for the life of me recall when this list was given unto me.
                No matter. Let us see what remains to be done before I retire for the night.

                Tonight's Duties

                - Obtain the list of tasks appointed for the morrow.
                - Bank the fire in the main quarters, lest the hearth grow cold before dawn.
                - Answer nature's call.
                - Wash my hands and face, and rid myself of the day's grime.
                - Extinguish all candles before retiring.

                There. A simple enough set of duties. Surely even my failing memory cannot betray me to forget.
            """)
            dialogue_packet = {'message': message, 'btns': ['Close List', 'Quit'], 'btn_keys': ['C', 'Q']}
            Scenes.dialogue_scene(dialogue_packet)
            key = stdscr.getch()
            match chr(key):
                case "c":
                    action_key['status'] = True
                    next_scene_pack = {
                            'location': {'location': 'The Inn',
                                'sub_location': '',
                                'region': ''
                            },
                            'attributes': gameState['attributes'],
                            'imagepath': 'innBedroom.jpeg',
                            'desc': 'Well i best get on with the nights task',
                            'actions': ar.actions_dep['puzzle_0001']['actions_name'],
                            'action_btn': ar.actions_dep['puzzle_0001']['action_btn']
                    }
                    return action_key, next_scene_pack
                case "q":
                    gen.globalQuit()
        
        case 'q':
            gen.globalQuit()

def render_scene(Scenes, image_name, message, actions, act_btns):
    image_path = base_dir / "assets" / "art" / image_name

    act_packet = {
        "actions": actions,
        "act_btn": act_btns
    }

    cU.change_imDescActScene(
        Scenes, image_path, message, act_packet
    )

def puzzle0001(Scenes, gameState):
    action_key = {
            'status': False,
            'action_id': 'speak0001',
            'state_changed': None
    }
    stdscr = Scenes.stdscr
    message1 = """
        Ahh, yes... now I remember. There was an opening for a position at the library.Though my memory has begun to fail me, I haven't forgotten the history of this great land.
        The powerful magicians and the kings they swore to protect... the noble knights who fought tooth and nail for control and dominion. Ah, what a grand history it is.
    """
    message2 = """
        My trusty pocket watch... a gift from Madam. Madam never approved of her, but Elenoire always saw me for who I truly was. And though Madam has always been there for me,
        I could never forget Elenoire. That's why I keep her picture tucked away inside... a little piece of her that time can never take from me.
    """
    message3 = """
        There is the list, what would i do without it? I dare not think. Now, I'd best hurry,
        with an interview to attend first thing in the morning. Wouldn't do to arrive half-asleep, now would it?
    """
    kisk_items = {
        'letter': {
            'image': 'puzzle0001Kistvar1.png',
            'message': message1,
            'actions': ['Put Back', 'Look Somewhere Else', 'Quit'],
            'action_btns': ['C', 'E', 'Q']
        },
        'pocket_watch': {
            'image': 'puzzle0001Kistvar3.png', 
            'message': message2,
            'actions': ['Put Back', 'Look Somewhere Else', 'Quit'],
            'action_btns': ['C', 'E', 'Q']
        },
        'list': {
            'image': 'puzzle0001Kistvar2.png',
            'message': message3,
            'actions': ['Close The Kist', 'Quit'],
            'action_btns': ['C', 'Q']
        }
    }
    kist_stage_message = """
        I really must learn to pack lighter. Every journey becomes twice as difficult with all this baggage... 
        I only hope I haven't forgotten the list Madam gave me. Though, if I'm being honest, I've already forgotten what I came here for.
    """
    found_kisk_item = []
    all_items_found = False
    in_bedroom = True
    has_rake = False
    fireplace_comp = False
    while True:
        key = stdscr.getch()
        match chr(key):
            case 'c' if not all_items_found:
                in_bedroom = False
                image_name =  'puzzle0001Kist.png'
                imagePath = base_dir / 'assets' / 'art' / image_name
                actions = ['Look In Kist', 'Look Somewhere Else', 'Quit']
                act_btns = ['L', 'E', 'Q']
                act_packet = {'actions': actions, 'act_btn': act_btns}
                message = kist_stage_message
                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                key = stdscr.getch()
                match chr(key):
                    case 'l':
                        for item, detail in kisk_items.items():
                            if item in found_kisk_item:
                                continue
                            image_name = detail['image']
                            imagePath = base_dir / 'assets' / 'art' / image_name
                            actions = detail['actions']     
                            act_btns = detail['action_btns']
                            act_packet = {'actions': actions, 'act_btn': act_btns}
                            message = detail['message']
                            cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                            kist_stage_message = """
                                Well that wasn't what I was looking for, I best keep looking.
                            """
                            found_kisk_item.append(item)
                            if all_items_found and fireplace_comp:
                                break
                            break
                        all_items_found = len(found_kisk_item) == len(kisk_items)
                    case 'e' if not fireplace_comp and not all_items_found:
                        in_bedroom = True
                        image_name = 'innBedroom.jpeg'
                        imagePath = base_dir / 'assets' / 'art' / image_name
                        actions = ['Check The Kist', 'Go To The Fireplace', 'Quit']
                        act_btns = ['C', 'G', 'Q']
                        act_packet = {'actions': actions, 'act_btn': act_btns}
                        message = """
                           Well I best get on with the night's task's 
                        """
                        cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                        continue

                    case 'e' if fireplace_comp and not all_items_found:
                        in_bedroom = True
                        image_name = 'innBedroom.jpeg'
                        imagePath = base_dir / 'assets' / 'art' / image_name
                        actions = ['Check The Kist', 'Quit']
                        act_btns = ['C', 'Q']
                        act_packet = {'actions': actions, 'act_btn': act_btns}
                        message = """
                           Well I best get on with the night's task's 
                        """
                        cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                        continue

                    case 'e' if not fireplace_comp and all_items_found:
                        in_bedroom = True
                        image_name = 'innBedroom.jpeg'
                        imagePath = base_dir / 'assets' / 'art' / image_name
                        actions = ['Go To The Fireplace', 'Quit']
                        act_btns = ['G', 'Q']
                        act_packet = {'actions': actions, 'act_btn': act_btns}
                        message = """
                           Well I best get on with the night's task's 
                        """
                        cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                        continue
                    case 'q':
                        gen.globalQuit()

                    case _:
                        continue
            case 'c' if all_items_found and not fireplace_comp:
                in_bedroom = True
                image_name = 'innBedroom.jpeg'
                imagePath = base_dir / 'assets' / 'art' / image_name
                actions = ['Go To The Fireplace', 'Quit']
                act_btns = ['G', 'Q']
                act_packet = {'actions': actions, 'act_btn': act_btns}
                message = """
                    I Best get on the the other tasks
                """
                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
            case 'c' if all_items_found and fireplace_comp:
                break
            case 'e' if not in_bedroom and fireplace_comp and not all_items_found:
                in_bedroom = True
                image_name = 'innBedroom.jpeg'
                imagePath = base_dir / 'assets' / 'art' / image_name
                actions = ['Check The Kist', 'Quit']
                act_btns = ['C', 'Q']
                act_packet = {'actions': actions, 'act_btn': act_btns}
                message = """
                    Well I best get on with the night's task's 
                """
                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                continue
            case 'e' if not in_bedroom or not fireplace_comp and not all_items_found:
                in_bedroom = True
                image_name = 'innBedroom.jpeg'
                imagePath = base_dir / 'assets' / 'art' / image_name
                actions = ['Check The Kist', 'Go To Fireplace', 'Quit']
                act_btns = ['C', 'G', 'Q']
                act_packet = {'actions': actions, 'act_btn': act_btns}
                message = """
                    Well I best get on with the night's task's 
                """
                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                continue
            case 'e' if not in_bedroom or all_items_found and not fireplace_comp:
                in_bedroom = True
                image_name = 'innBedroom.jpeg'
                imagePath = base_dir / 'assets' / 'art' / image_name
                actions = ['Go To Fireplace', 'Quit']
                act_btns = ['G', 'Q']
                act_packet = {'actions': actions, 'act_btn': act_btns}
                message = """
                    Well I best get on with the night's task's 
                """
                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                continue
            case 'g' if not has_rake and not fireplace_comp:
                in_bedroom = False
                image_name = 'puzzle0001fire.png'
                imagePath = base_dir / 'assets' / 'art' / image_name
                actions = ['Take Ash Rake', 'Exit Fireplace', 'Q']
                act_btns = ['T', 'E', 'Q']
                act_packet = {'actions': actions, 'act_btn': act_btns}
                message = """
                    I'd best bank the fire before the night is through. Wouldn't do to have the whole town go up in flames on my account... 
                    Now, where on earth do they keep that ash rake?
                """
                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                key = stdscr.getch()
                match chr(key):
                    case 't':
                        has_rake = True
                        image_name = 'puzzle0001firevar1.png'
                        imagePath = base_dir / 'assets' / 'art' / image_name
                        actions = ['Bank Fire', 'Exit Fireplace', 'Quit']
                        act_btns = ['B', 'E', 'Q']
                        act_packet = {'actions': actions, 'act_btn': act_btns}
                        message = """
                            Best not dally any longer. I'd best see this task through and be done with it.
                        """
                        cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                        key = stdscr.getch()
                        match chr(key):
                            case 'b':
                                image_name = 'puzzle0001firevar2.png'
                                imagePath = base_dir / 'assets' / 'art' / image_name
                                actions = ['Exit Fireplace', 'Quit']
                                act_btns = ['E', 'Q']
                                act_packet = {'actions': actions, 'act_btn': act_btns}
                                message = """
                                    Well I best get on with the night's task's 
                                """
                                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                                fireplace_comp = True
                                if fireplace_comp and all_items_found:
                                    break

                            case 'e' if not fireplace_comp and not all_items_found:
                                in_bedroom = True
                                image_name = 'innBedroom.jpeg'
                                imagePath = base_dir / 'assets' / 'art' / image_name
                                actions = ['Check The Kist', 'Go To The Fireplace', 'Quit']
                                act_btns = ['C', 'G', 'Q']
                                act_packet = {'actions': actions, 'act_btn': act_btns}
                                message = """
                                   Well I best get on with the night's task's 
                                """
                                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                                continue

                            case 'e' if fireplace_comp and not all_items_found:
                                in_bedroom = True
                                image_name = 'innBedroom.jpeg'
                                imagePath = base_dir / 'assets' / 'art' / image_name
                                actions = ['Check The Kist', 'Quit']
                                act_btns = ['C', 'Q']
                                act_packet = {'actions': actions, 'act_btn': act_btns}
                                message = """
                                   Well I best get on with the night's task's 
                                """
                                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                                continue

                            case 'e' if not fireplace_comp and all_items_found:
                                in_bedroom = True
                                image_name = 'innBedroom.jpeg'
                                imagePath = base_dir / 'assets' / 'art' / image_name
                                actions = ['Go To The Fireplace', 'Quit']
                                act_btns = ['G', 'Q']
                                act_packet = {'actions': actions, 'act_btn': act_btns}
                                message = """
                                   Well I best get on with the night's task's 
                                """
                                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                                continue
                            case 'e' if all_items_found and fireplace_comp:
                                break
                            case 'q':
                                gen.globalQuit()
                            case _:
                                continue
                    case 'e' if not all_items_found and not fireplace_comp:
                        in_bedroom = True
                        image_name = 'innBedroom.jpeg'
                        imagePath = base_dir / 'assets' / 'art' / image_name
                        actions = ['Check The Kist', 'Go To Fireplace', 'Quit']
                        act_btns = ['C', 'G', 'Q']
                        act_packet = {'actions': actions, 'act_btn': act_btns}
                        message = """
                            Well I best get on with the night's task's 
                        """
                        cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                    case 'e' if all_items_found:
                        in_bedroom = True
                        image_name = 'innBedroom.jpeg'
                        imagePath = base_dir / 'assets' / 'art' / image_name
                        actions = ['Go To Fireplace', 'Quit']
                        act_btns = ['G', 'Q']
                        act_packet = {'actions': actions, 'act_btn': act_btns}
                        message = """
                            Well I best get on with the night's task's 
                        """
                        cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                        continue
                    case 'q':
                        gen.globalQuit()
                    case _:
                        continue
            case 'g' if has_rake:
                in_bedroom = False
                image_name = 'puzzle0001firevar1.png'
                imagePath = base_dir / 'assets' / 'art' / image_name
                actions = ['Bank Fire', 'Exit Fireplace', 'Q']
                act_btns = ['B', 'E', 'Q']
                act_packet = {'actions': actions, 'act_btn': act_btns}
                message = """
                    Best not dally any longer. I'd best see this task through and be done with it.
                """
                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
            case 'b':
                image_name = 'puzzle0001firevar2.png'
                imagePath = base_dir / 'assets' / 'art' / image_name
                actions = ['Exit Fireplace', 'Quit']
                act_btns = ['E', 'Q']
                act_packet = {'actions': actions, 'act_btn': act_btns}
                message = """
                    Well I best get on with the night's task's 
                """
                cU.change_imDescActScene(Scenes, imagePath, message, act_packet)
                fireplace_comp = True
                if fireplace_comp and all_items_found:
                    break
            case 'q':
                gen.globalQuit()
            case _:
                continue
    message = """
        Now to wash these hands. I’ve no wish to fall ill over such a trivial matter. Hm… lavender soap. Eleanor’s favourite scent. She always did love it so.
        I remember how her eyes would light up whenever I brought her fresh bales of it from the market… Ah, those were kinder days.
    """
    message2 = """
        I’ve no cause to return here once I’m gone. Best see to the candles,
        snuff out the lights, and leave this place in darkness. No sense wasting good wax.
    """
    washroom_stages = {
        0: {
            'message': "There lies the privy, let's not waste time",
            'bmessage': "I best find a privy soon, lest nature's call becomes a unfortunate burden.", 
            'action': ['Use The Privy', 'Quit'],
            'act_btns': ['U', 'Q'],
            'image': 'innWashroom.png'
        },
        1: {
            'message': message,
            'bmessage': 'Should clean these filthy hands',
            'action': ['Clean Yourselve', 'Quit'],
            'act_btns': ['C', 'Q'],
            'image': 'innWashroom.png' 
        },
        2: {
            'message': message2,
            'bmessage': "I shouldn't waste wax",
            'action': ['Blow Candle Out', 'Quit'],
            'act_btns': ['B', 'Q'],
            'image': 'innWashroom.png'
        },
        3: {
            'message': 'Sleep is calling my name, I shall see myself to slumber',
            'action': ['Go To Bedroom', 'Quit'],
            'act_btns': ['G', 'Q'],
            'image': 'innWashroomvar1.png'
        }
    }
    washroom_stage = 0
    scene = "bedroom"

    def show_bedroom():
        image = 'innBedroom.jpeg'
        actions = ['Go To Washroom', 'Quit']
        btns = ['W', 'Q']
        message = washroom_stages[washroom_stage]['bmessage']
        render_scene(Scenes, image, message, actions, btns)

    def show_washroom():
        image = washroom_stages[washroom_stage]['image']
        message = washroom_stages[washroom_stage]['message']
        action = washroom_stages[washroom_stage]['action']
        btns = washroom_stages[washroom_stage]['act_btns']
        render_scene(Scenes, image, message, action, btns)


    while True:
        match scene:
            case 'bedroom':
                show_bedroom()
            case 'washroom':
                show_washroom()

        key = chr(stdscr.getch())
        match (scene, key, washroom_stage):
            case (_, 'q', _):
                gen.globalQuit()

            case ('bedroom', 'w', _):
                scene = 'washroom'
            case ('washroom', 'u', 0):
                washroom_stage = 1
            case ('washroom', 'c', 1):
                washroom_stage = 2
            case ('washroom', 'b', 2):
                washroom_stage = 3
            case ('washroom', 'g', 3):
                break

    image = 'innBedroom.jpeg'
    actions = ['Blow Out Candle', 'Quit']
    btns = ['B', 'Q']
    message = """
        Whew… these chores have worn me down something fierce. Best snuff the candles, draw the room into darkness, and retire to my bed.     
    """
    render_scene(Scenes, image, message, actions, btns) 
    key = chr(stdscr.getch())
    match key:
        case 'b':
            stdscr.erase()
            stdscr.refresh()
            time.sleep(20)


