import pygame
import pytmx
import pyscroll
from person import NPC

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


class ScrollMap:
    def __init__(self, filename, screen):
        renderer = Map(filename)
        self.map_data = pyscroll.data.TiledMapData(renderer.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, (screen.get_rect().width
                                                                   , screen.get_rect().height), clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        self.blockers = make_object(renderer, 'blocker')    # 禁止角色横跨的位置
        self.doors = make_object(renderer, 'door')  # 通往其它地图的门
        self.start_points = make_object(renderer, 'start point')    # 角色在一张地图的起始点
        self.sprites = make_object(renderer, 'sprite')  # 精灵对象
        self.image_sprites = []  # 储存精灵图片对象
        self.image_row = 0  # 图片素材中精灵图片的行
        self.image_col = 0  # 图片素材中精灵图片的列
        self.image_num = 2  # 图片素材标号
        self.image_maxcol = 4   # 图片素材中精灵图片最大行
        self.image_maxrow = 2   # 图片素材中精灵图片最大列
        self.create_sprite_object()
        self.screen = screen

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
            image = NPC("./images/Actor" + str(self.image_num) + ".png", self.image_row * 4, self.image_col * 3)
            if self.image_col == self.image_maxcol: # 换到下一个精灵图片，相应地改变行列或图片素材
                if self.image_row == self.image_maxrow:
                    self.image_num += 1
                    self.image_row = 0
                    self.image_col = 0
                else:
                    self.image_row += 1
                    self.image_col = 0
            else:
                self.image_col += 1
            image.rect.center = sprite.rect.center
            image.state = sprite.properties['state']
            self.add(image)
            self.image_sprites.append(image)

    def sprite_update(self):
        for sprite in self.image_sprites:
            sprite.update(0)


class Object(pygame.sprite.Sprite):
    '''
    从地图中获取各种对象
    '''
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
