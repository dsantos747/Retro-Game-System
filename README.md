# Retro-Game-System
A little python project, designed to be an emulation of a retro arcade machine, with Snake, Space Invaders and Retro Helicopter. Hi-scores are stored locally in a database managed in PostgreSql.
This program has been developed purely for educational purposes (for myself).

## Screens
#### Main Menu
Main menu splash screen. Clicking "Space Invaders" or "Retro Helicopter" gives a console message stating the game is not yet ready.

![screen_1](https://github.com/dsantos747/Retro-Game-System/assets/51920488/2712cb67-7d18-4915-9607-9f19be71751a)

#### Username input
![screen_2](https://github.com/dsantos747/Retro-Game-System/assets/51920488/4de63425-6f84-4ca9-a81f-93f50dd0c963)

#### User login confirmation
The username input is checked against the database, and either the existing user data retrieved, or a new user created.

![screen_3](https://github.com/dsantos747/Retro-Game-System/assets/51920488/953ab5c6-6a42-4408-932d-c2a15a1f93b1)

#### Playing snake - shortly after eating
After eating a green "food" item, a coloured message appears in the food's location, to celebrate. Message text and colours are randomised from preset arrays. (In this screenshot, the snake is travelling down).

![screen_4](https://github.com/dsantos747/Retro-Game-System/assets/51920488/e0c1a221-3ec5-4fa1-a9ca-0c9df06bc69d)

#### Playing snake - showing "shorty" powerup
After eating a blue "shorty" item, the snake's length is reduced by 3.

![screen_5](https://github.com/dsantos747/Retro-Game-System/assets/51920488/7f31a4b7-89a8-47b2-8a41-f7634b95b9b5)

#### Game Over screen
![screen_6](https://github.com/dsantos747/Retro-Game-System/assets/51920488/e4d0ec0c-6780-4e8c-adf1-c935fe9cf7ce)
