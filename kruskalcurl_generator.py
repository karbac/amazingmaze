from util import *   

               
#N = int(input("Entrez la taille du labyrinthe : "))
N = 42
filename = f"kruskalcurl{N}.txt"
maze = Maze(N,filename)
maze.kruskal_curl()
create_file(maze)

#Affiche le labyrinthe graphique
maze.display()
#maze.solving_display( maze.backtrack_solving_path() )



        
        
                
            
    
