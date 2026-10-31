import time
from dependencies.gamestate_log import gamestage_subchapters, next_subchapter_key
from dependencies.action_registry import actions_dep
import utils.curses as cU
import server.DbWriter as dbw


def orchestrate_game(Session, Scenes):
    while True:
        gameStateInfo = Scenes.render_scene(Session.gameState)
        actions = gameStateInfo['actions']
        completed_reqs = []
        for i in range(len(actions)):
            func_file = actions_dep[actions[i]]['function_file']
            if func_file is None:
                return
            action_key = func_file(Scenes, Session.gameState)
            if action_key['status']:
                #handle the next scene file
                    for change in action_key['next_action']:
                        match change:
                            case 'renderScene':
                                Scenes.render_next_scene(action_key['next_scene_pack'])
                            case 'reqChange':
                                completed_reqs.append(action_key['state_changed']['req'])
                            case 'updateGamestate':
                                Session.gameState = action_key['gameState']

        requirements = gameStateInfo['reqs']
        cU.debug_message(Scenes.stdscr, str(completed_reqs))
        for req in requirements:
            cU.debug_message(Scenes.stdscr, str(req))
            if req not in completed_reqs:
                cU.debug_message(Scenes.stdscr, 'nope')
                return 
        next_subchapter = next_subchapter_key[Session.gameState['gamestage']]
        Session.gameState['gamestage'] = next_subchapter
        dbw.update_save(Session.player_id, Session.gameState)
        # time to save all gamestate
        

