from Maze import *


#Création d'un fichier texte représentant un labyrinthe
def create_file(maze):
    with open(f"doodles/{maze.filename}",'w') as f:
        f.write(maze.doodle())

#Création d'un objet labyrinthe à partir d'un fichier texte
def create_maze_from_file(filename):
    with open(f"doodles/{filename}",'r') as f:
        doodle = [x.strip() for x in f.readlines()] 
    length = len(doodle)
    N = int( length / 2 )
    maze = Maze(N, filename)
    for i in range(length):
        for j in range(length):
            if doodle[i][j] != ".": continue #murs
            if i%2 and j%2: continue #cellules
            #murs brisés
            if i%2:
                maze.layout[int(i/2)][int((j-2)/2)].breakWall( (maze.layout[int(i/2)][int((j-2)/2)+1] , "E") )
            else:
                maze.layout[int((i-2)/2)][int(j/2)].breakWall( (maze.layout[int((i-2)/2)+1][int(j/2)] , "S") )
    maze.done = True
    return maze            
            
             
             
    
