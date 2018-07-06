import pygame
from pygame.locals import *
from sys import exit
import const

font_file_name = "resources/fonts/ink.ttf"
start_file_name = "resources/images/start.jpg"

class Start():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(font_file_name, 35)
        self.start_color = (255, 255, 255)
        self.continue_color = (255, 255, 255)
        self.exit_color = (255, 255, 255)

    def draw(self):
        while True:
            image = pygame.image.load(start_file_name)
            start_game = self.font.render("新的游戏", True, self.start_color)
            continue_game = self.font.render("继续游戏", True, self.continue_color)
            exit_game = self.font.render("退出游戏", True, self.exit_color)
            image.blit(start_game, (50, 360))
            image.blit(continue_game, (50, 430))
            image.blit(exit_game, (50, 500))
            self.screen.blit(image, (0, 0))
            pygame.display.update()
            self.take_control()

    def take_control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEMOTION:
                self.move_event(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()
                for index in range(len(buttons)):
                    if buttons[index]:
                        if index == 0:
                            self.mouse_event(pygame.mouse.get_pos())

    def mouse_event(self, pos):
        start_game = self.font.render("新的游戏", True, self.start_color)
        font_width = start_game.get_width()
        font_height = start_game.get_height()
        if pygame.Rect(50, 360, font_width, font_height).collidepoint(pos):
            pass
        elif pygame.Rect(50, 430, font_width, font_height).collidepoint(pos):
            pass
        elif pygame.Rect(50, 500, font_width, font_height).collidepoint(pos):
            pygame.quit()
            exit()

    def move_event(self, pos):
        start_game = self.font.render("新的游戏", True, self.start_color)
        font_width = start_game.get_width()
        font_height = start_game.get_height()
        if pygame.Rect(50, 360, font_width, font_height).collidepoint(pos):
            self.start_color = (0, 255, 255)
        else:
            self.start_color = (255, 255, 255)
        if pygame.Rect(50, 430, font_width, font_height).collidepoint(pos):
            self.continue_color = (0, 255, 255)
        else:
            self.continue_color = (255, 255, 255)
        if pygame.Rect(50, 500, font_width, font_height).collidepoint(pos):
            self.exit_color = (0, 255, 255)
        else:
            self.exit_color = (255, 255, 255)