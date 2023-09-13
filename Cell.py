class Cell:
    def __init__(self,x,y,id):
        self.x = x
        self.y = y
        self.id = id
        self.walls = {
            "N": True,
            "S": True,
            "W": True,
            "E": True}

    def setId(self,id):
        self.id = id
        return self
    
    def isVisited(self):
        return True if False in self.walls.values() else False

    #Paramètre neighbor : tuple contenant une cellule ainsi qu'une direction
    def breakWall(self,neighbor):
        adj_cell, direction = neighbor
        OPPDIR = {"N": "S", "S": "N" , "W": "E" , "E": "W"} 
        self.walls[direction] = False
        adj_cell.walls[OPPDIR[direction]] = False
