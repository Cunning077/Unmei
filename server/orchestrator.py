import time

def orchestrate_game(Session, Scenes):
    Scenes.render_scene(Session.gameState)
    time.sleep(20)
