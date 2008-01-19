# -*- coding: latin-1 -*-

# Menu for SecretCode is based on:

# The Menu class was originally develop by Juan José Conti <jjconti@gnu.org>
# for Life Fighter game. It is intentionally placed in a separeted file so you
# can use it if it's fine for you. If not you can improve it :-)
# Please use it under GPL licence like the rest of the game.

# I am sorry. I have no include exausted controls here, so be carefull with the size
# of the images you use.

#import os
import sys
from random import shuffle

import pygame
from pygame.locals import *

from defaults import *

class Menu(object):
    '''A generic NOT VERY menu user interface. Allow both keyboard and mouse selection'''

    def __init__(self, screen, font, options, index=0):

        self.screen = screen
        self.font = font
        self.items = options
        self.hstep = height / len(options)
        self.last_index = len(self.items) - 1
        self.index = index
        self.done = False
        self.clock = pygame.time.Clock()
        
        #self.screen.blit(self.background, (0,0))
        #title_img = font_title.render(title, True, tit_color)
        #topleft = (background.get_rect().width - title_img.get_rect().width) / 2, 30
        #bg = background.copy()
        #bg.blit(title_img, topleft)
        #self.background = bg


        self._draw_items()

        #pygame.mouse.set_pos(self.unselected_rects[index].center)
        
        #pygame.display.flip()

    def main_loop(self):
        '''Returns the asosiated object for the selected item'''

        while not self.done:

            self.clock.tick(10)

            #self.screen.blit(self.background, (0,0))    

            for event in pygame.event.get():
                self.control(event)

            pygame.display.flip()
            
        return self.index

    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN:
            if event.key in (K_SPACE, K_RETURN, K_KP_ENTER):
                self.select()
            elif event.key == K_UP:
                if self.index > 0:
                    self.set_index(self.index - 1)
                else:
                    self.set_index(self.last_index)
            elif event.key == K_DOWN:
                if self.index < self.last_index:
                    self.set_index(self.index + 1)
                else:
                    self.set_index(0)

            self._draw_items()  # Solo redibujar si se apreto una tecla
                
    def set_index(self, index):
        if self.index != index:
            #self.sounds["snd1"].play()
            self.index = index

    def select(self):
        #self.sounds["snd2"].play()
        self.done = True

    def _draw_items(self):
        colours = raw_colours[:]
        unsel_bg = colours.pop(0)
        unsel_fg = colours.pop(0)
        shuffle(colours)
        sel_fg = colours.pop()
        sel_bg = colours.pop()
        y = (self.hstep - fonth) / 2
        rect = Rect(0, 0, self.screen.get_width(), self.hstep) 
        for i,t in enumerate(self.items):
            if i == self.index:
                img = self.font.render(t, True, sel_fg)
                pygame.draw.rect(self.screen, sel_bg, rect)
            else:
                img = self.font.render(t, True, unsel_fg)
                pygame.draw.rect(self.screen, unsel_bg, rect)
            x = (self.screen.get_width() - img.get_width()) / 2
            self.screen.blit(img, (x,y))
            y += self.hstep
            rect.move_ip(0, self.hstep)
