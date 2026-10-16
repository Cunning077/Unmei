def createNewAccountTemp():
    sql = """
    INSERT INTO players (
        username,
        passphrase_hash
    )
    VALUES (%s,%s)
    """
    return sql

def authenticateAccountWithIdTemp():
    sql = """
    SELECT username, passphrase_hash, account_status
    FROM players
    WHERE player_id = %s;
    """
    return sql

def authenticateAccountWithUserTemp():
    sql = """
    SELECT player_id, passphrase_hash, account_status
    FROM players
    WHERE username = %s;
    """
    return sql

def searchForUsernameTemp():
    sql = """
    SELECT username
    FROM players
    WHERE username = %s;
    """
    return sql

def getuseridTemp():
    sql = """
    SELECT player_id
    FROM players
    WHERE username = %s;
    """
    return sql
