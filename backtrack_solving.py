from util import *
import os

#filename = input("Entrez le nom du fichier texte : ")

#if not os.path.isfile(filename):
#    print("Fichier non-existant")
#    exit()

filename = "random50.txt"
maze = create_maze_from_file(filename)


maze.solving_display( maze.backtrack_solving_path() )
