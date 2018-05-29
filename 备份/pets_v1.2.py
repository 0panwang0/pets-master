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
    def __init__(self, _image):
        pygame.sprite.Sprite.__init__(self)

        self.vary_image = self.get_image(_image)
        self.state = "rest_down"
        # .convert_alpha allows for transparency around you character
        self.image = self.vary_image[self.state][0]
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.old_state = self.state
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)
        self.first_frame = 0
        self.last_frame = 1
        self.last_time = 0
        self.frame = 0

    def get_image(self, _image):
        image = {"move_left": list(),
                 "move_up": list(),
                 "move_down": list(),
                 "move_right": list(),
                 "rest_left": list(),
                 "rest_right":list(),
                 "rest_up":list(),
                 "rest_down":list()
                 }
        image["move_down"].append(_image.subsurface((32 * 0, 32 * 0, 32, 32)))
        image["move_down"].append(_image.subsurface((32 * 2, 32 * 0, 32, 32)))
        image["rest_down"].append(_image.subsurface((32 * 1, 32 * 0, 32, 32)))
        image["move_left"].append(_image.subsurface((32 * 0, 32 * 1, 32, 32)))
        image["move_left"].append(_image.subsurface((32 * 2, 32 * 1, 32, 32)))
        image["rest_left"].append(_image.subsurface((32 * 1, 32 * 1, 32, 32)))
        image["move_right"].append(_image.subsurface((32 * 0, 32 * 2, 32, 32)))
        image["move_right"].append(_image.subsurface((32 * 2, 32 * 2, 32, 32)))
        image["rest_right"].append(_image.subsurface((32 * 1, 32 * 2, 32, 32)))
        image["move_up"].append(_image.subsurface((32 * 0, 32 * 3, 32, 32)))
        image["move_up"].append(_image.subsurface((32 * 2, 32 * 3, 32, 32)))
        image["rest_up"].append(_image.subsurface((32 * 1, 32 * 3, 32, 32)))

        return image

    def position(self):
        return list(self._position)

    def position(self, value):
        self._position = list(value)

    def update(self, distance, _blockers, current_time):
        if self.state[:4] == 'rest':
            self.image = self.vary_image[self.state][0]
        else:

            if current_time > self.last_time + 150:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                self.last_time = current_time
            self.image = self.vary_image[self.state][self.frame]
            print('current_time: ' + str(current_time) + ', last_time: ' + str(self.last_time))


        self.old_state = self.state
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * distance
        self._position[1] += self.velocity[1] * distance
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
        if pygame.sprite.spritecollideany(player, _blockers):
            player.move_back()
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
image = pygame.image.load('./images/Actor1.png').convert_alpha()
player = Hero(image)
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
lock = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if keys[K_RIGHT]:
        # print(player.rect)
        # print(player.rect.center)
        player.velocity[0] = 1
        player.state = 'move_right'
    if keys[K_LEFT]:
        player.velocity[0] = -1
        player.state = 'move_left'
    if keys[K_UP]:
        player.velocity[1] = -1
        player.state = 'move_up'
    if keys[K_DOWN]:
        player.velocity[1] = 1
        player.state = 'move_down'
    elif 1 not in keys:
        if player.state == 'move_right':
            player.state = 'rest_right'
        elif player.state == 'move_up':
            player.state = 'rest_up'
        elif player.state == 'move_down':
            player.state = 'rest_down'
        elif player.state == 'move_left':
            player.state = 'rest_left'

    #  设置帧数
    frame_rate.tick(60)
    tick = pygame.time.get_ticks()
    pg.display.set_caption("GameName " + str(frame_rate.get_fps()) + 'time: ' +  str(tick))
    player.update(move_dist, blockers, tick)
    group.center(player.rect.center)
    group.draw(screen)

    pg.display.flip()

pg.quit()
