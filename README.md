# PRESENTATION
On se propose d'implémenter des algorithmes de génération et de résolution de labyrinthe.  
Il existe variété d'algorithmes de conception et de résolution des labyrinthes.  
Nous nous intérésserons ici à l'algorithme de **Recursive Backtracking** pour la génération et la résolution, l'algorithme de **Kruskal** pour la génération, ainsi que l'algorithme d'**A-star** pour la résolution.  
On considérera qu'un **labyrinthe** est composé de N x N **cellules**, si N est la taille du labyrinthe, et que des **murs** peuvent exister entre ces cellules.  
On ne peut se déplacer que d'une cellule à une **cellule adjacente**, et que s'il n'existe pas de mur entre les deux. On ne peut pas se déplacer diagonalement.  
L'entrée du labyrinthe se situera dans un coin et la sortie au coin opposé.  

# ALGORITHMES
## GENERATION DE LABYRINTHES
Deux algorithmes différents, dont le fonctionnement global est le même : On part d'un labyrinthe totalement fermé où tous les murs sont érigés et chaque cellule est isolée.  
On casse progressivement les murs jusqu'à obtenir un labyrinthe parfait, c'est-à-dire un labyrinthe dont chaque paire de cellules ne peut être reliée que par un unique chemin.  
Un labyrinhthe parfait est un labyrinthe sans boucles. Ainsi la solution d'un labyrinthe parfait est unique
### RECURSIVE BACKTRACKING : 
On se place initialement sur la cellule de départ.   
On se déplace vers une cellule voisine non-visitée au hasard en cassant le mur relatif.    
Si aucune cellule voisine non-visitée existe, on revient à la cellule précédente. On répète ce procédé jusqu'à ce que toutes les cases soient visitées.    
On génère ainsi un labyrinthe parfait.

### ALGORITHME DE KRUSKAL : 
On attribue à chaque case un numéro différent. On liste tous les murs du labyrinthe - séparant deux cellules.  
On mélange cette liste et on la parcourt. Pour chaque mur, si les deux cellules adjacentes ne partagent pas le même numéro, on casse ce mur et on fusionne les numéros de toutes les cellules connexes à ces 2 cellules.  
Ainsi chaque cellule d'une composante connexe du labyrinthe partagera le même numéro.  
A la fin de ce procédé, toutes les cellules partagent le même numéro. On aura ainsi généré un labyrinthe parfait.  

## RESOLUTION DE LABYRINTHES
Le but de ces algorithmes est de trouver un chemin reliant l'entrée et la sortie
### Algorithme de résolution par recursive backtracking.
_Algorithme de résolution par voyage au hasard et à l'aveugle_  
On part de la cellule de départ.
On se déplace un voisin non-visité au hasard. Si il n'existe pas de voisin non-visité, on revient en arrière.
On répète ce procédé jusqu'à arriver à la sortie et reconstruire le chemin.

### Algorithme de résolution d'A-star
_Algorithme de résolution par recherche du chemin optimal_  
Nos cellules se voient attribuées plusieurs propriétés :  
Le **coût** : Représente le nombre de mouvements minimum nécéssaires pour arriver à cette cellule depuis la case de départ - Un mouvement représente un déplacement d'une cellule à une cellule adjacente  
La **distance heuristique** : La distance minimale possible entre la cellule et la sortie, en termes de mouvements  
Le **score** ou le coût total : Représente la somme entre le coût et la distance restante  
On tiendra deux listes : Une liste ouverte représentant les cases à explorer et une liste fermée représentant les cases déjà explorées    

On part de la cellule de départ et on lui attribut un coût de 0.  
La cellule actuelle - à visiter - sera la cellule de la liste ouverte avec le score le plus bas.    
La cellule actuelle est déplacée de la cellule ouverte à la cellule fermée.  
Les cellules voisines non-explorés de la cellule actuelle sont ajoutés à la liste ouverte.  
Chacune de ces cellules voisines voit également son coût évalué (= coût de la cellule précédente + 1)  
Si ce coût évalué est inférieur à celui qui lui est effectivement attribué ou si il n'a jamais été évalué, on conserve/actualise les informations de cette cellule(coût, score)  
Lorsque la cellule actuelle est la cellule de sortie, alors il faudra reconstruire le chemin.  

# FICHIERS

## CLASSES

### Cell.py & Maze.py 
Contiennent la logique des classes Cell et Maze

### util.py 
Contient les méthodes qui ne sont pas relatives aux classes Cell et Maze

## SCRIPTS
### backtrack_generator.py & kruskal_generator.py
Génération d'un labyrinthe de la taille demandée en utilisant la méthode, respectivement du Recursive Backtracking ou de l'algorithme de Kruskal.  
Enregistre ce labyrinthe au format texte avec le nom demandé, affiche ce labyrinthe sur une fenêtre pygame et l'enregistre au format JPG

