# Main Menu for game selection

# Add "logout" button for username
# Add link to SQL table for username logging
# Add difficulty button
# Add retro helicopter option


import pygame
import Snake
import psycopg2

conn = psycopg2.connect(database="users",
                        host="localhost",
                        user="postgres",
                        password="passW0rd",
                        port="5432")

cursor = conn.cursor()

# cursor.execute("SELECT * FROM users")
# print("User list is" + str(cursor.fetchall()))

pygame.init()

# Colours
white = '#ffffff'
yellow = '#ffff00'
black = '#000000'
red = '#ff0000'
green = '#00ff00'
blue = '#0000ff'
darkGreen = '#007010'
lightGrey = '#f9f9f9'
medLightGrey = '#bbbbbb'
medDarkGrey = '#707070'
darkGrey = '#333333'

dis_width=600
dis_height=450

dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption("Retro-Play")
pygame.display.update()

fps = 60
clock = pygame.time.Clock()

menu_font = pygame.font.SysFont('Consolas', 18)
form_font = pygame.font.SysFont('Arial', 15)

back_img = pygame.image.load("back_main.png")
back_img = pygame.transform.scale(back_img, (dis_width, dis_height))

objects = []

class SQL_select(): #
    def __init__(self, table='', column='', refcolumn='',refvalue=''):
        self.table=str(table)
        self.columns=str(column)
        self.refcolumn=str(refcolumn)
        self.refvalue=str(refvalue)

        self.query = f"SELECT {self.columns} FROM {self.table} WHERE {self.refcolumn}='{self.refvalue}'"
           
    def execute(self):
        # Build Query and commit into PostgreSQL db
        cursor.execute(self.query)
        result = cursor.fetchall()
        return result

class SQL_insert(): #
    def __init__(self, table='', columns=[], values=''):
        self.table=str(table)
        self.columns=str(columns).replace("[","(").replace("]",")").replace("'","")
        self.values=str(values)

        # Build Query and commit into PostgreSQL db
        query = f"INSERT INTO {self.table}{self.columns} VALUES{self.values}"
        cursor.execute(query)
        conn.commit()

class SQL_update(): # Use this class for updating a user value - e.g. high scores.
    def __init__(self, table='', column='', value='', refcolumn='', refvalue=''):
        self.table=str(table)
        self.column=str(column)
        self.value=str(value)
        self.refcolumn=str(refcolumn)
        self.refvalue=str(refvalue)

        # Build Query and commit into PostgreSQL db
        query = f"UPDATE {self.table} SET {self.column}='{self.value}' WHERE ({self.refcolumn}='{self.refvalue}')"
        cursor.execute(query)
        conn.commit()

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
            'normal': black,
            'hover': darkGrey,
            'pressed': medDarkGrey,
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = menu_font.render(buttonText, True, medLightGrey)

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
        self.colour = lightGrey
        self.textcolour = white
        self.text = text    
        self.txt_surface = form_font.render(text, True, self.colour)
        self.active = False
        self.submit_value = False
        #self.output = ''

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
            self.colour = medDarkGrey if self.active else medLightGrey
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.output = self.text

                    # Check if username exists yet, add if not, and assign value to username value
                    user_check=SQL_select('users','username','username',f"{self.output}").execute()
                    if len(user_check) > 1:
                        print(f"Database error - contact system administrator")
                    elif len(user_check) == 0:
                        SQL_insert('users',f"[username]",f"('{self.output}')")
                        print(f"New user added")
                        self.text = 'Logged in as ' + self.output
                        self.txt_surface = form_font.render(self.text, True, self.textcolour)
                        return self.output
                    elif len(user_check) == 1:
                        print(f"Existing user found")
                        self.text = 'Logged in as ' + self.output
                        self.txt_surface = form_font.render(self.text, True, self.textcolour)
                        return self.output                        

                    self.textcolour = medLightGrey
                    self.colour = medLightGrey
                    self.active = False

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

button_width=180
button_height=30
field_width=200
field_height=30

difficulty=1

snake_button = Button((dis_width/2)-(button_width/2), 250, button_width, button_height, 'Slippery Snek', lambda: Snake.main(username,difficulty))
space_button = Button((dis_width/2)-(button_width/2), 300, button_width, button_height, 'Space Invaders', lambda: print(f"Game not yet ready. Have patience please - I'm learning!"))
heli_button = Button((dis_width/2)-(button_width/2), 350, button_width, button_height, 'Retro Helicopter', lambda: print(f"Game not yet ready. Have patience please - I'm learning!"))

username_field = formBox((dis_width/2)-(field_width/2),140, field_width, field_height, 'Enter Username for Hi-Scores')
username=""

form_boxes = [username_field]

def menuLoop():
    global username
    menu_close=False

    while not menu_close:
        dis.blit(back_img,(0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_close=True
            for box in form_boxes:
                output=box.handle_event(event)
                if output != None:
                    username = output
                    print(username)
        
        for box in form_boxes:
            box.update()
            box.draw(dis)

        for object in objects:
            object.process()

        pygame.display.flip()   
        clock.tick(fps)

    pygame.quit()
    quit()

menuLoop()