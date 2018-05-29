from pygame.locals import *
import sys
from person import Person
from renderer import *


pygame.init()
white = (255, 255, 255)
# create window
screenSize = (800, 600)
screen = pygame.display.set_mode(screenSize)
screen.fill(white)
renderer = Map("resources/tmx/desert.tmx")
blockers = make_blockers(renderer)
frame_rate = pygame.time.Clock()
image = pygame.image.load('./images/Actor1.png').convert_alpha()
player = Person(image)
# player._position = [screen.get_rect().centerx, screen.get_rect().bottom]
# player.rect.centerx = screen.get_rect().centerx
# player.rect.bottom = screen.get_rect().bottom
scroll_map = ScrollMap(renderer, screen)
scroll_map.add(player)
scroll_map.center(player.rect.center)
move_dist = 2

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if keys[K_RIGHT]:
        player.velocity[0] = 1
        player.state = 'move_right'
    if keys[K_LEFT]:
        player.velocity[0] = -1
        player.state = 'move_left'
    if keys[K_UP]:
        player.velocity[1] = -1
        player.state = 'move_up'
    if keys[K_DOWN]:
        player.velocity[1] = 1
        player.state = 'move_down'
    elif 1 not in keys:
        if player.state == 'move_right':
            player.state = 'rest_right'
        elif player.state == 'move_up':
            player.state = 'rest_up'
        elif player.state == 'move_down':
            player.state = 'rest_down'
        elif player.state == 'move_left':
            player.state = 'rest_left'
    #  设置帧数
    frame_rate.tick(60)
    tick = pygame.time.get_ticks()
    pygame.display.set_caption("GameName " + str(frame_rate.get_fps()) + ' time: ' + str(tick))
    player.update(move_dist, blockers, tick)
    scroll_map.center(player.rect.center)
    scroll_map.draw(screen)
    pygame.display.flip()
pygame.quit()
