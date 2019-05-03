import math
import random

#generators return tuples of (map, (player_x, player_y))

def mapPrint(map):
    for i in range(len(map)):
        print(map[i])

def mapToFile(genMap, player_init, fileName):
    f = open(fileName, 'w')
    f.write(str(player_init[0]) + ' ' + str(player_init[1]) + '\n')
    for row in genMap:
        f.write(str(row)+'\n')

def fileToMap(fileName):
    f = open(fileName, 'r')
    string_f = f.read()
    map_flag = True
    val = 'x'
    player_x = 0
    player_y = 0
    genMap = []
    row = -1
    for i in range(len(string_f)):
        if map_flag:
            if string_f[i] == '\n':
                map_flag = False
            elif string_f[i] == ' ':
                val = 'y'
            else:
                if val == 'x':
                    player_x *= 10
                    player_x += (int)(string_f[i])
                else:
                    player_y *= 10
                    player_y += (int)(string_f[i])
        else:
            if string_f[i] == '[':
                genMap.append([])
                row += 1
            if (string_f[i] == '1') or (string_f[i] == '0') or (string_f[i] == '2'):
                genMap[row].append((int)(string_f[i]))

    return genMap, (player_x, player_y)

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

    d = sum / A
    print 'Current density {}'.format(d)
    return d

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

    internal_w = width - 2
    internal_h = height - 2
    root = [0, 0] #where chains are started
    genMap[portal_y][portal_x] = 0
    open_space = 1
    while (open_space*1./Area) < density:
        #print('Current density: {}'.format(density_calc(genMap, width, height)))
        while True:
            row = (int)(random.random()*internal_h)+1
            col = (int)(random.random()*internal_w)+1

            if genMap[row][col] == 0:
                root[0] = col
                root[1] = row
                break
        direction = (int)(random.random()*4)
        #print('Root point: {}'.format(root))
        #print('Direction {}'.format(direction))
        #print('Current map:')
        #for i in genMap:
        #    print(i)
        if direction == 0:
            #up
            max_dist = root[1] 
            length = (int)(random.random()*max_dist)+1
            for i in range(length):
                try:
                    if genMap[root[1]-i][root[0]] == 1:
                        open_space += 1
                    genMap[root[1]-i][root[0]] = 0
                except IndexError:
                    print('Index Error at [{},{}] in direction: {} with chain length {}'.format(root[1],root[0],direction,length))
                    raise
        elif direction == 1:
            #down
            max_dist = internal_h - root[1] + 1
            length = (int)(random.random()*max_dist)+1
            for i in range(length):
                try:
                    if genMap[root[1]+i][root[0]] == 1:
                        open_space += 1
                    genMap[root[1]+i][root[0]] = 0
                except IndexError:
                    print('Index Error at [{},{}] in direction: {} with chain length {}'.format(root[1],root[0],direction,length))
        elif direction == 2:
            #pos x
            max_dist = internal_w - root[0] + 1
            length = (int)(random.random()*max_dist)+1
            for i in range(length):
                try:
                    if genMap[root[1]][root[0]+1] == 1:
                        open_space += 1
                    genMap[root[1]][root[0]+i] = 0
                except IndexError:
                    print('Index Error at [{},{}] in direction: {} with chain length {}'.format(root[1],root[0],direction,length))
        else:
            #neg x
            max_dist = root[0]
            length = (int)(random.random()*max_dist)+1
            for i in range(length):
                try:
                    if genMap[root[1]][root[0]-i] == 1:
                        open_space += 1
                    genMap[root[1]][root[0]-i] = 0
                except IndexError:
                    print('Index Error at [{},{}] in direction: {} with chain length {}'.format(root[1],root[0],direction,length))

        #print 'Current density: {}'.format(open_space/Area)
    player_x = 0
    player_y = 0
    while True:
        player_x = (int)(random.random()*internal_w)+1
        player_y = (int)(random.random()*internal_h)+1
        if genMap[player_y][player_x] == 0:
            break

    genMap[portal_y][portal_x] = 2
    return genMap, (player_x, player_y)
