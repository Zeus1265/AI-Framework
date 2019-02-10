'''
AI Framework
Version 0.1
Authors: Sean McGee and Preston Mouw
'''
import pygame

pygame.init()

map_t = [[ 1, 1, 1, 1],
	 [ 1, 0, 0, 1],
	 [ 1, 0, 0, 1],
	 [ 1, 1, 1, 1]]
COL = 4
ROW = 4
TILE_SZ = 16

size = (1500, 1000)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Very bad demo")

BLUE = pygame.Color(0, 0, 255, 0)
RED = pygame.Color(255, 0, 0, 0)

for r in range(0, ROW):
	for c in range(0, col):
		if map_t[r, c] is 1:
			color = RED
		else:
			color = BLUE
		pygame.draw.rect(screen, RED, pygame.Rect(r*TILE_SZ, c*TILE_SZ, TILE_SZ, TILE_SZ), 0)


pygame.display.update()

pygame.wait(1500)

pygame.quit()

'''
Change log
Ver 0.2:
Adding map functionailty
Ver 0.1:
Created file and added basic pygame structure
'''
