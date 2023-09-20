from util import *
import os

#filename = input("Entrez le nom du fichier texte : ")

#if not os.path.isfile(filename):
#    print("Fichier non-existant")
#    exit()

filename = "kruskal21.txt"
maze = create_maze_from_file(filename)
mapping = maze.astar_solving_map()
#mapping2 = maze.backtrack_solving_map()
maze.solving_display( mapping)

#print(maze.doodle(mapping))
