import random
import math
#import  numpy as  np

class DecisionFactory:

    class Backtrack_Obj:
        def __init__(self, direction):
            self.count = 1
            self.dir = direction
            #self.phase = []

        def __str__(self):
            ret = '[Direction: ' + self.dir + ', count: {}]'.format(self.count) 
            return ret


    def __init__(self, name ='Bad man'):
        self.name = name
        self.directions = ['wait', 'up', 'down', 'right', 'left']
        self.last_result = 'SUCCESS'
        self.last_direction = 'wait'
        self.back_track = False
        
        self.backtrack_stack = []
        
        self.map = [ [-1, -1, -1],
                     [-1,  0, -1],
                     [-1, -1, -1] ]
        self.location = [1, 1]

        self.invert = {
                'up': 'down',
                'down': 'up',
                'left': 'right',
                'right': 'left' }

        self.follow_instructions = False

    def dirToInd(self, dir):
        if dir == 'up':
            return 1
        elif dir == 'down':
            return 2
        elif dir == 'right':
            return 3
        elif dir == 'left':
            return 4
        return 0
    
    def backtrack(self):
        stack_dir = self.backtrack_stack[-1].dir
        ret_val = ''
        if stack_dir == 'up' or stack_dir == 'down':
            perp = 'x'
        elif stack_dir == 'right' or stack_dir == 'left':
            perp = 'y'
        else:
            raise Exception('Error: Wait Found in Backtrack Stack')
        
        map_x = self.location[0]
        map_y = self.location[1]
        if perp == 'x':
            if self.map[map_y][map_x + 1] == -1:
                ret_val = self.directions[3]
            elif self.map[map_y][map_x - 1] == -1:
                ret_val = self.directions[4]
            else:
                ret_val = self.invert[stack_dir]
        elif perp == 'y':
            if self.map[map_y - 1][map_x] == -1:
                ret_val = self.directions[1]
            elif self.map[map_y + 1][map_x] == -1:
                ret_val = self.directions[2]
            else:
                ret_val = self.invert[stack_dir]

        return ret_val
            

    def get_decision(self, verbose = True):
        if self.follow_instructions:
            #print('Current instruction: ' + str(self.backtrack_stack[0]))
            self.last_direction = self.backtrack_stack[0].dir
            self.backtrack_stack[0].count -= 1
            if self.backtrack_stack[0].count == 0:
                self.backtrack_stack.pop(0)
            
            return self.last_direction

        for x in self.backtrack_stack:
            print(x)
        if len(self.backtrack_stack) == 0:
            print('Stack empty')
            rel_x = self.location[0]
            rel_y = self.location[1]
            while True:
                r = (int)(random.random()*4)+1
                tmp_dir = self.directions[r]
                while tmp_dir == self.last_direction:
                    r = (int)(random.random()*4)+1
                    tmp_dir = self.directions[r]
                self.last_direction = tmp_dir
                index = self.dirToInd(self.last_direction)
                mod_x = 0
                mod_y = 0
                if index == 1:
                    mod_y = -1
                elif index == 2:
                    mod_y = 1
                elif index == 3:
                    mod_x = 1
                elif index == 4:
                    mod_x = -1
                #print 'Mod_X: {}'.format(mod_x)
                #print 'Mod_Y: {}'.format(mod_y)
                #print 'Map shape: {}x{}'.format(len(self.map[0]), len(self.map))
                if self.map[rel_y+mod_y][rel_x+mod_x] == -1:
                    print(self.last_direction)
                    break
        elif self.last_result == 'SUCCESS':
            index = self.dirToInd(self.last_direction)
            if index == 1:
                map_loc = [self.location[0],self.location[1]-1]
            elif index == 2:
                map_loc = [self.location[0],self.location[1]+1]
            elif index == 3:
                map_loc = [self.location[0]+1, self.location[1]]
            elif index == 4:
                map_loc = [self.location[0]-1, self.location[1]]

            if self.map[map_loc[1]][map_loc[0]] != -1:
                self.last_direction = self.backtrack()
        elif self.last_result == 'WALL':
            self.last_direction = self.backtrack()
        print self.last_direction
        return self.last_direction

    def put_result(self, result):
        self.last_result = result.upper()

        if (self.last_result == 'SUCCESS' or self.last_result == 'PORTAL') and not self.follow_instructions:
            if len(self.backtrack_stack) == 0:
                self.backtrack_stack.append(self.Backtrack_Obj(self.last_direction))
            elif self.backtrack_stack[-1].dir == self.last_direction:
                self.backtrack_stack[-1].count += 1
            elif self.invert[self.backtrack_stack[-1].dir] == self.last_direction:
                self.backtrack_stack[-1].count -= 1
                if self.backtrack_stack[-1].count == 0:
                    self.backtrack_stack.pop()
            else:
                self.backtrack_stack.append(self.Backtrack_Obj(self.last_direction))

        if self.last_result == 'PORTAL':
            '''
            if not self.follow_instructions:
                for i in self.backtrack_stack:
                    print(i)
            '''
            self.follow_instructions = True

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

        '''
        for i in range(0, len(self.map)):
            print self.map[i]
        print "AI Relative location: " + str(self.location)
        '''
