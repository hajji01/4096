#!/usr/bin/env python3
import sys
import uuid
import random
import subprocess
import socket
import os
import platform
import matplotlib.pyplot as plt

sys.path.append("4096")
import engine

if len(sys.argv) < 3:
    sys.stderr.write("Usage: interface.py <randomseed> <executable>\n")
    sys.exit()

random.seed(sys.argv[1])

def write(conn, str):
    conn.send(str.encode("utf-8"))

def read(conn):
    return conn.recv(4096).decode("utf-8").strip()

identifier = ""

if platform.system() == 'Windows':
    print("Must connect differently")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 8765))
    print(sys.argv[2])
    process = subprocess.Popen([sys.executable, sys.argv[2], '8765'])
else:
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(2)
    identifier = str(uuid.uuid4())
    s_path = "/tmp/4096-" + identifier
    s.bind(s_path)

    process = subprocess.Popen([sys.executable, sys.argv[2], s_path])
s.listen(1)
conn, addr = s.accept()

game = engine.Engine()
move_count = 0
game_name = read(conn)

sys.stderr.write("Game: " + game_name + "\n")
sys.stderr.write("Identifier: " + identifier + "\n")

write(conn, game.to_string())

game_counter = 0
scores = []

try:
    while conn:
        c = read(conn)

        if c == 'u':
            game.up()
        elif c == 'd':
            game.down()
        elif c == 'l':
            game.left()
        elif c == 'r':
            game.right()

        write(conn, game.to_string())

        move_count += 1

                    
        if game_counter > 100 : 
            scores.append(game.score)

            #A faire : conserver le score dans une liste et pouvoir afficher à la fin à l'aide d'un graph
            #A l'aide d'une librairie Matplotlib

        if game.is_board_locked():
            # lancer une nouvelle partie
            game_counter += 1
            game = engine.Engine()
            move_count = 0
            if game_counter % 20 == 0 : 
                print(f"Game n# {game_counter} finished")
                plt.plot(range(len(scores)), scores)
                plt.xlabel('Game Number')
                plt.ylabel('Score')
                plt.title('Scores Evolution')
                plt.show()

                            
                    
except (socket.timeout):
    sys.stderr.write(" * Socket timed out.\n")
except:
    pass

# Affichage du score
sys.stderr.write("Score: " + str(game.score) + "\n")
sys.stderr.write("Moves: " + str(move_count) + "\n")

# Nettoyage
process.terminate()
if not platform.system() == 'Windows':
    os.remove(s_path)
