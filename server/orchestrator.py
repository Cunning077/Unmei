import time
from dependencies.gamestate_log import gamestage_subchapters
from dependencies.action_registry import actions_dep
import utils.curses as cU


def orchestrate_game(Session, Scenes):
    while True:
        gameStateInfo = Scenes.render_scene(Session.gameState)
        actions = gameStateInfo['actions']
        for i in range(len(actions)):
            while True:
                func_file = actions_dep[actions[i]]['function_file']
                if func_file is None:
                    return
                action_key, next_scene_pack = func_file(Scenes, Session.gameState)
                if action_key['status']:
                    #handle the next scene file
                    Scenes.render_next_scene(next_scene_pack)
                    break
