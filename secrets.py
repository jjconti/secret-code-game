import pygame
from pygame.locals import *
from random import shuffle

from defaults import *
from utils import Circular

import sys

class SC(object):
    '''Secret Code Engine'''

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.redraw_group = pygame.sprite.RenderUpdates()
        self._rows()
        self.row_index = 0
        [self.redraw_group.add(r.elements) for r in self.rows]
        self.rows[self.row_index].elements.current().select()
        self.rows[self.row_index].elements.current()._image()
        self.cond = True
        self.finalkey = False

        self.screen.fill(bg_color)

    def _rows(self):
        self.rows = []
        top, left = step, step
        for i in xrange(10):
            self.rows += [Row(top,left, False)]
            top += step
        top += step
        self.ans = Row(top,left, True)
        self.ans.hide()
        self.rows += [self.ans]

    def main_loop(self):

        while self.cond or not self.finalkey:

            self.clock.tick()

            for event in pygame.event.get():
                    self.control(event)

            self.redraw_group.draw(self.screen)

            pygame.display.flip()

    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)

        if event.type == KEYDOWN:

            if not self.cond:
                self.finalkey = True
                return

            if event.key == K_UP:
                self.up()
            elif event.key in (K_DOWN, K_SPACE):
                self.down()
            elif event.key == K_RIGHT:
                self.right()
            elif event.key == K_LEFT:
                self.left()
            elif event.key == K_RETURN:
                self.enter()


    def up(self):
        self.rows[self.row_index].elements.current().prev()
            
    def down(self):
        self.rows[self.row_index].elements.current().next()
        
    def right(self):
        self.rows[self.row_index].elements.current().unselect()
        self.rows[self.row_index].elements.current()._image()
        self.rows[self.row_index].elements.next()
        self.rows[self.row_index].elements.current().select()
        self.rows[self.row_index].elements.current()._image()

    def left(self):
        self.rows[self.row_index].elements.current().unselect()
        self.rows[self.row_index].elements.current()._image()            
        self.rows[self.row_index].elements.prev()
        self.rows[self.row_index].elements.current().select()
        self.rows[self.row_index].elements.current()._image()

    def enter(self):
        rcp, rc = self.rights()
        ib = InfoBox(step + step * self.row_index, step * 6, rcp, rc)
        self.redraw_group.add(ib)
        self.did_win()
        self.rows[self.row_index].elements.current().unselect()
        self.rows[self.row_index].elements.current()._image()
        self.row_index +=1
        if self.row_index != 10:
            self.rows[self.row_index].elements.current().select()
            self.rows[self.row_index].elements.current()._image()

    def rights(self): #UGLY
        '''How many colours are right?'''
        row = self.rows[self.row_index]
        ans = self.rows[-1]
        rowels = row.elements[:]
        ansels = ans.elements[:]
        indexes = []
        colour_row = [0 for x in raw_colours]
        colour_ans = [0 for x in raw_colours]
        rcp = 0
        rc = 0
        for i,(r,a) in enumerate(zip(row.elements, ans.elements)):
            if r == a:
                rcp += 1
                indexes += [i]
        indexes.reverse()        
        for i in indexes:
            rowels.pop(i)
            ansels.pop(i)
        rowels = [c.colour for c in rowels]
        ansels = [c.colour for c in ansels]
        for i,c in enumerate(raw_colours):
            colour_row[i] = rowels.count(c)
            colour_ans[i] = ansels.count(c)
        rc = sum([min(x,y) for x,y in zip(colour_row, colour_ans)])
        return (rcp, rc)
            
    def did_win(self):
        if self.rows[self.row_index] == self.rows[-1]:
            print "Gano!", self.row_index
            self.cond = False
            self.rows[-1].unhide()
            return
        if self.row_index == 9:     # 9 is the 10th position
            print "Perdio!"
            self.cond = False
            self.rows[-1].unhide()
            return        
                
 
class Colour(pygame.sprite.Sprite):
    '''A colour '''
    
    def __init__(self, top, left, random):        

        pygame.sprite.Sprite.__init__(self)

        self.selected = False
        self.colour_list = Circular(raw_colours)
        if random:
            shuffle(self.colour_list)
        self._colour()
        self._image()
        self.rect = self.image.get_rect()      
        self.rect.x = left
        self.rect.y = top


    def _colour(self):
       self.colour = self.colour_list.current()

    def _image(self):
        self.image = pygame.Surface((step, step))
        if self.selected:
            c = selected_color
        else:
            c = bg_color
        #self.image.set_colorkey(c)
        self.image.fill(c)
        pos = (step/2 + 1,step/2 + 1)
        radius = int(0.4 * step)
        pygame.draw.circle(self.image, self.colour, pos, radius, 0)

    def hide(self):
        self.image = pygame.Surface((step, step))
        self.image.fill(hide_color)

    def unhide(self):
        self._image()
    
    def next(self, n=1):
        self.colour_list.next(n)
        self._colour()
        self._image()

    def prev(self, n=1):
        self.colour_list.prev(n)
        self._colour()
        self._image()

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def __eq__(self, other):
        return self.colour == other.colour

    def __str__(self):
        return "Colour: %s" % (self.colour,)

class Row(object):
    '''A colour row'''

    def __init__(self, top, left, random=True):
        self.elements = Circular([None, None, None, None])
        for i in xrange(4):       
            self.elements[i] = Colour(top, left + step*i, random)
       
    def hide(self):
       [e.hide() for e in self.elements]

    def unhide(self):
       [e.unhide() for e in self.elements]

    def __eq__(self, other):
        for i in xrange(4):
            if not (self.elements[i] == other.elements[i]):
                return False
        return True

    def __str__(self):
        return "Row: [" + ",".join([str(x) for x in self.elements]) + "]"

class InfoBox(pygame.sprite.Sprite):
    '''Information about your try: 
    black: right colour and position
    withe: right colour'''
 
    def __init__(self, top, left, rcp, rc):        

        pygame.sprite.Sprite.__init__(self)

        self.rcp = rcp
        self.rc = rc
        self._image()
        self.rect = self.image.get_rect()      
        self.rect.x = left
        self.rect.y = top

    def _image(self):
        self.image = pygame.Surface((step, step))
        self.image.set_colorkey(bg_color)
        self.image.fill(bg_color)
        rights = ['rcp'] * self.rcp + ['rc'] * self.rc
        rights
        ss = step / 2
        toplefts = [(0,0), (0, 0 + ss), (0 + ss, 0), (0 + ss, 0 + ss)]
        for pos,r in zip(toplefts,rights):
            if r == 'rcp': colour = black
            else: colour = white
            rect = Rect(pos[0], pos[1], ss, ss)
            pygame.draw.rect(self.image, colour, rect)

