import bcrypt

import database.sql_scripts.playerAuthTemp as paTemp
import database.conn as dbconn

def usernameValid(username):
    if username is None or not username.strip():
        return False
    username = username.strip()
    conn, cursor = dbconn.gen_cursor('reader')
    sql = paTemp.searchForUsernameTemp()
    try:
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        if row:
            return False
        return True
    except Exception:
        raise
    finally:
        dbconn.kill_cursor(conn, cursor)

def checkIfEmpty(string):
    if string is None or not string.strip():
        return False
    return True

def verify_passphrase(plain_password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        stored_hash.encode("utf-8")
    )

def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf-8")
    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(rounds=12)
    )
    return hashed.decode("utf-8")
