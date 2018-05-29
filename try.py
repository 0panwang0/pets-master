from tools import *
from renderer import *
from icons import *
from dialog import Dialog

# global
sprites = []
frame_rate = pygame.time.Clock()

# main
pygame.init()
white = (255, 255, 255)
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
screen.fill(white)
pygame.display.set_caption("Pet Master")

player = NPC('resources/images/Actor1.png', 0, 0)
scroll_map = ScrollMap("resources/tmx/home.tmx", screen)
icon = Icons("resources/images/IconSet.png", screen)
dialog = Dialog(screen)
scroll_map.add(player)
for start_point in scroll_map.start_points:
    if start_point.properties['__name__'] == 'start_point':
        player.rect.center = (start_point.rect.left, start_point.rect.top)
        break
scroll_map.center(player.rect.center)

icon.get_item('萝卜')
icon.get_item('鲜鱼')


# main loop
running = True
while running:
    running = check_event(player, scroll_map, icon)
    frame_rate.tick(60)    # 设置帧数
    time = pygame.time.get_ticks()  #获得以pygame.init()为起点的时间，用于图片变换

    scroll_map = check_switch_scene(player, scroll_map, screen)

    player.update(time)
    check_collision(player, scroll_map)
    scroll_map.center(player.rect.center)
    scroll_map.sprite_update()
    scroll_map.draw()
    icon.draw()
    pygame.display.flip()
pygame.quit()
