import os
import subprocess
from pathlib import Path
import time

import database.sql_scripts.playerAuthTemp as paTemp
import database.sql_scripts.sshSessionTemps as sshTemps
from utils.auth import verify_passphrase, hash_password
import utils.curses as uC
import database.conn as dbconn


def initiate_connection(Scenes):
    public_key, fingerprint = inspect_ssh_identity()
    player_id = settleConnection(fingerprint)
    if not player_id:
        response = Scenes.logcreateMenu()
        with open("/tmp/unmei_debug.log", "a") as log:
            log.write("after logincreate menu\n")

        player_id = authResponseMenu(response, Scenes)
        with open("/tmp/unmei_debug.log", "a") as log:
            log.write("after account auth\n")

        gen_ssh_save(player_id, public_key, fingerprint)
        with open("/tmp/unmei_debug.log", "a") as log:
            log.write("create ssh save\n")

        return player_id, response
        #when fingerprint is empty
    #now i have to get username, passphrase_filename, passphrase_hash
    username, passphrase_hash, passphrase_filename = fetchPlayerById(player_id)
    if username is None:
        #this shouldnt happen due to db rules so will purge player_id
        return None
    return player_id, 'ssh'

def authResponseMenu(response, Scenes):
    match response:
        case "login":
            username, passphrase = Scenes.loginMenu()
            resp, user_id = loginUserbyUser(username, passphrase)
            if resp:
                return user_id
        case 'create_account':
            username, passphrase = Scenes.createAccMenu()
            if createUser(username, passphrase):
                user_id = get_user_id(username)
                if user_id:
                    return user_id

def inspect_ssh_identity():
    auth_path = os.environ.get("SSH_USER_AUTH")
    if not auth_path:
        return None, None
    auth_file = Path(auth_path)
    if not auth_file.is_file():
        return None, None
    for line in auth_file.read_text().splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0].startswith("publickey") and parts[1].startswith("ssh-"):
            public_key = f"{parts[1]} {parts[2]}"
            results = subprocess.run(
                    ['ssh-keygen', '-lf', '-'],
                    input=public_key + "\n",
                    capture_output=True,
                    text=True,
                    check=True
            )
            fingerprint = results.stdout.split()[1]
            return public_key, fingerprint
    return None, None

def settleConnection(fingerprint):
    conn, cursor = dbconn.gen_cursor('reader')
    sql = sshTemps.validateConnectionTemp()
    try:
        cursor.execute(sql, (fingerprint,))
        row = cursor.fetchone()
        if row is None:
            return None
        #at this point account has passed ssh auth
        return row[0]
    except Exception as e:
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)

def fetchPlayerById(player_id):
    conn, cursor = dbconn.gen_cursor('reader')
    sql = paTemp.authenticateAccountWithIdTemp()
    try:
        cursor.execute(sql, (player_id,))
        row = cursor.fetchone()
        if row is None:
            return None, None, None
        return row[0], row[1], row[2]
    except Exception as e:
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)

def loginUserbyUser(username, passphrase):
    conn, cursor = dbconn.gen_cursor('reader')
    sql = paTemp.authenticateAccountWithUserTemp()
    try:
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        if row is None:
            return False
        if row[2] == 'active':
            stored_hash = row[1]
            if verify_passphrase(passphrase, stored_hash):
                return True, row[0]
        return False
    except Exception as e:
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)
    
def createUser(username, passphrase):
    conn, cursor = dbconn.gen_cursor('writer')
    sql = paTemp.createNewAccountTemp()
    hashed = hash_password(passphrase)
    try:
        cursor.execute(sql, (username, hashed))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)

def get_user_id(username):
    conn, cursor = dbconn.gen_cursor('reader')
    sql = paTemp.getuseridTemp()
    try:
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        if row is None:
            return None
        return row[0]
    except Exception as e:
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)

def gen_ssh_save(player_id, public_key, fingerprint):
    conn, cursor = dbconn.gen_cursor('writer')
    sql = sshTemps.createNewConnectionTemp()
    try:
        cursor.execute(sql, (player_id, public_key, fingerprint, ''))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        dbconn.kill_cursor(conn, cursor)
