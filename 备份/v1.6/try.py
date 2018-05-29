from tools import *
from renderer import *

# global
sprites = []
frame_rate = pygame.time.Clock()

# main
pygame.init()
white = (255, 255, 255)
screenSize = (800, 600)
screen = pygame.display.set_mode(screenSize)
screen.fill(white)
pygame.display.set_caption("Pet Master")

player = Person('./images/Actor1.png', 0, 0)
scroll_map = ScrollMap("resources/tmx/home.tmx", screen)
scroll_map.add(player)
for start_point in scroll_map.start_points:
    if start_point.properties['__name__'] == 'start_point':
        player.rect.center = (start_point.rect.left, start_point.rect.top)
        break
scroll_map.center(player.rect.center)

# main loop
running = True
while running:
    running = check_event(player, scroll_map)
    frame_rate.tick(60)    # 设置帧数
    time = pygame.time.get_ticks()  #获得以pygame.init()为起点的时间，用于图片变换

    scroll_map = check_switch_scene(player, scroll_map, screen)

    player.update(time)
    check_collision(player, scroll_map)
    scroll_map.center(player.rect.center)
    scroll_map.sprite_update()
    scroll_map.draw(screen)
    pygame.display.flip()
pygame.quit()
