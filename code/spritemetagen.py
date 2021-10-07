# @pranshuj73
# Utility Program to generate a json file for spritesheet containing tile position & dimensions


import pygame
import json


filepath = input("Enter path to spritesheet:\t")
rows = int(input("How many rows are in your spritesheet?\t"))
cols = int(input("How many columns are in your spritesheet?\t"))

img = pygame.image.load(filepath)


width = img.get_width()
height = img.get_height()

tile_width = width // cols
tile_height = height // rows

result_dict = {}

for row_index in range(rows):
    for col_index in range(cols):
        tile_name = 'tile' + str(row_index) + str(col_index)
        tile_dimensions = {
            'x': tile_width * col_index,
            'y': tile_width * row_index,
            'w': tile_width,
            'h': tile_height,
        }

        result_dict[tile_name] = tile_dimensions


with open(filepath.replace('png', 'json'), 'w') as result_file:
    json.dump(result_dict, result_file)
