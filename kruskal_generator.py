from util import *   

               
#N = int(input("Entrez la taille du labyrinthe : "))
N = 55
filename = f"kruskal{N}.txt"
maze = Maze(N,filename)
maze.kruskal()
create_file(maze)

#Affiche le labyrinthe graphique
#maze.display()
maze.solving_display( maze.backtrack_solving_path() )



        
        
                
            
    
