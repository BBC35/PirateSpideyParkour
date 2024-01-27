import sys
from level import *
from mainmenu import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.max_level = 1
        self.status = 'over_world'
        self.over_world = Overworld(0, self.max_level, self.screen, self.create_lvl)
        self.background = pygame.transform.scale(pygame.image.load('christmasbackground.webp'), (1280, 780))

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def create_lvl(self, current_lvl):
        self.level = Level(self.screen, current_lvl, self.create_over_world)
        self.status = 'level'

    def create_over_world(self, current_lvl, new_max_lvl):
        if new_max_lvl > self.max_level:
            self.max_level = new_max_lvl
        self.over_world = Overworld(current_lvl, self.max_level, self.screen, self.create_lvl)
        self.status = 'over_world'

    def draw(self):
        self.screen.fill('#060C17')
        self.screen.blit(self.background, (0, 0))
        if self.status == 'over_world':
            self.over_world.run()
        else:
            self.level.run()
        pygame.display.update()

    def run(self):
        while True:
            self.input()
            self.draw()
            self.clock.tick(60)


if __name__ == '__main__':
    Game().run()
