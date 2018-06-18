import pygame
from pygame.locals import *
from sys import exit

screen_size = (800, 600)

icon_size = (32, 32)
icon_alpha = [180, 180, 180]
icon_location = [(8, 16), (7, 14), (9, 7)]
ui_location = {'bag':(50, 60), 'map':(100, 70), 'panel':(150, 60)}
ui_state_list = ['bag', 'map', 'panel', 'main']
ui_file_name = ["resources/images/bag.tga", "resources/images/map.png", "resources/images/panel.tga"]
font_file_name = "resources/fonts/ink.ttf"
icon_file_name = "resources/images/IconSet.png"

item_dict = { '萝卜':(0, 18), '洋葱':(1, 18), '土豆':(2, 18), '生肉':(3, 18), '鲜鱼':(4, 18),}

class Icon:
    def __init__(self, player, dialog, screen):
        self.icon = pygame.image.load(icon_file_name).convert()
        self.player = player
        self.dialog = dialog
        self.screen = screen
        self.bag_font = pygame.font.Font(font_file_name, 40)
        self.panel_font = pygame.font.Font(font_file_name, 25)
        self.gold_font = pygame.font.Font(font_file_name, 20)
        self.ui = {}
        self.item_name = []
        self.item_position = []
        for i in range(len(ui_file_name)):
            self.ui[ui_state_list[i]] = pygame.image.load(ui_file_name[i]).convert_alpha()
        self.update_bag()
        self.state = 'main'

    def get_image(self, pos):
        return self.icon.subsurface(24 * pos[0], 24 * pos[1], 24, 24)

    def get_item(self, item_name):
        self.item_name.append(item_name)

    def draw_item(self):
        self.item_position.clear()
        for i in range(len(self.item_name)):
            col = i // 6
            row = i % 6
            self.ui[self.state].blit(self.get_image(item_dict[self.item_name[i]]), (22 + 40 * row, 134 + 40 * col))
            self.item_position.append((72 + 40 * row, 184 + 40 * col))

    def draw_value(self):
        for i in range(len(ui_state_list)):
            if ui_state_list[i] == 'panel':
                self.ui['panel'] = pygame.image.load(ui_file_name[i]).convert_alpha()
        self.ui['panel'].blit(self.panel_font.render('生命值：' + str(self.player.hp) + '/' + str(self.player.max_hp), True, (0, 0, 0)), (25, 130))
        self.ui['panel'].blit(self.panel_font.render('法力值：' + str(self.player.mp) + '/' + str(self.player.max_mp), True, (0, 0, 0)), (25, 170))
        self.ui['panel'].blit(self.panel_font.render('攻击力：' + str(self.player.attack), True, (0, 0, 0)), (25, 210))
        self.ui['panel'].blit(self.panel_font.render('防御力：' + str(self.player.defense), True, (0, 0, 0)), (25, 250))
        self.ui['panel'].blit(self.panel_font.render('经验值：' + str(self.player.exp) + '/' + str(self.player.exp_list[self.player.level]), True, (0, 0, 0)), (25, 290))
        self.ui['panel'].blit(self.bag_font.render('人物', True, (0, 0, 0)), (96, 65))

    def draw(self):
        for i in range(len(icon_location)):
            image = self.get_image(icon_location[i])
            image.set_alpha(icon_alpha[i])
            self.screen.blit(image, (20 + 50*i , 20))
        if self.state != 'main':
            self.screen.blit(self.ui[self.state], ui_location[self.state])
        if self.state == 'bag':
            self.draw_item()
        if self.state == 'panel':
            self.draw_value()

    def check_mouse_left_event(self, pos):
        if self.state == 'main':
            for i in range(len(icon_location)):
                if pygame.Rect(20 + 50*i, 20, 32, 32).collidepoint(pos):
                    self.state = ui_state_list[i]
        elif not pygame.Rect(ui_location[self.state], (50 + self.ui[self.state].get_width(), 50 + self.ui[self.state].get_height())).collidepoint(pos):
            for i in range(len(ui_state_list)):
                if ui_state_list[i] == self.state:
                    break
            icon_alpha[i] = 180
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
            self.update_bag()
            item_name = self.item_name[use]
            del self.item_name[use]
            self.draw_item()
            pygame.display.update()
            self.dialog.info("使用了物品["+item_name+"]!")
            self.player.controller = 'main'

    def update_bag(self):
        for i in range(len(ui_state_list)):
            if ui_state_list[i] == 'bag':
                self.ui['bag'] = pygame.image.load(ui_file_name[i]).convert_alpha()
        self.ui['bag'].blit(self.bag_font.render('背包', True, (0, 0, 0)), (96, 65))
        self.ui['bag'].blit(self.gold_font.render('金币', True, (0, 0, 0)), (200, 468))
        gold_font = self.gold_font.render(str(self.player.money), True, (254, 254, 65))
        self.ui['bag'].blit(gold_font, (110 - gold_font.get_width()/2, 468))

    def check_mouse_move_event(self, pos):
        if self.state == 'main':
            for i in range(len(icon_location)):
                if pygame.Rect(20 + 50 * i, 20, 32, 32).collidepoint(pos):
                    icon_alpha[i] = 255
                else:
                    icon_alpha[i] = 180
