from util import *
import os

#filename = input("Entrez le nom du fichier texte : ")

#if not os.path.isfile(filename):
#    print("Fichier non-existant")
#    exit()

filename = "random50.txt"
maze = create_maze_from_file(filename)
path = maze.astar_solving_path()
maze.solving_display( path )

print(len(path))
