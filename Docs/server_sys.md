# Server functionality

    The orchestrator is gonna handle essentially all communication beetween
    classes and the database, it will not itself handle the actual data or
    anything simply just the higher lvl.

## Game sequence
    To start i will take a book out of my hackpad project and treat this as
    a high level queue.

- Initation: 
    The overarching command if this isnt satisfied nothing will happen.

    For one it starts by detecting a new connection, which from there it
    will first check the ssh public key and check for the key in the db, 
    heres where it branches:
        (1.0)Has public key         (2.0)No public key found
(1.1)Looks for passphrase file  (2.1)create new account or login to account
(1.2)Passphrase file found      (2.1.1) Create new account (2.2) Login
(1.1.1) No passphrase found     (2.1.2)Setup account
(1.2.1)Init account info
(1.1.2) Register new passphrase
(1.1.1.1) Create new account
                                                    

    

        
