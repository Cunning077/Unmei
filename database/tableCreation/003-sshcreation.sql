USE unmei;

CREATE TABLE IF NOT EXISTS ssh_keys (
    ssh_key_id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    player_id CHAR(36) NOT NULL,
    public_key VARCHAR(2048) NOT NULL,
    key_fingerprint VARCHAR(128) NOT NULL UNIQUE,
    key_label VARCHAR(64) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP NULL DEFAULT NULL,

    FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;
    
