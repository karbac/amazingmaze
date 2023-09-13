import random as rd
import sys, time, pygame
from Cell import *
pygame.init()

class Maze:
    def __init__(self, N):
        self.N = N
        self.layout = [[Cell(i,j,N*i+j) for j in range(N)] for i in range(N)]
        self.done = False

    #Affichage
    def doodle(self):
        LENGTH = 2*self.N+1
        doodle = [""] * LENGTH
        for i in range(LENGTH):
            for j in range(LENGTH):
                if (i,j) == (1,0) or (i,j) == (LENGTH-2, LENGTH-1):
                    doodle[i] += ">"
                    continue
                if i in (0,LENGTH-1) or j in (0,LENGTH-1):
                    doodle[i] += "#"
                    continue
                if i%2:
                    if j%2:
                        doodle[i] += "."
                    else:
                        doodle[i] += "." if not self.layout[int(i/2)][int((j-2)/2)].walls.get("E") else "#"
                else:
                    if not j%2:
                        doodle[i] += "#"
                    else:
                        doodle[i] += "." if not self.layout[int((i-2)/2)][int(j/2)].walls.get("S") else "#"

        return '\n'.join(doodle)

    def display(self):
        LENGTH = 2*self.N+1
        WIDTH = 825
        COLOR = (0,255,0)
        SIZE = WIDTH,WIDTH
        SCREEN = pygame.display.set_mode(SIZE)
        CHUNK = WIDTH/LENGTH
        MCHUNK = CHUNK*1.125
        surfaceg = pygame.Surface((MCHUNK, MCHUNK))
        surfaceg.fill(COLOR)
        doodle = self.doodle().split('\n')
        for i in range(LENGTH):
            for j in range(LENGTH):
                if doodle[i][j] == "#":
                    SCREEN.blit( surfaceg, (j*CHUNK,i*CHUNK))
        pygame.display.set_caption(f"Labyrinthe {self.N}x{self.N}")     
        pygame.display.flip()

    def get_neighbors(self, cell):
        CARD = {
         (1,0): "S",
         (0,1): "E",
         (-1,0): "N",
         (0,-1): "W"
        }

        neighbors = []
        
        for direction in CARD:
            xtarg , ytarg = cell.x+direction[0] , cell.y+direction[1]
            if min(xtarg,ytarg) < 0 or max(xtarg,ytarg) >= self.N:
                continue
            targ = self.layout[xtarg][ytarg]
            neighbors.append((targ, CARD.get(direction)))
        return neighbors
        

    #Retourne une cellule aléatoire, d'un id différent que celui passé en paramètre
    def get_random_other_cell(self, id):
        cells = []
        for i in range(self.N):
            for j in range(self.N):
                if self.layout[i][j].id != id:
                    cells.append(self.layout[i][j])
        return rd.choice(cells) if cells else None

    #Propagation de l'id
    def fuse_id(self, cell1, cell2):
        for i in range(self.N):
            for j in range(self.N):
                if self.layout[i][j].id in (cell1.id, cell2.id):
                    self.layout[i][j].setId(min(cell1.id, cell2.id))
                    
        

    def backtrack(self):
        if self.done: return False
        current_cell = self.layout[0][0]
        pile = [current_cell]
        visited_count = 1
        while visited_count < self.N * self.N:
            neighbors = [x for x in self.get_neighbors(current_cell) if not x[0].isVisited()] #Voisins non-visités
            if neighbors: #Si un voisin valide existe
                neighbor = next_cell, direction = rd.choice(neighbors)
                current_cell.breakWall(neighbor) #On casse le mur
                pile.append(next_cell) #La cellule s'ajoute à la pile
                current_cell = next_cell #Update cellule courante
                visited_count += 1 # +1
            else:
                pile.pop(-1) #Dépilage
                current_cell = pile[-1] #Retour en arrière
        self.done = True
        return True
    
    def kruskal(self):
        if self.done: return False
        current_cell = self.layout[0][0] #Point de départ
        while current_cell: #
            neighbors = [x for x in self.get_neighbors(current_cell) if x[0].id != current_cell.id] #Voisins avec un id différent
            if neighbors: #Si un voisin valide existe
                neighbor = next_cell, direction = rd.choice(neighbors)
                current_cell.breakWall(neighbor) #Cassage du mur d'un voisin aléatoire
                self.fuse_id(current_cell, next_cell) #Propagation de l'id
                current_cell = next_cell #Update cellule courante
                
            else:
                current_cell = self.get_random_other_cell(current_cell.id) #On repart d'une cellule aléatoire avec un différent id
        self.done = True
        return True

    def backtrack_solving_path(self):
        current_cell = self.layout[0][0]
        path = [current_cell]
        visited = []
        while current_cell != self.layout[self.N-1][self.N-1]:
            visited.append(current_cell)
            neighbors = [x for x in self.get_neighbors(current_cell) if x[0] not in visited and not current_cell.walls[x[1]]]
            if neighbors:
                neighbor = next_cell, direction = rd.choice(neighbors)
                path.append(next_cell)
                current_cell = next_cell
            else:
                path.pop(-1)
                current_cell = path[-1]
        return [(cell.x, cell.y) for cell in path]

    def solving_display(self, path):
        WIDTH = 825
        COLOR = (255,0,255)
        LENGTH = 2*self.N+1
        SIZE = WIDTH,WIDTH
        SCREEN = pygame.display.set_mode(SIZE)
        CHUNK = WIDTH/LENGTH
        THICKNESS = int(CHUNK/4)
        TEMPO = 0.02
        
        self.display()
        pygame.draw.line(SCREEN, COLOR , (0,3*CHUNK/2) , (3*CHUNK/2,3*CHUNK/2), THICKNESS) #Entrée
        for i,coord in enumerate(path):
            if i==0: continue
            x2,y2 = coord
            x1,y1 = path[i-1]
            pygame.draw.line( SCREEN, COLOR, ((3+4*y1)*CHUNK/2 , (3+4*x1)*CHUNK/2 ) , ((3+4*y2)*CHUNK/2 , (3+4*x2)*CHUNK/2),THICKNESS)
            pygame.display.flip()
            time.sleep(TEMPO)
        pygame.draw.line(SCREEN, COLOR , (WIDTH-3*CHUNK/2,WIDTH-3*CHUNK/2) , (WIDTH,WIDTH-3*CHUNK/2), THICKNESS) #Sortie
        pygame.display.flip()
        
        
        
    

                
    
