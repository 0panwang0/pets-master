from pygame import *
from renderer import *
from battle import *
from shop import *
import random
import os
import pickle

def check_keydown(event, player, scroll_map, dialog, shop):
    '''
    :param event: 获取事件
    :param player: 角色
    :param scroll_map: 地图
    :param dialog: 对话框
    :return: 无
    '''
    if event.key == pygame.K_d:
        player.state = 'move_right'
        player.moving.append(player.state)
    elif event.key == pygame.K_a:
        player.state = 'move_left'
        player.moving.append(player.state)
    elif event.key == pygame.K_w:
        player.state = 'move_up'
        player.moving.append(player.state)
    elif event.key == pygame.K_s:
        player.state = 'move_down'
        player.moving.append(player.state)
    elif event.key == pygame.K_SPACE:
        check_dialogue(player, scroll_map, dialog, shop)


def check_keyup(event, player):
    '''
    :param event: 获取事件
    :param player: 角色
    :return: 无
    '''
    if event.key == pygame.K_d:
        if 'move_right' in player.moving:
            player.moving.remove('move_right')
            if not player.moving:
                player.state = 'rest_right'
            else:
                player.state = player.moving[-1]
        else:
            player.state = 'rest_right'
    elif event.key == pygame.K_a:
        if 'move_left' in player.moving:
            player.moving.remove('move_left')
            if not player.moving:
                player.state = 'rest_left'
            else:
                player.state = player.moving[-1]
        else:
            player.state = 'rest_left'
    elif event.key == pygame.K_w:
        if 'move_up' in player.moving:
            player.moving.remove('move_up')
            if not player.moving:
                player.state = 'rest_up'
            else:
                player.state = player.moving[-1]
        else:
            player.state = 'rest_up'
    elif event.key == pygame.K_s:
        if 'move_down' in player.moving:
            player.moving.remove('move_down')
            if not player.moving:
                player.state = 'rest_down'
            else:
                player.state = player.moving[-1]
        else:
            player.state = 'rest_down'


def check_event(player, scroll_map, icon, dialog, shop):
    '''
    :param player: 玩家对象
    :return: 如果
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, player, scroll_map, dialog, shop)
        if event.type == pygame.KEYUP:
            check_keyup(event, player)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            buttons = pygame.mouse.get_pressed()
            for index in range(len(buttons)):
                if buttons[index]:
                    if index == 0:
                        icon.check_mouse_left_event(pygame.mouse.get_pos())
                    elif index == 2:
                        icon.check_mouse_right_event(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEMOTION:
            icon.check_mouse_move_event(pygame.mouse.get_pos())
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
        scroll_map.BGM.stop()
        screen.fill((0, 0, 0))
        pygame.display.flip()
        scroll_map = ScrollMap(TMX[door_list[0].properties['type']], screen, pygame.mixer.Sound(const.MUSIC_DIR + door_list[0].properties['type'] + ".ogg"))
        for door in scroll_map.doors.sprites():
            if door.properties['type'] == door_list[0].properties['world']:
                for start_point in scroll_map.start_points.sprites():
                    if '__name__' in start_point.properties.keys() and \
                            start_point.properties['__name__'] == door.properties['start']:
                        player.rect.centerx = start_point.rect.centerx
                        player.rect.bottom = start_point.rect.bottom
        scroll_map.add(player)
        scroll_map.center(player.rect.center)
        scroll_map.BGM.play(loops=-1)
    return scroll_map


def check_collision(player, scroll_map):
    if pygame.sprite.spritecollideany(player, scroll_map.blockers):
        player.move_back()
    for sprite in scroll_map.image_sprites:
        if pygame.sprite.collide_rect(player, sprite):
            player.move_back()
            break


# 随机生成怪物
def random_choose_enermy(enermy_list, scroll_map):
    random_num = random.randint(1, 4)
    enermy_num = len(os.listdir('resources/pet_bin/forest'))
    for _ in range(random_num):
        random_enermy = random.randint(0, enermy_num-1)
        with open('resources\pet_bin\\' + scroll_map.doors.sprites()[0].properties['world']
                  + '\\' + str(random_enermy) + '.bin', "rb") as object:
            bin = object.read()
            enermy = pickle.loads(bin)
        enermy_list.append(enermy)


# 检查什么时候触发战斗
def check_battle(player, scroll_map, screen, dialog):
    if scroll_map.nobattle_area:
        if not pygame.sprite.spritecollideany(player, scroll_map.nobattle_area) and player.moving:
            start_batlle = random.randint(0, 250)
            if start_batlle < 5:
                scroll_map.BGM.stop()
                enermy_list = []
                random_choose_enermy(enermy_list, scroll_map)
                battle = Battle(screen, player, enermy_list, dialog)
                battle.start_battle()
                player.state = "rest_" + player.moving[-1][5:]
                player.moving.clear()
                scroll_map.BGM.play(loops=True)

def check_dialogue(player, scroll_map, dialog, shop):
    for sprite in scroll_map.image_sprites:
        left = Object(pygame.Rect(sprite.rect.left-sprite.rect.width, sprite.rect.top, sprite.rect.width, sprite.rect.height))
        right = Object(pygame.Rect(sprite.rect.left+sprite.rect.width, sprite.rect.top, sprite.rect.width, sprite.rect.height))
        up = Object(pygame.Rect(sprite.rect.left, sprite.rect.top-sprite.rect.height, sprite.rect.width, sprite.rect.height))
        down = Object(pygame.Rect(sprite.rect.left, sprite.rect.top+sprite.rect.height, sprite.rect.width, sprite.rect.height))
        if pygame.sprite.collide_rect(player, left) and player.state[5:] == "right":
            sprite.state = "rest_left"
            player.moving.clear()
        elif pygame.sprite.collide_rect(player, right) and player.state[5:] == "left":
            sprite.state = "rest_right"
            player.moving.clear()
        elif pygame.sprite.collide_rect(player, up) and player.state[5:] == "down":
            sprite.state = "rest_up"
            player.moving.clear()
        elif pygame.sprite.collide_rect(player, down) and player.state[5:] == "up":
            if sprite.file_name == "shop":
                dialog.info('欢迎，我们为您提供了许多东西~',  'mid')
                shop.draw()
            else:
                sprite.state = "rest_down"
                player.moving.clear()
        else:
            continue
        player.controller = 'dialog'
        scroll_map.sprite_update()
        scroll_map.draw()
        pygame.display.update()
        dialog.run(sprite)



TMX = load_all_tmx(os.path.join('resources', 'tmx'))