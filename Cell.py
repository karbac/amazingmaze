class Cell:
    def __init__(self,v,h,id):
        self.v = v
        self.h = h
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
        adj_cell, card = neighbor
        OPPCARD = {"N": "S", "S": "N" , "W": "E" , "E": "W"} 
        self.walls[card] = False
        adj_cell.walls[OPPCARD[card]] = False
