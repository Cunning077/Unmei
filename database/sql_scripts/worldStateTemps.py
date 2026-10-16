def createWorldStateSaveTemp():
    sql = """
    INSERT INTO world_state (
        player_id, gamestage
    )
    VALUES (%s, %s);
    """
    return sql

def getWorldStateTemp():
    sql = """
    SELECT gamestage, location_id, coordinates, discovered_locations, activated_mechanisms,
        def_unique_enemies, short_fasttravel
    FROM world_state
    WHERE player_id = %s;
    """
    return sql

def updateWorldStateTemp():
    sql = """
    UPDATE world_state 
    SET
        gamestage = %s,
        location_id = %s,
        coordinates = %s,
        discovered_locations = %s, 
        activated_mechanisms = %s,
        def_unique_enemies = %s,
        short_fasttravel = %s
    WHERE player_id = %s;
    """
    return sql
