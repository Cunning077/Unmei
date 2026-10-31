import database.sql_scripts.progressionTemps as pTemps
import database.sql_scripts.worldStateTemps as wTemps
import database.sql_scripts.inventoryTemps as iTemps
import database.conn as dbconn
import utils.gen as gen 

import json

def init_save(player_id):
    health = 5
    maxhealth = 5
    attributes = {
        'strength': 3,
        'agility': 1,
        'intelligence': 0,
        'critical_attack': 0,
        'critical_chance': 0,
        'fortitude': 3,
        'dexterity': 5
    }
    clean_attributes = gen.listToJSON(attributes)
    talent_tree = {'wip': 'wip'}
    ctalent_tree = gen.listToJSON(talent_tree)
    conn, cursor = dbconn.gen_cursor('writer')
    sql = pTemps.createProgressionSaveTemp()
    try:
        cursor.execute(sql, (player_id, health, maxhealth, clean_attributes, ctalent_tree))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)
    gamestage = '0-0001'

    conn, cursor = dbconn.gen_cursor('writer')
    sql = wTemps.createWorldStateSaveTemp()
    try:
        cursor.execute(sql, (player_id, gamestage))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)
    conn, cursor = dbconn.gen_cursor('writer')
    sql = iTemps.createInventorySaveTemp()
    try:
        cursor.execute(sql, (player_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)
    save_packet = {
            'player_lvl': 1,
            'curr_exp': 0,
            'health': health,
            'max_health': maxhealth,
            'attributes': attributes,
            'talent_tree': talent_tree,
            'talent_points': 0,
            'currency': 0,      
            'gamestage': gamestage,
            'location_id': [],
            'coordinates': [],
            'discovered_locations': [],
            'activated_mechanisms': [],
            'unique_enemies': [],
            'short_fasttravel': [],
            'weapons': [],
            'armor': [],
            'spells': [],
            'consumables': [],
            'speciality_items': [],
            'player_loadout': {'weapon':'', 'armor':'', 'active_passives': []},
    }
    return save_packet

def load_save(player_id):
    conn, cursor = dbconn.gen_cursor('reader')
    sql = pTemps.getProgressionTemp()
    try:
        cursor.execute(sql, (player_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        pp = row
    except Exception as e:
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)

    conn, cursor = dbconn.gen_cursor('reader')
    sql = wTemps.getWorldStateTemp()
    try:
        cursor.execute(sql, (player_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        wp = row
    except Exception as e:
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)
    conn, cursor = dbconn.gen_cursor('reader')
    sql = iTemps.getInventoryTemp()
    try:
        cursor.execute(sql, (player_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        ip = row
    except Exception as e:
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)

    save_packet = {
            'player_lvl': pp[0],
            'curr_exp': pp[1],
            'health': pp[2],
            'max_health': pp[3],
            'attributes': json.loads(pp[4]),
            'talent_tree': json.loads(pp[5]),
            'talent_points': pp[6],
            'currency': pp[7],
            'gamestage': wp[0],
            'location_id': json.loads(wp[1]),
            'coordinates': json.loads(wp[2]),
            'discovered_locations': json.loads(wp[3]),
            'activated_mechanisms': json.loads(wp[4]),
            'unique_enemies': json.loads(wp[5]),
            'short_fasttravel': json.loads(wp[6]),
            'weapons': json.loads(ip[0]),
            'armor': json.loads(ip[1]),
            'spells': json.loads(ip[2]),
            'consumables': json.loads(ip[3]),
            'speciality_items': json.loads(ip[4]),
            'player_loadout': json.loads(ip[5])

    }
    return save_packet

def update_save(player_id, gameState):
    sql = pTemps.updateProgressionTemp()
    conn, cursor = dbconn.gen_cursor('writer')

    try:
        cursor.execute(sql, (
            gameState['player_lvl'],
            gameState['curr_exp'],
            gameState['health'],
            gameState['max_health'],
            json.dumps(gameState['attributes']),
            json.dumps(gameState['talent_tree']),
            gameState['talent_points'],
            gameState['currency'],
            player_id
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)
    conn, cursor = dbconn.gen_cursor('writer')
    sql = wTemps.updateWorldStateTemp()
    try:
        cursor.execute(sql, (
            gameState['gamestage'],
            json.dumps(gameState['location_id']),
            json.dumps(gameState['coordinates']),
            json.dumps(gameState['discovered_locations']),
            json.dumps(gameState['activated_mechanisms']),
            json.dumps(gameState['unique_enemies']),
            json.dumps(gameState['short_fasttravel']),
            player_id
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)
    conn, cursor = dbconn.gen_cursor('writer')
    sql = iTemps.updateInventoryTemp()
    try:
        cursor.execute(sql, (
            json.dumps(gameState['weapons']),
            json.dumps(gameState['armor']),
            json.dumps(gameState['spells']),
            json.dumps(gameState['consumables']),
            json.dumps(gameState['speciality_items']),
            json.dumps(gameState['player_loadout']),
            player_id
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)

    

