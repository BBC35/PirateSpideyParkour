from support import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=position)


    def update(self, x_shift):
        self.rect.x += x_shift

class StaticTile(Tile):
    def __init__(self, position, size, surface):
        super().__init__(position, size)
        self.image = surface

class AnimatedTile(Tile):
    def __init__(self, position, size, path):
        super().__init__(position, size)
        self.frames = import_folder(path)
        for i, frame in enumerate(self.frames):
            new_surface = pygame.transform.scale(frame, (size, size * 2))
            pygame.transform.scale(frame, (size, size))
            self.frames[i] = new_surface
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift


    class Create(Tile):
        pass
