# Main Menu for game selection

import pygame
import Snake

pygame.init()

# Colours
# white = (255, 255, 255)
# yellow = (255, 255, 102)
# black = (0, 0, 0)
# red = (255, 0, 0)
# green = (0, 255, 0)
# blue = (0, 0, 255)
# darkGreen = (5, 149, 37)
white = '#ffffff'
yellow = '#ffff00'
black = '#000000'
red = '#ff0000'
green = '#00ff00'
blue = '#0000ff'
darkGreen = '#007010'

dis_width=400
dis_height=300

dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption("Danny's Game Portal")
pygame.display.update()

fps = 60
clock = pygame.time.Clock()

menu_font = pygame.font.SysFont('bahnschrift', 18)

objects = []

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = menu_font.render(buttonText, True, (20, 20, 20))

        objects.append(self)
    
    def process(self):

        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        dis.blit(self.buttonSurface, self.buttonRect)

def launch_snake():
    Snake.main()

def launch_space():
    print('Game not yet ready')

snake_button = Button(30, 30, 300, 50, 'Slippery Snek', launch_snake)
space_button = Button(30, 100, 300, 50, 'Space Invaders', launch_space)


def menuLoop():
    menu_close=False

    while not menu_close:
        dis.fill(white)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_close=True
        
        for object in objects:
            object.process()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    quit()

menuLoop()