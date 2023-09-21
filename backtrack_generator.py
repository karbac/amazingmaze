from util import *              


#Génére un fichier .txt représentant un labyrinthe aléatoire de la taille demandée

#N = int(input("Entrez la taille du labyrinthe : "))
N = 50
#filename = input("Entrez le nom du fichier : ")
filename = f"random{N}"
start = time.time()
maze = Maze(N,filename)
maze.backtrack_generate()
end = time.time()
print(end-start)
maze.create_file()

#Affiche graphiquement le labyrinthe
maze.display()



