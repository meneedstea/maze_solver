import numpy as np
class pathSolver:
    popSize = 500
    def __init__(self, ROWS, maze_map):
        self.ROWS = self.COLS = ROWS
        self.mazeMap = maze_map
        self.gen = []
    def get_random_gen(self):
        self.gen = np.random.choice(range(1, self.ROWS + 1), size=(self.popSize, self.ROWS - 2))
        self.gen = np.insert(self.gen, 0, 1, axis=1)
        self.gen = np.insert(self.gen, self.ROWS - 1, self.ROWS, axis=1)
    def geneToCoords(self, gene):
        coords = []
        for col in range(len(gene) - 1, 0, -1):
            rowDirection = -1 if gene[col] > gene[col-1] else 1
            coords.append((gene[col], col + 1))
            row = gene[col]
            while (row != gene[col-1]):
                row += rowDirection
                coords.append((row, col + 1))
        coords.append((1, 1))
        return coords
    def coordsToMap(self, coords):
        dir = []
        for i in range(len(coords) - 1):
            if coords[i][0] > coords[i + 1][0]:
                dir.append('N')
            elif coords[i][0] < coords[i + 1][0]:
                dir.append('S')
            elif coords[i][1] > coords[i + 1][1]:
                dir.append('W')
            elif coords[i][1] < coords[i + 1][1]:
                dir.append('E')
        dir.append('L')
        map = {coords[i]: dir[i] for i in range(len(coords))}
        return map
    def geneToMap(self, gene):
        return self.coordsToMap(self.geneToCoords(gene))
    def infSteps(self, gene):
        infStep = 0
        for key, value in gene.items():
            if value != 'L' and self.mazeMap[key][value] == 0:
                infStep += 1
        return infStep
    def fitness(self, gene):
        return self.infSteps(self.geneToMap(gene))
    def sort_pop(self, genes):
        temp = list(genes)
        temp.sort(key=lambda x: self.fitness(x))
        genes = np.array(temp)
        return genes
    def parentSlection(self):
        contestants = self.gen[np.random.choice(
            len(self.gen), size=4, replace=True)]
        fittest = self.sort_pop(contestants)
        return fittest[0]
    def crossover(self):
        for j in range(0, len(self.gen) - 10, 2):
            crossoverPoint = np.random.randint(0, len(self.gen[0]))
            parent_one = self.parentSlection()
            parent_two = self.parentSlection()
            for i in range(crossoverPoint, len(self.gen[0])):
                parent_one[i], parent_two[i] = parent_two[i], parent_one[i]
            self.gen[j + 10] = parent_one
            self.gen[j + 11] = parent_two
    def mutation(self):
        for i in range(0, len(self.gen), 2):
            self.gen[i][np.random.randint(1, self.ROWS - 1)] = np.random.randint(1, self.ROWS)
    def checkSolution(self):
        return self.fitness(self.gen[0]) == 0
    def solve(self, maxIter=100):
        self.get_random_gen()
        for i in range(maxIter):
            self.gen = self.sort_pop(self.gen)
            # print(f"gen > {i}, fittest > {self.fitness(self.gen[0])}")
            if self.checkSolution():
                print("solution reached")
                return self.geneToCoords(self.gen[0])
            self.crossover()
            self.mutation()
        self.gen = self.sort_pop(self.gen)
        return self.geneToCoords(self.gen[0])
