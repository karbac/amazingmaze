from util import *              


#Génére un fichier .txt représentant un labyrinthe aléatoire de la taille demandée

#N = int(input("Entrez la taille du labyrinthe : "))
N = 50
#filename = input("Entrez le nom du fichier : ")
filename = f"random{N}.txt"
maze = Maze(N,filename)
maze.backtrack()
create_file(maze)

#Affiche graphiquement le labyrinthe
maze.display()



