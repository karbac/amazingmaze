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

    #Casse un mur au hasard
    def break_random_wall(self):
        neighbors = []
        while not neighbors:
            cell = rd.choice( rd.choice(self.layout) )
            neighbors = [x for x in self.get_neighbors(cell) if cell.walls[x[1]]]
        cell.breakWall(rd.choice(neighbors))

    #Création d'un fichier texte représentant un labyrinthe
    def create_file(self):
        with open(f"doodles/{self.filename}",'w') as f:
            f.write(self.doodle())
            
    #Retourne une chaîne de caractères, une version .txt du labyrinthe
    def doodle(self,mapping=None):
        LENGTH = 2*self.N+1
        doodle = [""] * LENGTH
        if mapping:
            path, heatmap = mapping
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
                        if not mapping:
                            doodle[i] += "."
                        else:
                            cell = self.layout[int(i/2)][int(j/2)]                            
                            doodle[i] += "o" if (cell.x,cell.y) in path else "*" if (cell.x,cell.y) in heatmap else "."
                    else:
                        doodle[i] += "." if not self.layout[int(i/2)][int((j-2)/2)].walls.get("E") else "#"
                else:
                    if not j%2:
                        doodle[i] += "#"
                    else:
                        doodle[i] += "." if not self.layout[int((i-2)/2)][int(j/2)].walls.get("S") else "#"

        return '\n'.join(doodle)

    #Affichage graphique du labyrinthe avec pygame
    def display(self):
        #Paramètres
        LENGTH = 2*self.N+1
        WIDTH = 825
        COLOR = (0,255,0)
        SIZE = WIDTH,WIDTH
        SCREEN = pygame.display.set_mode(SIZE)
        CHUNK = WIDTH/LENGTH
        MCHUNK = CHUNK + 1
        SURFACE = pygame.Surface((MCHUNK, MCHUNK))
        SURFACE.fill(COLOR)
        DOODLE = self.doodle().split('\n')
        pygame.display.set_caption(f"Labyrinthe {self.N}x{self.N}") 
        for i in range(LENGTH):
            for j in range(LENGTH):
                if DOODLE[i][j] == "#":
                    SCREEN.blit( SURFACE, (j*CHUNK,i*CHUNK))
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
            if min(xtarg,ytarg) < 0 or max(xtarg,ytarg) >= self.N: #out of range
                continue
            targ = self.layout[xtarg][ytarg]
            neighbors.append((targ, CARD.get(direction)))
        return neighbors

    
        
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

    #Propagation de l'id
    def fuse_id(self, cell1, cell2):
        max_id,min_id = max(cell1.id,cell2.id) , min(cell1.id,cell2.id)
        for i in range(self.N):
            for j in range(self.N):
                if self.layout[i][j].id == max_id:
                    self.layout[i][j].setId(min_id)

    #Retourne une cellule aléatoire, d'un id différent que celui passé en paramètre
    def get_random_other_cell(self, id):
        cells = []
        for i in range(self.N):
            for j in range(self.N):
                if self.layout[i][j].id != id:
                    cells.append(self.layout[i][j])
        return rd.choice(cells) if cells else None
    
    #Créaton d'un labyrinthe par la méthode de l'algorithme de Kruskal
    #On part d'une cellule aléatoire et on casse les murs de proche en proche
    #En arrivant à une impasse, on repart d'une autre cellule aléatoire et on reprend le processus
    #Condition de fin : Toutes les cellules partagent le même id
    def kruskal(self):
        if self.done: return False
        current_cell = rd.choice(rd.choice(self.layout)) #Point de départ aléatoire
        while current_cell: #Tant qu'il existe une cellule avec un id différent
            neighbors = [x for x in self.get_neighbors(current_cell) if x[0].id != current_cell.id] #Voisins avec un id différent
            if neighbors: #Si un voisin valide existe
                neighbor = next_cell, direction = rd.choice(neighbors)
                current_cell.breakWall(neighbor) #Cassage du mur d'un voisin aléatoire
                self.fuse_id(current_cell, next_cell) #Fusion des cellules
                current_cell = next_cell #Update cellule courante
                
            else:
                current_cell = self.get_random_other_cell(current_cell.id) #On repart d'une cellule aléatoire avec un différent id
        self.done = True
        return True
    
    #Algorithme de Kruskal
    #Alternative avec le mélange des murs
    #On parcourt chaque mur, et on détruit si les deux cellules adjacentes n'ont pas le même id
    def kruskal2(self):
        if self.done: return False
        walls = []
        DIR = {
            "S": (1,0),
            "E": (0,1)
        }
        for i in range(self.N):
            for j in range(self.N):
                if i != self.N - 1:
                    walls.append( (self.layout[i][j] , "S") )
                if j != self.N - 1:
                    walls.append( (self.layout[i][j] , "E") )
        rd.shuffle(walls)
        for wall in walls:
            cell , direction = wall
            neighboring_cell = self.layout[cell.x + DIR[direction][0]][cell.y + DIR[direction][1]]
            if cell.id == neighboring_cell.id: continue
            cell.breakWall((neighboring_cell, direction))
            self.fuse_id(cell, neighboring_cell)
        self.done = True
        return True
    

    #Résolution par Recursive backtracking
    #Retourne un tuple de 2 éléments contenant :
    #Un tableau contenant les coordonnées du chemin de résolution
    #Un tableau contenant les coordonnées des cases visitées
    def backtrack_solving_map(self):
        current_cell = self.layout[0][0] #Case de départ
        path = [current_cell] #Chemin de résolution
        heatmap = [current_cell]
        while current_cell != self.layout[self.N-1][self.N-1]: #Boucle tant qu'on est pas à la sortie
            #On recherche les voisins non-visités auxquels on peut accéder
            neighboring_cells = [x[0] for x in self.get_neighbors(current_cell) if x[0] not in heatmap and not current_cell.walls[x[1]]] 
            if neighboring_cells:
                #On ajoute un voisin aléatoire au chemin et update la cellule courante
                next_cell = rd.choice(neighboring_cells) 
                current_cell = next_cell
                path.append(current_cell)
                heatmap.append(current_cell) #La cellule est marquée comme visitée
            else:
                #Si il n'y a plus de voisins disponibles
                path.pop(-1) #Dépilage
                current_cell = path[-1] #Retour en arrière
        return ( [(cell.x, cell.y) for cell in path] , [(cell.x, cell.y) for cell in heatmap] )


    def dist(self, cell):
        return 2*(self.N-1) - cell.x - cell.y
    
    #Résolution par l'algorithme A-star
    #Retourne un tuple de 2 éléments contenant :
    #Un tableau contenant les coordonnées du chemin de résolution
    #Un tableau contenant les coordonnées des cases visitées
    def astar_solving_map(self):
        #Dictionnaires dont les clés sont les cellules, 
        cost = {} #Coût - du déplacement de la cellule initiale jusqu'à la cellule
        score = {} #Score = Coût total heuristique, somme du coût et de la distance à l'arrivée
        parent = {} #Enregistre l'arborescence pour reconstruire le chemin
        #Initialisation
        heatmap = []  #Liste fermée des cases visitées
        current_cell = self.layout[0][0]
        open_list = [current_cell]
        cost[current_cell] = 0
        score[current_cell] = self.dist(current_cell)

        while open_list:
            #On choisit la cellule avec le coût total le plus bas
            current_cell = min(open_list, key = lambda x: score[x])
            heatmap.append(current_cell)
            if current_cell == self.layout[self.N-1][self.N-1]: break #On a trouvé la sortie

            #La cellule est retirée de la liste ouverte
            open_list.remove(current_cell)
            #On collecte les voisins possibles
            neighboring_cells = [x[0] for x in self.get_neighbors(current_cell) if not current_cell.walls[x[1]] ]
            for neighboring_cell in neighboring_cells:
                if neighboring_cell in heatmap: continue
                int_cost = cost[current_cell] + 1
                if int_cost < score.get(neighboring_cell, float('inf')):
                    #Si coût inférieur : on garde et on update les valeurs
                    cost[neighboring_cell] = int_cost 
                    score[neighboring_cell] = cost[neighboring_cell] + self.dist(neighboring_cell)
                    parent[neighboring_cell] = current_cell
                #Ajout du voisin à la liste ouverte
                if not neighboring_cell in open_list:
                    open_list.append(neighboring_cell)
        if not open_list: #N'est pas censé arriver si le labyrinthe est bien construit
            print('Pas de chemin trouvé')
            return False
        #Reconstruction du chemin par l'arborescence
        path = [current_cell]
        while parent.get(current_cell):
            current_cell = parent[current_cell]
            path = [current_cell] + path
        return ( [(cell.x, cell.y) for cell in path] , [(cell.x, cell.y) for cell in heatmap])


        
    #Chemin de résolution en entrée
    #Affichage graphique du labyrinthe et du chemin de résolution
    def solving_display(self, mapping, mapping2 = None , show_heatmap=True):
        #Paramètres
        WIDTH = 825
        PATHCOLOR = (255,255,255)
        HEATCOLOR = (255,0,255)
        PATHCOLOR2 = HEATCOLOR
        LENGTH = 2*self.N+1
        SIZE = WIDTH,WIDTH
        SCREEN = pygame.display.set_mode(SIZE)
        CHUNK = WIDTH/LENGTH
        THICKNESS = int(CHUNK/2)
        TEMPO = 1

        path, heatmap = mapping
        self.display() #Affichage du labyrinthe brut
        time.sleep(TEMPO)

        #Affiche tous les points visités par l'algorithme
        if show_heatmap and not mapping2:
            HEATCHUNK = pygame.Surface((CHUNK,CHUNK))
            HEATCHUNK.fill(HEATCOLOR)
            for coord in heatmap:
                x,y = coord
                SCREEN.blit( HEATCHUNK , ( (2*y+1)*CHUNK , (2*x+1)*CHUNK) )
                pygame.display.flip()
                #time.sleep(0.1)

        time.sleep(TEMPO)
        
        #Affiche le second chemin si demandé
        if mapping2:
            path2 = mapping2[0]
            for i,coord in enumerate(path2):
                if i==0: continue
                x2,y2 = coord
                x1,y1 = path2[i-1]
                pygame.draw.line( SCREEN, PATHCOLOR2 , ((3+4*y1)*CHUNK/2 , (3+4*x1)*CHUNK/2 ) , ((3+4*y2)*CHUNK/2 , (3+4*x2)*CHUNK/2), THICKNESS)
                pygame.display.flip()
                #time.sleep(0.002)

        time.sleep(TEMPO)
        pygame.draw.line(SCREEN, PATHCOLOR , (0,3*CHUNK/2) , (3*CHUNK/2,3*CHUNK/2), THICKNESS) #Entrée
        #Liaison de tous les points du chemin
        for i,coord in enumerate(path):
            if i==0: continue
            x2,y2 = coord
            x1,y1 = path[i-1]
            pygame.draw.line( SCREEN, PATHCOLOR, ((3+4*y1)*CHUNK/2 , (3+4*x1)*CHUNK/2 ) , ((3+4*y2)*CHUNK/2 , (3+4*x2)*CHUNK/2), THICKNESS)
            pygame.display.flip()
            #time.sleep(0.002)
        pygame.draw.line(SCREEN, PATHCOLOR , (WIDTH-3*CHUNK/2,WIDTH-3*CHUNK/2) , (WIDTH,WIDTH-3*CHUNK/2), THICKNESS) #Sortie
        pygame.display.flip()

            
       
        
        
        
    

                
    
