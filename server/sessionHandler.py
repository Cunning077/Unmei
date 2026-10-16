import server.DbWriter as Writer
import utils.curses as cU
import time

class Session:
    def __init__(self, player_id, init_packet):
        self.player_id = player_id 
        self.gameState = init_packet

def initSession(player_id, resp, Scenes):
    #this function is gonna decide what happened during init connection - 
    # and it main job is to pull world state info, this is where it will be stored
    match resp:
        case "create_account":
            gameState = Writer.init_save(player_id)
            session = Session(player_id, gameState)
            return session

        case 'login':
            gameState = Writer.load_save(player_id)
            session = Session(player_id, gameState)
            return session
        case 'ssh':
            gameState = Writer.load_save(player_id)
            session = Session(player_id, gameState)
            return session


