# Main Menu for game selection

# Add "logout" button for username
# Add link to SQL table for username logging

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
lightGrey = '#f9f9f9'
medLightGrey = '#bbbbbb'
meddarkGrey = '#707070'

dis_width=400
dis_height=300

dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption("Danny's Game Portal")
pygame.display.update()

fps = 60
clock = pygame.time.Clock()

menu_font = pygame.font.SysFont('bahnschrift', 18)
form_font = pygame.font.SysFont('Arial', 15)

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

class formBox():

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = meddarkGrey
        self.textcolour = black
        self.text = text
        self.txt_surface = form_font.render(text, True, self.colour)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                self.text = ''
            else:
                self.active = False
            # Change the current color of the input box.
            self.colour = medLightGrey if self.active else meddarkGrey
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    # HERE NEED TO ADD FUNCTIONALITY TO LINK TO SQL
                    self.text = 'Logged in as ' + self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = form_font.render(self.text, True, self.textcolour)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, ((self.rect.x)+(self.rect.w/2)-(self.txt_surface.get_width()/2), (self.rect.y)+(self.rect.h/2)-(self.txt_surface.get_height()/2)))
        # Blit the rect.
        pygame.draw.rect(screen, self.colour, self.rect, 2)

def launch_snake():
    Snake.main()

def launch_space():
    print('Game not yet ready')

button_width=200
button_height=40
field_width=200
field_height=30

snake_button = Button((dis_width/2)-(button_width/2), 100, button_width, button_height, 'Slippery Snek', launch_snake)
space_button = Button((dis_width/2)-(button_width/2), 150, button_width, button_height, 'Space Invaders', launch_space)

username_field = formBox((dis_width/2)-(field_width/2),250, field_width, field_height, 'Enter Username for Hi-Scores')

form_boxes = [username_field]

def menuLoop():
    menu_close=False

    while not menu_close:
        dis.fill(white)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_close=True
            for box in form_boxes:
                box.handle_event(event)
        
        for box in form_boxes:
            box.update()
           # box.draw(dis)

        dis.fill(white)
        for box in form_boxes:
            box.draw(dis)

        for object in objects:
            object.process()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    quit()

menuLoop()