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
        #self.vary_image = self.get_image()
        self.image = self.image.subsurface((0, 0, 32, 32))
        self.state = "rest_down"
        # .convert_alpha allows for transparency around you character
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.old_state = self.state
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)
        self.ch = 1

    def get_image(self):
        image = {"move_left": list(),
                 "move_up": list(),
                 "move_down": list(),
                 "move_right": list(),
                 "rest_left": list(),
                 "rest_right":list(),
                 "rest_up":list(),
                 "rest_down":list()
                 }
        image["rest_down"].append(self.image.subsurface((32 * 0, 32 * 0, 32, 32)))
        # image["move_down"].append(self.image.subsurface((32 * 0, 32 * 0, 32, 32)))
        # image["move_down"].append(self.image.subsurface((32 * 2, 32 * 0, 32, 32)))
        # image["rest_down"].append(self.image.subsurface((32 * 1, 32 * 0, 32, 32)))
        # image["move_left"].append(self.image.subsurface((32 * 0, 32 * 1, 32, 32)))
        # image["move_left"].append(self.image.subsurface((32 * 2, 32 * 1, 32, 32)))
        # image["rest_left"].append(self.image.subsurface((32 * 1, 32 * 1, 32, 32)))
        # image["move_right"].append(self.image.subsurface((32 * 0, 32 * 2, 32, 32)))
        # image["move_right"].append(self.image.subsurface((32 * 2, 32 * 2, 32, 32)))
        # image["rest_right"].append(self.image.subsurface((32 * 1, 32 * 2, 32, 32)))
        # image["move_up"].append(self.image.subsurface((32 * 0, 32 * 3, 32, 32)))
        # image["move_up"].append(self.image.subsurface((32 * 2, 32 * 3, 32, 32)))
        # image["rest_up"].append(self.image.subsurface((32 * 1, 32 * 3, 32, 32)))

        return image

    def position(self):
        return list(self._position)

    def position(self, value):
        self._position = list(value)

    def update(self, dt, _blockers):
        # if self.state[:4] == 'rest':
        #     self.image = self.vary_image[self.state][0]
        #     self.ch = 0
        # else:
        #     self.image = self.vary_image[self.state][self.ch%2]
        #     old_ch = self.ch
        #     self.ch += 1
        #     if self.ch == 8:
        #         self.ch = 0
        self.old_state = self.state
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
        if pygame.sprite.spritecollideany(player, _blockers):
            player.move_back()
            #self.ch = old_ch
        player.velocity=[0, 0]


    def move_back(self):
        """ If called after an update, the sprite can move back to give the
            illusion of the sprite not moving.
        """
        self.state = self.old_state
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom


class Blocker(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect


def make_blockers(_renderer):
    """
    Make the blockers for the level.
    """
    _blockers = pygame.sprite.Group()
    objects = _renderer.tmx_data.get_layer_by_name("object")
    for _object in objects:
        properties = _object.__dict__
        if properties['name'] == 'blocker':
            left = properties['x']
            top = properties['y']
            blocker = Blocker(pg.Rect(left, top, 32, 32))
            _blockers.add(blocker)
    return _blockers


pg.init()
white = (255, 255, 255)
# create window
screenSize = (800, 600)
screen = pg.display.set_mode(screenSize)

screen.fill(white)
renderer = Renderer("resources/tmx/desert.tmx")
blockers = make_blockers(renderer)

frame_rate = pygame.time.Clock()
player = Hero()
# player._position = [screen.get_rect().centerx, screen.get_rect().bottom]
# player.rect.centerx = screen.get_rect().centerx
# player.rect.bottom = screen.get_rect().bottom
map_data = pyscroll.data.TiledMapData(renderer.tmx_data)
w, h = screen.get_size()
map_layer = pyscroll.BufferedRenderer(map_data, (w, h), clamp_camera=True)
group = pyscroll.PyscrollGroup(map_layer=map_layer)
group.add(player)
group.center(player.rect.center)
move_dist = 2
# main loop
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RIGHT:
        #         player.velocity[0] = 1
        #         player.state = 'move_right'
        #     if event.key == pygame.K_LEFT:
        #         player.velocity[0] = -1
        #         player.state = 'move_left'
        #     if event.key == pygame.K_UP:
        #         player.velocity[1] = -1
        #         player.state = 'move_up'
        #     if event.key == pygame.K_DOWN:
        #         player.velocity[1] = 1
        #         player.state = 'move_down'
        # elif event.type == pygame.KEYUP:
        #     player.velocity = [0, 0]
        #     if player.state == 'move_right':
        #         player.state = 'rest_right'
        #     elif player.state == 'move_up':
        #         player.state = 'rest_up'
        #     elif player.state == 'move_down':
        #         player.state = 'rest_down'
        #     elif player.state == 'move_left':
        #         player.state = 'rest_left'

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if keys[K_RIGHT]:
        # print(player.rect)
        # print(player.rect.center)
        player.velocity[0] = 1
    if keys[K_LEFT]:
        player.velocity[0] = -1
    if keys[K_UP]:
        player.velocity[1] = -1
    if keys[K_DOWN]:
        player.velocity[1] = 1

    #  设置帧数
    frame_rate.tick(60)
#    dt = frame_rate.get_ticks()
    pg.display.set_caption("GameName " + str(frame_rate.get_fps()))
    player.update(move_dist, blockers)
    group.center(player.rect.center)
    group.draw(screen)

    pg.display.flip()

pg.quit()
