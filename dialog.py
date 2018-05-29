import pygame
from pygame.locals import *

dialog_file_name = "resources/images/dialog.png"
player_file_name = "resources/images/Faces/Actor1.png"
frame_file_name = "resources/images/frame.tga"
font_file_name = "resources/fonts/ink.ttf"
screen_size = (800, 600)

class Dialog:
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.font = pygame.font.Font(font_file_name, 20)
        self.dialog = pygame.image.load(dialog_file_name).convert_alpha()
        self.frame = pygame.image.load(frame_file_name).convert_alpha()
        self.frame = pygame.transform.scale(self.frame, (120, 120))
        self.image = pygame.image.load(player_file_name).convert_alpha()
        self.hero = self.image.subsurface(0, 0, 96, 96)
        self.dialog_position = (
        (screen_size[0] - self.dialog.get_width()) / 2, (screen_size[1] - self.dialog.get_height()) / 2)
        self.frame_position = (
        (screen_size[0] - self.frame.get_width()) / 2 - 220, (screen_size[1] - self.frame.get_height()) / 2)


    def write(self, *text):
        for i in range(len(text)):
            surface = self.font.render(text[i], True, (0, 0, 0))
            self.dialog.blit(surface, (30, 30*(i+1)))
        self.frame.blit(self.hero, (12, 12))
        self.screen.blit(self.dialog, self.dialog_position)
        self.screen.blit(self.frame, self.frame_position)
        pygame.display.update()
        self.player.dialog = True





