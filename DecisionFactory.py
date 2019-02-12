import random
#import  numpy as  np

class DecisionFactory:
    def __init__(self, name ='Davros'):
        self.name = name
        self.directions = ['wait', 'up', 'down', 'right', 'left']
        self.last_result = 'Success'
        self.last_direction = 'wait'
        self.walls_hit = 0
        self.move_mod = -1
        # Note : we have relativistic coordinates recorded here, since the map
        # self.state.pos = (0, 0)
    def get_decision(self, verbose = True):
        if self.walls_hit is 0:
            self.last_direction = self.directions[2]
            return self.directions[2]
        elif self.walls_hit is 1:
            self.last_direction = self.directions[3]
            return self.directions[3]
        else:
            self.last_direction = self.climb()
            return self.last_direction

    def climb(self):
        if self.last_result is 'Wall' and self.walls_hit is not 2:
            self.move_mod = -1 * self.move_mod
            return self.directions[1]
        elif self.move_mod is -1:
            return self.directions[4]
        else:
            return self.directions[3]
    
    def put_result(self, result):
        self.last_result = result
        if result is 'Wall':
            self.walls_hit += 1
