from pyamaze import maze, agent
import numpy as np
import time
from os import system
from functools import wraps


# >TODO: implement rectangular grid
#TODO: implement orientation
#TODO: optimize code
#TODO: comment the whole code
#TODO: factor the length in the slection
#TODO: introduce elitism // should you??

COLS = 5
ROWS = 9
pop_size = 1000

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

def generateRandomPopulation():
    dir_bits = np.random.randint(2, size=(pop_size, 1))                 # random direction bits
    pop = np.random.randint(1, ROWS, size=(pop_size, COLS - 2))     # random path (cols first)  
    pop = np.insert(pop, 0, 1, axis=1)                          # initialize end point
    pop = np.insert(pop, COLS - 1, ROWS, axis=1)                 # initialize start point
    pop = np.append(dir_bits, pop, axis=1)                              # join dir bits and path
    # ort_bits = np.random.randint(2, size=(pop_size,1))          
    # pop = np.append(pop, ort_bits, axis=1)
    return pop


def chrToCoords(chr):
    coords = []
    for col in range(COLS, 1, -1):
        row_direction = -1 if chr[col] >= chr[col - 1] else 1
        if chr[0] == 1:
            coords.append((chr[col], col))
            for row in range(chr[col], chr[col - 1], row_direction):
                coords.append((row, col - 1))
        else:
            for row in range(chr[col], chr[col - 1], row_direction):
                coords.append((row, col))
            coords.append((chr[col - 1], col))
    coords.append((1,1))
    return coords


def coordsToDir(coords):
    map = {}
    for i in range(len(coords) - 1):
        if   coords[i][0] > coords[i + 1][0]: dir = 'N' 
        elif coords[i][0] < coords[i + 1][0]: dir = 'S' 
        elif coords[i][1] > coords[i + 1][1]: dir = 'W' 
        elif coords[i][1] < coords[i + 1][1]: dir = 'E'
        map[coords[i]] = dir
    return map

def getMap(chr):
    return coordsToDir(chrToCoords(chr))

def infeasibleSteps(path_map, maze_map):
    inf_steps = 0
    for coord, dir in path_map.items():
        if maze_map[coord][dir] == 0:
            inf_steps += 1
    return inf_steps


def getFitness(chr,maze_map):
    path_map = getMap(chr)
    return 99 - infeasibleSteps(path_map, maze_map)

def getFitnessArr_s(pop, maze_map):
    f = lambda i, j : getFitness(pop[int(i)], maze_map)
    fitness_arr = np.fromfunction(f, shape=(pop_size, 1), dtype=np.int32)
    return fitness_arr
def getFitnessArr_g(pop, maze_map):
    return np.array([getFitness(pop[i], maze_map) for i in range(pop_size)])

def getFitnessArr_r(pop, maze_map):
    return np.fromiter([getFitness(pop[i], maze_map) for i in range(pop_size)] , dtype=np.int32)

def getFitnessArr_z(pop, maze_map):
    return [getFitness(pop[i], maze_map) for i in range(pop_size)]

def parentSlection(pop, fitness_arr, num_parents=25):
    sum_fitness = np.sum(fitness_arr)
    cum_fitness = [sum(fitness_arr[:i+1]) for i in range(len(fitness_arr))]
    pointer_distance = sum_fitness / num_parents
    start = np.random.uniform(0, pointer_distance)
    parents = np.empty((num_parents, COLS + 1 ), dtype=int)
    for i in range(num_parents):
        position = start + i * pointer_distance
        j = 0
        while cum_fitness[j] < position:
            j += 1
        parents[i] = pop[j]
    return parents

def crossover(pop, fitness_arr, maze_map):
    parents = parentSlection(pop, fitness_arr)
    def offSpring():
        cut_point = np.random.randint(2, COLS - 1)
        parent_one = parents[np.random.randint(len(parents))]
        parent_two = parents[np.random.randint(len(parents))]
        for i in range(0, cut_point):
            parent_one[i], parent_two[i] = parent_two[i], parent_one[i]
        return parent_one, parent_two
    new_pop = np.empty((pop_size, COLS + 1), dtype=int)
    for i in range(0,len(pop), 2):
        off_springs = offSpring()
        new_pop[i] = off_springs[0]
        new_pop[i + 1] = off_springs[1]
    return new_pop

def mutation(pop , mutation_rate = 0.5):
    for i in range(len(pop)):
        if np.random.random() < mutation_rate:
            pop[i][np.random.randint(2, COLS)] = np.random.randint(1, ROWS)
        if np.random.random() < 0.1:
            pop[i][0] = 1 - pop[i][0]
    return pop

def solve(maze_map):
    start_time = time.time()
    pop = generateRandomPopulation()
    for gen in range(1000):
        system("cls")
        print("time elapsed: %.4s seconds " % (time.time() - start_time))
        fitness_arr = getFitnessArr_z(pop, maze_map)
        if max(fitness_arr) == 99:
            print(f"solution found in {gen} th generation")
            print(pop[0])
            sol = list(fitness_arr)
            idx = sol.index(max(sol))
            return chrToCoords(pop[idx])
        pop = crossover(pop, fitness_arr, maze_map)
        pop = mutation(pop)

def main():
    m = maze(ROWS, COLS)
    m.CreateMaze(loopPercent=90)
    a = agent(m, footprints=True)
    path = solve(m.maze_map)
    m.tracePath({a:path})
    m.run()

def test():
    m = maze(ROWS, COLS)
    m.CreateMaze()
    gen = generateRandomPopulation()
    arr_z = getFitnessArr_z(gen, m.maze_map)
    arr_z.sort(reverse=True)
    print(arr_z)
#0.0098 -> smeksy method

if __name__ == '__main__':
    main()
    # test()