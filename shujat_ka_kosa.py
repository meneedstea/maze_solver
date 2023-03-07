from pyamaze import maze, agent
import random

gen = []
ROWS = 5
pop_size = 10

def generate_random():
    # index is column number and value is row number
    for i in range(pop_size):
        gen.append([])
        for j in range(ROWS):
            gen[i].append(random.randint(1, ROWS))  # appending random steps
        gen[i][0] = ROWS   # initialize starting point
        gen[i][ROWS - 1] = 1     # initialize ending point

def geneToCoords(chr):
    coords = []
    for i in range(len(chr) - 1, 0 , -1):
        coords.append((chr[i], i + 1))
        row_direction = 1 if chr[i] < chr[i + 1] else -1
        start = chr[i]
        while(start != chr[i + 1]):
            start += row_direction
            coords.append((start, i + 1))
        coords.reverse()
    coords.append((1, 1))
    return coords


def coordsToDir(coords):
    map = {}
    for i in range(len(coords) - 1):
        if coords[i][0] > coords[i + 1][0]: dir = 'N'       
        elif coords[i][0] < coords[i + 1][0]: dir = 'S'       
        elif coords[i][1] > coords[i + 1][1]: dir = 'W'       
        elif coords[i][1] < coords[i + 1][1]: dir = 'E' 
        map[coords[i]] = dir
    return map

generate_random()
gen[0] = [1, 2, 3, 4, 5]

m = maze(ROWS, ROWS)
m.CreateMaze()
a = agent(m , footprints= True)
path = geneToCoords(gen[0])
# path = path.reverse()
print(path)
print(type(path))
m.tracePath({a:path})
m.run()
