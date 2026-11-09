battle_actions = {
    'home': {
        'actions': ['Attacks', 'Defense', 'Items', 'Spells', 'Quit'],
        'action_btns': ['A', 'D', 'I', 'S', 'Q']
    },
    'attacks': {
        'actions': ['Quick-Attack', 'Light-Attack', 'Heavy-Attack', 'Back', 'Quit'],
        'action_btns': ['K', 'L', 'H', 'B', 'Q']
    },
    'defense': {
        'actions': ['Guard', 'Ward', 'Evade', 'Brace', 'Parry', 'Back', 'Quit'],
        'action_btns': ['G', 'W', 'E', 'R', 'P', 'B', 'Q']
    }
}

attack_types = {
    'quick-physical': {
        'multiple': 0.9,
        'penetrate': 0.7,
        'stamina_cost': 5
    },
    'light-physical': {
        'multiple': 1.1,
        'penetrate': 0.4,
        'stamina_cost': 10
    },
    'heavy-physical': {
        'multiple': 1.5,
        'penetrate': 0,
        'stamina_cost': 20
    }
}

enemy_attack_types = {
    'melee-slow': ['calculated_attack', 'impatient_attack', 'general_attack']
}

eat_trans = {
    'calculated_attack': {
        'time': 10,
        'multiple': 1.5,
        'penetrate': 0.7,
        'types': ['physical']
    },
    'impatient_attack': {
        'time': 4,
        'multiple': 0.9,
        'penetrate': 0,
        'types': ['physical', 'parryable']
    },
    'general_attack': {
        'time': 7,
        'multiple': 1.1,
        'penetrate': 0.4,
        'types': ['physical']
    }
}

defense_trans = {
    'guard': {
        'stamina_cost': 5,
        'damage_reduction': 0.2,
        'types': ['all']
    },
    'ward': {
        'stamina_cost': 15,
        'damage_reduction': 1,
        'types': ['magical']
    },
    'evade': {
        'stamina_cost': 10,
        'agility_bonus': 0.5,
        'dodge_bonus': 0.1,
        'types': ['all']
    },
    'brace': {
        'stamina_cost': 15,
        'damage_reduction': 0.5,
        'types': ['physical']
    },
    'parry': {
        'stamina_cost': 10,
        'parry_chance': 0.8,
        'types': ['parryable'],
        'counter': 'quick-physical'
    }
}

spell_dict = {
    'cleave': {
        'name': 'Cleave',
        'description': 'Add a 10% attack bonus to next attack',
        'mana_cost': 10,
        'target': 'self',
        'effects': [
            {
                'type': 'damage_buff',
                'boost': 0.25
            }
        ]
    }
}
