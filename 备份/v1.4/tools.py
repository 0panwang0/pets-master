import pygame
from pygame import *
import sys


def check_key_events(keys, player):
    if keys[K_RIGHT]:
        player.state = 'move_right'
    elif keys[K_LEFT]:
        player.state = 'move_left'
    elif keys[K_UP]:
        player.state = 'move_up'
    elif keys[K_DOWN]:
        player.state = 'move_down'
    elif keys[K_RIGHT] != True and keys[K_LEFT] != True and keys[K_UP] != True and keys[K_DOWN] != True:
        if player.state == 'move_right':
            player.state = 'rest_right'
        elif player.state == 'move_up':
            player.state = 'rest_up'
        elif player.state == 'move_down':
            player.state = 'rest_down'
        elif player.state == 'move_left':
            player.state = 'rest_left'


def check_event(player):
    for event in pygame.event.get():
        pass
        if event.type == pygame.QUIT:
            return False
    keys = pygame.key.get_pressed()
    check_key_events(keys, player)
    return True