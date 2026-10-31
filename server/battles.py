import curses

from dependencies.entity_registry import entities
from dependencies.action_registry import battle_actions
import dependencies.battle_deps as bd
import utils.curses as cU 
import utils.gen as gen

class Battles:
    def __init__(self, character_packet, entity_id, Scenes):
        self.Scenes = Scenes
        self.chHealth = character_packet['health'] 
        self.chMaxHealth = character_packet['max_health']
        self.playerLoadout = character_packet['player_loadout']
        self.strength = character_packet['attributes']['strength']
        self.agility = character_packet['attributes']['agility']
        self.intelligence = character_packet['attributes']['intelligence']
        self.criticalAttack = character_packet['attributes']['critical_attack']
        self.criticalChance = character_packet['attributes']['critical_chance']
        self.fortitude = character_packet['attributes']['fortitude']
        self.dexterity = character_packet['attributes']['dexterity']
        self.heroAttributes = character_packet['attributes']
        enemy_packet = self.getEnemyPacket(entity_id)
        self.battleImage = enemy_packet['image']
        self.enemyName = enemy_packet['name']
        self.enemyType = enemy_packet['type']
        self.enemyAttackStyle = enemy_packet['attack_style']
        self.enemyLvl = enemy_packet['lvl']
        self.enemyMaxHealth = enemy_packet['health']
        self.enemyCurrHealth = enemy_packet['health']
        self.enemyMaxMana = enemy_packet['mana']
        self.enemyCurrMana = enemy_packet['mana']
        self.enemyStrength = enemy_packet['strength']
        self.enemyAgility = enemy_packet['agility']
        self.enemyCriticalAttack = enemy_packet['critical_attack']
        self.enemyCriticalChance = enemy_packet['critical_chance']
        self.enemyDexterity = enemy_packet['dexterity']
        self.enemyDesc = enemy_packet['desc']

    def start_battle(self):
        self.init_battle()
        action_win = self.Scenes.battle_actions_window
        attack_menu = 'home'
        while True:
            match attack_menu:
                case 'home' | 'attacks':
                    cU.draw_action(
                        action_win,
                        battle_actions[attack_menu]['actions'],
                        battle_actions[attack_menu]['action_btns']
                    )
                    curses.doupdate()
            key = chr(action_win.getch())
            with open('/tmp/unmei_battle.log', 'a') as f:
                f.write(f"Menu: {attack_menu}, Key: {repr(key)}\n")
            match (attack_menu, key):
                case (_, 'q'):
                    gen.globalQuit()
                case ('home', 'a'):
                    attack_menu = 'attacks'
                case ('attacks', 'b'):
                    attack_menu = 'home'



    def getEnemyPacket(self, entity_id):
        return entities[entity_id]

    def init_battle(self):
        init_battle_pack = {
            'enemy_info': {
                'enemy_name': self.enemyName,
                'current_health': self.enemyCurrHealth,
                'max_health': self.enemyMaxHealth,
                'enemy_type': self.enemyType,
                'attack_style': self.enemyAttackStyle,
                'enemy_lvl': self.enemyLvl
            },
            'imagepath': self.battleImage,
            'hero_info': {
                'health': self.chHealth,
                'max_health': self.chMaxHealth,
                'mana': 10,
                'max_mana': 10,
                'attributes': self.heroAttributes
            },
            'actions': ['Attacks', 'Defense', 'Items', 'Spells', 'Quit'],
            'action_btns': ['A', 'D', 'I', 'S', 'Q'],
            'desc': self.enemyDesc  
        }
        self.Scenes.battle_scene(init_battle_pack)

    def calc_dmg(attack_type, attributes, player_loadout):
        attack_multiple = bd.attack_types[attack_type]['multiple']
        weapon_damage = 1
        strength_b = attributes['strength'] * 2
        
