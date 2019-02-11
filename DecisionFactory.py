import random
#import  numpy as  np

class DecisionFactory:
    def __init__(self, name ='Davros'):
        self.name = name
        self.directions = ['wait', 'up', 'down', 'right', 'left']
        self.last_result = 'success'
        self.last_direction = 'wait'
        # Note : we have relativistic coordinates recorded here, since the map
        # self.state.pos = (0, 0)
    def get_decision(self, verbose = True):
        return self.random_direction()

    def random_direction(self):
        #r = random . randint (0 ,4) # Includes  wait  state
        r = random.randint (1 ,4)  # Does NOT include  wait  state
        # Update  last direction  to  be  the  one  just  selected:
        self.last_direction = self.directions[r]
        return self.directions[r]

    def put_result(self, result):
        self.last_result = result
