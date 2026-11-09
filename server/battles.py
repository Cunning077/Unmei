import curses
import curses.panel
import time
import random

from dependencies.entity_registry import entities
import dependencies.battle_deps as bd
import utils.curses as cU 
import utils.gen as gen

class Battles:
    def __init__(self, character_packet, entity_id, Scenes):
        self.Scenes = Scenes
        self.character_packet = character_packet
        self.chHealth = character_packet['health'] 
        self.chMaxHealth = character_packet['max_health']
        self.chStamina = character_packet['stamina']
        self.chMaxStamina = character_packet['max_stamina']
        self.playerLoadout = character_packet['player_loadout']
        self.strength = character_packet['attributes']['strength']
        self.agility = character_packet['attributes']['agility']
        self.intelligence = character_packet['attributes']['intelligence']
        self.criticalAttack = character_packet['attributes']['critical_attack']
        self.criticalChance = character_packet['attributes']['critical_chance']
        self.fortitude = character_packet['attributes']['fortitude']
        self.dexterity = character_packet['attributes']['dexterity']
        self.endurance = character_packet['attributes']['endurance']
        self.heroAttributes = character_packet['attributes']
        self.chSpells = character_packet['spells']
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
        self.popupTexts = enemy_packet['popup_texts']

    def start_battle(self):
        enemy_attack_types = bd.enemy_attack_types[self.enemyAttackStyle]
        choice = random.choice(enemy_attack_types) 
        self.next_enemy_attack = time.monotonic() + bd.eat_trans[choice]['time']
        times = {'time-to-attack': self.next_enemy_attack, 'tot_time': self.next_enemy_attack}
        self.init_battle(times)
        action_win = self.Scenes.battle_actions_window
        attack_menu = 'home'
        self.selected_attack = {'name': '', 'btn': ''}
        self.selected_defense = {'name': '', 'btn': ''}
        action_win.timeout(100)
        #pauseing
        self.paused = False
        self.pause_battle()
        popup_packet = {
            'texts': self.popupTexts 
        }
        popup, panels = self.Scenes.create_popup(popup_packet)
        while True:
            key = popup.getch()
            match key:
                case 10 | 13 | curses.KEY_ENTER:
                    panels.hide()
                    curses.panel.update_panels()
                    curses.doupdate()
                    break
                case _:
                    pass
        self.resume_battle()
        while True:
            if self.chHealth <= 0:
                return {'result': 'lose'}
            if self.enemyCurrHealth <= 0:
                self.character_packet['health'] = self.chHealth
                self.character_packet['stamina'] = self.chStamina
                return {'result': 'win', 'gamestate': self.character_packet}
            match attack_menu:
                case 'home':
                    cU.draw_selected_action(
                        action_win,
                        bd.battle_actions[attack_menu]['actions'],
                        bd.battle_actions[attack_menu]['action_btns'],
                        None
                    )
                    curses.doupdate()
                case 'attacks':
                    cU.draw_selected_action(
                        action_win,
                        bd.battle_actions[attack_menu]['actions'],
                        bd.battle_actions[attack_menu]['action_btns'],
                        self.selected_attack['btn']
                    )
                    curses.doupdate()
                case 'defense':
                    cU.draw_selected_action(
                        action_win,
                        bd.battle_actions[attack_menu]['actions'],
                        bd.battle_actions[attack_menu]['action_btns'],
                        self.selected_defense['btn']
                    )
                    curses.doupdate()
            key = action_win.getch()
            if key != -1:
                key = chr(key)
                match (attack_menu, key):
                    case (_, 'q'):
                        gen.globalQuit()
                    case ('home', 'a'):
                        attack_menu = 'attacks'
                    case ('home', 'd'):
                        attack_menu = 'defense'
                    case ('attacks', 'k'):
                        req_stamina = bd.attack_types['quick-physical']['stamina_cost']
                        if self.check_stamina(self.chStamina, req_stamina):
                            self.selected_attack['name'] = 'quick-physical'
                            self.selected_attack['btn'] = 0
                    case ('attacks', 'l'):
                        req_stamina = bd.attack_types['light-physical']['stamina_cost']
                        if self.check_stamina(self.chStamina, req_stamina):
                            self.selected_attack['name'] = 'light-physical'
                            self.selected_attack['btn'] = 1
                    case ('attacks', 'h'):
                        req_stamina = bd.attack_types['heavy-physical']['stamina_cost']
                        if self.check_stamina(self.chStamina, req_stamina):
                            self.selected_attack['name'] = 'heavy-physical'
                            self.selected_attack['btn'] = 2
                    case ('attacks', 'b'):
                        attack_menu = 'home'
                    case ('defense', 'g'):
                        req_stamina = bd.defense_trans['guard']['stamina_cost']
                        if self.check_stamina(self.chStamina, req_stamina):
                            self.selected_defense['name'] = 'guard'
                            self.selected_defense['btn'] = 0
                    case ('defense', 'w'):
                        req_stamina = bd.defense_trans['ward']['stamina_cost']
                        if self.check_stamina(self.chStamina, req_stamina):
                            self.selected_defense['name'] = 'ward'
                            self.selected_defense['btn'] = 1
                    case ('defense', 'e'):
                        req_stamina = bd.defense_trans['evade']['stamina_cost']
                        if self.check_stamina(self.chStamina, req_stamina):
                            self.selected_defense['name'] = 'evade'
                            self.selected_defense['btn'] = 2
                    case ('defense', 'r'):
                        req_stamina = bd.defense_trans['brace']['stamina_cost']
                        if self.check_stamina(self.chStamina, req_stamina):
                            self.selected_defense['name'] = 'brace'
                            self.selected_defense['btn'] = 3
                    case ('defense', 'p'):
                        req_stamina = bd.defense_trans['parry']['stamina_cost']
                        if self.check_stamina(self.chStamina, req_stamina):
                            self.selected_defense['name'] = 'parry'
                            self.selected_defense['btn'] = 4

                    case ('defense', 'b'):
                        attack_menu = 'home'

            current_time = time.monotonic()
            time_to_attack = self.next_enemy_attack - current_time
            enemy_status_pack = {
                'curr_time': time_to_attack, 
                'tot_time': bd.eat_trans[choice]['time']
            }
            cU.draw_enemy_status(self.Scenes.enemy_status_window, enemy_status_pack)
            self.Scenes.enemy_status_window.noutrefresh()
            curses.doupdate()
            if current_time >= self.next_enemy_attack:
                if self.selected_attack['name']:
                    self.player_attack(self.selected_attack['name'])
                    self.selected_attack = {'name': '', 'btn': ''}
                    cU.draw_selected_action(
                        action_win,
                        bd.battle_actions[attack_menu]['actions'],
                        bd.battle_actions[attack_menu]['action_btns'],
                        None
                    )
                enemy_dmg = self.settleDefense(choice, self.selected_defense['name'])
                self.selected_defense = {'name': None, 'btn': ''}
                self.enemy_attack(enemy_dmg)
                choice = random.choice(enemy_attack_types) 
                self.next_enemy_attack += bd.eat_trans[choice]['time']

    def getEnemyPacket(self, entity_id):
        return entities[entity_id]

    def set_attack(self, attack, actions, act_btns):
        actions_win = self.Scenes.battle_actions_window
        cU.draw_selected_action(actions_win, actions, act_btns, attack['btn'])
        curses.doupdate()
        self.selected_attack = attack

    def settleDefense(self, enemy_attack, defense):
        if defense:
            types = bd.defense_trans[defense]['types']
            attack_types = bd.eat_trans[enemy_attack]['types']
            self.chStamina -= bd.defense_trans[defense]['stamina_cost']
            match defense:
                case 'guard':
                    enemy_dmg = self.calc_enemy_dmg(enemy_attack)
                    reduction = bd.defense_trans[defense]['damage_reduction']
                    enemy_dmg *= (1 - reduction)
                    return int(enemy_dmg)
                case 'ward':
                    pass
                case 'evade':
                    prev_agility = self.agility
                    self.agility = self.agility + (self.agility * bd.defense_trans[defense]['agility_bonus'])
                    enemy_dmg = self.calc_enemy_dmg(enemy_attack)
                    return enemy_dmg
                case 'brace':
                    if any(Type in types for Type in attack_types):
                        enemy_dmg = self.calc_enemy_dmg(enemy_attack)
                        reduction = bd.defense_trans[defense]['damage_reduction']
                        enemy_dmg *= (1-reduction)
                        return int(enemy_dmg)
                    else:
                        return self.calc_enemy_dmg(enemy_attack)
                case 'parry':
                    if 'parryable' in attack_types:
                        if random.random() < bd.defense_trans[defense]['parry_chance']:
                            self.player_attack('quick-physical')
                            return 0
                        else:
                            return self.calc_enemy_dmg(enemy_attack)
                    else:
                        return self.calc_enemy_dmg(enemy_attack)
        else:
            return self.calc_enemy_dmg(enemy_attack)

    def init_battle(self, times):
        init_battle_pack = {
            'enemy_info': {
                'enemy_name': self.enemyName,
                'current_health': self.enemyCurrHealth,
                'max_health': self.enemyMaxHealth,
                'enemy_type': self.enemyType,
                'attack_style': self.enemyAttackStyle,
                'enemy_lvl': self.enemyLvl
            },
            'enemy_status_pack': {
                'curr_time': times['time-to-attack'],
                'tot_time': times['tot_time']
            },
            'imagepath': self.battleImage,
            'hero_info': {
                'health': self.chHealth,
                'max_health': self.chMaxHealth,
                'stamina': self.chStamina,
                'max_stamina': self.chMaxStamina,
                'mana': 10,
                'max_mana': 10,
                'attributes': self.heroAttributes
            },
            'actions': ['Attacks', 'Defense', 'Items', 'Spells', 'Quit'],
            'action_btns': ['A', 'D', 'I', 'S', 'Q'],
            'desc': self.enemyDesc  
        }
        self.Scenes.battle_scene(init_battle_pack)

    def player_attack(self, attack_type):
        player_dmg = self.calc_playerdmg(attack_type)
        self.enemyCurrHealth = self.enemyCurrHealth - player_dmg
        self.chStamina -= bd.attack_types[attack_type]['stamina_cost']
        enemy_info_window = self.Scenes.enemy_info_window
        enemy_info_pack = {
            'enemy_name': self.enemyName,
            'current_health': self.enemyCurrHealth,
            'max_health': self.enemyMaxHealth,
            'enemy_type': self.enemyType,
            'attack_style': self.enemyAttackStyle,
            'enemy_lvl': self.enemyLvl
        }
        cU.draw_enemy_info(enemy_info_window, enemy_info_pack)
        enemy_info_window.noutrefresh()
        curses.doupdate()

    def check_stamina(self, stamina, req_stamina):
        return stamina >= req_stamina

    def enemy_attack(self, enemy_dmg):
        self.chHealth = self.chHealth - enemy_dmg
        hero_info_window = self.Scenes.hero_info_window
        hero_info_pack = {
            'health': self.chHealth,
            'max_health': self.chMaxHealth,
            'stamina': self.chStamina,
            'max_stamina': self.chMaxStamina,
            'mana': 10,
            'max_mana': 10,
            'attributes': self.heroAttributes
        }
        cU.draw_character_info(hero_info_window, hero_info_pack)
        hero_info_window.noutrefresh()
        curses.doupdate()


    def calc_playerdmg(self, attack_type):
        attack_multiple = bd.attack_types[attack_type]['multiple']
        weapon_damage = 1
        strength_damage = self.heroAttributes['strength'] * 2
        tot_dmg = (weapon_damage + strength_damage) * attack_multiple
        enemy_dodge = self.enemyAgility * 0.01
        player_penetration = bd.attack_types[attack_type]['penetrate']
        enemy_dodge = enemy_dodge - (enemy_dodge * player_penetration)
        tot_dmg = int(tot_dmg - (tot_dmg * enemy_dodge))
        return tot_dmg

    def calc_enemy_dmg(self, attack_type):
        attack_multiple = bd.eat_trans[attack_type]['multiple']
        weapon_damage = 1
        strength_damage = self.enemyStrength * 2
        tot_dmg = (weapon_damage + strength_damage) * attack_multiple
        player_dodge = self.agility * 0.01
        enemy_penetration = bd.eat_trans[attack_type]['penetrate']
        player_dodge = player_dodge - (player_dodge * enemy_penetration)
        tot_dmg = int(tot_dmg - (tot_dmg * player_dodge))
        return tot_dmg

    def pause_battle(self):
        if not self.paused:
            self.paused = True
            self.pause_start = time.monotonic()

    def resume_battle(self):
        if self.paused:
            paused_duration = time.monotonic() - self.pause_start
            self.next_enemy_attack += paused_duration
            self.paused = False

