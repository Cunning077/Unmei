import time
import textwrap

from server.battles import Battles



def battle0001(Scenes, gamestate):
    action_key = {
        'status': False,
        'action_id': 'battle0001',
        'next_action': ['reqChange', 'updateGamestate'],
        'state_changed': None
    }
    while True:
        battle = Battles(gamestate, '0-0001', Scenes)
        result = battle.start_battle()
        match result['result']:
            case 'lose':
                continue
            case "win":
                action_key['status'] = True
                action_key['state_changed'] = {'req': 'battle0001'}
                action_key['gameState'] = result['gamestate']
                break
    return action_key

def speak0003(Scenes, gamestate):
    action_key = {
        'status': False,
        'action_id': 'speak0003',
        'next_action': [],
        'state_changed': []
    }
    stdscr = Scenes.loc_window
    message = textwrap.dedent("""
        By the gods! Never have I witnessed such a magnificent display of strength!
        The manner in which you wielded that rake reminded me of Kratos himself, the Ghost of Sparta!
    """
    )
    dialogue_packet = {
        'message': message,
        'btns': ['Oh Well Thanks', 'Quit'],
        'btn_keys': ['T', 'Q'],
        'image': 'k1.png'
    }
    Scenes.dialogue_scene(dialogue_packet)
    key = stdscr.getch()
    match chr(key):
        case 't':
            message = textwrap.dedent("""
                Forgive me, good sir! I've been rambling on without so much as offering my name. Hugh, Hugh is the name!
                I serve at the Leatherwork Mission, where I've spent the better part of five years as an apprentice,
                learning the trade beneath my master's watchful eye. Five years, mind you! And still, I'm paid by the cent!
                My dear wife has long pleaded with me to seek employment elsewhere, but I reckon honest toil and a little patience will see a man through most hardships.
            """)

