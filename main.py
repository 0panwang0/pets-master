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
pygame.mixer.music.load(const.MUSIC_DIR + "startGame.ogg")
pygame.mixer.music.set_volume(const.BGM_VOL)
pygame.mixer.music.play()

player = Hero('resources/images/Actor/Actor1.png', 0, 0)
dialog = Dialog(player, screen)

start = Start(screen, dialog)
start.draw()

if const.CONTINUEGAME:
    player, scroll_map, dialog, icon, shop = load_game(screen)
    const.CONTINUEGAME = 0
elif const.NEWGAME:
    player, scroll_map, dialog, icon, shop = initial_game(screen)
    const.NEWGAME = 0

# main loop
running = True

while running:
    frame_rate.tick(60)    # 设置帧数
    time = pygame.time.get_ticks()  # 获得以pygame.init()为起点的时间，用于图片变换

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
    if player.hp == 0:
        start = Start(screen, dialog)
        start.draw()
        if const.CONTINUEGAME:
            player, scroll_map, dialog, icon, shop = load_game(screen)
            const.CONTINUEGAME = 0
        elif const.NEWGAME:
            player, scroll_map, dialog, icon, shop = initial_game(screen)
            const.NEWGAME = 0

    scroll_map.sprite_update()
    scroll_map.draw()
    icon.draw()
    pygame.display.flip()

pygame.quit()
