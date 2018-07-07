import pygame
from pygame.locals import *
from sys import exit
import const


screen_size = (800, 600)

icon_size = (32, 32)
icon_alpha = [180, 180, 180, 180, 180, 190]
icon_location = [(8, 16), (7, 14), (9, 7), (3, 7), (14, 14), (5, 7)]
ui_location = {'bag':(50, 60), 'map':(100, 70), 'panel':(150, 60), 'sprite':(200, 60),'task':(250, 60), 'setting':(300, 60)}
ui_state_list = ['bag', 'map', 'panel', 'sprite', 'task', 'setting','main']
ui_file_name = ["resources/images/bag.tga", "resources/images/map.png", "resources/images/panel.tga", "resources/images/sprite.tga", "resources/images/task.tga", "resources/images/setting.tga"]
font_file_name = "resources/fonts/ink.ttf"
icon_file_name = "resources/images/IconSet.png"
arrow_file_name = "resources/images/arrow.png"
plus_file_name = "resources/images/plus.tga"
minus_file_name = "resources/images/minus.tga"
download_file_name = "resources/images/download.png"
upload_file_name = "resources/images/upload.png"
exit_file_name = "resources/images/exit.png"
board_file_name = "resources/images/board.tga"
finish_file_name = "resources/images/finish.png"
summit_file_name = "resources/images/summit.png"

item_dict = { '萝卜':(0, 18), '洋葱':(1, 18), '土豆':(2, 18), '生肉':(3, 18), '鲜鱼':(4, 18),}

