from util import *

N = 75
filename = f"loopy{N}"
maze = Maze(N,filename)
maze.kruskal_generate()
for i in range(N):
    maze.break_random_wall()
start = time.time()
astar_mapping = maze.astar_solving_map()
end = time.time()
print(f"Astar running time : {end-start}")
start = time.time()
rb_mapping = maze.backtrack_solving_map()
end = time.time()
print(f"Recursive Backtracking running time : {end-start}")
maze.create_file()
maze.solving_display( astar_mapping , rb_mapping , animate=True)
