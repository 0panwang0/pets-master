import pygame

class Person(pygame.sprite.Sprite):
    def __init__(self, file_addr, row, col):
        pygame.sprite.Sprite.__init__(self)
        # vary_states[self.state][0]:速度元组，vary_states[self.state][1(2)]，图片。(注意rest状态只有1张图片)
        self.speed = 8
        _image = pygame.image.load(file_addr).convert_alpha()
        self.vary_states = self.get_image(_image, row, col) # 获得人物各个状态的速度及图片, row, col表示该人物块左上角的行列
        self.state = "rest_down"       # 人物状态
        self.image = self.vary_states[self.state][1]
        self.old_state = self.state     # 人物旧的状态
        self.rect = self.image.get_rect()   #人物的位置
        self.old_rect = pygame.Rect(self.rect)  # 人物旧的位置
        self.frame = 1      # 人物的当前图片
        self.first_frame = 1    #人物的第一个图片
        self.last_frame = 2     #人物的最后一个图片
        self.last_time = 0      #人物图片变换的最近一次时间(时间以pygame.init()为起点)
        self.change_image_time = 150  # 人物图片变换的时间间隔 ms


    def get_image(self, _image, row, col):
        image = {"move_down": [(0, self.speed)],
                 "move_left": [(-self.speed, 0)],
                 "move_right": [(self.speed, 0)],
                 "move_up": [(0, -self.speed)],
                 "rest_down": [(0, 0)],
                 "rest_left": [(0, 0)],
                 "rest_right": [(0, 0)],
                 "rest_up": [(0, 0)],
                 }
        _col = col
        _row = row
        for state, list in image.items():
            if state[:4] == 'move':
                for i in range(2):
                    list.append(_image.subsurface((32 * _col, 32 * _row, 32, 32)))
                    _col += 2
                _col = col
                _row += 1
        _col = col
        _row = row
        for state, list in image.items():
            if state[:4] == 'rest':
                list.append(_image.subsurface((32 * (_col+1), 32 * _row, 32, 32)))
                _row += 1
        return image

    def update(self, current_time):
        if self.state[:4] == 'rest':
            self.image = self.vary_states[self.state][self.first_frame]
        else:
            if current_time > self.last_time + self.change_image_time:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                self.last_time = current_time
            self.image = self.vary_states[self.state][self.frame]
        self.old_state = self.state
        self.old_rect = pygame.Rect(self.rect)
        self.rect.left += self.vary_states[self.state][0][0]
        self.rect.top += self.vary_states[self.state][0][1]


class Hero(Person):
    def __init__(self, file_addr, row, col, screen):
        super().__init__(file_addr, row, col)
        self.moving = [] # 这是一个堆，玩家可能同时按下多个移动键，储存这些状态，当玩家释放移动键时可以选择角色下一个状态
        self.tasks = [1, 2, 3, 4, -1]
        self.money = 100
        self.hp = 100
        self.max_hp = 100
        self.mp = 55
        self.max_mp = 60
        self.attack = 17
        self.defense = 13
        self.own_list = []
        self.battle_list = []
        self.level = 1
        self.exp = 0
        self.battle_nums = 4
        self.exp_list = {
            1: 1000,
            2: 2000,
            3: 4000
        }

    def gain_exp(self, exp):
        self.exp += exp
        while self.exp >= self.exp_list[self.level]:
            self.level = self.level + 1
            self.attack = int(self.attack * 1.2)    # 增加攻击力
            self.max_hp = int(self.max_hp * 1.2)    # 增加血量
            self.max_mp = int(self.max_mp * 1.2)    # 增加蓝量
            self.exp -= self.exp_list[self.level]

    def gain_money(self, money):
        self.money += money

    def get_damage(self):
        return self.attack

    def get_skill_cost(self, index):
        return self.battle_list[index].get_skill().skill_cost

    def get_skill_type(self, index):
        return self.battle_list[index].get_skill().skill_type

    def get_skill_effort(self, index):
        print("---", self.battle_list[index].get_skill().skill_effort)
        return int(self.battle_list[index].get_skill().skill_effort * (0.5 + self.battle_list[index].level * 0.5))

    def get_skill_available(self, index):
        return self.mp >= self.get_skill_cost(index)

    def get_skill_info(self, index):
        return self.get_skill_type(index), self.get_skill_effort(index), self.get_skill_cost(index)

    def use_skill(self, index):
        self.mp -= self.get_skill_cost(index)
        return self.get_skill_type(index), self.get_skill_effort(index), self.get_skill_cost(index)

    def take_damage(self, attack):
        self.hp -= attack
        if self.hp < 0:
            self.hp = 0

    def take_heal(self, heal):
        self.hp += heal
        if self.hp > self.max_hp:
            self.hp = self.max_mp

    def is_alive(self):
        return self.hp > 0

    # 宠物参战
    def put_pet(self, index):
        if len(self.battle_list) < self.battle_nums:
            self.battle_list.append(self.own_list[index])
        else:
            # 提示出战宠物已满
            pass

    # 参战宠物休息
    def rest_pet(self, index):
        del self.battle_list[index]

    def move_back(self):
        """ If called after an update, the sprite can move back to give the
            illusion of the sprite not moving.
        """
        self.state = self.old_state
        self.rect.topleft = self.old_rect.topleft

class NPC(Person):
    def __init__(self, file_addr, row, col, image_num, file_name):
        super().__init__(file_addr, row, col)
        self.row = row // 4
        self.col = col // 3
        self.image_num = image_num
        self.file_name = file_name

