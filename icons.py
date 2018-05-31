import pygame
from pygame.locals import *
from sys import exit

screen_size = (800, 600)

icon_size = (32, 32)
icon_alpha = [180, 180]
icon_location = [(8, 16), (7, 14)]
ui_location = {'bag':(50, 50), 'map':(100, 50)}
ui_state_list = ['bag', 'map', 'main']
ui_file_name = ["resources/images/bag.tga", "resources/images/map.png"]
font_file_name = "resources/fonts/ink.ttf"
icon_file_name = "resources/images/IconSet.png"

item_dict = { '萝卜':(0, 18), '洋葱':(1, 18), '土豆':(2, 18), '生肉':(3, 18), '鲜鱼':(4, 18),}

class Icon:
    def __init__(self, player, dialog, screen):
        self.icon = pygame.image.load(icon_file_name).convert()
        self.player = player
        self.dialog = dialog
        self.screen = screen
        self.font = pygame.font.Font(font_file_name, 40)
        self.ui = {}
        self.item_name = []
        self.item_position = []
        for i in range(len(ui_file_name)):
            self.ui[ui_state_list[i]] = pygame.image.load(ui_file_name[i]).convert_alpha()
        self.ui['bag'].blit(self.font.render('背包', True, (0, 0, 0)), (96, 65))
        self.state = 'main'

    def get_image(self, pos):
        return pygame.transform.scale(self.icon.subsurface(24 * pos[0], 24 * pos[1], 24, 24), icon_size)

    def get_item(self, item_name):
        self.item_name.append(item_name)

    def draw_item(self):
        self.item_position.clear()
        for i in range(len(self.item_name)):
            col = i // 6
            row = i % 6
            self.ui[self.state].blit(self.get_image(item_dict[self.item_name[i]]), (18 + 40 * row, 130 + 40 * col))
            self.item_position.append((68 + 40 * row, 180 + 40 * col))

    def draw(self):
        for i in range(len(icon_location)):
            image = self.get_image(icon_location[i])
            image.set_alpha(icon_alpha[i])
            self.screen.blit(image, (20 + 50*i , 20))
        if self.state != 'main':
            self.screen.blit(self.ui[self.state], ui_location[self.state])
        if self.state == 'bag':
            self.draw_item()

    def check_mouse_left_event(self, pos):
        if self.state == 'main':
            for i in range(len(icon_location)):
                if pygame.Rect(20 + 50*i, 20, 32, 32).collidepoint(pos):
                    self.state = ui_state_list[i]
        elif not pygame.Rect(ui_location[self.state], (50 + self.ui[self.state].get_width(), 50 + self.ui[self.state].get_height())).collidepoint(pos):
            self.state = 'main'

    def check_mouse_right_event(self, pos):
        if self.state == 'bag':
            use = -1
            for i in range(len(self.item_position)):
                if pygame.Rect(self.item_position[i], (40, 40)).collidepoint(pos):
                    use = i
                    break
            if use < 0:
                return
            item_name = self.item_name[use]
            del self.item_name[use]
            for i in range(len(ui_state_list)):
                if ui_state_list[i] == 'bag':
                    self.ui['bag'] = pygame.image.load(ui_file_name[i]).convert_alpha()
                    self.ui['bag'].blit(self.font.render('背包', True, (0, 0, 0)), (96, 65))
            self.draw_item()
            pygame.display.update()

            self.player.controller = 'info'
            self.dialog.info("使用了物品["+item_name+"]!")
            while self.player.controller != 'main':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                        self.player.controller = 'main'

    def check_mouse_move_event(self, pos):
        if self.state == 'main':
            for i in range(len(icon_location)):
                if pygame.Rect(20 + 50 * i, 20, 32, 32).collidepoint(pos):
                    icon_alpha[i] = 255
                else:
                    icon_alpha[i] = 180
