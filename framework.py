'''
AI Framework
Version 0.4
Authors: Sean McGee and Preston Mouw
'''
import pygame
from DecisionFactory import *

#asks user if df will play or human will play

player = raw_input("Who will play? (H)uman or (D)ecisionFactory")

if player is 'H' or player is 'h':
	human_input = 1
	REFRESH_RATE = 8 #how many times the game checks for input and updates per sec
else:
	human_input = 0
	REFRESH_RATE = 60
	moves = 0
	DF = DecisionFactory()

pause = (int)(1000.0/REFRESH_RATE)


pygame.init()

COL = 16
ROW = 16

map_t = [[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

TILE_SZ = 32

size = (1200, 800)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Preston-ta-Sean Framework")

BLUE = pygame.Color(0, 0, 255, 0)
RED = pygame.Color(255, 0, 0, 0)
GREY = pygame.Color(90, 90, 90, 0)
WHITE = pygame.Color(255, 255, 255, 0)
GREEN = pygame.Color(0, 255, 0, 0)

portal = [0, 0]

running = 1
player_x = 1
player_y = 1

move_type = 4
#0: up
#1: down
#2: left
#3: right
#4: wait
while(running):

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
        pygame.quit()
        if human_input is 0:
			print moves
        running = 0

	if human_input is 1:
	    for event in pygame.event.get():
	        if event.type is pygame.QUIT:
	            pygame.quit()
	            running = 0
	        elif (event.type is pygame.KEYDOWN):
	            keys = pygame.key.get_pressed()
	            #print(event.key)
	            if keys[pygame.K_UP]:
	                move_type = 0
	                #print('UP KEY PRESSED')
	            elif keys[pygame.K_DOWN]:
	                move_type = 1
	                #print('DOWN KEY PRESSED')
	            elif keys[pygame.K_LEFT]:
	                move_type = 2
	                #print('LEFT KEY PRESSED')
	            elif keys[pygame.K_RIGHT]:
	                move_type = 3
	                #print('RIGHT KEY PRESSED')
	        elif (event.type is pygame.KEYUP):
	            move_type = 4
	else:
		move_type = DF.get_decision()
		# This is decremented because in the DecisionFactory code 0 is the wait
		# decision so this is to compensate and align with the human input code
		move_type -= 1

	if move_type is 0:
			player_x -= 1
        if map_t[player_x][player_y] is 1:
            player_x += 1
            result = "Wall"
        else:
			result = "Success"

    elif move_type is 1:
        player_x += 1
        if map_t[player_x][player_y] is 1:
            player_x -= 1
            result = "Wall"
        else:
			result = "Success"

    elif move_type is 2:
        player_y -= 1
        if map_t[player_x][player_y] is 1:
            player_y += 1
            result = "Wall"
        else:
			result = "Success"

    elif move_type is 3:
        player_y += 1
        if map_t[player_x][player_y] is 1:
            player_y -= 1
            result = "Wall"
        else:
			result = "Success"

	if human_input is 0:
		DF.put_result(result)
		moves += 1

    pygame.time.wait(pause)

'''
Change log
Ver 0.4:
Added ability to use df or human input
Ver 0.3:
Added basic human input
Ver 0.2:
Adding map functionailty
Ver 0.1:
Created file and added basic pygame structure
'''
