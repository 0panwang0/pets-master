from tools import *
from renderer import *
from icons import *
from dialog import *
from person import *
from shop import *


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

player = Hero('resources/images/Actor/Actor1.png', 0, 0, screen)
skill1 = Skill("Direct", SkillType.DirectDamage, 6, 5)
skill2 = Skill("Heal", SkillType.Heal, 10, 5)
frined_pet1 = Pet("Friend Pet1", 20, 5, skill1, 1, 20, 500, 20, const.PET_DIR + "pet00.png", 18)
frined_pet2 = Pet("Friend Pet2", 20, 5, skill2, 1, 20, 500, 20, const.PET_DIR + "pet01.png", 18)
player.own_list = [frined_pet1, frined_pet2]
player.battle_list = [frined_pet1, frined_pet2]

scroll_map = ScrollMap(const.TMX_DIR + "home.tmx", screen)
scroll_map.BGM = pygame.mixer.Sound(const.MUSIC_DIR + "home.ogg")
scroll_map.BGM.play(loops=True)
dialog = Dialog(player, screen)
icon = Icon(player, dialog, screen)
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


# main loop
running = True
while running:

    frame_rate.tick(60)    # 设置帧数
    time = pygame.time.get_ticks()  #获得以pygame.init()为起点的时间，用于图片变换

    running = check_event(player, scroll_map, icon, dialog, shop)
    scroll_map = check_switch_scene(player, scroll_map, screen)

    player.update(time)
    check_collision(player, scroll_map)
    scroll_map.center(player.rect.center)
    check_battle(player, scroll_map, screen)
    scroll_map.sprite_update()

    if player.controller == 'main':
        scroll_map.draw()
        icon.draw()
        pygame.display.flip()
    # elif player.controller == 'battle':
    #     battle = Battle(screen, player, enermy_list)
    #     battle.start_battle()

pygame.quit()
