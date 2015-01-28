import pygame
import os
import json
import datetime
from pygame.locals import *

class Settings:
  def __init__(self):
    self.interval = '30s'
    self.duration = '10h'
    self.push_to_drive = False

  def load(self):
    with open('tl_settings.json', 'r') as f:
      old = json.loads(f.read())
      self.interval = old['interval']
      self.duration = old['duration']
      self.push_to_drive = old['push_to_drive']
    print old

  def save(self):
    with open('tl_settings.json', 'w') as f:
      f.write(json.dumps({'interval': self.interval, 'duration': self.duration, 'push_to_drive': self.push_to_drive}))

  def get_next_interval(self, value):
    intervals = ['5s', '10s', '15s', '30s', '1m', '5m', '10m', '15m', '30m', '1h', '2h', '5h']
    if value == -1:
      intervals.reverse()
    for k, i in enumerate(intervals):
      if self.interval == i:
        return intervals[(k + 1) % len(intervals)]

  def get_next_duration(self, value):
    durations = ['1m', '5m', '15m', '30m', '1h', '2h', '3h', '4h', '5h', '7h', '10h', '15h', '1j', '2j', '3j', '5j', '10j', '15j', '30j']
    if value == -1:
      durations.reverse()
    for k, d in enumerate(durations):
      if self.duration == d:
        return durations[(k + 1) % len(durations)]
      
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

# ------ callbacks ------
def change_interval(value):
  global settings, value_interval, values
  settings.interval = settings.get_next_interval(value)
  value_interval = (font.render(settings.interval, 1, (255,255,255)), (20,80))
  value_preview_interval = (font.render(settings.interval, 1, (255,255,255)), (95,10))
  values[0][0] = value_interval
  values[1][0] = value_preview_interval

def change_duration(value):
  global settings, value_duration, values
  settings.duration = settings.get_next_duration(value)
  value_duration = (font.render(settings.duration, 1, (255,255,255)), (100,80))
  value_preview_duration = (font.render(settings.duration, 1, (255,255,255)), (95,30))
  values[0][1] = value_duration
  values[1][1] = value_preview_duration

def change_todrive():
  global settings, buttons, values
  settings.push_to_drive = not settings.push_to_drive
  if settings.push_to_drive:
    buttons[0][4].icon = Icon('check')
  else:
    buttons[0][4].icon = Icon('cross')
  value_preview_drive = (font.render(str(settings.push_to_drive), 1, (255,255,255)), (95,50))
  values[1][2] = value_preview_drive

def save_settings():
  global settings
  settings.save()

def load_settings():
  global settings, value_interval, value_duration, values, buttons
  settings.load()
  #global value_interval
  value_interval = (font.render(settings.interval, 1, (255,255,255)), (20,80))
  value_duration = (font.render(settings.duration, 1, (255,255,255)), (100,80))
  values[0][0] = value_interval
  values[0][1] = value_duration
  if settings.push_to_drive:
    buttons[0][4].icon = Icon('check')
  else:
    buttons[0][4].icon = Icon('cross')

def validate_settings():
  global current_screen
  current_screen = 1

def change_settings():
  global current_screen
  current_screen = 0

def start_recording():
  global current_screen
  current_screen = 2
  #TODO

def stop_recording():
  global current_screen
  current_screen = 1
  #TODO

DEBUG = True
iconPath = 'icons'
settings = Settings()
settings.load()

current_screen = 2 # 0=settings, 1=preview, 2=recording


if not DEBUG:
  os.putenv('SDL_VIDEODRIVER', 'fbcon')
  os.putenv('SDL_FBDEV', '/dev/fb1')
  os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
  os.putenv('SDL_MOUSEDRV', 'TSLIB')


pygame.init()
if not DEBUG:
  pygame.mouse.set_visible(False)
  screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
else:
  screen = pygame.display.set_mode([320,240])

