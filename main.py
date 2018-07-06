from tools import *
from renderer import *
from icons import *
from dialog import *
from person import *
from shop import *
from start import *

# global
sprites = []
frame_rate = pygame.time.Clock()

# main
pygame.mixer.pre_init(44100, 16, 2, 1024*4)
pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
screen.fill((255, 255, 255))
pygame.display.set_caption("Pet Master")

if os.listdir(const.SAVE_DIR):
    player, scroll_map, dialog, icon, shop = load_game(screen)
else:
    player = Hero('resources/images/Actor/Actor1.png', 0, 0)
    skill1 = Skill("霸王拳", SkillType.DirectDamage, 10, 5)
    skill2 = Skill("霸王若水", SkillType.Heal, 10, 5)
    skill3 = Skill("霸王无敌轰", SkillType.AreaDamage, 7, 10)
    frined_pet1 = Pet("秋田犬", 20, 5, skill1, 1, 20, 500, 20, const.PET_DIR + "pet00.png", 18)
    frined_pet2 = Pet("皮尤", 20, 5, skill2, 1, 20, 500, 20, const.PET_DIR + "pet01.png", 18)
    frined_pet3 = Pet("仙人兽", 20, 5, skill3, 1, 20, 500, 20, const.PET_DIR + "pet02.png", 18)
    player.own_list = [frined_pet1, frined_pet2, frined_pet3]
    player.battle_list = [frined_pet1, frined_pet2, frined_pet3]
    load_tasks(player)
    pygame.mixer.music.load(const.MUSIC_DIR + "home.ogg")
    pygame.mixer.music.set_volume(const.BGM_VOL)
    scroll_map = ScrollMap(const.TMX_DIR + "home.tmx", screen, const.MUSIC_DIR + "home.ogg")
    pygame.mixer.music.play(loops=-1)
    dialog = Dialog(player, screen)
    icon = Icon(scroll_map, player, dialog, screen)
    shop = Shop(player, icon, screen)
    player.controller = "main"
    scroll_map.add(player)
    icon.get_item('萝卜')
    icon.get_item('鲜鱼')

    for start_point in scroll_map.start_points:
        if start_point.properties['__name__'] == 'start_point':
            player.rect.center = (start_point.rect.left, start_point.rect.top)
            break
    scroll_map.center(player.rect.center)

start = Start(screen)
start.draw()


# main loop
running = True


while running:
    frame_rate.tick(60)    # 设置帧数
    time = pygame.time.get_ticks()  #获得以pygame.init()为起点的时间，用于图片变换

    running = check_event(player, scroll_map, icon, dialog, shop, screen)
    if const.LOAD:
        player, scroll_map, dialog, icon, shop = load_game(screen)
        continue
    elif const.SAVE:
        save_game(scroll_map, player, dialog)
    scroll_map = check_switch_scene(player, scroll_map, screen, dialog)
    player.update(time)
    check_collision(player, scroll_map)
    scroll_map.center(player.rect.center)
    check_battle(player, scroll_map, screen, dialog)
    scroll_map.sprite_update()

    scroll_map.draw()
    icon.draw()
    pygame.display.flip()

pygame.quit()
