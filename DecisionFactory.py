import random
import math
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
        self.closest_unknown = [[]]
        self.closest_unknown_distance = 99999
        #self.walls_hit = 0
        #self.move_mod = -1
        # Note : we have relativistic coordinates recorded here, since the map
        # self.state.pos = (0, 0)

    def distance(self, player, location):
        return math.sqrt(math.pow(location[0] - player[0], 2) + math.pow(location[1] - player[1], 2))

    def dir_chooser(self, player, location):
        if math.fabs(location[0] - player[0]) > math.fabs(location[1] - player[1]):
            if location[0] > player[0]:
                dir = 3
            elif location[0] < player[0]:
                dir = 4
            else:
                dir = int(random.random()) + 3
        elif math.fabs(location[0] - player[0]) < math.fabs(location[1] - player[1]):
            if location[1] > player[1]:
                dir = 2
            elif location[1] < player[1]:
                dir = 1
            else:
                dir = int(random.random())+1
        else:
            dir = int(random.random() * 4) + 1
        return dir

    def get_decision(self, verbose = True):
        self.closest_unknown = []
        for i in range(0, len(self.map)):
            for j in range(0, len(self.map[0])):
                if self.map[i][j] == -1:
                    left_w = True
                    right_w = True
                    top_w = True
                    bot_w = True
                    #don't check edges
                    if i != 0:
                        left_w = (self.map[i-1][j] == 1)
                    if i != len(self.map)-1:
                        right_w = (self.map[i+1][j] == 1)
                    if j != 0:
                        top_w = (self.map[i][j-1] == 1)
                    if j != len(self.map[0])-1:
                        bot_w = (self.map[i][j+1] == 1)

                    if self.closest_unknown == []:
                        if not (left_w and right_w and top_w and bot_w):
                            self.closest_unknown.append([j,i])
                            self.closest_unknown_distance = self.distance(self.location, self.closest_unknown[0])
                    else:
                        if not (left_w and right_w and top_w and bot_w):
                            if self.distance(self.location, [j,i]) == self.closest_unknown_distance:
                                self.closest_unknown.append([j,i])
                            elif self.distance(self.location, [j,i]) < self.closest_unknown_distance:
                                self.closest_unknown = []
                                self.closest_unknown.append([j,i])
                                self.closest_unknown_distance = self.distance(self.location, self.closest_unknown[0])
        
        print self.closest_unknown
        if len(self.closest_unknown) > 0:
            index = int(random.random() * len(self.closest_unknown))
        else:
            index = 0
        
        print self.closest_unknown[index]
        dir = self.dir_chooser(self.location, self.closest_unknown[index])

        self.last_direction = self.directions[dir]
        print self.last_direction
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

            if self.location[1] == 0:
                #location and map must be shifted
                self.map.append([-1]*len(self.map[0]))
                for i in range(len(self.map)-1,0,-1):
                    self.map[i] = self.map[i-1]
                self.map[0] = [-1]*len(self.map[0])
                self.location[1] += 1
            elif self.location[1] == (len(self.map)-1):
                #shifting unnecessary
                self.map.append([-1]*len(self.map[0]))
            elif self.location[0] == 0:
                #location and map must be shifted
                for i in range(0, len(self.map)):
                    self.map[i].append(-1)

                for i in range(0, len(self.map)):
                    for j in range(len(self.map[0])-1, 0, -1):
                        self.map[i][j] = self.map[i][j-1]
                    self.map[i][0] = -1

                self.location[0] += 1
            elif self.location[0] == (len(self.map[0])-1):
                #shifting unnecessary
                for i in range(0, len(self.map)):
                    self.map[i].append(-1)
        for i in range(0, len(self.map)):
            print self.map[i]
        print self.location
