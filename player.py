from support import *
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, position, display_surface, create_jump_parti):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = .2
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = .2
        self.display_surface = display_surface
        self.create_jump_parti = create_jump_parti

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_speed = -15

        self.on_floor = False
        self.status = 'idle'
        self.on_da_clelelebedemelegelingityling = False
        self.facing_right = True
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = 'graphics/character/'
        self.animations = {
            'idle': [],
            'run': [],
            'fall': [],
            'jump': []
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        #self.rect = self.image.get.rect(midbottom=self.rect.midbottom)
        # if self.on_right and self.on_floor:
        #     self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        # elif self.on_left and self.on_floor:
        #     self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        # elif self.on_da_clelelebedemelegelingityling and self.on_right:
        #     self.rect = self.image.get_rect(topright = self.rect.topright)
        # elif self.on_da_clelelebedemelegelingityling and self.on_left:
        #     self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # elif self.on_floor:
        #     self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # elif self.on_da_clelelebedemelegelingityling:
        #     self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_floor:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            if self.facing_right:
                position = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, position)
            else:
                position = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flip_dust_parti = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flip_dust_parti, position)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0
        if keys[pygame.K_w] and self.on_floor:
            self.jump()
            self.create_jump_parti(self.rect.midbottom)

    def jump(self):
        self.direction.y = self.jump_speed

    def git_da_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_grav(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.input()
        self.git_da_status()
        self.animate()
        #self.run_dust_animation()
