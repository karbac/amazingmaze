from util import *   

               
#N = int(input("Entrez la taille du labyrinthe : "))
N = 150
filename = f"kruskal{N}"
start = time.time()
maze = Maze(N,filename)
maze.kruskal_generate()
end = time.time()
print(end-start)
maze.create_file()

#Affiche le labyrinthe graphique
maze.display()




        
        
                
            
    
