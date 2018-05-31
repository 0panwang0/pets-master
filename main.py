from tools import *
from renderer import *
from icons import *
from dialog import *
from person import *

# global
sprites = []
frame_rate = pygame.time.Clock()

# main
pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
screen.fill((255, 255, 255))
pygame.display.set_caption("Pet Master")

player = Hero('resources/images/Actor1.png', 0, 0, screen)
scroll_map = ScrollMap("resources/tmx/home.tmx", screen)

dialog = Dialog(player, screen)
icon = Icon(player, dialog, screen)


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

    running = check_event(player, scroll_map, icon, dialog)
    scroll_map = check_switch_scene(player, scroll_map, screen)

    player.update(time)
    check_collision(player, scroll_map)
    scroll_map.center(player.rect.center)
    scroll_map.sprite_update()

    if player.controller == 'main':
        scroll_map.draw()
        icon.draw()
        pygame.display.flip()

pygame.quit()
