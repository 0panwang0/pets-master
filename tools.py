from pygame import *
from renderer import *
from battle import *
from shop import *
import random
import os
import pickle
from dialog import Dialog
from shop import Shop
from icons import Icon
import json
from person import Hero
from pets import *
import time


def check_keydown(event, player, scroll_map, dialog, shop, screen):
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
        check_dialogue(player, scroll_map, dialog, shop, screen)


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


def check_event(player, scroll_map, icon, dialog, shop, screen):
    '''
    :param player: 玩家对象
    :return: 如果
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, player, scroll_map, dialog, shop, screen)
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


def load_all_tmx(directory, accept='.tmx'):
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


def check_switch_scene(player, scroll_map, screen, dialog):
    '''
    :param player: 玩家对象
    :param scroll_map: 地图对象
    :param screen: 层
    :return:scroll_map
    '''
    door_list = pygame.sprite.spritecollide(player, scroll_map.doors, False)
    if door_list and door_list[0].properties['state'] == player.state[5:]:
        pygame.mixer.music.stop()
        screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.mixer.music.load(const.MUSIC_DIR + door_list[0].properties['type'] + ".ogg")
        pygame.mixer.music.play(loops=-1)
        scroll_map.reload(TMX[door_list[0].properties['type']], screen, const.MUSIC_DIR + door_list[0].properties['type'] + ".ogg")
        for door in scroll_map.doors.sprites():
            if door.properties['type'] == door_list[0].properties['world']:
                for start_point in scroll_map.start_points.sprites():
                    if '__name__' in start_point.properties.keys() and \
                            start_point.properties['__name__'] == door.properties['start']:
                        player.rect.centerx = start_point.rect.centerx
                        player.rect.bottom = start_point.rect.bottom
        scroll_map.add(player)
        scroll_map.center(player.rect.center)
        scroll_map.sprite_update()
        scroll_map.draw()
        if scroll_map.info:
            if player.level < int(scroll_map.info.sprites()[0].properties['level']) and \
                    door_list[0].properties['type'] not in player.place:
                dialog.info('危险！推荐等级为' + scroll_map.info.sprites()[0].properties['level'], 'mid')
                player.place.append(door_list[0].properties['type'])
        if player.moving:
            player.state = 'rest' + player.moving[-1][4:]
            player.moving.clear()
    return scroll_map


def check_collision(player, scroll_map):
    if pygame.sprite.spritecollideany(player, scroll_map.blockers):
        player.move_back()
    for sprite in scroll_map.image_sprites:
        if pygame.sprite.collide_rect(player, sprite):
            player.move_back()
            break


# 随机生成怪物
def random_choose_enemy(enemy_list, scroll_map):
    random_num = random.randint(1, 4)
    enemy_num = len(os.listdir('resources/pet/forest'))
    for _ in range(random_num):
        random_enemy = random.randint(0, enemy_num-1)
        with open('resources\pet\\' + scroll_map.doors.sprites()[0].properties['world']
                  + '\\' + str(random_enemy) + '.bin', "rb") as object:
            bin_data = object.read()
            enemy = pickle.loads(bin_data)
        enemy_list.append(enemy)


# 检查什么时候触发战斗
def check_battle(player, scroll_map, screen, dialog):
    if scroll_map.nobattle_area:
        if not pygame.sprite.spritecollideany(player, scroll_map.nobattle_area) and player.moving:
            start_batlle = random.randint(0, 250)
            if start_batlle < 5:
                pygame.mixer.music.stop()
                enermy_list = []
                random_choose_enemy(enermy_list, scroll_map)
                battle = Battle(screen, player, enermy_list, dialog, scroll_map.doors.sprites()[0].properties['world'])
                battle.start_battle()
                if player.hp == 0:
                    pygame.mixer.music.load(const.MUSIC_DIR + "startGame.ogg")
                    pygame.mixer.music.set_volume(const.BGM_VOL)
                    pygame.mixer.music.play()
                    return
                player.state = "rest_" + player.moving[-1][5:]
                player.moving.clear()
                pygame.mixer.music.load(const.MUSIC_DIR + scroll_map.doors.sprites()[0].properties['world'] + '.ogg')
                pygame.mixer.music.play(loops=True)


def hotel(player, dialog, screen):
    if player.money >= const.HOTEL_MONEY:
        dialog.info('小伙子，来客栈休息一下吧~', 'mid')
        screen.fill((0, 0, 0))
        pygame.display.flip()
        time.sleep(1)
        player.hp = player.max_hp
        player.mp = player.max_mp
        dialog.info('人物恢复最佳状态', 'mid')
        dialog.info('失去' + str(const.HOTEL_MONEY) + '金币', 'mid')
        player.money -= const.HOTEL_MONEY
        const.HOTEL_MONEY = int(const.HOTEL_MONEY + const.HOTEL_MONEY * 0.5)
    else:
        dialog.info('小伙子，你没钱不能在这里休息啊！', 'mid')


def check_task(player, task_num):
    for task in player.tasks_list:
        if task_num == task.task_num:
            return True
    return False


def check_dialogue(player, scroll_map, dialog, shop, screen):
    for sprite in scroll_map.image_sprites:
        left = Object(pygame.Rect(sprite.rect.left-sprite.rect.width, sprite.rect.top,
                                  sprite.rect.width, sprite.rect.height))
        right = Object(pygame.Rect(sprite.rect.left+sprite.rect.width, sprite.rect.top,
                                   sprite.rect.width, sprite.rect.height))
        up = Object(pygame.Rect(sprite.rect.left, sprite.rect.top-sprite.rect.height,
                                sprite.rect.width, sprite.rect.height))
        down = Object(pygame.Rect(sprite.rect.left, sprite.rect.top+sprite.rect.height,
                                  sprite.rect.width, sprite.rect.height))
        if pygame.sprite.collide_rect(player, left) and player.state[5:] == "right":
            if sprite.file_name == "shop":
                dialog.info('欢迎，我们为您提供了许多东西~',  'mid')
                shop.draw()
            else:
                sprite.state = "rest_left"
                player.moving.clear()
        elif pygame.sprite.collide_rect(player, right) and player.state[5:] == "left":
            if sprite.file_name == "shop":
                dialog.info('欢迎，我们为您提供了许多东西~',  'mid')
                shop.draw()
            elif sprite.file_name == "hotel":
                hotel(player, dialog, screen)
            else:
                sprite.state = "rest_right"
                player.moving.clear()
        elif pygame.sprite.collide_rect(player, up) and player.state[5:] == "down":
            if sprite.file_name == "shop":
                dialog.info('欢迎，我们为您提供了许多东西~',  'mid')
                shop.draw()
            else:
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
        if len(sprite.file_name) < 4 and not check_task(player, int(sprite.file_name)):
            with open("resources\\task\\initial\\" + sprite.file_name + ".bin", "rb") as ob:
                bin_data = ob.read()
                task = pickle.loads(bin_data)
                player.tasks_list.append(task)
                dialog.info("接受任务[" + task.task_name + "]", "mid")


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            pass
        else:
            os.remove(c_path)


def save_tasks(player):
    for i in range(len(player.tasks_list)):
        task_packet = pickle.dumps(player.tasks_list[i])
        with open("resources\\task\\" + str(i+1) + ".bin", "wb") as object:
            object.write(task_packet)


def load_tasks(player):
    tasks_list = []
    for task in os.listdir("resources\\task\\")[:-1]:
        with open("resources\\task\\" + task, "rb") as ob:
            bin_data = ob.read()
            tasks_list.append(pickle.loads(bin_data))
    player.tasks_list = tasks_list


def save_game(scroll_map, player, dialog):
    del_file("resources\\save")
    del_file("resources\\task")

    save_scroll_map = []
    save_scroll_map.append(scroll_map.filename)
    save_scroll_map.append(scroll_map.music)
    with open("resources\\save\\scroll_map.json", "w") as ob:
        json.dump(save_scroll_map, ob)

    save_hero = player.save()
    with open("resources\\save\\hero.json", "w") as ob:
        json.dump(save_hero, ob)

    save_own_pet = []
    for i in range(len(player.own_list)):
        save_own_pet.append(player.own_list[i].save())
    with open("resources\\save\\own_list.json", "w") as ob:
        json.dump(save_own_pet, ob)

    save_battle_pet = []
    for i in range(len(player.battle_list)):
        save_battle_pet.append(player.own_list.index(player.battle_list[i]))
    with open("resources\\save\\battle_list.json", "w") as ob:
        json.dump(save_battle_pet, ob)

    save_tasks(player)

    const.SAVE = 0

    dialog.info("保存成功", "mid")


# 返回储存有宠物信息的列表
def pet_list(path):
    with open(path, "r") as ob:
        load_pet = json.load(ob)

    pet_info = []
    for i in range(len(load_pet)):
        if load_pet[i][3][1] == SkillType.DirectDamage.value:
            skill = Skill(load_pet[i][3][0], SkillType.DirectDamage, load_pet[i][3][2], load_pet[i][3][3])
        elif load_pet[i][3][1] == SkillType.AreaDamage.value:
            skill = Skill(load_pet[i][3][0], SkillType.AreaDamage, load_pet[i][3][2], load_pet[i][3][3])
        else:
            skill = Skill(load_pet[i][3][0], SkillType.Heal, load_pet[i][3][2], load_pet[i][3][3])
        pet = Pet(load_pet[i][0], load_pet[i][1], load_pet[i][2], skill, load_pet[i][4], load_pet[i][5],
                  load_pet[i][6], load_pet[i][7], load_pet[i][8], load_pet[i][9])
        pet_info.append(pet)

    return pet_info


def load_game(screen):
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    pygame.display.flip()

    own_list = pet_list("resources\\save\\own_list.json")
    battle_list = []
    with open("resources\\save\\battle_list.json", "r") as ob:
        load_battle_list = json.load(ob)
    for i in range(len(load_battle_list)):
        battle_list.append(own_list[load_battle_list[i]])

    with open("resources\\save\\hero.json", "r") as ob:
        load_hero = json.load(ob)
    player = Hero(load_hero[0], load_hero[1], load_hero[2])
    player.load(load_hero)
    player.own_list = own_list
    player.battle_list = battle_list
    load_tasks(player)

    with open("resources\\save\\scroll_map.json", "r") as ob:
        load_scroll_map = json.load(ob)
    scroll_map = ScrollMap(load_scroll_map[0], screen, load_scroll_map[1])
    scroll_map.add(player)
    scroll_map.center(player.rect.center)

    dialog = Dialog(player, screen)

    icon = Icon(scroll_map, player, dialog, screen)

    shop = Shop(player, icon, screen)

    pygame.mixer.music.load(scroll_map.music)
    pygame.mixer.music.set_volume(const.BGM_VOL)
    pygame.mixer.music.play(loops=-1)

    const.LOAD = 0

    return player, scroll_map, dialog, icon, shop


def initial_game(screen):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(const.MUSIC_DIR + "home.ogg")
    pygame.mixer.music.set_volume(const.BGM_VOL)
    player = Hero('resources/images/Actor/Actor1.png', 0, 0)
    # load_tasks(player)
    player.controller = "main"
    dialog = Dialog(player, screen)
    scroll_map = ScrollMap(const.TMX_DIR + "home.tmx", screen, const.MUSIC_DIR + "home.ogg")
    pygame.mixer.music.play(loops=-1)
    icon = Icon(scroll_map, player, dialog, screen)
    shop = Shop(player, icon, screen)
    scroll_map.add(player)
    for start_point in scroll_map.start_points:
        if start_point.properties['__name__'] == 'start_point':
            player.rect.center = (start_point.rect.left, start_point.rect.top)
            break
    scroll_map.center(player.rect.center)
    return player, scroll_map, dialog, icon, shop

TMX = load_all_tmx(os.path.join('resources', 'tmx'))
