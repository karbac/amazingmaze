from util import *   

               
#N = int(input("Entrez la taille du labyrinthe : "))
N = 21
filename = f"kruskal{N}.txt"
maze = Maze(N,filename)
maze.kruskal2()
for i in range(N):
    maze.break_random_wall()
create_file(maze)

#Affiche le labyrinthe graphique
maze.display()




        
        
                
            
    
