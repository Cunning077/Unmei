def createProgressionSaveTemp():
    sql = """
    INSERT INTO player_progression (
        player_id, health, max_health, stamina, max_stamina, attributes, talent_tree
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """ 
    return sql

def getProgressionTemp():
    sql = """
    SELECT player_lvl, curr_exp, health, max_health, stamina, max_stamina, attributes, talent_tree, talent_points, currency
    FROM player_progression
    WHERE player_id = %s;
    """
    return sql

def updateProgressionTemp():
    sql = """
    UPDATE player_progression
    SET
        player_lvl = %s,
        curr_exp = %s,
        health = %s,
        max_health = %s,
        stamina = %s,
        max_stamina = %s,
        attributes = %s,
        talent_tree = %s,
        talent_points = %s,
        currency = %s
    WHERE player_id = %s;
    """
    return sql
