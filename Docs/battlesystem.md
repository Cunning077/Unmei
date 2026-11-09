# The battle system
This doc is meant to explain how the battle system works

## General overview

The battle system essentially is very similar to pokemon in which there is a vast amount of different attacks and mechanics, the attempt is to essentially give the player an oppurtinity to truly think like a chess player, every move should be reasonable and a wrong move can prove costly, in addition the attacks arent dictated by action but by time, the enemy will attack wether you do or not and he will essentially be on his own attack timer, this attack timer will also be relativly random depending on what move they do, this is why each battle will be initiated with a massive dict containing the information required for the battle to take place.

## First page
So the first page displays the enemy health, type, attack style, time to attack

## Defense Mechanism
For the defense mechanism im thinking of doing like a sort of block style system so for instance say the enemy does a magic style attack, you can do a defensive block on the attack, or if the enemys attack is physical with little penetration you can essentially increase your dodge chance, sort of like blocks on certain styles of attacks

- Guard: Meant to block a broad 20% of all damage regardless of type, this will cost 5 stamina points
- Ward: Any magical attack damage is fully blocked
- Evade: boost agility by 50%, and chance to dodge by 10%
- Brace: reduce physical attacks damage by 50% must be a physical damage
- Parry: Any underpreparred attacks have a 80% chance to be parried which blocks all damage and counters,
    with a quick physical attack

Each defense will have its own function as they are very different from each other and require weird 
conditions

