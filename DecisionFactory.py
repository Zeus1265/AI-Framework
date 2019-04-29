import random
import math
#import  numpy as  np

class DecisionFactory:
    

    def __init__(self, name ='Bad man'):
        self.name = name
        self.directions = ['wait', 'up', 'down', 'right', 'left']
        self.last_result = 'SUCCESS'
        self.last_direction = 'wait'

        self.sight = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

        self.invert = {
                'up': 'down',
                'down': 'up',
                'left': 'right',
                'right': 'left' }

        self.follow_instructions = False

    def get_decision(self, verbose = True):
        self.last_direction = self.directions[(int)(random.random()*4)+1]
        return self.last_direction

    def put_result(self, result):
        self.last_result = result.upper()

    def pass_sight(self, array):
        for i in range(3):
            for j in range(3):
                self.sight[i][j] = array[i][j]
