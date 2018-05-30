import pygame
from pygame.locals import *
from sys import exit

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
        self.player_image = self.image.subsurface(0, 0, 96, 96)
        self.npc_image = self.image.subsurface(0, 0, 96, 96)
        self.dialog_position = (
        (screen_size[0] - self.dialog.get_width()) / 2, (screen_size[1] - self.dialog.get_height()) / 2)
        self.frame_position = (
        (screen_size[0] - self.frame.get_width()) / 2 - 220, (screen_size[1] - self.frame.get_height()) / 2)
        self.tasks = []
        self.starts = []
        self.ends = []


    def draw(self, image, text):
        self.dialog = pygame.image.load(dialog_file_name).convert_alpha()
        self.frame = pygame.image.load(frame_file_name).convert_alpha()
        self.frame = pygame.transform.scale(self.frame, (120, 120))
        for i in range(len(text)):
            surface = self.font.render(text[i].rstrip(), True, (0, 0, 0))
            self.dialog.blit(surface, (30, 30*(i+1)))
        self.frame.blit(image, (12, 12))
        self.screen.blit(self.dialog, self.dialog_position)
        self.screen.blit(self.frame, self.frame_position)
        pygame.display.update()

    def run(self, npc):
        self.npc_image_name = "resources/images/Faces/Actor" + npc.image_num + ".png"
        self.image = pygame.image.load(self.npc_image_name)
        with open("resources/dates/" + npc.file_name + ".txt") as file_object:
            lines = file_object.readlines()
        self.tasks = lines[0].split(' ')
        self.starts = lines[1].split(' ')
        self.ends = lines[2].split(' ')
        self.npc_image = self.image.subsurface(96 * npc.col, 96 * npc.row, 96, 96)
        for i in range(len(self.tasks)):
            if int(self.tasks[i]) in self.player.tasks:
                order = int(self.tasks[i])
                start = int(self.starts[i])
                end = int(self.ends[i])
                break
        i = start
        while i != end + 1:
            content = lines[i].split(' ')
            self.speak(content)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    i += 1
        self.player.power = 'main'
        if order >= 0:
            self.player.tasks.remove(order)


    def speak(self, content):
        image = self.player_image
        if content[0] == 'player':
            image = self.player_image
            self.draw(image, content[1:])
        elif content[0] == 'npc':
            image = self.npc_image
            self.draw(image, content[1:])
        elif content[0] == 'task':
            pass












