USE unmei;

CREATE TABLE IF NOT EXISTS world_state (
    player_id CHAR(36) NOT NULL PRIMARY KEY,
    gamestage VARCHAR(8) NOT NULL,
    location_id VARCHAR(9) NOT NULL DEFAULT ('[]'),
    coordinates VARCHAR(8) NOT NULL DEFAULT ('[]'),
    discovered_locations JSON NOT NULL DEFAULT ('[]'),
    activated_mechanisms JSON NOT NULL DEFAULT ('[]'),
    def_unique_enemies JSON NOT NULL DEFAULT ('[]'),
    short_fasttravel JSON NOT NULL DEFAULT ('[]'),

    FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;
