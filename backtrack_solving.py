from util import *
import os

#filename = input("Entrez le nom du fichier texte : ")

#if not os.path.isfile(filename):
#    print("Fichier non-existant")
#    exit()

filename = "kruskal32.txt"
maze = create_maze_from_file(filename)
path = maze.backtrack_solving_path()
path2 = maze.astar_solving_path()
print(len(path))
print(len(path2))

maze.solving_display( path , path2 )

