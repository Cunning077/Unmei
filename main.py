import curses
import time

from server.initConnection import initiate_connection
from server.loadScenes import LoadScenes
from server.battles import Battles
import server.orchestrator as Orch
import server.sessionHandler as sessionH
import utils.curses as cU

def main(stdscr):
    Scenes = LoadScenes(stdscr)

    Scenes.welcomeBoard()
    player_id, resp = initiate_connection(Scenes)
    Session = sessionH.initSession(player_id, resp, Scenes)
    #battle = Battles(Session.gameState, '0-0001', Scenes)
    #battle.start_battle()
    Orch.orchestrate_game(Session, Scenes)
  

if __name__ == "__main__":
    curses.wrapper(main)


