from support import *


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.2
        if type == 'jump':
            self.frames = import_folder('graphics/character/dust_particles/jump')
        elif type == 'land':
            self.frames = import_folder('graphics/character/dust_particles/land')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animation()
        self.rect.x += x_shift
