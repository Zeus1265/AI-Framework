import random
import math
import DFNN
import numpy as np

class DecisionFactory:
    

    def __init__(self, nn, name ='Bastard man'):
        self.name = name
        self.directions = ['wait', 'up', 'down', 'right', 'left']
        self.last_result = 'SUCCESS'
        self.last_direction = 'wait'

        self.neural_net = nn
    
        self.sight = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

        self.invert = {
                'up': 'down',
                'down': 'up',
                'left': 'right',
                'right': 'left' }

        self.inverse = {
                'wait': 0,
                'up': 1,
                'down': 2,
                'right': 3,
                'left': 4 }

        self.follow_instructions = False

    def get_decision(self, verbose = True):
        ul = self.sight[0][0]
        uc = self.sight[0][1]
        ur = self.sight[0][2]
        cl = self.sight[1][0]
        #cc = self.sight[1][1] NOT NEEDED
        cr = self.sight[1][2]
        dl = self.sight[2][0]
        dc = self.sight[2][1]
        dr = self.sight[2][2]
        
        direct = self.inverse[self.last_direction]

        res = 0
        if self.last_result == 'WALL':
            res = 0
        else:
            res = 1

        vect = np.transpose(np.matrix([ul, uc, ur, cl, cr, dl, dc, dr, direct, res], dtype=np.float64))

        result = self.neural_net.compute(vect)
        #print self.directions[result]
        self.last_direction = self.directions[result]

        #print self.last_direction
        return self.last_direction

    def put_result(self, result):
        self.last_result = result.upper()

    def pass_sight(self, array):
        for i in range(3):
            for j in range(3):
                self.sight[i][j] = array[i][j]
