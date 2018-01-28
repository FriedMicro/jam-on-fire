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
        self.mute = False

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

def play_intro():
    introAudio.set_volume(0.1)
    introAudio.play(-1, 0, 1000)

def render_empty_buttons():
    for i in posX:
        for j in posY:
            emptyButton.move((i,j))
            screen.blit(emptyButton.image, emptyButton.rect)

def render_buttons():
    render_empty_buttons()
    screen.blit(powerButton.image, powerButton.rect)
    screen.blit(speakerButton.image, speakerButton.rect)
    for button in gameButtons:
        screen.blit(button.image, button.rect)

def move_button(button):
    screen.fill((0,0,0), button.rect)
    screen.blit(emptyButton.image, button.rect)
    pygame.display.update(button.rect)

    button.move_by_index()
    screen.blit(button.image, button.rect)
    pygame.display.update(button.rect)

def switch_speaker(current, change):
    screen.blit(change.image, current.rect)
    pygame.display.update(current.rect)

def button_event(button):
    if button == powerButton:
        pygame.mixer.stop()
        pygame.display.quit()
        sys.exit()
    elif button in gameButtons:
        move_button(button)
    elif button == speakerButton:
        if speakerButton.mute:
            switch_speaker(speakerOffButton, speakerButton)
            sample11.stop()
            play_intro()
            speakerButton.mute = False
        else:
            switch_speaker(speakerButton, speakerOffButton)
            introAudio.stop()
            sample11.play()
            speakerButton.mute = True

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
posY = [height*0.3+20, height*0.5+20, height*0.7+20]
emptyButton = Button("res/Empty_Button.png")
powerButton = Button("res/Power_Button.png", (width-32,32))
speakerOffButton = Button("res/SpeakerOff_Button.png", (32,32))
speakerButton = Button("res/Speaker_Button.png", (32,32))
smallSpeakerButton = Button("res/SmallSpeaker_Button.png")
smallSpeakerOffButton = Button("res/SmallSpeakerOff_Button.png")
purpleButton = Button("res/Purple_Button.png", None, 0)
pinkButton = Button("res/Pink_Button.png", None, 1)
cyanButton = Button("res/Cyan_Button.png", None, 2)
gameButtons = [purpleButton, pinkButton, cyanButton]
utilityButtons = [powerButton, speakerButton, speakerOffButton]
speakerButtons = [smallSpeakerOffButton, smallSpeakerButton]
buttons = gameButtons + utilityButtons + speakerButtons
render_buttons()

introAudio = pygame.mixer.Sound(file="res/Intro.wav")
sample11 = pygame.mixer.Sound(file="res/Sample-1-1.ogg")
sample12 = pygame.mixer.Sound(file="res/Sample-1-2.ogg")
sample13 = pygame.mixer.Sound(file="res/Sample-1-3.ogg")
sample14 = pygame.mixer.Sound(file="res/Sample-1-4.ogg")
sample21 = pygame.mixer.Sound(file="res/Sample-2-1.ogg")
sample22 = pygame.mixer.Sound(file="res/Sample-2-2.ogg")
sample23 = pygame.mixer.Sound(file="res/Sample-2-3.ogg")
sample24 = pygame.mixer.Sound(file="res/Sample-2-4.ogg")

pygame.display.flip()

play_intro()
event_loop()
