from pygame import *
from renderer import *
import os


def check_key_events(keys, player):
    '''
    :param keys: 玩家按下的按键列表
    :param player: 玩家对象
    :return: 无
    '''
    if keys[K_RIGHT]:
        player.state = 'move_right'
    elif keys[K_LEFT]:
        player.state = 'move_left'
    elif keys[K_UP]:
        player.state = 'move_up'
    elif keys[K_DOWN]:
        player.state = 'move_down'
    elif keys[K_RIGHT] != True and keys[K_LEFT] != True and keys[K_UP] != True and keys[K_DOWN] != True:
        if player.state == 'move_right':
            player.state = 'rest_right'
        elif player.state == 'move_up':
            player.state = 'rest_up'
        elif player.state == 'move_down':
            player.state = 'rest_down'
        elif player.state == 'move_left':
            player.state = 'rest_left'


def check_event(player):
    '''
    :param player: 玩家对象
    :return: 如果
    '''
    for event in pygame.event.get():
        pass
        if event.type == pygame.QUIT:
            return False
    keys = pygame.key.get_pressed()
    check_key_events(keys, player)
    return True


def load_all_tmx(directory, accept=('.tmx')):
    '''
    :param directory: 文件路径
    :param accept: 文件属性
    :return: 对应文件
    '''
    tmxs = {}
    for tmx in os.listdir(directory):
        name, ext = os.path.splitext(tmx)
        if ext.lower() in accept:
            tmxs[name] = os.path.join(directory, tmx)
    return tmxs


def check_switch_scene(player, scroll_map, screen):
    '''
    :param player: 玩家对象
    :param scroll_map: 地图对象
    :param screen: 层
    :return:scroll_map
    '''
    door_list = pygame.sprite.spritecollide(player, scroll_map.doors, False)
    if door_list and door_list[0].properties['state'] == player.state[5:]:
        scroll_map = ScrollMap(TMX[door_list[0].properties['type']], screen)
        for door in scroll_map.doors.sprites():
            if door.properties['type'] == door_list[0].properties['world']:
                for start_point in scroll_map.start_points.sprites():
                    if '__name__' in start_point.properties.keys() and \
                            start_point.properties['__name__'] == door.properties['start']:
                        player.rect.centerx = start_point.rect.centerx
                        player.rect.bottom = start_point.rect.bottom
        scroll_map.add(player)
        scroll_map.center(player.rect.center)
    return scroll_map


TMX = load_all_tmx(os.path.join('resources', 'tmx'))