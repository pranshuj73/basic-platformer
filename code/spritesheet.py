import pygame
import json


class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.meta_data = self.filename.replace('png', 'json')
        try:
            with open(self.meta_data) as f:
                self.data = json.load(f)
                f.close()
        except Exception as e:
            print(e)

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self):
        surface_list = []
        for name in self.data:
            sprite = self.data[name]
            x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
            image = self.get_sprite(x, y, w, h)
            surface_list.append(image)

        return surface_list
