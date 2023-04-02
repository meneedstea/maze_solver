from pyamaze import maze, agent
import random
from os import system
import time

ROWS = 10
COLS = 10

def RemoveOverlap(path: list):
    new_path = [path[0]]
    i = 0
    while i < len(path) - 1:
        i += 1  
        if path[i] in path[i + 1:]:  
            i = path.index(path[i], i + 1)
        new_path.append(path[i])
    return new_path

def generate_st_path(start: tuple, end: tuple):
    path = [start]
    start_y , start_x = start
    end_y , end_x = end
    row_dir = -1 if start_y > end_y else 1
    col_dir = -1 if start_x > end_x else 1
    while start_x != end_x:
        start_x += col_dir
        path.append((start_y, start_x))
    while start_y != end_y:
        start_y += row_dir
        path.append((start_y, start_x))
    return path



def generate_path(start: tuple, end: tuple):
    path = [start]
    while path[-1] != end:
        row, col = path[-1]
        next_coords = []
        if row > 1:      next_coords.append((row-1, col))   # North
        if row < ROWS-1: next_coords.append((row+1, col))   # South
        if col > 1:      next_coords.append((row, col-1))   # West
        if col < COLS-1: next_coords.append((row, col+1))   # East
        next_coords = [coord for coord in next_coords if coord not in path]
        if not next_coords: path = [start]
        else:
            next_coord = random.choice(next_coords)
            path.append(next_coord)
    return path


def generate_population(pop_size, start, end):
    pop = [generate_path(start, end) for _ in range(pop_size)]
    return pop


def coords_to_map(path):
    map = {}
    for i in range(len(path) - 1):
        row, col = path[i]
        next_row, next_col = path[i + 1]
        if   row > next_row: dir = 'N'
        elif row < next_row: dir = 'S'
        elif col > next_col: dir = 'W'
        elif col < next_col: dir = 'E'
        map[path[i]] = dir
    return map


def infeasible_steps(path, maze_map):
    path_map = coords_to_map(path)
    inf_steps = 0
    for coord, dir in path_map.items():
        if maze_map[coord][dir] == 0: inf_steps += 1
    return inf_steps
    
def crossover(parent_one: list, parent_two: list):
    length = min(len(parent_one), len(parent_two))
    cut_point = random.randint(2, length - 2)
    child_one = parent_one[:cut_point]
    child_two = parent_two[:cut_point]
    child_one_mp = generate_st_path(parent_one[cut_point], parent_two[cut_point + 1])
    child_two_mp = generate_st_path(parent_two[cut_point], parent_one[cut_point + 1])
    child_one.extend(child_one_mp)
    child_two.extend(child_two_mp)
    child_one.extend(parent_two[cut_point:])
    child_two.extend(parent_one[cut_point:])
    return RemoveOverlap(child_one), RemoveOverlap(child_two)

def mutate_path(path: list):
    new_path = []
    mut_idx = random.randint(2, len(path) - 2)
    new_path = path[:mut_idx]
    old_row, old_col = path[mut_idx]
    margin = random.randint(2, 4)
    row_rg_min ,row_rg_max = old_row - margin, old_row + margin
    col_rg_min ,col_rg_max = old_col - margin, old_col + margin
    if row_rg_min < 1 : row_rg_min = old_row
    if row_rg_max > ROWS: row_rg_max = old_row
    if col_rg_min < 1 : col_rg_min = old_col
    if col_rg_max > COLS: col_rg_max = old_col
    new_coord = ((random.randint(row_rg_min, row_rg_max), random.randint(col_rg_min, col_rg_max)))
    prev_seg = generate_st_path(path[mut_idx - 1], new_coord)
    next_seg = generate_st_path(new_coord, path[mut_idx + 1])
    new_path.extend(prev_seg)
    new_path.extend(next_seg)
    new_path.extend(path[mut_idx + 1:])
    return RemoveOverlap(new_path)

def crossover_pop(pop: list):
    new_pop = []
    for i in range(0, len(pop) - int(len(pop)/10) , 2):
        child_one, child_two = crossover(pop[random.randint(0, int(len(pop)/3))], pop[random.randint(0, int(len(pop)/3))])
        new_pop.append(child_one)
        new_pop.append(child_two)
    pop[int(len(pop)/10):] = new_pop
    return pop

def mutate_pop(pop: list, mutation_rate=0.5):
    for i in range(0, len(pop)):
        if random.random() < mutation_rate:
            pop[i] = mutate_path(pop[i])
            pop[i] = mutate_path(pop[i])
    return pop

def main():
    pop_size = 500
    start = (ROWS, COLS)     
    end = (1, 1)             
    m = maze(ROWS, COLS)
    m.CreateMaze(loopPercent=0)
    a = agent(m, footprints=True, filled=False, shape="arrow")
    maze_map = m.maze_map
    gen = generate_population(pop_size, start, end)
    inf = lambda x: infeasible_steps(x, maze_map)
    MAX_ITER = 0
    start_time = time.time()
    # main loop
    for t in range(MAX_ITER):
        system("cls")
        gen.sort(key=inf, reverse=False) 
        print("genertion : ", t, "infsteps :", infeasible_steps(gen[0], maze_map))
        print("time elapsed: %.4s seconds " % (time.time() - start_time))
        if infeasible_steps(gen[0], maze_map) == 0: break
        gen = crossover_pop(gen)
        gen = mutate_pop(gen, 0.5)
    gen.sort(key=inf, reverse=False) 
    path = gen[0]
    m.tracePath({a: path}, delay=50)
    m.run()
    return




if __name__ == '__main__':
    main()
