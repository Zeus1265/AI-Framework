'''
AI Framework
Version 0.4
Authors: Sean McGee and Preston Mouw
'''
import pygame
import random
import DecisionFactory
import mapGen

pygame.init()
#asks user if df will play or human will play

#player = input("Who will play? Human(1) or DecisionFactory(0)\n")
player = 0
human_input = 0
DF = DecisionFactory.DecisionFactory('Dice Roller 2000')
moves = 0
if player is 1: #or (player is 'h'):
	human_input = 1
	REFRESH_RATE = 12 #how many times the game checks for input and updates per sec
else:
	human_input = 0
	REFRESH_RATE = 60


#print(human_input)

pause = (int)(1000.0/REFRESH_RATE)

COL = 8
ROW = 12

(map_t, player_init) = mapGen.type0(COL, ROW)  

player_x = player_init[0]
player_y = player_init[1]

TILE_SZ = 24

size = (700, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Preston-ta-Sean Framework")

BLUE = pygame.Color(0, 0, 255, 0)
RED = pygame.Color(255, 0, 0, 0)
GREY = pygame.Color(90, 90, 90, 0)
WHITE = pygame.Color(255, 255, 255, 0)
GREEN = pygame.Color(0, 255, 0, 0)

#portal = [0, 0]

running = 1

round2 = False

move_type = 4
#0: wait
#1: up
#2: down
#3: right
#4: left

timer = pygame.time.Clock()
while(running):
    events = pygame.event.get()
    for event in events:
        if event.type is pygame.QUIT:
            pygame.quit()
            running = 0
        if human_input is 1:
            if (event.type is pygame.KEYDOWN):
                keys = pygame.key.get_pressed()

                #print(event.key)
                if keys[pygame.K_UP]:
                    move_type = 1
                    #print('UP KEY PRESSED')
                elif keys[pygame.K_DOWN]:
                    move_type = 2
                    #print('DOWN KEY PRESSED')
                elif keys[pygame.K_LEFT]:
                    move_type = 4
                    #print('LEFT KEY PRESSED')
                elif keys[pygame.K_RIGHT]:
                    move_type = 3
                    #print('RIGHT KEY PRESSED')
            elif (event.type is pygame.KEYUP):
                move_type = 0
    else:
        d = DF.get_decision()
        if d is 'wait':
            move_type = 0
        elif d is 'up':
            move_type = 1
        elif d is 'down':
            move_type = 2
        elif d is 'right':
            move_type = 3
        elif d is 'left':
            move_type = 4

    #print(move_type)
    if move_type is 1:
        moves += 1
        player_x -= 1
        if map_t[player_y][player_x] is 1:
            player_x += 1
            result = "Wall"
        elif map_t[player_y][player_x] == 2:
            result = 'Portal'
        else:
            result = "Success"
    elif move_type is 2:
        moves += 1
        player_x += 1
        if map_t[player_y][player_x] is 1:
            player_x -= 1
            result = "Wall"
        elif map_t[player_y][player_x] == 2:
            result = 'Portal'
        else:
            result = "Success"
    elif move_type is 4:
        moves += 1
        player_y -= 1
        if map_t[player_y][player_x] is 1:
            player_y += 1
            result = "Wall"
        elif map_t[player_y][player_x] == 2:
            result = 'Portal'
        else:
            result = "Success"
    elif move_type is 3:
        moves += 1
        player_y += 1
        if map_t[player_y][player_x] is 1:
            player_y -= 1
            result = "Wall"
        elif map_t[player_y][player_x] == 2:
            result = 'Portal'
        else:
            result = "Success"
    else:
		result = "Success"

    if human_input is 0:
        DF.put_result(result)
        moves += 1
        #print(result)
		
    #timer.tick(REFRESH_RATE)
    timer.tick(60)
    for r in range(0, ROW):
        for c in range(0, COL):
            if map_t[r][c] is 1:
                color = RED
            elif map_t[r][c] is 0:
                color = BLUE
            elif map_t[r][c] is 2:
                color = WHITE
                portal = [r, c]
            #print('Drawing rectangle at {}, {}'.format(r, c))
            pygame.draw.rect(screen, color, pygame.Rect(r*TILE_SZ, c*TILE_SZ, TILE_SZ, TILE_SZ), 0)
            pygame.draw.rect(screen, GREY, pygame.Rect(r*TILE_SZ, c*TILE_SZ, TILE_SZ, TILE_SZ), 1)
    pygame.draw.rect(screen, GREEN, pygame.Rect(player_y * TILE_SZ, player_x * TILE_SZ, TILE_SZ, TILE_SZ), 0)
    #print('portal at {}'.format(portal))
    pygame.display.update()

    if portal[0] is player_y and portal[1] is player_x:
        if round2:
            pygame.quit()
            running = 0
            print('Round 2 moves: {}'.format(moves))
        else:
            round2 = True
            player_x = player_init[0]
            player_y = player_init[1]
            print('Round 1 moves: {}'.format(moves))
            moves = 0


'''
Change log
Ver 1.1:
Fixed Decision factory to work with Cone's framework maybe hopefully
Ver 1.0:
Increased AI ability of decision factory to better than random
Did not actually integrate with Cone's Framework :C
Ver 0.4:
Added ability to use df or human input
Ver 0.3:
Added basic human input
Ver 0.2:
Adding map functionailty
Ver 0.1:
Created file and added basic pygame structure
'''
