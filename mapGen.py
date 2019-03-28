import math
import random

#generators return tuples of (map, (player_x, player_y))

def mapPrint(map):
    for i in range(len(map)):
        print(map[i])

def type0(width, height):
    #Type 0 is completely empty with 4 exterior walls and a portal

    genMap = []

    for i in range(height):
        genMap.append([])
        for j in range(width):
            genMap[i].append(0)

    #mapPrint(genMap)
    #print('\n')
    for i in range(width):
        genMap[0][i] = 1
        genMap[-1][i] = 1

    #mapPrint(genMap)
    #print('\n')
    for i in range(height):
        genMap[i][0] = 1
        genMap[i][-1] = 1

    #mapPrint(genMap)

    portal_x = (int)(random.random()*(width-2)+1)
    portal_y = (int)(random.random()*(height-2)+1)

    genMap[portal_y][portal_x] = 2

    while True:
        player_x = (int)(random.random()*(width-2)+1)
        player_y = (int)(random.random()*(height-2)+1)

        if not (player_x == portal_x and player_y == portal_y):
            break

    return genMap, (player_x, player_y)

def type1(width, height):
    #Type 1 is mostly empty, with surrounding walls
    #and some interal walls
    return 0

def density_calc(map, width, height):
    sum = 0
    for i in range(height):
        for j in range(width):
            if map[i][j] == 0:
                sum += 1
    A = width * height * 1.

    return sum / A

def type2(width, height, density):
    #Type 2 is a maze-like
    #set of hallways
    
    Area = (width * height) * 1.

    genMap = []

    for i in range(height):
        genMap.append([])
        for j in range(width):
            genMap[i].append(1)

    portal_x = (int)(random.random()*(width-2)+1)
    portal_y = (int)(random.random()*(height-2)+1)

    
    while density_calc(genMap, width, height) < density:
        direction = (int)(random.random()*4)
        break

    return 0
