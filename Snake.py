# A simple snake game in Python

##### TASKS #####
# Add difficulty level - controlled by main menu choice
# Add music
# Add snake colour swatches (four) - controlled by main menu choice
# Add map options
#   Add maps with obstacles

def main(username,difficulty):
    import pygame
    import time
    import random
    import psycopg2

    conn = psycopg2.connect(database="users",
                        host="localhost",
                        user="postgres",
                        password="passW0rd",
                        port="5432")

    cursor = conn.cursor()
    cursor.execute(f"SELECT hiscore_snake FROM users WHERE username='{username}'")
    player_hiscore=cursor.fetchone()[0]
    print(player_hiscore)

    pygame.init()

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
    pygame.display.set_caption("Slippery Snek")
    pygame.display.update()

    clock = pygame.time.Clock()

    snake_block_size=10
    shortener_length=3

    colour_array=[yellow,black,red,green,blue,darkGreen]
    food_message=["Ohh yeahh","So good!","Mmmmm","Give me more!","Gotta keep munchin'","Scrumptious","Nom nom nom","Quite delectable actually","A little savoury...","*chef's kiss*"]

    main_font = pygame.font.SysFont("bahnschrift",15)
    score_font = pygame.font.SysFont("roboto",20)

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

    def player_score(score,player_hiscore):
        value=score_font.render("Current score: " + str(score), True, black)
        hiscore=score_font.render(str(username) + "'s hi-score: " + str(player_hiscore), True, black)
        hiscore_pos=score_font.size(str(username) + "'s hi-score: " + str(player_hiscore))
        dis.blit(value,[5,5])
        dis.blit(hiscore,[(dis_width-hiscore_pos[0]-5),5])

    def our_snake(snake_block_size, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis,darkGreen,[x[0],x[1],snake_block_size,snake_block_size])

    def message(msg,colour): # Consider amending this function to take an input for the position of the message. Currently it is fixed in the middle
        mesg_pos=main_font.size(msg)
        mesg = main_font.render(msg, True, colour)
        dis.blit(mesg, [(dis_width/2)-(mesg_pos[0]/2), (dis_height/2)-(mesg_pos[1]/2)])

    def popup_msg(txt_choice,colour_choice,food_x0,food_y0):
        txt=txt_choice
        colour=colour_choice
        mesg_pos=main_font.size(txt)
        mesg = main_font.render(txt, True, colour)
        dis.blit(mesg, [(food_x0)-(mesg_pos[0]/2)+snake_block_size/2, (food_y0)-(mesg_pos[1]/2)+snake_block_size/2])

    def gameLoop(player_hiscore,difficulty): #Function to run the game
        game_over=False
        game_close=False
        current_score = -1

        x1=dis_width/2
        y1=dis_height/2
        x1_change=0
        y1_change=0

        food_x=round(random.randrange(0,dis_width-snake_block_size)/10)*10
        food_y=round(random.randrange(0,dis_height-snake_block_size)/10)*10
        food_x0=food_x
        food_y0=food_y

        snake_List = []
        snake_Length = 1

        snake_speed=15*difficulty
        snake_speed_step=0.5*difficulty

        snake_Length_past=0

        shortener_x=-snake_block_size
        shortener_y=-snake_block_size

        t_food=time.time_ns()

        while not game_over: #Continue running until game over triggered
            while game_close == True:
                dis.fill(black)
                message("Jeez, you suck! Press Esc to Quit or Space to Play Again", red)
                message(f"Your score: {current_score}", green)
                pygame.display.update()
                if current_score > player_hiscore:
                    print('New Hi Score!')
                    player_hiscore = current_score
                    SQL_update('users','hiscore_snake',f"{player_hiscore}",'username',username)
                # Here, should run a PSQL query to commit the new hi score to the database, if it exceeds the existing hi score

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_over=True
                            pygame.quit()
                            quit()
                        if event.key == pygame.K_SPACE:
                            snake_speed=20
                            gameLoop(player_hiscore,difficulty)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over=True
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and x1_change != snake_block_size:
                        x1_change = -snake_block_size
                        y1_change = 0
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and x1_change != -snake_block_size:
                        x1_change = snake_block_size
                        y1_change = 0
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and y1_change != snake_block_size:
                        x1_change = 0
                        y1_change = -snake_block_size
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and y1_change != -snake_block_size:
                        x1_change = 0
                        y1_change = snake_block_size

            if (x1 >= dis_width) or (x1 < 0) or (y1 >= dis_height) or (y1 < 0):
                game_close=True

            x1 += x1_change
            y1 += y1_change
            dis.fill(white)
            pygame.draw.rect(dis,green,[food_x,food_y,snake_block_size,snake_block_size])

            # Score counter
            if (snake_Length > snake_Length_past):
                current_score += 1

            # Shortener powerup
            if (snake_Length != snake_Length_past):
                shortener_x=round(random.randrange(0,dis_width-snake_block_size)/10)*10
                shortener_y=round(random.randrange(0,dis_height-snake_block_size)/10)*10
            if ((snake_Length) >= 7) and ((snake_Length) % (shortener_length+2))==0:
                pygame.draw.rect(dis,blue,[shortener_x,shortener_y,snake_block_size,snake_block_size])
            snake_Length_past = snake_Length

            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if abs((len(snake_List) - snake_Length)) >= 2:
                del snake_List[:shortener_length]
            elif len(snake_List) > snake_Length: 
                del snake_List[0]               

            # Game over if you eat yourself
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            our_snake(snake_block_size,snake_List)
            player_score(current_score,player_hiscore)

            pygame.display.update()

            t=time.time()

            if x1 == food_x and y1 == food_y:
                food_x0=food_x
                food_y0=food_y
                food_x=round(random.randrange(0,dis_width-snake_block_size)/10)*10
                food_y=round(random.randrange(0,dis_height-snake_block_size)/10)*10
                shortener_x=-snake_block_size
                shortener_y=-snake_block_size
                snake_Length += 1
                snake_speed += snake_speed_step #ADD SPEED INCREASE
                txt_choice=random.choice(food_message)
                colour_choice=random.choice(colour_array)
                t_food=time.time()
                
            if (t-t_food) < 1 and current_score > 0:
                popup_msg(txt_choice,colour_choice,food_x0,food_y0)
                pygame.display.update()

            if ((snake_Length-1) > shortener_length) and x1 == shortener_x and y1 == shortener_y:
                shortener_x=-snake_block_size
                shortener_y=-snake_block_size
                snake_Length -= shortener_length
            
            clock.tick(snake_speed)

        pygame.quit()
        quit()
    
    gameLoop(player_hiscore,difficulty)

if __name__ == "__main__":
    pass