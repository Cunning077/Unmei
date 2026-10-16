import database.sql_scripts.progressionTemps as pTemps
import database.sql_scripts.worldStateTemps as wTemps
import database.conn as dbconn
import utils.gen as gen 

import json

def init_save(player_id):
    health = 5
    maxhealth = 5
    attributes = {'fortitude': 1}
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
    save_packet = {
            'health': health,
            'maxhealth': maxhealth,
            'attributes': attributes,
            'gamestage': gamestage,
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
            'location_id': wp[1],
            'cordinates': wp[2],
            'discovered_locations': json.loads(wp[3]),
            'activated_mechanisms': json.loads(wp[4]),
            'unique_enemies': json.loads(wp[5]),
            'short_fasttravel': json.loads(wp[6])
    }
    return save_packet
