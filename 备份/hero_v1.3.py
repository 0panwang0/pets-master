import pygame
class Hero(pygame.sprite.Sprite):
    def __init__(self, _image):
        pygame.sprite.Sprite.__init__(self)
        self.vary_image = self.get_image(_image)    #获得人物各个状态的图片
        self.state = "rest_down"       # 人物状态
        self.image = self.vary_image[self.state][0]
        self.velocity = [0, 0]  # 人物速度
        self.old_state = self.state     # 人物旧的状态
        self.rect = self.image.get_rect()   #人物的位置
        self.old_rect = pygame.Rect(self.rect)  # 人物旧的位置
        self.frame = 0      # 人物的当前图片
        self.first_frame = 0    #人物的第一个图片
        self.last_frame = 1     #人物的最后一个图片
        self.last_time = 0      #人物图片变换的最近依次时间(时间以pygame.init()为起点)

    def get_image(self, _image):
        image = {"move_left": list(),
                 "move_up": list(),
                 "move_down": list(),
                 "move_right": list(),
                 "rest_left": list(),
                 "rest_right":list(),
                 "rest_up":list(),
                 "rest_down":list()
                 }
        image["move_down"].append(_image.subsurface((32 * 0, 32 * 0, 32, 32)))
        image["move_down"].append(_image.subsurface((32 * 2, 32 * 0, 32, 32)))
        image["rest_down"].append(_image.subsurface((32 * 1, 32 * 0, 32, 32)))
        image["move_left"].append(_image.subsurface((32 * 0, 32 * 1, 32, 32)))
        image["move_left"].append(_image.subsurface((32 * 2, 32 * 1, 32, 32)))
        image["rest_left"].append(_image.subsurface((32 * 1, 32 * 1, 32, 32)))
        image["move_right"].append(_image.subsurface((32 * 0, 32 * 2, 32, 32)))
        image["move_right"].append(_image.subsurface((32 * 2, 32 * 2, 32, 32)))
        image["rest_right"].append(_image.subsurface((32 * 1, 32 * 2, 32, 32)))
        image["move_up"].append(_image.subsurface((32 * 0, 32 * 3, 32, 32)))
        image["move_up"].append(_image.subsurface((32 * 2, 32 * 3, 32, 32)))
        image["rest_up"].append(_image.subsurface((32 * 1, 32 * 3, 32, 32)))
        return image

    def update(self, distance, _blockers, current_time):
        if self.state[:4] == 'rest':
            self.image = self.vary_image[self.state][0]
        else:
            if current_time > self.last_time + 150:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                self.last_time = current_time
            self.image = self.vary_image[self.state][self.frame]
        self.old_state = self.state
        self.old_rect = pygame.Rect(self.rect)
        self.rect.left += self.velocity[0] * distance
        self.rect.top += self.velocity[1] * distance
        if pygame.sprite.spritecollideany(self, _blockers):
            self.move_back()
        self.velocity=[0, 0]

    def move_back(self):
        """ If called after an update, the sprite can move back to give the
            illusion of the sprite not moving.
        """
        self.state = self.old_state
        self.rect.topleft = self.old_rect.topleft