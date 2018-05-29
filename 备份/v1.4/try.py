from tools import *
from person import Person
from renderer import *


pygame.init()
white = (255, 255, 255)
screenSize = (800, 600)
screen = pygame.display.set_mode(screenSize)
screen.fill(white)
pygame.display.set_caption("Pet Master")

renderer = Map("resources/tmx/desert.tmx")
blockers = make_blockers(renderer)
doors = make_door(renderer)
player = Person('./images/Actor1.png', 0, 0)
# player.rect.centerx = doors.sprites()[0].rect.centerx
# player.rect.bottom = doors.sprites()[0].rect.bottom
scroll_map = ScrollMap(renderer, screen)
scroll_map.add(player)
scroll_map.center(player.rect.center)

frame_rate = pygame.time.Clock()

# main loop
running = True
while running:
    running = check_event(player)
    frame_rate.tick(60)    # 设置帧数
    time = pygame.time.get_ticks()  #获得以pygame.init()为起点的时间，用于图片变换
    door_list =  pygame.sprite.spritecollide(player, doors, False)
    if door_list:
        renderer = Map("resources/tmx/" + door_list[0].type + ".tmx")
        blockers = make_blockers(renderer)
        doorss = make_door(renderer)
        player.rect.centerx = doorss.sprites()[0].rect.centerx
        player.rect.bottom = doorss.sprites()[0].rect.bottom
        player.state = "rest_up"
        scroll_map = ScrollMap(renderer, screen)
        scroll_map.add(player)
        scroll_map.center(player.rect.center)
        doors.remove(door_list[0])
        door_list.clear()

    player.update(blockers, time)
    scroll_map.center(player.rect.center)
    scroll_map.draw(screen)
    pygame.display.flip()
pygame.quit()
