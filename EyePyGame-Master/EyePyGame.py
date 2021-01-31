import pygame
import os
import time
from random import *
import cv2
#from gaze_tracking import GazeTracking

pygame.font.init()
pygame.mixer.init()

#Initialize pygame window
WIDTH, HEIGHT = 1920, 1080
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("EyePyGame")

# Upload background image
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "GameMenu.png")).convert_alpha(), (WIDTH, HEIGHT))

ritchey_sound = pygame.mixer.Sound(os.path.join("assets", "You_know_the_rules.mp3"))
ritchey_sound.set_volume(0.15)
DARKNESS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Darkness.jpg")).convert_alpha(), (WIDTH, HEIGHT))
epic_sound = pygame.mixer.Sound(os.path.join("assets", "Epic_music.mp3"))
epic_sound.set_volume(0.01)

wrong = pygame.mixer.Sound(os.path.join("assets", "WrongAnswer.mp3"))
wrong.set_volume(0.33)

gameMusic = pygame.mixer.Sound(os.path.join("assets", "bensound-slowmotion.mp3"))
gameMusic.set_volume(0.08)

LEFT_ARROW = pygame.transform.scale(pygame.image.load(os.path.join("assets", "LeftArrow-removebg-preview.png")), (200,200))
DOWN_ARROW = pygame.transform.scale(pygame.image.load(os.path.join("assets", "DownArrow-removebg-preview.png")), (200,200))
CENTER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Center-removebg-preview.png")), (200,200))
BLINK = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Blink-removebg-preview.png")), (200,200))
UP_ARROW = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UpArrow-removebg-preview.png")), (200,200))
RIGHT_ARROW = pygame.transform.scale(pygame.image.load(os.path.join("assets", "RightArrow-removebg-preview.png")), (200,200))

LEFT_ARROWB = pygame.transform.scale(pygame.image.load(os.path.join("assets", "LeftBase-removebg-preview.png")), (200,200))
DOWN_ARROWB = pygame.transform.scale(pygame.image.load(os.path.join("assets", "DownBase-removebg-preview.png")), (200,200))
CENTERB = pygame.transform.scale(pygame.image.load(os.path.join("assets", "CenterBase-removebg-preview.png")), (200,200))
BLINKB = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BlinkBase-removebg-preview.png")), (200,200))
UP_ARROWB = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UpBase-removebg-preview.png")), (200,200))
RIGHT_ARROWB = pygame.transform.scale(pygame.image.load(os.path.join("assets", "RightBase-removebg-preview.png")), (200,200))


class movingArrow():
    DIRECTION_MAP = {
        "left": (LEFT_ARROW),
        "down": (DOWN_ARROW),
        "center": (CENTER),
        "blink": (BLINK),
        "up": (UP_ARROW),
        "right": (RIGHT_ARROW)}

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.arrow_img = self.DIRECTION_MAP[direction]
        # Create mask
        self.mask = pygame.mask.from_surface(self.arrow_img)
       
    def draw(self, window):
        window.blit(self.arrow_img, (self.x, self.y))        
        
    def move(self, vel):
        self.y += vel
        
    def get_width(self):
        return self.arrow_img.get_width()

    def get_height(self):
        return self.arrow_img.get_height()

class baseArrow():
    BASE_MAP = {
        "left": (LEFT_ARROWB),
        "down": (DOWN_ARROWB),
        "center": (CENTERB),
        "blink": (BLINKB),
        "up": (UP_ARROWB),
        "right": (RIGHT_ARROWB)}
     
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.arrow_img = self.BASE_MAP[direction]
        # Create a mask to create pixel-perfect collisions
        self.mask = pygame.mask.from_surface(self.arrow_img)
    
    def draw(self, window):
        window.blit(self.arrow_img, (self.x, self.y)) 
        
    def get_width(self):
        return self.arrow_img.get_width()

    def get_height(self):
        return self.arrow_img.get_height()
     
        
def collide(obj1, obj2):
    #global movesScreen
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # Return True or False depending on if two objects are overlapping each other
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

'''
# added by Pranav
def looking_left(gaze):
    if gaze.horizontal_ratio() >= 0.75:
        return True
    return False

def looking_right(gaze):
    if gaze.horizontal_ratio() <= 0.50:
        return True
    return False

def looking_up(gaze):
    if gaze.vertical_ratio() <= 0.65:
        return True
    return False

def looking_down(gaze):
    if gaze.vertical_ratio() >= 0.95:
        return True
    return False

def looking_center(gaze):
    if not (looking_up(gaze) or looking_down(gaze)) and \
        not (looking_right(gaze) or looking_left(gaze)):
        return True
    return False

def blink_detect(gaze):
    blinking_ratio = (gaze.eye_left.blinking + gaze.eye_right.blinking) / 2
    if blinking_ratio > 3.8:
        return True
    return False
'''

def createArrow():
    rando = randint(0,5)
    if(rando == 0):
        return movingArrow(375, 0, "left")
    elif(rando == 1):
        return movingArrow(580, 0, "down")
    elif(rando == 2):
        return movingArrow(765, 0, "center")
    elif(rando == 3):
        return movingArrow(945,0, "blink")
    elif(rando == 4):
        return movingArrow(1120,0, "up")
    elif(rando == 5):
        return movingArrow(1305, 0, "right")

