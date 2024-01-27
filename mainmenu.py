from gamedata import *
from support import *


class Node(pygame.sprite.Sprite):
    def __init__(self, position, status, icon_speed, path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == "unlocked":
            self.status = 'unlocked'
        else:
            self.status = "locked"
        self.rect = self.image.get_rect(center=position)
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2),
                                          self.rect.centery - (icon_speed / 2),
                                          icon_speed,
                                          icon_speed)
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.status == 'unlocked':
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surface, (0, 0))

    def import_node_images(self):
        node_path = 'graphics/overworld/'
        self.nodes = {
            '0': [],
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [0]
        }
        for level in self.nodes.keys():
            full_path = node_path + level
            self.nodes[level] = import_folder(full_path)
        else:
            print(self.nodes)

    def animate(self):
        self.frame_index += .1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]


class Icon(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.Surface((20, 20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center = self.position

class Overworld:
    def __init__(self, start_level, max_level, display_surface, create_level):
        self.current_level = start_level
        self.max_level = max_level
        self.display_surface = display_surface
        self.create_level = create_level

        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, nodedata in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(nodedata['node_pos'], 'unlocked', self.speed, nodedata['node_graphics'])
            else:
                node_sprite = Node(nodedata['node_pos'], 'locked', self.speed, nodedata['node_graphics'])
            self.nodes.add(node_sprite)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        points = [node_data['node_pos'] for index, node_data in enumerate(levels.values()) if index <= self.max_level]
        pygame.draw.lines(self.display_surface, (0, 0, 0), False, points, 6)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and self.current_level < self.max_level:
            self.move_direction = self.get_movement_data('next')
            self.current_level += 1
            self.moving = True
        elif keys[pygame.K_a] and self.current_level > 0:
            self.move_direction = self.get_movement_data('previous')
            self.current_level -= 1
            self.moving = True
        elif keys[pygame.K_SPACE]:
            self.create_level(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return(end - start).normalize()

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.position += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.position):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)


    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
