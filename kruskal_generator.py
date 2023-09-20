from util import *   

               
#N = int(input("Entrez la taille du labyrinthe : "))
N = 30
filename = f"kruskal{N}.txt"
maze = Maze(N,filename)
maze.kruskal2()

maze.create_file()

#Affiche le labyrinthe graphique
maze.display()




        
        
                
            
    
