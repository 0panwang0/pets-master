from tools import *
from person import Person
from renderer import *

pygame.init()
white = (255, 255, 255)
screenSize = (800, 600)
screen = pygame.display.set_mode(screenSize)
screen.fill(white)
pygame.display.set_caption("Pet Master")

player = Person('./images/Actor1.png', 0, 0)
player2 = Person('./images/Actor1.png', 4, 0)
# player.rect.centerx = doors.sprites()[0].rect.centerx
# player.rect.bottom = doors.sprites()[0].rect.bottom
scroll_map = ScrollMap("resources/tmx/home.tmx", screen)

player2.rect.center = (100, 100)
scroll_map.add(player)
scroll_map.add(player2)
for start_point in scroll_map.start_points:
    if start_point.properties['__name__'] == 'start_point':
        player.rect.center = (start_point.rect.left, start_point.rect.top)
        break
scroll_map.center(player.rect.center)

frame_rate = pygame.time.Clock()


# main loop
running = True
while running:
    running = check_event(player)
    frame_rate.tick(60)    # 设置帧数
    time = pygame.time.get_ticks()  #获得以pygame.init()为起点的时间，用于图片变换

    scroll_map = check_switch_scene(player, scroll_map, screen)

    player.update(scroll_map.blockers, time)
    scroll_map.center(player.rect.center)
    scroll_map.draw(screen)
    pygame.display.flip()
pygame.quit()
