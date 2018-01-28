import sys, pygame
from pygame.locals import *
import os

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.event.pump()

class Button:

    def __init__(self, imageName, pos = (0,0), index = None):
        self.image = pygame.image.load(imageName)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.index = index
        if index is not None:
            self.x = posX[index]
            self.y = posY[index]
            self.pos = (self.x, self.y)
        self.rect.center = self.pos

    def move(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.rect.center = self.pos

    def move_by_index(self):
        if self.index == 0:
            self.move((posX[1], self.y))
            self.index = 1
        elif self.index == 1:
            self.move((posX[2], self.y))
            self.index = 2
        else:
            self.move((posX[0], self.y))
            self.index = 0

def start_audio():
    introAudio.set_volume(0.3)
    introAudio.play(-1, 0, 2000)

def render_empty_buttons():
    for i in posX:
        for j in posY:
            emptyButton.move((i,j))
            screen.blit(emptyButton.image, emptyButton.rect)

def render_buttons():
    render_empty_buttons()
    for button in buttons:
        screen.blit(button.image, button.rect)

def move_button(button):
    screen.fill((0,0,0), button.rect)
    screen.blit(emptyButton.image, button.rect)
    pygame.display.update(button.rect)

    button.move_by_index()
    screen.blit(button.image, button.rect)
    pygame.display.update(button.rect)

def button_event(button):
    if button == powerButton:
        pygame.mixer.stop()
        pygame.display.quit()
        sys.exit()
    elif button in gameButtons:
        move_button(button)
    elif button == speakerButton:
        introAudio.stop()
        sample.play(0, 0, 0)
        

def mouse_click(pos):
    for button in buttons:
        if button.rect.collidepoint(pos):
            button_event(button)

def event_loop():
    while True:
        for event in pygame.event.get():
            if event.type == 5:
                mouse_click(pygame.mouse.get_pos())

os.environ['SDL_VIDEO_CENTERED'] = '1'
size = width, height = 320, 240
screen = pygame.display.set_mode(size, pygame.NOFRAME)
screen.fill( (0,0,0) ) #black

posX = [width*0.25, width*0.5, width*0.75]
posY = [height*0.3, height*0.5, height*0.7]
emptyButton = Button("res/Empty_Button.png")
powerButton = Button("res/Power_Button.png", (width-32,32))
speakerButton = Button("res/Speaker_Button.png", (32, 32))
purpleButton = Button("res/Purple_Button.png", None, 0)
pinkButton = Button("res/Pink_Button.png", None, 1)
cyanButton = Button("res/Cyan_Button.png", None, 2)
gameButtons = [purpleButton, pinkButton, cyanButton]
buttons = gameButtons + [powerButton, speakerButton]
render_buttons()

introAudio = pygame.mixer.Sound(file="res/Intro.wav")
sample = pygame.mixer.Sound(file="res/Sample.ogg")

pygame.display.flip()

start_audio()
event_loop()
