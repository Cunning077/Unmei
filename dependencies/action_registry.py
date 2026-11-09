import gamefiles.theinn_funcs as c0s0001
import gamefiles.street_funcs as c0s0002

actions_dep = {
    "speak_0001": {
        "actions_name": ['Check List', 'Quit'],
        "action_btn": ['C', 'Q'],
        "function_file": c0s0001.speak0001
    },
    'puzzle_0001': {
        'actions_name': ['Check The Kist', 'Go To The Fireplace', 'Quit'],
        'action_btn': ['C', 'G', 'Q'],
        "function_file": c0s0001.puzzle0001
    },
    'speak_0002': {
        'actions_name': [''],
        "action_btn": [''],
        'function_file': c0s0001.speak0002
    },
    'battle_0001': {
        'actions_name': [''],
        'action_btn': [''],
        'function_file': c0s0002.battle0001
    },
    'speak_0003': {
        'actions_name': [''],
        'action_btn': [''],
        'function_file': c0s0002.speak0003
    }
}


