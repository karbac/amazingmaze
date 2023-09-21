from util import *
import os

#filename = input("Entrez le nom du fichier - sans extension : ")
#filename += ".txt"

#if not os.path.isfile(filename):
#    print("Fichier non-existant")
#    exit()

filename = "kruskal40.txt"
start = time.time()
maze = create_maze_from_doodlefile(filename)
mapping = maze.astar_solving_map()
end = time.time()
print(end-start)
#mapping2 = maze.backtrack_solving_map()
maze.solving_display( mapping)

#print(maze.doodle(mapping))