class Icon:
    def __init__(self, scroll_map, player, dialog, screen):
        self.icon = pygame.image.load(icon_file_name).convert()
        self.scroll_map = scroll_map
        self.player = player
        self.dialog = dialog
        self.screen = screen
        self.bag_font = pygame.font.Font(font_file_name, 40)
        self.setting_font = pygame.font.Font(font_file_name, 35)
        self.sprite_font = pygame.font.Font(font_file_name, 30)
        self.task_font  = pygame.font.Font(font_file_name, 30)
        self.description_font = pygame.font.Font(font_file_name, 20)
        self.panel_font = pygame.font.Font(font_file_name, 25)
        self.gold_font = pygame.font.Font(font_file_name, 20)
        self.plus = pygame.image.load(plus_file_name).convert()
        self.minus = pygame.image.load(minus_file_name).convert()
        self.download = pygame.image.load(download_file_name).convert()
        self.upload = pygame.image.load(upload_file_name).convert()
        self.exit = pygame.image.load(exit_file_name).convert()
        self.summit = pygame.image.load(summit_file_name).convert()
        self.finish = pygame.image.load(finish_file_name).convert_alpha()
        self.exit.set_colorkey((255, 255, 255))
        self.summit.set_alpha(180)
        self.plus.set_alpha(180)
        self.minus.set_alpha(180)
        self.download.set_alpha(180)
        self.upload.set_alpha(180)
        self.exit.set_alpha(180)
        self.ui = {}
        self.sprite_index = 0
        self.task_index = 0
        self.description_item = ["等级", "经验", "威力", "技能", "状态"]
        self.description_setting = ["音量", "读写", "退出"]
        for i in range(len(ui_file_name)):
            self.ui[ui_state_list[i]] = pygame.image.load(ui_file_name[i]).convert_alpha()
        self.arrow = pygame.image.load(arrow_file_name).convert_alpha()
        self.update_bag()
        self.state = 'main'

    def get_image(self, pos):
        return self.icon.subsurface(24 * pos[0], 24 * pos[1], 24, 24)

    def draw(self):
        for i in range(len(icon_location)):
            image = self.get_image(icon_location[i])
            image.set_alpha(icon_alpha[i])
            self.screen.blit(image, (20 + 50*i , 20))
        self.draw_board()
        if self.state != 'main':
            self.screen.blit(self.ui[self.state], ui_location[self.state])
        if self.state == 'bag':
            self.update_bag()
            self.draw_item()
        elif self.state == 'panel':
            self.draw_value()
        elif self.state == 'sprite':
            self.draw_sprite()
        elif self.state == 'setting':
            self.draw_setting()
        elif self.state == 'task':
            self.draw_task()

    def get_item(self, item_name):
        self.player.item_name.append(item_name)

    def draw_item(self):
        self.player.item_position.clear()
        for i in range(len(self.player.item_name)):
            col = i // 6
            row = i % 6
            self.ui[self.state].blit(self.get_image(item_dict[self.player.item_name[i]]), (22 + 40 * row, 134 + 40 * col))
            self.player.item_position.append((72 + 40 * row, 184 + 40 * col))

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

    def draw_board(self):
        board = self.panel_font.render(self.scroll_map.info.sprites()[0].properties['world'], True, (255, 255, 255))
        self.screen.blit(board, (770-board.get_width(), 20))

    def draw_value(self):
        for i in range(len(ui_state_list)):
            if ui_state_list[i] == 'panel':
                self.ui['panel'] = pygame.image.load(ui_file_name[i]).convert_alpha()
        self.ui['panel'].blit(self.panel_font.render('等  级：' + str(self.player.level), True, (0, 0, 0)), (25, 130))
        self.ui['panel'].blit(self.panel_font.render('生命值：' + str(self.player.hp) + '/' + str(self.player.max_hp), True, (0, 0, 0)), (25, 170))
        self.ui['panel'].blit(self.panel_font.render('法力值：' + str(self.player.mp) + '/' + str(self.player.max_mp), True, (0, 0, 0)), (25, 210))
        self.ui['panel'].blit(self.panel_font.render('攻击力：' + str(self.player.attack), True, (0, 0, 0)), (25, 250))
        self.ui['panel'].blit(self.panel_font.render('防御力：' + str(self.player.defense), True, (0, 0, 0)), (25, 290))
        self.ui['panel'].blit(self.panel_font.render('经验值：' + str(self.player.exp) + '/' + str(self.player.lvup_exp), True, (0, 0, 0)), (25, 330))
        self.ui['panel'].blit(self.bag_font.render('人物', True, (0, 0, 0)), (96, 65))

    def draw_task(self):
        for i in range(len(ui_state_list)):
            if ui_state_list[i] == 'task':
                self.ui['task'] = pygame.image.load(ui_file_name[i]).convert_alpha()
        if not self.player.tasks_list:
            text = self.setting_font.render('暂时没有任务!', True, (0, 0, 0))
            self.ui['task'].blit(text, ((self.ui['task'].get_width() - text.get_width())/2, (self.ui['task'].get_height()-text.get_height())/2))
            return
        title = self.setting_font.render('任务', True, (0, 0, 0))
        self.ui['task'].blit(title, ((self.ui['task'].get_width() - title.get_width()) / 2, 65))
        description_item = ["名称", "进度", "说明"]
        for i in range(len(description_item)):
            description_name = self.description_font.render(description_item[i], True, (0, 0, 0))
            self.ui['task'].blit(description_name, (30, 120+40*i))
        description_value = []
        task = self.player.tasks_list[self.task_index]
        self.ui['task'].blit(self.description_font.render(task.task_name, True, (0, 0, 0)), (80, 120))
        self.ui['task'].blit(self.description_font.render(str(task.present_material)+'/'+str(task.max_material), True, (0, 0, 0)), (80, 160))
        for i in range(len(task.info)):
            self.ui['task'].blit(self.description_font.render(task.info[i], True, (0, 0, 0)), (80, 200+30*i))
        self.ui['task'].blit(self.arrow, (320, 280))
        self.ui['task'].blit(self.description_font.render('第' + str(self.task_index + 1) + '页', True, (0, 0, 0)),(260, 275))
        if not task.finish:
            self.ui['task'].blit(self.summit, (320, 65))
        else:
            self.ui['task'].blit(self.finish, (320, 65))

    def draw_setting(self):
        for i in range(len(ui_state_list)):
            if ui_state_list[i] == 'setting':
                self.ui['setting'] = pygame.image.load(ui_file_name[i]).convert_alpha()
        title = self.setting_font.render('设置', True, (0, 0, 0))
        self.ui['setting'].blit(title, ((self.ui['sprite'].get_width()-title.get_width())/2, 65))
        for i in range(len(self.description_setting)):
            self.ui['setting'].blit(self.panel_font.render(self.description_setting[i],True, (0, 0, 0)), (50, 140 + i * 50))
        self.ui['setting'].blit(self.plus, (300, 140))
        vol = self.panel_font.render(str(const.BGM_VOL), True, (0, 0, 0))
        self.ui['setting'].blit(vol, (265-vol.get_width()/2, 140))
        self.ui['setting'].blit(self.minus, (200, 140))
        self.ui['setting'].blit(self.upload, (200, 190))
        self.ui['setting'].blit(self.download, (300, 190))
        self.ui['setting'].blit(self.exit, (200, 240))

    def draw_sprite(self):
        for i in range(len(ui_state_list)):
            if ui_state_list[i] == 'sprite':
                self.ui['sprite'] = pygame.image.load(ui_file_name[i]).convert_alpha()
        if not self.player.own_list:
            name = self.sprite_font.render("暂时没有宠物!", True, (0, 0, 0))
            self.ui['sprite'].blit(name, ((self.ui['sprite'].get_width() - name.get_width()) / 2, (self.ui['sprite'].get_height() - name.get_height()) / 2))
            return
        self.ui['sprite'].blit(self.arrow, (320, 280))
        self.ui['sprite'].blit(self.description_font.render('第'+str(self.sprite_index+1)+'页', True, (0, 0, 0)),(260, 275))
        sprite = self.player.own_list[self.sprite_index]
        name = self.sprite_font.render(sprite.pet_name, True, (0, 0, 0))
        self.ui['sprite'].blit(name, ((self.ui['sprite'].get_width()-name.get_width())/2, 65))
        pet_file_name = sprite.pet_file[:-3]+"gif"
        sprite_image = pygame.image.load(pet_file_name).convert_alpha()
        sprite_value = []
        sprite_value.append(str(sprite.level))
        sprite_value.append(str(sprite.exp)+'/'+str(sprite.lvup_exp))
        sprite_value.append(str(sprite.get_effort()))
        sprite_value.append(str(sprite.pet_skill.skill_name))
        if sprite in self.player.battle_list:
            sprite_value.append("已出战")
        else:
            sprite_value.append("未出战")
        self.ui['sprite'].blit(sprite_image, (50, 150))
        for i in range(len(self.description_item)):
            self.ui['sprite'].blit(self.description_font.render(self.description_item[i]+"："+sprite_value[i], True, (0, 0, 0)), (200, 120 + i * 30))

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
        if self.state == 'sprite' and self.player.own_list:
            sprite = self.player.own_list[self.sprite_index]
            pet_file_name = sprite.pet_file[:-3] + "gif"
            sprite_image = pygame.image.load(pet_file_name).convert_alpha()
            if pygame.Rect(320 +(screen_size[0]-self.ui['sprite'].get_width())/2,215+(screen_size[1]-self.ui['sprite'].get_height())/2,self.arrow.get_width(),self.arrow.get_height()).collidepoint(pos):
                self.sprite_index = (self.sprite_index + 1) % len(self.player.own_list)
            elif pygame.Rect(50+(screen_size[0]-self.ui['sprite'].get_width())/2,75+(screen_size[1]-self.ui['sprite'].get_height())/2,sprite_image.get_width(),sprite_image.get_height()).collidepoint(pos):
                if self.player.own_list[self.sprite_index] not in self.player.battle_list:
                    if len(self.player.battle_list) < 3:
                        self.player.battle_list.append(self.player.own_list[self.sprite_index])
                    else:
                        self.dialog.info("宠物出战数量已达上限","mid")
                self.draw_sprite()
        elif self.state == 'task' and self.player.tasks_list:
            if pygame.Rect(370 +(screen_size[0]-self.ui['task'].get_width())/2,215+(screen_size[1]-self.ui['task'].get_height())/2,self.arrow.get_width(),self.arrow.get_height()).collidepoint(pos):
                self.task_index = (self.task_index + 1) % len(self.player.tasks_list)
            if pygame.Rect(570, 125, self.summit.get_width(), self.summit.get_height()).collidepoint(pos):
                task = self.player.tasks_list[self.task_index]
                if task.present_material >= task.max_material:
                    self.dialog.info("任务完成!","mid")
                    self.player.money += task.money
                    self.player.gain_exp(task.exp)
                    for pet in self.player.battle_list:
                        pet.gain_exp(task.exp)
                    self.dialog.info("获得" + str(task.money) + "金币", "mid")
                    self.dialog.info("获得" + str(task.exp) + "经验", "mid")
                    self.player.tasks_list[self.task_index].finish = True
                else:
                    self.dialog.info("完成进度不足!", "mid")
        elif self.state == 'setting':
            if pygame.Rect(600, 200, self.plus.get_width(), self.plus.get_height()).collidepoint(pos):
                self.scroll_map.bgm_up()
            elif pygame.Rect(500, 200, self.minus.get_width(), self.minus.get_height()).collidepoint(pos):
                self.scroll_map.bgm_down()
            elif pygame.Rect(600, 250, self.download.get_width(), self.download.get_height()).collidepoint(pos):
                const.LOAD = 1
            elif pygame.Rect(500, 250, self.upload.get_width(), self.upload.get_height()).collidepoint(pos):
                const.SAVE = 1
            elif pygame.Rect(500, 300, self.exit.get_width(), self.exit.get_height()).collidepoint(pos):
                pygame.quit()
                exit()

    def check_mouse_right_event(self, pos):
        if self.state == 'bag':
            use = -1
            for i in range(len(self.player.item_position)):
                if pygame.Rect(self.player.item_position[i], (40, 40)).collidepoint(pos):
                    use = i
                    break
            if use < 0:
                return
            self.update_bag()
            item_name = self.player.item_name[use]
            del self.player.item_name[use]
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

    def check_mouse_move_event(self, pos):
        if self.state == 'main':
            for i in range(len(icon_location)):
                if pygame.Rect(20 + 50 * i, 20, 32, 32).collidepoint(pos):
                    icon_alpha[i] = 255
                else:
                    icon_alpha[i] = 180
        elif self.state == 'setting':
            if pygame.Rect(600, 200, self.plus.get_width(), self.plus.get_height()).collidepoint(pos):
                self.plus.set_alpha(255)
            else:
                self.plus.set_alpha(180)
            if pygame.Rect(500, 200, self.minus.get_width(), self.minus.get_height()).collidepoint(pos):
                self.minus.set_alpha(255)
            else:
                self.minus.set_alpha(180)
            if pygame.Rect(500, 250, self.upload.get_width(), self.upload.get_height()).collidepoint(pos):
                self.upload.set_alpha(255)
            else:
                self.upload.set_alpha(180)
            if pygame.Rect(600, 250, self.download.get_width(), self.download.get_height()).collidepoint(pos):
                self.download.set_alpha(255)
            else:
                self.download.set_alpha(180)
            if pygame.Rect(500, 300, self.exit.get_width(), self.exit.get_height()).collidepoint(pos):
                self.exit.set_alpha(255)
            else:
                self.exit.set_alpha(180)
        elif self.state == 'task' and self.player.tasks_list:
            if pygame.Rect(570, 125, self.summit.get_width(), self.summit.get_height()).collidepoint(pos):
                self.summit.set_alpha(255)
            else:
                self.summit.set_alpha(180)