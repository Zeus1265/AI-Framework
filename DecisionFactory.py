import random
import math
#import  numpy as  np

class DecisionFactory:
    def __init__(self, name ='Davros'):
        self.name = name
        self.directions = ['wait', 'up', 'down', 'right', 'left']
        self.last_result = 'SUCCESS'
        self.last_direction = 'wait'
        self.target = [0,0] #where to path to
        self.target_reached = True #whether or not a new target is needed
        self.unreachables = [] #mark certain locations as unreachable. Try other locations first

        self.tasks = [] #stack memory of what instructions to follow
        self.wall_climber_modifier = [] #used by the wall climber algorithm to determine what direction to move in

        
        self.map = [[ 1, 1, 1, 1, 1, 1, 1],
                    [ 1, 0, 0, 0, 0, 0, 1],
                    [ 1, 0, 0, 0, 0, 0, 1],
                    [ 1, 0, 0, 0, 0, 0, 1],
                    [ 1, 0, 1, 1, 1, 0, 1],
                    [ 1, 0, 0, -1, 0, 0, 1],
                    [ 1, 1, 1, 1, 1, 1, 1]]
        '''
        self.map = [[-1, -1, -1],
                    [-1,  0, -1],
                    [-1, -1, -1]]
        '''
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
                dir = int(random.random()* 2) + 3
        elif math.fabs(location[0] - player[0]) < math.fabs(location[1] - player[1]):
            if location[1] > player[1]:
                dir = 2
            elif location[1] < player[1]:
                dir = 1
            else:
                dir = int(random.random()*2)+1
        else:
            if location[0] > player[0]:
                dir = (int)(random.random() * 2) + 2
            elif (int)(random.random()*2) == 0:
                dir = 1
            else:
                dir = 4
        return dir

    def get_target(self):
        #print "List of unreachable points: "+str(self.unreachables)
        self.closest_unknown = []
        for i in range(0, len(self.map)):
            for j in range(0, len(self.map[0])):
                if self.map[i][j] == -1 and [j, i] not in self.unreachables:
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

        if len(self.closest_unknown) == 0:
            return [-1, -1]

        return self.closest_unknown[(int)(random.random() * len(self.closest_unknown))]

    def direction_inverter(self, direction):
        #up -> down
        #down -> up
        #left -> right
        #right -> left
        if direction == 1:
            return 2
        elif direction == 2:
            return 1
        elif direction == 3:
            return 4
        elif direction == 4:
            return 3
        return 0

    def wall_climber(self, wall_direction, default_movement):
        #wall_direction MUST match an entry in self.directions[]
        #default_movement is an index corresponding to a direction in self.directions[]
        #wall_climber_modifier is a stack of modifiers, which correspond to that level's wall_climber
	
        if self.wall_climber_modifier[len(self.wall_climber_modifier)-1] == -1: #modified case
            default_movement = self.direction_inverter(default_movement)
        
        if self.last_direction == self.directions[default_movement] and self.last_result == "SUCCESS":
	    #print "Moved parallel last round, moving in wall direction"
            return wall_direction
        elif self.last_direction == self.directions[default_movement] and self.last_result == "WALL":
            self.tasks.append("wall_"+self.directions[default_movement])
	    self.wall_climber_modifier.append(0)
	    #print "Another wall encountered, calling another climb"
            #print "Tasks: "+str(self.tasks)
            return self.directions[default_movement]
        elif self.last_direction == wall_direction and self.last_result == "WALL":
            #print "Headbutted wall, moving parallel next round"
            return self.directions[default_movement]
        elif self.last_direction == wall_direction and self.last_result == "SUCCESS":
	    #print "Wall successfully navigated"
            #print "Task removed by wall_climber alg"
            
            self.tasks.pop()
            self.wall_climber_modifier.pop()
	    #print "Tasks: "+str(self.tasks)
            return "wait"
        return wall_direction

    def get_decision(self, verbose = True):
	if len(self.tasks) >= 5:
		self.tasks = []
		self.wall_climber_modifier = []
        if len(self.tasks) == 0 or self.tasks[len(self.tasks) - 1] == "target":
            if len(self.tasks) == 0:
                self.tasks.append("target")
                #print "Added \'target\' task"
                #print "Tasks: "+str(self.tasks)
	    	self.target_reached = True
            if self.target_reached:
                #self.unreachables = []
                self.target = self.get_target()
                self.target_reached = False


            if self.target[0] != -1 and self.target[1] != -1:               
                dir = self.dir_chooser(self.location, self.target)
                self.last_direction = self.directions[dir]
            else:
                #add in wall movements
                self.tasks.pop()
                #print "Removed a task"
                self.wall_climber_modifier.append(0)
                self.tasks.append("wall_"+self.last_direction)
                #print "Added a wall task"
                #print "Tasks: "+str(self.tasks)
                self.target_reached = True
		self.unreachables = []

            
            #print "Last Direction: "+self.last_direction
            #print "Target: "+str(self.target)
            #print "Tasks: "+str(self.tasks)
            return self.last_direction
        elif self.tasks[len(self.tasks)-1] != "target":
            top = len(self.tasks) - 1
            
            if self.tasks[top] == "wall_up":
                #wall encountered is *above* DF
                #default move left, mod move right
                self.last_direction = self.wall_climber("up", 4)
            elif self.tasks[top] == "wall_down":
                #wall encountered is *below* DF
                #default move right, mod move left
                self.last_direction = self.wall_climber("down", 3)
            elif self.tasks[top] == "wall_right":
                #wall encountered is *right* of DF
                #default move up, mod move down
                self.last_direction = self.wall_climber("right", 1)
            elif self.tasks[top] == "wall_left":
                #wall encountered is *left* of DF
                #default move down, mod move up
                self.last_direction = self.wall_climber("left", 2)
            
            #print self.last_direction
            #print "Tasks: "+str(self.tasks)
            return self.last_direction
        else:
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

            x_mod = 0
            y_mod = 0
            if self.last_direction == "up":
                y_mod = -1
            elif self.last_direction == "down":
                y_mod = 1
            elif self.last_direction == "left":
                x_mod = -1
            elif self.last_direction == "right":
                x_mod = 1
            if self.target == [x + x_mod, y + y_mod]:
                self.target_reached = True
                self.unreachables = []
            else:
                self.unreachables.append(self.target)
                self.target_reached = True
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

            self.target_reached = self.target == [x, y]
            if self.target_reached:
                self.unreachables = []

        #for i in range(0, len(self.map)):
        #    print self.map[i]
        #print "AI Relative location: " + str(self.location)
