from pyamaze import maze, agent
import numpy as np

COLS = 8
pop_size = 500

def randomPop(pop_size=10, end_point=1, start_point=COLS):
    dir_bits = np.random.randint(2, size=(pop_size, 1))
    pop = np.random.randint(1, COLS + 1, size=(pop_size, COLS - 2)) 
    pop = np.insert(pop, 0, end_point, axis=1)                  
    pop = np.insert(pop, COLS - 1, start_point, axis=1)          
    pop = np.append(dir_bits, pop, axis=1)
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


def infSteps(path_map, maze_map):
    inf_steps = 0
    for coord, dir in path_map.items():
        if maze_map[coord][dir] == 0:
            inf_steps += 1
    return inf_steps


def fitness(path_map,maze_map):
    return 999 - infSteps(path_map, maze_map)

def calculate_fitness(pop, maze_map):
    fitness_arr = np.empty(0, dtype=int)
    for i in range(len(pop)):
        fitness_arr = np.append(fitness_arr, fitness(coordsToDir(chrToCoords(pop[i])), maze_map))
    return fitness_arr

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

def crossover(pop, fitness_arr):
    parents = parentSlection(pop, fitness_arr)
    def offSpring():
        cut_point = np.random.randint(1, COLS - 1)
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

def mutation(pop, mutation_rate = 0.5):
    for i in range(len(pop)):
        if np.random.random() < mutation_rate:
            pop[i][np.random.randint(2, COLS)] = np.random.randint(1, COLS)
        if np.random.random() < 0.1:
            pop[i][0] = 1 - pop[i][0]
    return pop

def solve(maze_map):
    pop = randomPop(500)
    for gen in range(1000):
        fitness_arr = calculate_fitness(pop, maze_map)
        if max(fitness_arr) == 999:
            print(gen)
            sol = list(fitness_arr)
            idx = sol.index(max(sol))
            return chrToCoords(pop[idx])
        pop = crossover(pop, fitness_arr)
        pop = mutation(pop)

def main():
    m = maze(COLS, COLS)
    m.CreateMaze(loopPercent=30)
    a = agent(m, footprints=True)

    path = solve(m.maze_map)
    m.tracePath({a:path})
    m.run()



if __name__ == '__main__':
    main()