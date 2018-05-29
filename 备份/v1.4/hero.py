import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, file_addr, row, col):
        pygame.sprite.Sprite.__init__(self)
        # vary_states[self.state][0]:速度元组，vary_states[self.state][1(2)]，图片。(注意rest状态只有1张图片)
        self.speed = 2
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
        # image["move_down"].append(_image.subsurface((32 * 0, 32 * row, 32, 32)))
        # image["move_down"].append(_image.subsurface((32 * 2, 32 * row, 32, 32)))
        # image["rest_down"].append(_image.subsurface((32 * 1, 32 * 0, 32, 32)))
        # image["move_left"].append(_image.subsurface((32 * 0, 32 * 1, 32, 32)))
        # image["move_left"].append(_image.subsurface((32 * 2, 32 * 1, 32, 32)))
        # image["rest_left"].append(_image.subsurface((32 * 1, 32 * 1, 32, 32)))
        # image["move_right"].append(_image.subsurface((32 * 0, 32 * 2, 32, 32)))
        # image["move_right"].append(_image.subsurface((32 * 2, 32 * 2, 32, 32)))
        # image["rest_right"].append(_image.subsurface((32 * 1, 32 * 2, 32, 32)))
        # image["move_up"].append(_image.subsurface((32 * 0, 32 * 3, 32, 32)))
        # image["move_up"].append(_image.subsurface((32 * 2, 32 * 3, 32, 32)))
        # image["rest_up"].append(_image.subsurface((32 * 1, 32 * 3, 32, 32)))
        return image

    def update(self, _blockers, current_time):
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
        if pygame.sprite.spritecollideany(self, _blockers):
            self.move_back()

    def move_back(self):
        """ If called after an update, the sprite can move back to give the
            illusion of the sprite not moving.
        """
        self.state = self.old_state
        self.rect.topleft = self.old_rect.topleft