def tutorial():
    run = True
    WINDOW.blit(BACKGROUND, (0,0))
    
    #title
    title_font = pygame.font.SysFont("comicsans", 70)
    title_label = title_font.render("Press the enter key to begin... ", 1, (255, 255, 255))
    WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 540)) 
    while run:
        tutorial_font = pygame.font.SysFont("comicsans", 50)
        tutorial_label = tutorial_font.render(f"Left - Look left, Right - Look right, Up - Look up, Down - Look Down", 1, (255, 255, 255))
        tutorial_label2 = tutorial_font.render(f"O - Look center, X - Blink", 1, (255, 255, 255))
        WINDOW.blit(tutorial_label, (WIDTH / 2 - tutorial_label.get_width() / 2, 650))
        WINDOW.blit(tutorial_label2, (WIDTH / 2 - tutorial_label2.get_width() / 2, 730))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    python.quit()
                if event.key == pygame.K_RETURN:
                    run = False
    main()
    
def main():
    run = True
    # Frame rate
    FPS = 60
    combo = 0
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    title_font = pygame.font.SysFont("comicsans", 70)
    
    movesScreen = [movingArrow(1120, 0, "up")]
    # Arrow velocity
    arrow_vel = 3
    finished = False;
    count = 115
    
    baseUp = baseArrow(1115,820,"up")
    baseDown = baseArrow(570,820,"down")
    baseLeft = baseArrow(375,820,"left")
    baseRight = baseArrow(1305,820,"right")
    baseCenter = baseArrow(765,820,"center")
    baseBlink = baseArrow(945,820,"blink")
    
    pygame.mixer.Sound.play(epic_sound)
    pygame.mixer.Sound.play(ritchey_sound)
    while(pygame.mixer.get_busy()):
        WINDOW.blit(DARKNESS, (0,0))
        loading_label = title_font.render(f"Loading...", 1, (255, 255, 255))
        WINDOW.blit(loading_label, (WIDTH/2 - loading_label.get_width()/2, 540)) 
        pygame.display.update()
    
    startTime = pygame.time.get_ticks()
    pygame.mixer.Sound.play(gameMusic)
    
    def redraw_window():
        # The blit method takes one of the images provided and draws it on the window
        # Draw image background at point 0, 0   
        # draw text
        WINDOW.blit(BACKGROUND, (0,0)) 
        
        combo_label = main_font.render(f"Combo: {combo}", 1, (255, 255, 255))
        WINDOW.blit(combo_label, (WIDTH - combo_label.get_width() - 10, 10))
        
        for arrow in movesScreen:
            arrow.draw(WINDOW)
        
        ##initializing base arrows
        baseUp.draw(WINDOW)
        baseDown.draw(WINDOW)
        baseLeft.draw(WINDOW)
        baseRight.draw(WINDOW)
        baseCenter.draw(WINDOW)
        baseBlink.draw(WINDOW)
        
        pygame.display.update()

    # added by pranav
 #   cap = cv2.VideoCapture(0)
 #   gaze = GazeTracking()

    while run:
        # added by pranav
  #      ret, frame = cap.read()

  #      gaze.refresh(frame)
   #     frame = gaze.annotated_frame()
   #     cv2.imshow("Blink Detector", frame)
        
        clock.tick(FPS)
        redraw_window()
        currentTime = pygame.time.get_ticks() - startTime
        count -= 1
        if(count == 0):
            arrow = createArrow()
            movesScreen.append(arrow)
            count = 125

        if len(movesScreen) == 0:
            combo += 1
            

        for event in pygame.event.get():
            # if event has occured, do something
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_ESCAPE:
                    pygame.quit()
              
        for arrow in movesScreen[:]:
            arrow.move(arrow_vel)        
            '''
            if gaze.pupils_located:

                 #need to combine with the eye detector
                if collide(arrow, baseBlink) and blink_detect(gaze):
                    combo += 1
                    movesScreen.remove(arrow)

                 #need to combine with the eye detector
                if collide(arrow, baseUp) and looking_up(gaze):
                    combo += 1
                    movesScreen.remove(arrow)

                 #need to combine with the eye detector
                if collide(arrow, baseDown) and (looking_down(gaze) or blink_detect(gaze)):
                    combo += 1
                    movesScreen.remove(arrow)

                 #need to combine with the eye detector
                if collide(arrow, baseLeft) and looking_left(gaze):
                    combo += 1
                    movesScreen.remove(arrow)

                 #need to combine with the eye detector
                if collide(arrow, baseRight) and looking_right(gaze):
                    combo += 1
                    movesScreen.remove(arrow)

                 #need to combine with the eye detector
                if collide(arrow, baseCenter) and looking_center(gaze):
                    combo += 1
                    movesScreen.remove(arrow)
            '''
            if arrow.y + arrow.get_height() > HEIGHT:
                # If arrow moves out of the screen, break combo
                combo = 0
                movesScreen.remove(arrow)
                pygame.mixer.Sound.play(wrong)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    main_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        
        #title
        title_label = title_font.render("Press the enter key to begin... ", 1, (255, 255, 255))
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 540))    
        
        #tutorial option
        tutorial_label = main_font.render(f"Press [T] for tutorial", 1, (255, 255, 255))
        WINDOW.blit(tutorial_label, (WIDTH - 350, HEIGHT - 50))
        
        pygame.display.update()
        
        #if mouse click or quit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RETURN:
                    main()
                if event.key == pygame.K_t:
                    tutorial()
    pygame.quit()

main_menu()