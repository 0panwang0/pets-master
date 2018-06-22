import pygame
import pytmx
import pyscroll
from person import NPC
import const

class Map(object):
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
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface)
        temp_surface = pygame.transform.scale2x(temp_surface)
        return temp_surface


class ScrollMap(Map):
    def __init__(self, filename, screen, bgm):
        super().__init__(filename)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, (screen.get_rect().width
                                                                   , screen.get_rect().height), clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        self.blockers = make_object(self, 'blocker')    # 禁止角色横跨的位置
        self.doors = make_object(self, 'door')  # 通往其它地图的门
        self.start_points = make_object(self, 'start point')    # 角色在一张地图的起始点
        self.sprites = make_object(self, 'sprite')  # 精灵对象
        self.nobattle_area = make_object(self, 'nobattle')  # 非战斗区域
        self.image_sprites = []  # 储存精灵图片对象
        self.screen = screen
        self.BGM = bgm
        self.BGM_VOL = 1.0
        self.create_sprite_object()


    def add(self, sprite):
        self.group.add(sprite)

    def center(self, _center):
        self.group.center(_center)

    def draw(self):
        self.group.draw(self.screen)

    def create_sprite_object(self):
        '''
        根据精灵对象创建精灵图片对象
        '''
        for sprite in self.sprites:
            row = int(sprite.properties['actor']) // 4 * 4
            col = int(sprite.properties['actor']) % 4 * 3
            image = NPC(const.IMAGE_DIR +  "Actor\Actor" + sprite.properties['__image__'] + ".png", row,
                        col, sprite.properties['__image__'], sprite.properties['filename'])
            image.rect = sprite.rect
            image.state = sprite.properties['state']
            self.add(image)
            self.image_sprites.append(image)

    def sprite_update(self):
        for sprite in self.image_sprites:
            sprite.update(0)

    def BGMUP(self):
        if self.BGM_VOL < 1.0:
            self.BGM_VOL += 0.1
            self.BGM.set_volume(self.BGM_VOL)

    def BGMDOWN(self):
        if self.BGM_VOL > 0.0:
            self.BGM_VOL -= 0.1
            self.BGM.set_volume(self.BGM_VOL)

class Object(pygame.sprite.Sprite):
    def __init__(self, rect, type=''):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.properties = {'type' : type}

    def add(self, pro_name, pro):
        self.properties[pro_name] = pro


def make_object(_renderer, name):
    """
    Make the blockers for the level.
    """
    sprites = pygame.sprite.Group()
    objects = _renderer.tmx_data.get_layer_by_name("object")
    for _object in objects:
        properties = _object.__dict__
        if properties['name'] == name:
            left = properties['x']
            top = properties['y']
            width = properties['width']
            height = properties['height']
            sprite = Object(pygame.Rect(left, top, width, height), properties['type'])
            for pro_name, pro in properties['properties'].items():
                sprite.add(pro_name, pro)
            sprites.add(sprite)
    return sprites
