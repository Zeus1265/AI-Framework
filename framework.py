'''
AI Framework
Version 0.1
Authors: Sean McGee and Preston Mouw
'''
import pygame

pygame.init()

size = (1500, 1000)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Very bad demo")

BLUE = pygame.Color(0, 0, 255, 0)
RED = pygame.Color(255, 0, 0, 0)
pygame.draw.circle(screen, RED, (750, 500), 100, 0)
pygame.draw.rect(screen, BLUE, pygame.Rect(0, 0, 1500, 1000), 0)
pygame.display.update()

pygame.time.delay(1500)

pygame.quit()

'''
Change log
Ver 0.1:
Created file and added basic pygame structure
'''
