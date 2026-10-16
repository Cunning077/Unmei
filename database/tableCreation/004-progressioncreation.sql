CREATE TABLE IF NOT EXISTS player_progression (
    player_id CHAR(36) NOT NULL PRIMARY KEY,
    player_lvl INT UNSIGNED NOT NULL DEFAULT 1,
    curr_exp BIGINT UNSIGNED NOT NULL DEFAULT 0,
    health DECIMAL(10,2) NOT NULL,
    max_health DECIMAL(10,2) NOT NULL,
    attributes JSON NOT NULL,
    talent_tree JSON NOT NULL,
    talent_points INT UNSIGNED NOT NULL DEFAULT 0,
    currency BIGINT UNSIGNED NOT NULL DEFAULT 0,

    FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_player_level
        CHECK (player_lvl >= 1),

    CONSTRAINT chk_player_health
        CHECK (health >= 0 AND max_health >= 0 AND health <= max_health)
) ENGINE=InnoDB;
