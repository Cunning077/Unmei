def createNewConnectionTemp():
    sql = """
    INSERT INTO ssh_keys(
        player_id,
        public_key,
        key_fingerprint,
        key_label
    )
    VALUES (%s, %s, %s, %s);
    """
    return sql

def validateConnectionTemp():
    sql = """
    SELECT player_id
    FROM ssh_keys
    WHERE key_fingerprint = %s
    """
    return sql


