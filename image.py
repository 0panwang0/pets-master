import time
import pygame


class PetImage:
    initial = time.time()

    def __init__(self, screen, file, number):
        """初始化宠物图像并设置其初始位置"""
        self.screen = screen
        self.delay = 0

        # 加载宠物图像并获取其外接矩形
        self.number = number
        self.index = 0
        self.images = pygame.image.load(file).convert_alpha()
        self.images = [self.images.subsurface(pygame.Rect(i * self.images.get_width() // self.number, 0,
                                                          self.images.get_width() // self.number,
                                                          self.images.get_height())) for i in range(number)]
        self.rect = self.images[0].get_rect()
        self.screen_rect = self.screen.get_rect()

        # 将每个新宠物图像放在屏幕底部以下（隐藏）
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.bottom

    def update(self, pos):
        # 更新宠物图像位置
        self.delay = time.time() - self.initial
        self.index = int(self.delay * 8) % self.number
        self.rect.left = pos[0]
        self.rect.top = pos[1]

    def draw(self):
        # 绘制宠物图像到屏幕指定位置
        self.screen.blit(self.images[self.index], self.rect)


class ButtonImage:
    def __init__(self, screen, width, height, button_file, text, font_size):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮图像的尺寸和其他属性并获取其外接矩形
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.button_file = button_file
        self.button_image = pygame.image.load(self.button_file).convert()
        self.button_image.set_colorkey((255, 255, 255))
        self.button_rect = self.button_image.get_rect()
        self.button_rect.center = self.rect.center

        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self.text_image = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.rect.center

        # 将每个新按钮图像放在屏幕底部以下（隐藏）
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.bottom

    def click(self):
        self.button_image.set_alpha(200)

    def release(self):
        self.button_image.set_alpha(255)

    def update(self, pos):
        # 更新按钮图像位置
        self.rect.left = pos[0]
        self.rect.top = pos[1]
        self.button_rect.center = self.rect.center
        self.text_rect.center = self.rect.center

    def draw(self):
        # 在按钮图像上绘制文字
        self.button_rect.center = self.rect.center
        self.screen.blit(self.button_image, self.button_rect)
        self.text_rect.center = self.rect.center
        self.screen.blit(self.text_image, self.text_rect)


class BarImage:
    def __init__(self, screen, width, height, bar_color, text_color, text, font_size, total, left):
        self.screen = screen
        self.width = width
        self.height = height
        self.screen_rect = self.screen.get_rect()

        self.total = total
        self.left = left
        self.bar_color = bar_color
        self.text_color = text_color

        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self.rect = pygame.Rect((self.screen_rect.left, self.screen_rect.bottom), (self.width, self.height))

        self.text_image = self.font.render(self.text + " " + str(self.left) + "/" + str(self.total),
                                           True, self.text_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.left = self.rect.left
        self.text_image_rect.centery = self.rect.centery
        self.bar_width = self.width - self.text_image_rect.width - 15
        self.bar_height = self.height / 2

    def update(self, left, pos):
        self.left = left if left < self.total else self.total
        self.rect.left = pos[0]
        self.rect.top = pos[1]
        self.text_image = self.font.render(self.text + " " + str(self.left) + "/" + str(self.total),
                                           True, self.text_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.left = self.rect.left
        self.text_image_rect.centery = self.rect.centery
        self.bar_width = self.width - self.text_image_rect.width - 15
        self.text_image_rect.left = self.rect.left
        self.text_image_rect.centery = self.rect.centery

    def draw(self):
        self.screen.blit(self.text_image, self.text_image_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (self.text_image_rect.right + 5,
                                                        self.rect.centery - self.bar_height / 2, self.bar_width,
                                                        self.bar_height))
        pygame.draw.rect(self.screen, self.bar_color, (self.text_image_rect.right + 5,
                                                       self.rect.centery - self.bar_height / 2,
                                                       self.bar_width * self.left / self.total, self.bar_height))
