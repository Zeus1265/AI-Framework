import framework
import DecisionFactory
import DFNN
import mapGen

import math

factories = []

for x in range(50):
    nn = DFNN.DFNN(10, [20, 20, 20, 30, 30, 20, 20, 20, 15, 4], rando=True)
    factories.append(DecisionFactory.DecisionFactory(nn, 'Reproduction machine')) 

for x in range(1000):
    maps = []
    move_totals = []
    maze_success = 0
    for l in range(10):
        map_combo = mapGen.type2(5,5,.4)
        maps.append(map_combo)

    best_moves = float('Inf')
    for i in range(50):
        sum_moves = 0
        num_inf = 0

        df = factories[i]

        for j in range(10):
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
        for i in range(9):
            factories.append(DecisionFactory.DecisionFactory(n.replicate()))
