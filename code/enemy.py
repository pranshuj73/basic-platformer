import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    def __init__(self, position, size, stationary):
        super().__init__(
            position,
            size,
            '../graphics/Hell-Beast-Files/with-stroke/hell-beast-idle.png',
        )
        self.rect.y += size - self.image.get_size()[1]
        # speed is 0 if enemy is stationary else b/w 1 & 3
        self.speed = 0 if stationary else randint(1, 3)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
