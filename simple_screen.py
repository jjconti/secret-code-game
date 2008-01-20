import pygame
from pygame.locals import *
from random import choice
import sys

from defaults import *

class SimpleScreen(object):
    
    def __init__(self, screen, img):
        img.set_colorkey(pink)
        screen.fill(choice(raw_colours[2:]))
        screen.blit(img, (0,0))       
        self.done = True
        self.clock = pygame.time.Clock()

    def main_loop(self):
       pygame.display.flip()
       while self.done:

            self.clock.tick(10)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                if event.type == KEYDOWN:
                    self.done = False

