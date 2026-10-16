USE unmei;

CREATE TABLE IF NOT EXISTS players (
    player_id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    username VARCHAR(32) NOT NULL UNIQUE,
    passphrase_hash VARCHAR(255) NOT NULL,
    passphrase_filename VARCHAR(255) NULL,
    account_status ENUM(
        'active',
        'suspended',
        'banned',
        'deleted'
    ) NOT NULL DEFAULT 'active',
    last_login TIMESTAMP NULL DEFAULT NULL,
    account_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
