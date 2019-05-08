import framework
import DecisionFactory
import DFNN
import mapGen

import math

NUM_DF = 250
NUM_GEN = 1000
NUM_MAP = 100

factories = []

for x in range(NUM_DF):
    nn = DFNN.DFNN(4, [20, 15, 10, 4], rando=True)
    factories.append(DecisionFactory.DecisionFactory(nn, 'Reproduction machine')) 

maps = []
for l in range(NUM_MAP):
    map_combo = mapGen.type2(20,20,.4)
    maps.append(map_combo)

for x in range(NUM_GEN):
    move_totals = []
    maze_success = 0

    best_moves = float('Inf')
    for i in range(NUM_DF):
        sum_moves = 0
        num_inf = 0

        df = factories[i]

        for j in range(NUM_MAP):
            map_combo = maps[j]
            moves = framework.run_maze(df, map_combo, GRAPHICS = False)
            
            if moves == float('Inf'):
                num_inf += 1
            else:
                maze_success += 1
                sum_moves += moves
        if num_inf < 10 and float(sum_moves)/(10-num_inf) < best_moves:
            best_moves = sum_moves

        #print 'DF{} finished {} times, and took {} moves total'.format(i, 10-num_inf, sum_moves)
        move_totals.append((num_inf, sum_moves))

    print 'Gen {} finished'.format(x+1)

    #find top 5 nn
    top_index = []
    for m in range(5):
        mini = m
        min = move_totals[m]
        k = 0
        for n in move_totals:
            if min[0] >= n[0] and min[1] > n[1]:
                mini = k
                min = n
            k += 1
        top_index.append(mini)
        move_totals.remove(min)

    print 'Best moves from this generation is {}'.format(best_moves)
    print 'Number of mazes cleared: {}'.format(maze_success)

    top_nns = []
    for i in top_index:
        top_nns.append(factories[i].neural_net)
    factories = []

    for n in top_nns:
        factories.append(DecisionFactory.DecisionFactory(n))
        for i in range(NUM_DF/5 - 1):
            factories.append(DecisionFactory.DecisionFactory(n.replicate()))
