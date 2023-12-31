from Maze import *



#Création d'un objet labyrinthe à partir d'un fichier texte
def create_maze_from_doodlefile(filename):
    with open(f"doodles/{filename}",'r') as f:
        doodle = [x.strip() for x in f.readlines()] 
    length = len(doodle)
    N = int( length / 2 )
    maze = Maze(N, filename[:-4])
    for i in range(length):
        for j in range(length):
            if doodle[i][j] != ".": continue #Murs
            if i%2 and j%2: continue #Position des cellules
            #Murs brisés
            if i%2:
                #Reliant deux cellules horizontalement
                maze.layout[int(i/2)][int((j-2)/2)].breakWall( (maze.layout[int(i/2)][int((j-2)/2)+1] , "E") )
            else:
                #Reliant deux cellules verticalement
                maze.layout[int((i-2)/2)][int(j/2)].breakWall( (maze.layout[int((i-2)/2)+1][int(j/2)] , "S") )
    maze.done = True
    return maze            
            
             
             
    
