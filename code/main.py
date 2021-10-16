import pygame
import sys

from pygame.constants import RESIZABLE
from settings import *
from level import Level
from gamedata import level_0

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height) , RESIZABLE)
pygame.display.set_caption("Basic Platformer")
clock = pygame.time.Clock()
level = Level(level_0, screen)
background = pygame.image.load("../graphics/Gothic-Horror-Files/layers/clouds.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))
bg_town = pygame.image.load("../graphics/Gothic-Horror-Files/layers/town.png").convert_alpha()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('white')
    screen.blit(background, background.get_rect())

    town_width, town_height = bg_town.get_rect().size
    town_loop_number = round(screen_width / town_width)
    for i in range(town_loop_number):
        screen.blit(bg_town, (i * town_width, screen_height - town_height))

    level.run()

    pygame.display.update()
    clock.tick(60)
