from pyamaze import maze, agent
import numpy as np
# Macros
ROWS = COLS = 8
# dir = ['N', 'E', 'S', 'W']

m = maze(ROWS, COLS)
m.CreateMaze(loopPercent= 40)


def generatePop(popSize=400, endPoint=1, startPoint=COLS):
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
def sort(genes, mazeMap):
    temp = list(genes)
    temp.sort(key = lambda x: fitness(x, mazeMap))
    genes = np.array(temp)
    return genes
def parentSlection(genes, mazeMap):
    contestants = genes[np.random.choice(len(genes), size = 4, replace= True)]
    fittest = sort(contestants, mazeMap)
    return fittest[0]
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
def mutation(genes, mutation_rate=5):
    for i in range(1, len(genes), 2):
        genes[i][np.random.randint(1, COLS)] = np.random.randint(1, ROWS)
        genes[i][np.random.randint(1, COLS)] = np.random.randint(1, ROWS)
    return genes
def checkSolution(genes, mazeMap):
    if fitness(genes[0], mazeMap) == 0: 
        return True
    return False
# main
def solve():
    path = []
    for i in range(500):
        gen = generatePop(100)
        gen = sort(gen, m.maze_map)
        print("gen >> ", i, fitness(gen[0], m.maze_map))
        if checkSolution(gen, m.maze_map):
            path = geneToCoords(gen[0])
            return path
        gen = crossover(gen, m.maze_map)
        gen = mutation(gen)

# path = solve()
gen = generatePop()
gen[0] = np.array([1, 7, 8, 7, 6, 4, 3, 8])
path = geneToCoords(gen[0])


a = agent(m)
m.tracePath({a:path})
m.run()
