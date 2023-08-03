# A simple snake game in Python

##### TASKS #####
# Add initial menu with difficulty settings
# Add music
# Add hi-score logging
#   Maybe use parent script, where you select your game, to allow user login. Then, all hi-scores obtained during that session will be recorded under that name.
# Add map options
#   Add maps with obstacles
def main():
    import pygame
    import time
    import random

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
    pygame.display.set_caption("Slippery Snek")
    pygame.display.update()
    game_over=False

    x1_change=0
    y1_change=0

    clock = pygame.time.Clock()

    snake_block_size=10
    shortener_length=3

    colour_array=[yellow,black,red,green,blue,darkGreen]
    food_message=["Ohh yeahh","So good!","Mmmmm","Give me more!","Gotta keep munchin'","Scrumptious"]

    font_style = pygame.font.SysFont("bahnschrift",15)
    score_font = pygame.font.SysFont("roboto",20)

    def player_score(score):
        value=score_font.render("Current score: " + str(score), True, black)
        dis.blit(value,[0,0])

    def our_snake(snake_block_size, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis,darkGreen,[x[0],x[1],snake_block_size,snake_block_size])

    def message(msg,colour):
        mesg_pos=font_style.size(msg)
        mesg = font_style.render(msg, True, colour)
        dis.blit(mesg, [(dis_width/2)-(mesg_pos[0]/2), (dis_height/2)-(mesg_pos[1]/2)])

    def popup_msg(txt_choice,colour_choice,food_x0,food_y0):
        txt=txt_choice
        colour=colour_choice
        mesg_pos=font_style.size(txt)
        mesg = font_style.render(txt, True, colour)
        dis.blit(mesg, [(food_x0)-(mesg_pos[0]/2)+snake_block_size/2, (food_y0)-(mesg_pos[1]/2)+snake_block_size/2])

    def gameLoop(): #Function to run the game
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

        snake_speed=15
        snake_speed_step=1

        snake_Length_past=0

        shortener_x=-snake_block_size
        shortener_y=-snake_block_size

        t_food=time.time_ns()

        while not game_over: #Continue running until game over triggered
            while game_close == True:
                dis.fill(black)
                message("Jeez, you suck! Press Q-Quit or C-Play Again", red)
                player_score(current_score)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over=True
                            game_close=False
                        if event.key == pygame.K_c:
                            snake_speed=20
                            gameLoop()

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
            if ((snake_Length) >= 7) and ((snake_Length) % shortener_length)==0:
                pygame.draw.rect(dis,blue,[shortener_x,shortener_y,snake_block_size,snake_block_size])
            snake_Length_past = snake_Length

            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if abs((len(snake_List) - snake_Length)) >= 2:
                del snake_List[:shortener_length]
                #snake_List[:-shortener_length] = []
                #snake_List[:len(snake_List)-shortener_length] = []
            elif len(snake_List) > snake_Length: 
                del snake_List[0]               

            # Game over if you eat yourself
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            our_snake(snake_block_size,snake_List)
            player_score(current_score)

            pygame.display.update()

            t=time.time()

            if x1 == food_x and y1 == food_y:
                #popup_msg()
                #print(random.choice(food_message))
                food_x0=food_x
                food_y0=food_y
                food_x=round(random.randrange(0,dis_width-snake_block_size)/10)*10
                food_y=round(random.randrange(0,dis_height-snake_block_size)/10)*10
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
    
    gameLoop()

if __name__ == "__main__":
    main()