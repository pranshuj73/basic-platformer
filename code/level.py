import pygame
from tiles import Tile, StaticTile
from settings import tile_size, screen_width
from player import Player
from enemy import Enemy
from support import import_csv_layout, import_cut_graphics


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface

        # Player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Load all tile data from CSV and create tile groups for them

        # Terrain Setup #
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # Ramp Setup #
        upward_ramp_layout = import_csv_layout(level_data['upward_ramps'])
        self.upward_ramp_sprites = self.create_tile_group(upward_ramp_layout, 'upward_ramp')
 
        downward_ramp_layout = import_csv_layout(level_data['downward_ramps'])
        self.downward_ramp_sprites = self.create_tile_group(downward_ramp_layout, 'downward_ramp')

        # Decoration tiles setup #
        decoration_layout = import_csv_layout(level_data['decorations'])
        self.decoration_sprites = self.create_tile_group(
            decoration_layout, 'decoration'
        )


        # Enemies & Constraints between which they can move #
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')

        constraint_layout = import_csv_layout(level_data['contraints'])
        self.constraint_sprites = self.create_tile_group(
            constraint_layout, 'constraint'
        )

        self.world_shift = 0
        self.current_x = 0

    def create_tile_group(self, layout, type):
        """
        Create various tile groups for the terrain, ramps, enemies & constraints which limit their movement"""

        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain' or type == 'upward_ramp' or type == 'downward_ramp' or type == 'decoration':
                        terrain_tile_list = import_cut_graphics(
                            '../tiles/terrain_tileset.png'
                        )
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile((x, y), tile_size, tile_surface)

                    if type == 'enemy':
                        sprite = Enemy((x, y), tile_size, False)

                    if type == 'constraint':
                        sprite = Tile((x, y), tile_size)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y))
                    self.player.add(sprite)
                if val == '1':
                    sprite = Tile((x, y), tile_size)
                    self.goal.add(sprite)

    def scroll_x(self):
        """Moves the camera along with the player"""

        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < (screen_width * 0.4) and direction_x < 0:
            self.world_shift = 3
            player.speed = 0
        elif player_x > (screen_width * 0.6) and direction_x > 0:
            self.world_shift = -3
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:  # moving left
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                    
                elif player.direction.x > 0:  # moving right
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        for sprite in self.upward_ramp_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                rel_x = player.rect.x - sprite.rect.x
                pos_height = rel_x + player.rect.width
                pos_height = min(pos_height, tile_size)
                pos_height = max(pos_height, 0)

                target_y = sprite.rect.y + tile_size - pos_height

                if player.rect.bottom > target_y:
                    player.rect.bottom = target_y
                    player.direction.y = 0
                    player.on_ground = True

        for sprite in self.downward_ramp_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                rel_x = player.rect.x - sprite.rect.x
                pos_height = tile_size - rel_x
                pos_height = min(pos_height, tile_size)
                pos_height = max(pos_height, 0)

                target_y = sprite.rect.y + tile_size - pos_height

                if player.rect.bottom > target_y:
                    player.rect.bottom = target_y
                    player.direction.y = 0
                    player.on_ground = True

        if player.on_left and (
            player.rect.left < self.current_x or player.direction.x >= 0
        ):
            player.on_left = False
        if player.on_right and (
            player.rect.right < self.current_x or player.direction.x <= 0
        ):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        for sprite in self.upward_ramp_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                rel_x = player.rect.x - sprite.rect.x
                pos_height = rel_x + player.rect.width
                pos_height = min(pos_height, tile_size)
                pos_height = max(pos_height, 0)

                target_y = sprite.rect.y + tile_size - pos_height

                if player.rect.bottom > target_y:
                    player.rect.bottom = target_y
                    player.direction.y = 0
                    player.on_ground = True

        for sprite in self.downward_ramp_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                rel_x = player.rect.x - sprite.rect.x
                pos_height = tile_size - rel_x
                pos_height = min(pos_height, tile_size)
                pos_height = max(pos_height, 0)

                target_y = sprite.rect.y + tile_size - pos_height

                if player.rect.bottom > target_y:
                    player.rect.bottom = target_y
                    player.direction.y = 0
                    player.on_ground = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 0.8:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
        """
        Draw all tiles on screen and update their positions
        Also enable Player & Enemy collisions
        """
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        self.upward_ramp_sprites.update(self.world_shift)
        self.upward_ramp_sprites.draw(self.display_surface)
        self.downward_ramp_sprites.update(self.world_shift)
        self.downward_ramp_sprites.draw(self.display_surface)

        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        self.player.update()
        self.goal.update(self.world_shift)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)

        self.decoration_sprites.update(self.world_shift)
        self.decoration_sprites.draw(self.display_surface)
