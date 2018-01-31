import os, sys, pygame, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.event.pump()

#Ensures random orientation of the one original and two modified audio pieces
first = random.randint(0,2)
mid = (1 if (first == 0) else 0)
if (mid == 0):
    last = (2 if (first == 1) else 1)
else:
    last = (2 if (mid == 1) else 1)

#Really should have been called sprites but whatever, my b
class Button:

    #Index is for the three game buttons - got tired of messing with intricate
    #positional junk so just labeling them 0, 1, and 2 seemed better (at the time)
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

    #Same line of thinking as the above - easier to position them using indices
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

#I set the background volume way too low (5% of original) but whatevs
def play_intro():
    intro.set_volume(0.05)
    return intro.play(-1, 0, 800)

#Thought it'd be easier to take one emptyButton object, move it to each of the 9 positions,
#and write it to the screen (underneath the game buttons) than make 9 emptyButtons
#since they don't have any properties other than existing
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

#Because the empty buttons are smaller than the game buttons, the rect objects
#had to be filled in before replacing it with the emptyButton image
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

#For the goal audio, this pauses background music and plays the unaltered pieces at once.
#Lucas was super happy that we could do this instead of having to combine them on the deck lol
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

#Gets user's button positions and plays the corresponding audio pieces (based on random indices chosen
#in lines 10-15)
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

#I hate the way I did this because it doesn't account for the player clicking the speaker,
#listening to the partial piece, and then moving the button (expecting to hear a change).
#Pretty sure it would just keep playing the initial piece until the player clicked the
#speaker again (twice, to mute and play) where it would then register the change...grrr

#Then again...not like we had much time to playtest lol. Also, indices are 0 2 and 4 because
#only the speakerButtons are used for events (the mute ones are just there for the image)
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

#There are DEFINITELY so many better ways of doing this, but time was not on my side lol.
#The mute condition got kind of confusing but its coming from this idea: if speaker.mute
#is False, the speaker's IMAGE is NOT the mute image. There were no winners here, because my
#other option was basing it off of audio (mute = False meaning the audio was not playing).
#However, I included it so I could reference what picture to show, so I did this
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

posX = [width*0.25+25, width*0.5+10, width*0.75-5]
posY = [height*0.3+20, height*0.5+20, height*0.7+20]

cwd = os.path.abspath('res/')
#The bg image and below two lines were literally created in the last 30 minutes
background = pygame.image.load(cwd + "/Background.png")
screen.blit(background, background.get_rect())
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
