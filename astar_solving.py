from util import *
import os

filename = input("Entrez le nom du labyrinthe : ") + ".txt"

if not os.path.isfile(f"doodles/{filename}"):
    print("Non-existant")
    exit()

#filename = "kruskal100.txt"
maze = create_maze_from_doodlefile(filename)

maze.solving_display( maze.astar_solving_map())

