import pygame as pg
import pytmx
from pygame.locals import *
import sys, pygame
import pyscroll


class Renderer(object):
    """
    This object renders tile maps from Tiled
    """
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm

    def render(self, surface):
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        gt = self.tmx_data.get_tile_image_by_gid

        if self.tmx_data.background_color:
            surface.fill(self.tmx_data.background_color)

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = gt(gid)
                    if tile:
                        surface.blit(tile, (x * tw, y * th))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                pass
            elif isinstance(layer, pytmx.TiledImageLayer):
                image = gt(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

    def make_2x_map(self):
        temp_surface = pg.Surface(self.size)
        self.render(temp_surface)
        temp_surface = pg.transform.scale2x(temp_surface)
        return temp_surface


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./images/ship.bmp').convert_alpha()
        self.image = self.image.subsurface((0, 0, 32, 32))
        # .convert_alpha allows for transparency around you character
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)

    def position(self):
        return list(self._position)

    def position(self, value):
        self._position = list(value)

    def update(self, dt, rect):
        self._old_rect = rect
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
        self.velocity = [0, 0]

    def move_back(self, rect):
        """ If called after an update, the sprite can move back to give the
            illusion of the sprite not moving.
        """
        rect = self._old_rect
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom


class Blocker(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect


def make_blockers(renderer):
    """
    Make the blockers for the level.
    """
    blockers = pygame.sprite.Group()
    objects = renderer.tmx_data.get_layer_by_name("object")
    for object in objects:
        properties = object.__dict__
        if properties['name'] == 'blocker':
            left = properties['x']
            top = properties['y']
            blocker = Blocker(pg.Rect(left, top, 32, 32))
            print(blocker.rect)
            blockers.add(blocker)
    return blockers


def cross(a, b):
    for each in a:
        if each in b:
            return True
    return False


# def clollideany(blockers, player_rect1):
#     player_rect = player_rect1
#     player_rangex = range(player_rect.x, player_rect.x + player_rect.width)
#     player_rangey = range(player_rect.y, player_rect.y + player_rect.height)
#     for blocker in blockers:
#         blocker_rect = blocker
#         blocker_rangex = range(blocker_rect.x, blocker_rect.x + blocker_rect.width)
#         blocker_rangey = range(blocker_rect.y, blocker_rect.y + blocker_rect.height)
#         if cross(player_rangex, blocker_rangex) and cross(player_rangey, blocker_rangey):
#             return True
#     return 0


pg.init()
white = (255, 255, 255)
# create window
screenSize = (800,600)
screen = pg.display.set_mode(screenSize)

screen.fill(white)
renderer = Renderer("resources/tmx/desert.tmx")
gameMap = make_blockers(renderer)
screen1 = renderer.make_2x_map()
framerate = pygame.time.Clock()
player = Hero()


map_data = pyscroll.data.TiledMapData(renderer.tmx_data)
w, h = screen.get_size()
map_layer = pyscroll.BufferedRenderer(map_data, (w, h), clamp_camera=True)
group = pyscroll.PyscrollGroup(map_layer=map_layer)
group.add(player)
group.center(player.rect.center)

#main loop
running = True
camera = player.rect

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    player_baseon_screen = player.rect
    player_baseon_screen.x = player_baseon_screen.x % screenSize[0]
    player_baseon_screen.y = player_baseon_screen.y % screenSize[1]

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if keys[K_RIGHT]:
        print(player.rect)
        print(player.rect.center)
        player.velocity[0] = 1
        if player_baseon_screen.x + player_baseon_screen.width > 2 / 3 * screenSize[0]:
            camera.x += 2
    if keys[K_LEFT]:
        player.velocity[0] = -1
        if player_baseon_screen.x < 1 / 3 * screenSize[0]:
            camera.x -= 2
    if keys[K_UP]:
        player.velocity[1] = -1
        if player_baseon_screen.y < 1 / 3 * screenSize[1]:
            camera.y -= 2
    if keys[K_DOWN]:
        player.velocity[1] = 1
        if player_baseon_screen.y + player_baseon_screen.height > 2 / 3 * screenSize[1]:
            camera.y += 2

    if(pygame.sprite.spritecollideany(player, gameMap)):
        player.move_back(camera)
    #  设置帧数
    framerate.tick(60)

    pg.display.set_caption("GameName " + str(framerate.get_fps()))

    player.update(2, camera)
    group.center(camera.center)
    group.draw(screen)

    pg.display.flip()

pg.quit()
