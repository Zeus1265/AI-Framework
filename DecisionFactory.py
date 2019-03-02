import random
#import  numpy as  np

class DecisionFactory:
    def __init__(self, name ='Davros'):
        self.name = name
        self.directions = ['wait', 'up', 'down', 'right', 'left']
        self.last_result = 'SUCCESS'
        self.last_direction = 'wait'
        self.map = [[-1, -1, -1],
                    [-1,  0, -1],
                    [-1, -1, -1]]
        self.location = [1, 1]
        #self.walls_hit = 0
        #self.move_mod = -1
        # Note : we have relativistic coordinates recorded here, since the map
        # self.state.pos = (0, 0)
    def get_decision(self, verbose = True):
        #made random walk to test map
        rng = int(random.random() * 4 + 1)
        self.last_direction = self.directions[rng]
        return self.last_direction

    def put_result(self, result):
        self.last_result = result.upper()
        x = self.location[0]
        y = self.location[1]
        if self.last_result == "WALL":
            #location should not change
            if self.last_direction == "up":
                self.map[y-1][x] = 1
            elif self.last_direction == "down":
                self.map[y+1][x] = 1
            elif self.last_direction == "right":
                self.map[y][x+1] = 1
            elif self.last_direction == "left":
                self.map[y][x-1] = 1
        else:
            #fill out map and update location
            if self.last_direction == "up":
                self.map[y-1][x] = 0
                self.location[1] -= 1
            elif self.last_direction == "down":
                self.map[y+1][x] = 0
                self.location[1] += 1
            elif self.last_direction == "right":
                self.map[y][x+1] = 0
                self.location[0] += 1
            elif self.last_direction == "left":
                self.map[y][x-1] = 0
                self.location[0] -= 1

            #add rows/cols to map if needed

            if self.location[0] == 0:
                #location and map must be shifted
                self.map.append([-1]*len(self.map[0]))
                for i in range(len(self.map)-1,0,-1):
                    self.map[i] = self.map[i-1]
                self.map[0] = [-1]*len(self.map[0])
                self.location[1] += 1
            elif self.location[0] == (len(self.map)-1):
                #shifting unnecessary
                self.map.append([-1]*len(self.map[0]))
            elif self.location[1] == 0:
                #location and map must be shifted
                for i in range(0, len(self.map)):
                    self.map[i].append(-1)

                for i in range(0, len(self.map)):
                    for j in range(len(self.map[0])-1, 0, -1):
                        self.map[i][j] = self.map[i][j-1]
                    self.map[i][0] = -1

                self.location[1] += 1
            elif self.location[1] == (len(self.map[0])-1):
                #shifting unnecessary
                for i in range(0, len(self.map)):
                    self.map[i].append(-1)
