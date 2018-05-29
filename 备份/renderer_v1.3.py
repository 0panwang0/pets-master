import pygame
import pytmx
import pyscroll

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
    def __init__(self, renderer, screen):
        self.map_data = pyscroll.data.TiledMapData(renderer.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, (screen.get_rect().width
                                                                   , screen.get_rect().height), clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)

    def add(self, sprite):
        self.group.add(sprite)

    def center(self, _center):
        self.group.center(_center)

    def draw(self, screen):
        self.group.draw(screen)


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
            blocker = Blocker(pygame.Rect(left, top, 32, 32))
            _blockers.add(blocker)
    return _blockers