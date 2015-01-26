import pygame
import os
from pygame.locals import *

iconPath = 'icons'

class Icon:
  def __init__(self, name):
    self.name = name
    try:
      self.bitmap = pygame.image.load(iconPath + '/' + name + '.png')
    except:
      print 'GUCK'
      pass

class Button:
  def __init__(self, rect, color, icon, **kwargs):
    self.rect     = rect # Bounds
    self.color    = color # Background fill color, if any
    self.icon   = icon # Background Icon (atop color fill)
    self.callback = None # Callback function
    self.value    = None # Value passed to callback
    for key, value in kwargs.iteritems():
      if key == 'cb'   : self.callback = value
      elif key == 'value': self.value    = value

  def selected(self, pos):
    x1 = self.rect[0]
    y1 = self.rect[1]
    x2 = x1 + self.rect[2] - 1
    y2 = y1 + self.rect[3] - 1
    if ((pos[0] >= x1) and (pos[0] <= x2) and
        (pos[1] >= y1) and (pos[1] <= y2)):
      print 'selected ' + self.icon.name
      if self.callback:
        if self.value is None:
          self.callback()
        else:
          self.callback(self.value)
      return True
    return False

  def draw(self, screen):
    if self.color:
      screen.fill(self.color, self.rect)
    if self.icon:
      screen.blit(self.icon.bitmap,
        (self.rect[0]+(self.rect[2]-self.icon.bitmap.get_width())/2,
         self.rect[1]+(self.rect[3]-self.icon.bitmap.get_height())/2))

  def setBg(self, name):
    if name is None:
      self.iconBg = None
    else:
      for i in icons:
        if name == i.name:
          self.iconBg = i
          break

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ('SDL_FBDEV', '/dev/fb1')
os.environ('SDL_MOUSEDEV', '/dev/input/touchscreen')
os.environ('SDL_MOUSEDRV', 'TSLIB')

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode([320,240])

continuer = 1

buttons = [Button((0,0,30,30), color=100, icon=Icon('1')),
           Button((290,0,30,30), color=100, icon=Icon('2')),
           Button((0,210,30,30), color=100, icon=Icon('3')),
           Button((290,210,30,30), color=100, icon=Icon('4')),
           Button((135,95,50,50), color=100, icon=Icon('zizi'))]

#Boucle infinie
while continuer:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:     #Si un de ces evenements est de type QUIT
      continuer = 0      #On arrete la boucle
    if event.type is MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      for b in buttons:
        if b.selected(pos): break
      print pos

  screen.fill(0)
  
  for b in buttons:
    b.draw(screen)
#  for i,b in enumerate(buttons[screenMode]):
#    b.draw(screen)
  pygame.display.update()
