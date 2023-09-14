from util import *
import os

#filename = input("Entrez le nom du fichier texte : ")

#if not os.path.isfile(filename):
#    print("Fichier non-existant")
#    exit()

filename = "kruskal36.txt"
maze = create_maze_from_file(filename)
maze.display()

#maze.solving_display( maze.astar_solving_path() )

