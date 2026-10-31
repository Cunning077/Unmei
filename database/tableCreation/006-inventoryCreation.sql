USE unmei;

CREATE TABLE IF NOT EXISTS player_inventory (
    player_id CHAR(36) NOT NULL PRIMARY KEY,
    weapons JSON NOT NULL DEFAULT ('[]'),
    armor JSON NOT NULL DEFAULT ('[]'),
    spells JSON NOT NULL DEFAULT ('[]'),
    consumables JSON NOT NULL DEFAULT ('[]'),
    Speciality_items JSON NOT NULL DEFAULT ('[]'),
    player_loadout JSON NOT NULL DEFAULT ('{"weapon": "", "armor": "", "active_passives": []}'),

    FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
) ENGINE=InnoDB
