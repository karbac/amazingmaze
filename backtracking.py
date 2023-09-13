from util import *              


#Initialisation
#N = int(input("Entrez la taille du labyrinthe : "))
N = 50
maze = Maze(N)
maze.backtrack()
maze.solving_display( maze.backtrack_solving_path() )


