import random as rd
import sys, time, pygame
from Cell import *
pygame.init()

class Maze:
    def __init__(self, N, filename):
        self.N = N
        self.filename = filename
        self.layout = [[Cell(i,j,N*i+j) for j in range(N)] for i in range(N)]
        self.done = False

    #Retourne une chaîne de caractères, une version .txt du labyrinthe
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

    #Affichage graphique du labyrinthe 
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
        pygame.display.set_caption(f"Labyrinthe {self.N}x{self.N}") 
        for i in range(LENGTH):
            for j in range(LENGTH):
                if doodle[i][j] == "#":
                    SCREEN.blit( surfaceg, (j*CHUNK,i*CHUNK))
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
        max_id,min_id = max(cell1.id,cell2.id) , min(cell1.id,cell2.id)
        for i in range(self.N):
            for j in range(self.N):
                if self.layout[i][j].id == max_id:
                    self.layout[i][j].setId(min_id)
                    
        
    #Création d'un labyrinthe par la méthode du recursive backtracking
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
    
    #Créaton d'un labyrinthe par la méthode de l'algorithme de Kruskal
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

    #Méthode : Recursive backtracking
    #Retourne un tableau contenant des tuples représentant les coordonnées du chemin de résolution
    def backtrack_solving_path(self):
        current_cell = self.layout[0][0] #Case de départ
        path = [current_cell] #Chemin de résolution
        visited = []
        while current_cell != self.layout[self.N-1][self.N-1]: #Boucle tant qu'on est pas à la sortie
            visited.append(current_cell) #La cellule actuelle est marquée comme visitée
            #On recherche les voisins non-visités auxquels on peut accéder
            neighbors = [x for x in self.get_neighbors(current_cell) if x[0] not in visited and not current_cell.walls[x[1]]] 
            if neighbors:
                #On ajoute un voisin aléatoire au chemin et update la cellule courante
                neighbor = next_cell, direction = rd.choice(neighbors) 
                path.append(next_cell)
                current_cell = next_cell
            else:
                #Si il n'y a plus de voisins disponibles
                path.pop(-1) #Dépilage
                current_cell = path[-1] #Retour en arrière
        return [(cell.x, cell.y) for cell in path]

    #Méthode : Algorithme A-star
    #Retourne un tableau contenant des tuples représentant les coordonnées du chemin de résolution
    def astar_solving_path(self):
        return              






        
    #Chemin de résolution en entrée
    #Affichage graphique du labyrinthe et du chemin de résolution
    def solving_display(self, path):
        WIDTH = 825
        COLOR = (255,0,255)
        LENGTH = 2*self.N+1
        SIZE = WIDTH,WIDTH
        SCREEN = pygame.display.set_mode(SIZE)
        CHUNK = WIDTH/LENGTH
        THICKNESS = int(CHUNK/2)
        TEMPO = 1.5
        
        
        self.display() #Affichage du labyrinthe
        time.sleep(TEMPO)
        pygame.draw.line(SCREEN, COLOR , (0,3*CHUNK/2) , (3*CHUNK/2,3*CHUNK/2), THICKNESS) #Entrée
        #Liaison de tous les points du chemin
        for i,coord in enumerate(path):
            if i==0: continue
            x2,y2 = coord
            x1,y1 = path[i-1]
            pygame.draw.line( SCREEN, COLOR, ((3+4*y1)*CHUNK/2 , (3+4*x1)*CHUNK/2 ) , ((3+4*y2)*CHUNK/2 , (3+4*x2)*CHUNK/2), THICKNESS)
            pygame.display.flip()
            time.sleep(0.002)
        pygame.draw.line(SCREEN, COLOR , (WIDTH-3*CHUNK/2,WIDTH-3*CHUNK/2) , (WIDTH,WIDTH-3*CHUNK/2), THICKNESS) #Sortie
        pygame.display.flip()
        
        
        
    

                
    
