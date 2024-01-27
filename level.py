import pygame.sprite

from settings import *
from tile import *
from player import *
from particles import *
from gamedata import *
from enemy import *

class Level:
    def __init__(self, surface, current_lvl, create_overworld):
        self.display_surface = surface
        self.current_lvl = current_lvl
        level_data = levels[self.current_lvl]
        self.set_up_level(level_data['layout'])
        self.level_shiftx = 0
        self.level_shifty = 0
        self.current_x = 0
        self.osp = level_data['player_pos']
        self.otp = {}
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.background = pygame.transform.scale(pygame.image.load('graphics/platformer background.png'), (1280, 780))
        self.player_on_ground = False
        self.create_overworld = create_overworld
        level_content = level_data['content']
        self.new_max_lvl = level_data['unlock']
        self.lives = 3
        self.font = pygame.font.Font('Gugi-Regular.ttf', 11)



        for sprite in self.tiles.sprites():
            self.otp[sprite] = sprite.rect.topleft

    def check_death_condition(self):
        if self.player.sprite.rect.top > SCREEN_HEIGHT:
            self.player.sprite.rect.midbottom = self.osp
            self.lives -= 1
            for sprite, original_position in self.otp.items():
                sprite.rect.topleft = original_position
        if self.lives < 1:
                self.create_overworld(self.current_lvl, 0)
                self.lives = self.lives - 1

    def check_win_condition(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.portal, False):
            self.create_overworld(self.current_lvl, self.new_max_lvl)

    def create_jump_parti(self, position):
        if self.player.sprite.facing_right:
            position -= pygame.math.Vector2(10, 17)
        else:
            position += pygame.math.Vector2(10, -17)
        jump_parti = ParticleEffect(position, 'jump')
        self.dust_sprite.add(jump_parti)

    def create_landing_parti(self):
        if not self.player_on_ground and self.player.sprite.on_floor and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_particle)

    def get_player_ground(self):
        if self.player.sprite.on_floor:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def set_up_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.portal = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                x = column_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if column == 'X':
                    terrain_tile_list = import_cut_graphics('graphics/terrain_tiles.png')
                    tile_surface = terrain_tile_list[0]
                    tile = StaticTile((x, y), 64, tile_surface)
                    self.tiles.add(tile)
                elif column == 'P':
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_parti)
                    self.player.add(player_sprite)
                elif column == 'T':
                    portal = AnimatedTile((x, y), 64, 'graphics/portal')
                    self.portal.add(portal)
                elif column == 'E':
                    enemy = Enemy((x, y), 64, 'graphics/run')
                    self.enemy.add(enemy)


    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x <= SCREEN_WIDTH / 4 and direction_x < 0:
            self.level_shiftx = 8
            player.speed = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 4) and direction_x > 0:
            self.level_shiftx = -8
            player.speed = 0
        else:
            self.level_shiftx = 0
            player.speed = 5

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y
        if player_y <= SCREEN_HEIGHT / 4 and direction_y < 0:
            self.level_shifty = 8
        elif player_y > SCREEN_HEIGHT - (SCREEN_HEIGHT / 4) and direction_y > 0:
            self.level_shifty = -8
        else:
            self.level_shifty = 0

    def h_collide(self):
            player = self.player.sprite
            player.rect.x += player.direction.x * player.speed
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                        player.on_left = True
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                        player.on_right = True
                        self.current_x = player.rect.right
            if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
                player.on_left = False
            if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
                player.on_right = False

    def v_collide(self):
        player = self.player.sprite
        player.apply_grav()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_da_clelelebedemelegelingityling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_floor = True
        if player.on_floor and player.direction.y < 0 or player.direction.y > 1:
            player.on_floor = False
        if player.on_da_clelelebedemelegelingityling and player.direction.y > 0.1:
            player.on_da_clelelebedemelegelingityling = False

        if player.rect.y > 1000:
            player.rect.midbottom = self.osp
            player.direction.y = 0
            for sprite, original_position in self.otp.items():
                sprite.rect.topleft = original_position

    def controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_lvl, self.new_max_lvl)
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_lvl, 0)

    def run(self):
        self.display_surface.blit(self.background, (0, 0))
        self.controls()
        self.dust_sprite.update(self.level_shiftx)
        self.dust_sprite.draw(self.display_surface)
        self.tiles.update(self.level_shiftx)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        self.scroll_y()

        self.player.update()
        self.h_collide()
        self.get_player_ground()
        self.v_collide()
        self.create_landing_parti()
        self.player.draw(self.display_surface)
        self.portal.update(self.level_shiftx)
        self.portal.draw(self.display_surface)
        self.check_death_condition()
        self.check_win_condition()
        #print(self.player.sprite.rect.x, self.player.sprite.rect.y)