import pygame
from pygame.locals import *

icon_size = (32, 32)
icon_alpha = [180, 180]
icon_location = [(8, 16), (7, 14)]
ui_location = [(50, 50), (100, 50)]
ui_file_name = ["resources/images/bag.png", "resources/images/map.png"]

class Icon((pygame.sprite.Sprite)):
    def __init__(self, filename, screen):
        pygame.sprite.Sprite.__init__(self)
        self.icon = pygame.image.load(filename).convert()
        self.screen = screen
        self.ui = []
        for i in range(len(ui_file_name)):
            self.ui.append(pygame.image.load(ui_file_name[i]).convert_alpha())
        self.state = -1

    def get_image(self, row, col):
        return pygame.transform.scale(self.icon.subsurface(24 * row, 24 * col, 24, 24), icon_size)

    def draw(self):
        for i in range(len(icon_location)):
            image = self.get_image(icon_location[i][0], icon_location[i][1])
            image.set_alpha(icon_alpha[i])
            self.screen.blit(image, (20 + 50*i , 20))
        if self.state != -1:
            self.screen.blit(self.ui[self.state], ui_location[self.state])
        pygame.display.update()

    def check_mouse_down_event(self, pos):
        if self.state == -1:
            for i in range(len(icon_location)):
                if pygame.Rect(20 + 50*i, 20, 32, 32).collidepoint(pos):
                    self.state = i
        elif not pygame.Rect(ui_location[self.state], (50+self.ui[self.state].get_width(), 50+self.ui[self.state].get_height())).collidepoint(pos):
            self.state = -1

    def check_mouse_move_event(self, pos):
        if self.state == -1:
            for i in range(len(icon_location)):
                if pygame.Rect(20 + 50 * i, 20, 32, 32).collidepoint(pos):
                    icon_alpha[i] = 255
                else:
                    icon_alpha[i] = 180
