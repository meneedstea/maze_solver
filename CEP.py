import random
from pyamaze import maze, agent
import time
from os import system


class MazeSolver:
    def __init__(self, parent_maze, pop_size=500):
        self.pop_size = pop_size
        self.ROWS = parent_maze.rows
        self.COLS = parent_maze.cols
        self.maze_map = parent_maze.maze_map
        self.goal = parent_maze._goal
        self.begin = (self.ROWS, self.COLS)

    
    def remove_overlap(self, path: list):
        new_path = [path[0]]
        i = 0
        while i < len(path) - 1:
            i += 1  
            if path[i] in path[i + 1:]:  
                i = path.index(path[i], i + 1)
            new_path.append(path[i])
        return new_path

    def generate_st_path(self, start: tuple, end: tuple):
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

    def generate_path(self):
        path = [self.begin]
        while path[-1] != self.goal:
            row, col = path[-1]
            next_coords = []
            if row > 1:           next_coords.append((row-1, col))   # North
            if row < self.ROWS-1: next_coords.append((row+1, col))   # South
            if col > 1:           next_coords.append((row, col-1))   # West
            if col < self.COLS-1: next_coords.append((row, col+1))   # East
            next_coords = [coord for coord in next_coords if coord not in path]
            if not next_coords: path = [self.begin]
            else:
                next_coord = random.choice(next_coords)
                path.append(next_coord)
        return path

    def generate_population(self):
        return [self.generate_path() for _ in range(self.pop_size)]

    def infeasible_steps(self, path):
        path_map = {}
        for i in range(len(path) - 1):
            row, col = path[i]
            next_row, next_col = path[i + 1]
            if   row > next_row: dir = 'N'
            elif row < next_row: dir = 'S'
            elif col > next_col: dir = 'W'
            elif col < next_col: dir = 'E'
            path_map[path[i]] = dir
        inf_steps = 0
        for coord, dir in path_map.items():
            if self.maze_map[coord][dir] == 0: inf_steps += 1
        return inf_steps
        
    def crossover(self, parent_one: list, parent_two: list):
        length = min(len(parent_one), len(parent_two))
        cut_point = random.randint(2, length - 2)
        child_one = parent_one[:cut_point]
        child_two = parent_two[:cut_point]
        child_one_mp = self.generate_st_path(parent_one[cut_point], parent_two[cut_point + 1])
        child_two_mp = self.generate_st_path(parent_two[cut_point], parent_one[cut_point + 1])
        child_one.extend(child_one_mp)
        child_two.extend(child_two_mp)
        child_one.extend(parent_two[cut_point:])
        child_two.extend(parent_one[cut_point:])
        return self.remove_overlap(child_one), self.remove_overlap(child_two)

    def mutate_path(self, path: list):
        new_path = []
        mut_idx = random.randint(2, len(path) - 2)
        new_path = path[:mut_idx]
        old_row, old_col = path[mut_idx]
        margin = random.randint(2, 4)
        row_rg_min ,row_rg_max = old_row - margin, old_row + margin
        col_rg_min ,col_rg_max = old_col - margin, old_col + margin
        if row_rg_min < 1 : row_rg_min = old_row
        if row_rg_max > self.ROWS: row_rg_max = old_row
        if col_rg_min < 1 : col_rg_min = old_col
        if col_rg_max > self.COLS: col_rg_max = old_col
        new_coord = ((random.randint(row_rg_min, row_rg_max), random.randint(col_rg_min, col_rg_max)))
        prev_seg = self.generate_st_path(path[mut_idx - 1], new_coord)
        next_seg = self.generate_st_path(new_coord, path[mut_idx + 1])
        new_path.extend(prev_seg)
        new_path.extend(next_seg)
        new_path.extend(path[mut_idx + 1:])
        return self.remove_overlap(new_path)

    def crossover_pop(self):
        for i in range(int(self.pop_size/10), self.pop_size, 2):
            parent_one = self.population[random.randint(0, self.pop_size/2)]
            parent_two = self.population[random.randint(0, self.pop_size/2)]
            child_one, child_two = self.crossover(parent_one, parent_two)
            self.population[i] = child_one
            self.population[i + 1] = child_two

    def mutate_pop(self, mutation_rate=0.5):
        for i in range(0, self.pop_size):
            if random.random() < mutation_rate:
                self.population[i] = self.mutate_path(self.population[i])

    def solve(self):
        self.population = self.generate_population()
        start_time = time.time()
        while time.time() - start_time <= 20:
            self.population = sorted(self.population, key=lambda x: self.infeasible_steps(x))
            system("cls")
            print("time elapsed: %.4s seconds " % (time.time() - start_time))
            print(f"minimum inf steps : {self.infeasible_steps(self.population[0])}")
            if self.infeasible_steps(self.population[0]) == 0: 
                return self.population[0]
            self.crossover_pop()
            self.mutate_pop()
        self.solve()

def main():
    m = maze(8,8)
    m.CreateMaze(loopPercent=0)
    solution = MazeSolver(m)
    path = solution.solve()
    a = agent(m, footprints=True, shape="arrow")
    m.tracePath({a:path}, delay=50)
    m.run()

main()