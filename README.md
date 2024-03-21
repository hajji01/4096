4096
====

Seminaire DEEP LEARNING

**Objectif** : Coder un DQN capable d'apprendre à jouer à 2048.

Avec PyTorch, dans le fichier "dqnlearner_bot.py" et dans le fichier "botDQN.py", vous devez créer une classe qui va pouvoir apprendre sur les différentes parties de 2048 qu'il pourra jouer.

Le serveur se trouve dans le fichier `interface.py`
La classe du bot DQN se trouve dans le fichier `dqnlearner_bot.py`
L'appel de la classe et l'interaction avec le jeu 2048 se trouve dans le fichier `botDQN.py`
Un exemple d'interaction se trouve dans le fichier `botsmarter.py`

Pour lancer le fichier il faut lancer au choix les commandes suivantes :

- Lancer le bot d'exemple : `$ ./interface.py 123 ./botsmarter.py`
- Lancer le bot DQN : `$ ./interface.py 123 ./botDQN.py`

====
A python implementation of [1024](https://play.google.com/store/apps/details?id=com.veewo.a1024)/[2048](http://saming.fr/p/2048/) with a local socket interface for creating competing bots.

Usage
-----

Use interface.py to launch the local unix socket interface to the game engine. You'll have to supply 
two arguments: the random seed (so all bots receive the same sequence if they perform the same actions),
and the path to the executable of your bot. Your bot will receive the path to the unix socket as it's
first and only argument. Read and write to this socket to interact with the game engine.

    ./interface.py 123 ./bot_file.py

The unix socket will be located in /tmp/4096-game-identifier (the path is provided as an argument to
the bot executable).

Protocol
--------

The client registers itself by providing a name of the client ("examplebot") and then a newline.

    examplebot

It will receive the initial state of the game board back, where the board ends with the line "== currentscore":

    0 0 2 0
    0 0 0 0
    2 0 0 0
    0 0 0 0
    == 4

The client must respond with the action it wants to perform (the direction it want to merge the board in),
where all commands are given as single letters indicating the direction. Valid directions are "l", "r", "u"
and "d".

    d

The server responds again with the changed game state, before waiting for input again:

    0 0 0 0
    4 0 0 0
    0 0 0 0
    2 0 2 0
    == 8

The cycle continues until the board is no longer playable, where the server will respond with "FIN endscore":

    FIN 450

This ends a game session, and the server prints out the score and the number of moves performed by the bot
before exiting (and terminating the bot if it hasn't terminated by itself).

Example
-------

See [the exampel bot implementation](4096/bot.py) in the repository.

License
-------

This project and all included files are licensed [under the MIT license](LICENSE).
