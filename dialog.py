import pygame


class Dialog:
    def __init__(self, screen):
        self.font = pygame.font.SysFont("arial", 30)
        self.screen = screen

    def draw(self, text):
        surface = self.font.render(text, True, (0, 255, 255))
        self.screen.blit(surface, (300, 300))