def createInventorySaveTemp():
    sql = """
    INSERT INTO player_inventory (
        player_id    
    )
    VALUES (%s)
    """
    return sql

def getInventoryTemp():
    sql = """
    SELECT weapons, armor, spells, consumables, Speciality_items, player_loadout
    FROM player_inventory
    WHERE player_id = %s;
    """
    return sql

def updateInventoryTemp():
    sql = """
    UPDATE player_inventory
    SET
        weapons = %s,
        armor = %s,
        spells = %s,
        consumables = %s,
        Speciality_items = %s, 
        player_loadout = %s
    WHERE player_id = %s
    """
    return sql

