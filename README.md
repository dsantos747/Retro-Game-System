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
After eating a green "food" item, a coloured message appears in the food's location, to celebrate. Message text and colours are randomised from preset arrays. (In this screenshot, the snake is travelling up).

![screen_7](https://github.com/dsantos747/Retro-Game-System/assets/51920488/beeb5e27-8148-4dcc-9e1e-1040dcfc856a)

#### Playing snake - showing "shorty" powerup
After eating a blue "shorty" item, the snake's length is reduced by 3.

![screen_8](https://github.com/dsantos747/Retro-Game-System/assets/51920488/5b9139f3-ddc9-4e7f-b830-2bf061b5eb84)

#### Game Over screen
![screen_6](https://github.com/dsantos747/Retro-Game-System/assets/51920488/e4d0ec0c-6780-4e8c-adf1-c935fe9cf7ce)
