# -*- coding: UTF-8 -*-
#Import Modules

import sys

import pygame
from pygame.locals import *

from utils import load_image
from secrets import *
from defaults import *
from menu import Menu
from simple_screen import SimpleScreen

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

WINDOW_TITLE = "Secret Code"

def main():
    #Initialize
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(WINDOW_TITLE)

    screen.fill(bg_color)
    clock = pygame.time.Clock()
    font = pygame.font.Font(font_path, fonth)

    img_reglas = load_image(reglas_path)
    img_creditos = load_image(creditos_path)

    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play()

    while True:

        menu = Menu(screen, font, ['Jugar', 'Reglas', 'Creditos', 'Salir'])
        op = menu.main_loop()
        
        if op == 0:    
            game = SC(screen, clock)
            game.main_loop()
        elif op == 1:
            SimpleScreen(screen, img_reglas).main_loop()
        elif op == 2:
            SimpleScreen(screen, img_creditos).main_loop()
        elif op == 3:
            sys.exit(0)


if __name__ == '__main__':
    main()
