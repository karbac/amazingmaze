from Maze import *


def create_maze_from_doodle(doodle):
    doodle = doodle.split('\n')
    length = len(doodle)
    N = int( length / 2 )
    maze = Maze(N)
    for i in range(length):
        for j in range(length):
            if doodle[i][j] != ".": continue
            if i%2 and j%2: continue
            if i%2:
                maze.layout[int(i/2)][int((j-2)/2)].breakWall(  maze.layout[int(i/2)][int((j-2)/2)+1] , "E")
            maze.layout[int(i/2)][int((j-2)/2)].breakWall(  maze.layout[int(i/2)+1][int((j-2)/2)+1] , "S")

    return maze


                
            
            
             
             
    
