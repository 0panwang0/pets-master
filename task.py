import pygame
from pygame.locals import *
from sys import exit
import const

billboard_file_name = "resources/images/task.tga"
arrow_file_name = "resources/images/arrow.png"
font_file_name = "resources/fonts/ink.ttf"

class Task:
    def __init__(self, screen):
        self.type = 0   # 任务类型
        self.screen = screen
        self.large_font = pygame.font.Font(font_file_name, 30)
        self.small_font = pygame.font.Font(font_file_name, 20)
        self.task_index = 0

    def draw(self):
        billboard = pygame.image.load(billboard_file_name)
        title = self.large_font.render("公告牌", True, (0, 0, 0))
        arrow = pygame.image.load(arrow_file_name)
        billboard.blit(title, ((billboard.get_width() - title.get_width()) / 2, 60))
        billboard.blit(arrow, (320, 280))
        billboard.blit(self.small_font.render('第' + str(self.task_index + 1) + '页', True, (0, 0, 0)),(260, 275))
        self.screen.blit(billboard, ((800-billboard.get_width())/2, (600-billboard.get_height())/2,))
        pygame.display.update()
        self.take_control()

    def take_control(self):
        flag = True
        while flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                    flag = False