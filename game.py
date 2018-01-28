import os, sys, pygame, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.event.pump()


first = random.randint(0,2)
mid = (1 if (first == 0) else 0)
if (mid == 0):
    last = (2 if (first == 1) else 1)
else:
    last = (2 if (mid == 1) else 1)

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
    intro.set_volume(0.05)
    return intro.play(-1, 0, 800)

def render_empty_buttons():
    for i in posX:
        for j in posY:
            emptyButton.move((i,j))
            screen.blit(emptyButton.image, emptyButton.rect)

def render_buttons():
    render_empty_buttons()
    screen.blit(powerButton.image, powerButton.rect)
    screen.blit(speakerButton.image, speakerButton.rect)
    screen.blit(finalSpeakerButton.image, finalSpeakerButton.rect)
    screen.blit(smallSpeakerButton1.image, smallSpeakerButton1.rect)
    screen.blit(smallSpeakerButton2.image, smallSpeakerButton2.rect)
    screen.blit(smallSpeakerButton3.image, smallSpeakerButton3.rect)
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

def play_original():
    channel.pause()
    vocal1.play()
    beat1.play()
    instrument1.play()

def stop_original():
    vocal1.stop()
    beat1.stop()
    instrument1.stop()
    channel.unpause()

def play_combined(pos1, pos2, pos3):
    channel.pause()
    vocals[pos1].play()
    beats[pos2].play()
    instruments[pos3].play()

def stop_combined(pos1, pos2, pos3):
    vocals[pos1].stop()
    beats[pos2].stop()
    instruments[pos3].stop()
    channel.unpause()

def play_piece(index, pos):
    channel.pause()
    if index == 0:
        vocals[pos].play()
    elif index == 2:
        beats[pos].play()
    elif index == 4:
        instruments[pos].play()

def stop_piece(index, pos):
    if index == 0:
        vocals[pos].stop()
    elif index == 2:
        beats[pos].stop()
    elif index == 4:
        instruments[pos].stop()
    channel.unpause()

def get_button_pos(index):
    if index == 0:
        if purpleButton.rect.collidepoint( (posX[0], posY[0]) ):
            return first
        elif purpleButton.rect.collidepoint( (posX[1], posY[0]) ):
            return mid
        elif purpleButton.rect.collidepoint( (posX[2], posY[0]) ):
            return last
    elif index == 2:
        if pinkButton.rect.collidepoint( (posX[0], posY[1]) ):
            return last
        elif pinkButton.rect.collidepoint( (posX[1], posY[1]) ):
            return mid
        elif pinkButton.rect.collidepoint( (posX[2], posY[1]) ):
            return first
    elif index == 4:
        if cyanButton.rect.collidepoint( (posX[0], posY[2]) ):
            return mid
        elif cyanButton.rect.collidepoint( (posX[1], posY[2]) ):
            return first
        elif cyanButton.rect.collidepoint( (posX[2], posY[2]) ):
            return last

def button_event(button):
    if button == powerButton:
        pygame.mixer.stop()
        pygame.display.quit()
        sys.exit()

    elif button == speakerButton:
        if button.mute:
            switch_speaker(speakerOffButton, button)
            stop_original()
            button.mute = False
        else:
            switch_speaker(button, speakerOffButton)
            play_original()
            button.mute = True

    elif button == finalSpeakerButton:
        button1 = get_button_pos(0)
        button2 = get_button_pos(2)
        button3 = get_button_pos(4)
        if button.mute:
            switch_speaker(finalSpeakerOffButton, button)
            stop_combined(button1, button2, button3)
            button.mute = False
        else:
            switch_speaker(button, finalSpeakerOffButton)
            play_combined(button1, button2, button3)
            button.mute = True

    elif button in speakerButtons:
        index = speakerButtons.index(button)
        pos = get_button_pos(index)
        if button.mute:
            switch_speaker(button, button)
            stop_piece(index, pos)
            button.mute = False
        else:
            switch_speaker(button, speakerButtons[index+1])
            play_piece(index, pos)
            button.mute = True

    elif button in gameButtons:
        move_button(button)


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

posX = [width*0.25+25, width*0.5+10, width*0.75-5]
posY = [height*0.3+20, height*0.5+20, height*0.7+20]

cwd = os.path.abspath('res/')
emptyButton = Button(cwd + "/Empty_Button.png")
powerButton = Button(cwd + "/Power_Button.png", (width-32,32))
speakerOffButton = Button(cwd + "/SpeakerOff_Button.png", (32,32))
speakerButton = Button(cwd + "/Speaker_Button.png", (32,32))
smallSpeakerOffButton1 = Button(cwd + "/PurpleOff_Speaker.png")
smallSpeakerOffButton2 = Button(cwd + "/PinkOff_Speaker.png")
smallSpeakerOffButton3 = Button(cwd + "/CyanOff_Speaker.png")
smallSpeakerButton1 = Button(cwd + "/Purple_Speaker.png", (width*0.25-25,posY[0]))
smallSpeakerButton2 = Button(cwd + "/Pink_Speaker.png", (width*0.25-25,posY[1]))
smallSpeakerButton3 = Button(cwd + "/Cyan_Speaker.png", (width*0.25-25,posY[2]))
finalSpeakerButton = Button(cwd + "/Final_Speaker.png", (width*0.75+40,posY[1]))
finalSpeakerOffButton = Button(cwd + "/FinalOff_Speaker.png", (width*0.75+40,posY[1]))
purpleButton = Button(cwd + "/Purple_Button.png", None, 0)
pinkButton = Button(cwd + "/Pink_Button.png", None, 1)
cyanButton = Button(cwd + "/Cyan_Button.png", None, 2)

gameButtons = [purpleButton, pinkButton, cyanButton]
utilityButtons = [powerButton, speakerButton, speakerOffButton, finalSpeakerButton, finalSpeakerOffButton]
speakerButtons = [smallSpeakerButton1, smallSpeakerOffButton1,
                  smallSpeakerButton2, smallSpeakerOffButton2,
                  smallSpeakerButton3, smallSpeakerOffButton3]

buttons = gameButtons + utilityButtons + speakerButtons
render_buttons()

intro = pygame.mixer.Sound(file=cwd + "/Intro.wav")
vocal1 = pygame.mixer.Sound(file=cwd + "/Alex-Vocal-1.wav")
vocal2 = pygame.mixer.Sound(file=cwd + "/Alex-Vocal-2.wav")
vocal3 = pygame.mixer.Sound(file=cwd + "/Alex-Vocal-3.wav")
beat1 = pygame.mixer.Sound(file=cwd + "/Beat-loop-1.ogg")
beat2 = pygame.mixer.Sound(file=cwd + "/Beat-loop-2.wav")
beat3 = pygame.mixer.Sound(file=cwd + "/Beat-loop-3.wav")
instrument1 = pygame.mixer.Sound(file=cwd + "/Instrument-1.ogg")
instrument2 = pygame.mixer.Sound(file=cwd + "/Instrument-2.wav")
instrument3 = pygame.mixer.Sound(file=cwd + "/Instrument-3.wav")

vocals = [vocal1, vocal2, vocal3]
beats = [beat1, beat2, beat3]
instruments = [instrument1, instrument2, instrument3]


pygame.display.flip()

channel = play_intro()
event_loop()
