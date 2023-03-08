from pyamaze import maze, agent
import numpy as np
# Macros
ROWS = COLS = 10
# dir = ['N', 'E', 'S', 'W']

m = maze(ROWS, COLS)
m.CreateMaze(loopPercent= 40)


def generatePop(popSize=500, endPoint=1, startPoint=COLS):
    genes = np.random.choice(range(1, ROWS + 1), size=(popSize, COLS - 2))
    genes = np.insert(genes, 0, endPoint, axis=1)
    genes = np.insert(genes, startPoint - 1, startPoint, axis=1)
    return genes


def geneToCoords(gene):
    coords = []
    for col in range(len(gene) - 1, 0, -1):
        rowDirection = -1 if gene[col] > gene[col-1] else 1
        coords.append((gene[col], col + 1))
        row = gene[col]
        while(row != gene[col-1]):
            row += rowDirection
            coords.append((row, col + 1))
    coords.append((1,1))
    return coords


def coordsToMap(coords):
    dir = []
    for i in range(len(coords) - 1):
        if   coords[i][0] > coords[i + 1][0]: dir.append('N') 
        elif coords[i][0] < coords[i + 1][0]: dir.append('S') 
        elif coords[i][1] > coords[i + 1][1]: dir.append('W') 
        elif coords[i][1] < coords[i + 1][1]: dir.append('E')
    dir.append('L')
    map = {coords[i] : dir[i] for i in range(len(coords))}
    return map



def geneToMap(gene):
    return coordsToMap(geneToCoords(gene))


def infSteps(gene, mazeMap):
    infStep = 0
    for key, value in gene.items():
        if value != 'L' and mazeMap[key][value] == 0:
            infStep += 1
    return infStep


def fitness(gene, mazeMap):
    return infSteps(geneToMap(gene), mazeMap)



def parent_slectoin_SUS(gen, maze_map):
    pass


def parentSlection(genes, mazeMap):
    contestants = genes[np.random.choice(len(genes), size = 4, replace= True)]
    pass

def crossover(genes, mazeMap):
    for j in range(0,len(genes) - 10, 2):
        crossoverPoint = np.random.randint(0, len(genes[0]))
        parent_one = parentSlection(genes, mazeMap)
        parent_two = parentSlection(genes, mazeMap)
        for i in range(crossoverPoint, len(genes[0])):
            parent_one[i], parent_two[i] = parent_two[i], parent_one[i]
        genes[j + 10] = parent_one
        genes[j + 11] = parent_two
    return genes


def mutation(pop, mutation_rate=0.6):
    for i in range(len(pop)):
        if np.random.random() > mutation_rate:
            pop[i][np.random.randint(1, COLS - 1)] = np.random.randint(1, ROWS)
    return pop


def checkSolution(genes, mazeMap):
    if fitness(genes[0], mazeMap) == 0: 
        return True
    return False


def solve():
    for i in range(500):
        gen = generatePop(500)
        print("gen >> ", i, "inf steps >>",  fitness(gen[0], m.maze_map))
        if checkSolution(gen, m.maze_map):
            path = geneToCoords(gen[0])
            return path
        gen = crossover(gen, m.maze_map)
        gen = mutation(gen)
    return geneToCoords(gen[0])

path = solve()

a = agent(m, footprints= True)
m.tracePath({a:path})
m.run()