### backtrack_solving.py & astar_solving.py
Prend en entrée un nom de fichier contenant un labyrinthe.  
A l'aide de l'algorithme de recursive backtracking ou de A-star, génère le chemin de résolution du labyrinthe.  
Affiche le labyrinthe avec le chemin de résolution et les cases visitées par l'algorithme et enregistre au format JPG 

### loopymaze.py
Génération d'un labyrinthe non-parfait, avec plusieurs chemins de résolution. Pour ce faire, on éxécute l'algorithme de génération de Kruskal puis on casse des murs supplémentaires au hasard.   
On affiche également la résolution de ce labyrinthe par les 2 algorithmes de résolution, afin de faire un comparatif.
L'algorithme d'A-star choisira toujours le chemin optimal - avec le moins de déplacements, alors que l'algorithme de Recursive Backtracking choisira un chemin au hasard, même non-optimal.  
Libre à vous de modifier la valeur de N.

## DOSSIERS
### doodles 
Contient les labyrithes générés, au format texte. Utile pour les régénérer lorsqu'un script de résolution est appelé
### mazes 
Contient les labyrinthes générés au format jpg
### solvedmazes
Contient les labyrinthes résolus, au format jpg

# PERFORMANCE
Les deux algorithmes de génération de labyrinthes sont de complexité **O(N²)**   
Doubler la taille équivaut à approximativement quadrupler le temps d'éxécution.  
L'algorithme de Kruskal est toujours plus performant en termes de temps d'éxécution que l'algorithme de Recursive Backtracking  

Résolution par Recursive Backtracking : Temps d'éxécution très variable car l'algorithme peut tourner pendant très longtemps si il explore des longues impasses  
Résolution par l'algorithme d'A-star : Assez variable également - Dépend de la structure du labyrinthe  
L'algorithme d'A-star est globalement plus performant que le Recursive Backtracking, mais il peut arriver que le Recursive Backtracking donne des résultats plus rapides s'il n'explore pas de longues impasses  
L'algorithme d'A-star retourne toujours le chemin optimal dans le cas d'un labyrinthe non-parfait, ce qui n'est pas le cas du Recursive Backtracking - Voir _loopymaze.py_

# NOTES
Bien que l'algorithme de Recursive Backtracking et de Kruskal génèrent des labyrinthes parfaits, on peut noter des différences sur l'architecture des labyrinthes :  
L'algorithme de Recursive Backtracking tend à génèrer des impasses de longueur hétérogène, c'est-à-dire des impasses "très" courtes et "très" longues  
L'algorithme de Kruskal tend à génèrer des impasses de longueur plus homogène.    

A partir d'une certaine taille, le rendu jpg ne sera plus très fiable, les cellules étant trop petites pour être représentées.  
Le paramètre **WIDTH** peut être modifié, dans les méthodes display() et solving_display() de la classe _Maze_, pour un rendu plus grand ou petit.

# TERMINOLOGIE DE CODE

## ATTRIBUTS
### Classe Cell - Cellule :
_v_ & _h_ : Entier - coordonnée indiquant le positionnement de la cellule dans le labyrinthe - v pour verticale , h pour horizontale  
_id_ : Entier - Identifiant de la cellule - utile pour l'algorithme de Kruskal  
_walls_ : Dictionnaire dont les clés sont les 4 points cardinaux (N,S,E,W) et dont les valeurs sont des booléens. Indique si un mur dans une direction existe ou non.

### Classe Maze - Labyrinthe:
_N_ : Entier - Dimension du labyrinthe
_layout_: Liste de liste de taille _N_ x _N_ composée des cellules composant le labyrinthe, l'entrée se situe à **(0,0)** et la sortie à **(N-1,N-1)**  
_filename_ : Chaîne de caractères - nom qui est donné labyrinthe lorsqu'il est exporté en fichier texte ou jpg
_done_ : Booléen - Indique l'état du labyrinthe : construit ou pas.

## VARIABLES
_maze_ : Objet - entité de Maze  
_cell_ : Objet - entité de Cell  
_card_ : cardinalité - N,S,E,W  
_neighbor_ : Tuple de 2 éléments composé d'une _cellule_ et d'une _cardinalité_ - argument de la méthode breakWall de la classe _Cell_ 
_doodle_ : Chaîne de caractères ou tableau de chaîne de caractères représentant le labyrinthe   
_heatmap_ : Liste composée de toutes les _cellules_ visitées par l'algorithme de résolution  
_path_ : Liste de _cellules_ contenant les cellules constituant le chemin de résolution  
_wall_ : Tuple composé d'une _cellule_ et d'une _cardinalité_ - représente un mur dans l'algorithme de Kruskal  
_mapping_ : Retour de l'algorithme de résolution - Tuple de 3 éléments composé de :  
  Un tableau de tuples représentant les coordonnées des cellules de _path_   
  Un tableau de tuples représentant les coordonnées des cellules de _heatmap_    
  Une chaîne de caractère représentant la méthode de résolution : "RB" pour Recursive Backtracking , "ASTAR" pour A-star ou "COMAP" pour les deux simultanés  











