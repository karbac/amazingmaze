from util import *              


#Génére un fichier .txt représentant un labyrinthe aléatoire de la taille demandée

#N = int(input("Entrez la taille du labyrinthe : "))
N = 120
#filename = input("Entrez le nom du fichier : ")
filename = f"random{N}.txt"
maze = Maze(N,filename)
start = time.time()
maze.backtrack()
end = time.time()
print(end-start)
create_file(maze)

#Affiche graphiquement le labyrinthe
maze.display()