buttons = [[Button((20,40,30,30), color=0, icon=Icon('up_arrow'), cb=change_interval, value=1), #setting buttons
            Button((20,110,30,30), color=0, icon=Icon('down_arrow'), cb=change_interval, value=-1),
            Button((100,40,30,30), color=0, icon=Icon('up_arrow'), cb=change_duration, value=1),
            Button((100,110,30,30), color=0, icon=Icon('down_arrow'), cb=change_duration, value=-1),
            Button((170,75,30,30), color=0, icon=(Icon('check') if settings.push_to_drive else Icon('cross')), cb=change_todrive),
            Button((250,50,30,30), color=0, icon=Icon('save'), cb=save_settings),
            Button((250,100,30,30), color=0, icon=Icon('load'), cb=load_settings),
            Button((180,165,124,70), color=0, icon=Icon('ok'), cb=validate_settings)],
           [Button((10,180,50,50), color=0, icon=Icon('play'), cb=start_recording), #preview buttons
            Button((260,180,50,50), color=0, icon=Icon('settings'), cb=change_settings)],
           [Button((10,180,50,50), color=0, icon=Icon('stop'), cb=stop_recording)]]
            
font = pygame.font.Font(None,25)
label_interval = (font.render("interval", 1, (255,255,255)), (5,10))
label_duration = (font.render("duration", 1, (255,255,255)), (80,10))
label_todrive = (font.render("drive", 1, (255,255,255)), (160,10))
label_settings = (font.render("settings", 1, (255,255,255)), (230,10))
value_interval = (font.render(settings.interval, 1, (255,255,255)), (20,80))
value_duration = (font.render(settings.duration, 1, (255,255,255)), (100,80))

label_preview_interval = (font.render("Interval =", 1, (255,255,255)), (5,10))
label_preview_duration = (font.render("Duration =", 1, (255,255,255)), (5,30))
label_preview_drive = (font.render("to_drive =", 1, (255,255,255)), (5,50))
value_preview_interval = (font.render(settings.interval, 1, (255,255,255)), (95,10))
value_preview_duration = (font.render(settings.duration, 1, (255,255,255)), (95,30))
value_preview_drive = (font.render(str(settings.push_to_drive), 1, (255,255,255)), (95,50))

until = datetime.datetime(2015,4,8,12,50)
label_recording_until = (font.render("until : ", 1, (255,255,255)), (10,10))
label_recording_nbpic = (font.render("picture : ", 1, (255,255,255)), (10,30))
#TODO
value_recording_until = (font.render(until.strftime('%x %X'), 1, (255,255,255)), (60,10))
value_recording_nbpic = (font.render("10/205", 1, (255,255,255)), (80,30))

labels=[[label_interval, label_duration, label_todrive, label_settings],
        [label_preview_interval, label_preview_duration, label_preview_drive],
        [label_recording_until, label_recording_nbpic]]
values=[[value_interval, value_duration],
        [value_preview_interval, value_preview_duration, value_preview_drive],
        [value_recording_until, value_recording_nbpic]]
lines=[[[(72,0), (72,160)], [(155,0), (155,160)], [(210,0), (210,160)]
        ,[(0,160), (320,160)]], [], []]

pygame.draw.line(screen, (0,200,200), (50,0), (50,220))

#import ipdb; ipdb.set_trace()
continuer = 1
#Boucle infinie
while continuer:
  for event in pygame.event.get():
    if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
      continuer = 0
      #pygame.quit()
      break

    if event.type is MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      for b in buttons[current_screen]:
        if b.selected(pos): break
      print pos

  screen.fill(0)
  
  for l in labels[current_screen]:
    screen.blit(l[0], l[1])
  for v in values[current_screen]:
    screen.blit(v[0], v[1])
  for b in buttons[current_screen]:
    b.draw(screen)
  for l in lines[current_screen]:
    pygame.draw.line(screen,(255,255,255), l[0], l[1])

  pygame.display.update()
