import pygame
from pygame.locals import *
from sys import exit
import const


screen_size = (800, 600)

icon_size = (32, 32)
icon_alpha = [180, 180, 180, 180]
icon_location = [(8, 16), (7, 14), (9, 7), (0, 14)]
ui_location = {'bag':(50, 60), 'map':(100, 70), 'panel':(150, 60), 'sprite':(200, 60)}
ui_state_list = ['bag', 'map', 'panel', 'sprite', 'main']
ui_file_name = ["resources/images/bag.tga", "resources/images/map.png", "resources/images/panel.tga", "resources/images/sprite.tga"]
font_file_name = "resources/fonts/ink.ttf"
icon_file_name = "resources/images/IconSet.png"
arrow_file_name = "resources/images/arrow.png"

item_dict = { '萝卜':(0, 18), '洋葱':(1, 18), '土豆':(2, 18), '生肉':(3, 18), '鲜鱼':(4, 18),}

class Icon:
    def __init__(self, player, dialog, screen):
        self.icon = pygame.image.load(icon_file_name).convert()
        self.player = player
        self.dialog = dialog
        self.screen = screen
        self.bag_font = pygame.font.Font(font_file_name, 40)
        self.sprite_font = pygame.font.Font(font_file_name, 30)
        self.description_font = pygame.font.Font(font_file_name, 20)
        self.panel_font = pygame.font.Font(font_file_name, 25)
        self.gold_font = pygame.font.Font(font_file_name, 20)
        self.ui = {}
        self.item_name = []
        self.item_position = []
        self.sprite_index = 0
        self.description_item = ["等级", "经验", "伤害", "技能", "状态"]
        for i in range(len(ui_file_name)):
            self.ui[ui_state_list[i]] = pygame.image.load(ui_file_name[i]).convert_alpha()
        self.arrow = pygame.image.load(arrow_file_name).convert_alpha()
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
        self.ui['panel'].blit(self.panel_font.render('经验值：' + str(self.player.exp) + '/' + str(self.player.lvup_exp), True, (0, 0, 0)), (25, 290))
        self.ui['panel'].blit(self.bag_font.render('人物', True, (0, 0, 0)), (96, 65))

    def draw_sprite(self):
        for i in range(len(ui_state_list)):
            if ui_state_list[i] == 'sprite':
                self.ui['sprite'] = pygame.image.load(ui_file_name[i]).convert_alpha()
        self.ui['sprite'].blit(self.arrow, (320, 280))
        sprite = self.player.own_list[self.sprite_index]
        name = self.sprite_font.render(sprite.pet_name, True, (0, 0, 0))
        self.ui['sprite'].blit(name, ((self.ui['sprite'].get_width()-name.get_width())/2, 65))
        pet_file_name = sprite.pet_file[:-3]+"gif"
        sprite_image = pygame.image.load(pet_file_name).convert_alpha()
        sprite_value = []
        sprite_value.append(str(sprite.level))
        sprite_value.append(str(sprite.exp))
        sprite_value.append(str(sprite.pet_damage))
        sprite_value.append(str(sprite.pet_skill.skill_name))
        if sprite in self.player.battle_list:
            sprite_value.append("已出战")
        else:
            sprite_value.append("未出战")
        self.ui['sprite'].blit(sprite_image, (50, 150))
        for i in range(len(self.description_item)):
            self.ui['sprite'].blit(self.description_font.render(self.description_item[i]+"："+sprite_value[i], True, (0, 0, 0)), (200, 120 + i * 30))

    def draw(self):
        for i in range(len(icon_location)):
            image = self.get_image(icon_location[i])
            image.set_alpha(icon_alpha[i])
            self.screen.blit(image, (20 + 50*i , 20))
        if self.state != 'main':
            self.screen.blit(self.ui[self.state], ui_location[self.state])
        if self.state == 'bag':
            self.update_bag()
            self.draw_item()
        elif self.state == 'panel':
            self.draw_value()
        elif self.state == 'sprite':
            self.draw_sprite()

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
        if self.state == 'sprite':
            sprite = self.player.own_list[self.sprite_index]
            pet_file_name = sprite.pet_file[:-3] + "gif"
            sprite_image = pygame.image.load(pet_file_name).convert_alpha()
            if pygame.Rect(320 +(screen_size[0]-self.ui['sprite'].get_width())/2,215+(screen_size[1]-self.ui['sprite'].get_height())/2,self.arrow.get_width(),self.arrow.get_height()).collidepoint(pos):
                self.sprite_index = (self.sprite_index + 1) % len(self.player.own_list)
            elif pygame.Rect(50+(screen_size[0]-self.ui['sprite'].get_width())/2,75+(screen_size[1]-self.ui['sprite'].get_height())/2,sprite_image.get_width(),sprite_image.get_height()).collidepoint(pos):
                if self.player.own_list[self.sprite_index] not in self.player.battle_list:
                    self.player.battle_list.append(self.player.own_list[self.sprite_index])
                self.draw_sprite()

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
            self.use_item(item_name)
            self.player.controller = 'main'
        if self.state == 'sprite':
            sprite = self.player.own_list[self.sprite_index]
            pet_file_name = sprite.pet_file[:-3] + "gif"
            sprite_image = pygame.image.load(pet_file_name).convert_alpha()
            if pygame.Rect(50+(screen_size[0]-self.ui['sprite'].get_width())/2,75+(screen_size[1]-self.ui['sprite'].get_height())/2,sprite_image.get_width(),sprite_image.get_height()).collidepoint(pos):
                if self.player.own_list[self.sprite_index] in self.player.battle_list:
                    self.player.battle_list.remove(self.player.own_list[self.sprite_index])
                self.draw_sprite()

    def use_item(self, item_name):
        if item_name == "萝卜":
            self.player.hp += const.CARROT_HP
            if self.player.hp > self.player.max_hp:
                self.dialog.info('回复了' + str(const.CARROT_HP - self.player.hp + self.player.max_hp) + '生命')
                self.player.hp = self.player.max_hp
            else:
                self.dialog.info('回复了' + str(const.CARROT_HP) + '生命')
        elif item_name == "洋葱":
            self.player.mp += const.ONION_MP
            if self.player.mp > self.player.max_mp:
                self.dialog.info('回复了' + str(const.ONION_MP - self.player.mp + self.player.max_mp) + '魔法')
                self.player.mp = self.player.max_mp
            else:
                self.dialog.info('回复了' + str(const.ONION_MP) + '魔法')
        elif item_name == "土豆":
            self.player.hp += const.POTATO_HP
            self.player.mp += const.POTATO_MP
            if self.player.hp > self.player.max_hp:
                self.dialog.info('回复了' + str(const.POTATO_HP - self.player.hp + self.player.max_hp) + '生命')
                self.player.hp = self.player.max_hp
            else:
                self.dialog.info('回复了' + str(const.POTATO_HP) + '生命')
            if self.player.mp > self.player.max_mp:
                self.dialog.info('回复了' + str(const.POTATO_MP - self.player.mp + self.player.max_mp) + '魔法')
                self.player.mp = self.player.max_mp
            else:
                self.dialog.info('回复了' + str(const.POTATO_MP) + '魔法')
        elif item_name == "生肉":
            self.player.max_hp += const.MEAT_MAX_HP
            self.dialog.info('生命上限+10')
        elif item_name == "鲜鱼":
            self.player.max_mp += const.FISH_MAX_MP
            self.dialog.info('魔法上限+10')


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
