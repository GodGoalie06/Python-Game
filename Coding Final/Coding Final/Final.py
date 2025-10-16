# @title Default title text
#Imports
import turtle as trtl
import random
import leaderboard as lb
import time
import pygame
from leaderboard import clear_leaderboard
#Screen Initilization
wn = trtl.Screen()
Screenw = 600
Screenh = 600
wn.tracer(0)
trtl.screensize(Screenw, Screenh)
pygame.mixer.init()
#Importing gifs/files
wn.bgpic("Coding Final/Coding Final/Background.gif")
leaderboard = "Coding Final/Coding Final/leaderboard.txt"
s_image = "Coding Final/Coding Final/falcon.gif"
e_image = "Coding Final/Coding Final/Tie1.gif"
e2_image = "Coding Final/Coding Final/Tie2.gif"
e3_image = "Coding Final/Coding Final/Tie3.gif"
s_sound = pygame.mixer.Sound("Coding Final/Coding Final/SOUND.mp3")
d_sound = pygame.mixer.Sound("Coding Final/Coding Final/Death.mp3")
d2_sound = pygame.mixer.Sound("Coding Final/Coding Final/Death2.mp3")
wn.addshape(s_image)
wn.addshape(e_image)
wn.addshape(e2_image)
wn.addshape(e3_image)
#Statements/getting player name
name = wn.textinput("Please enter your name.", "Press 'OK' when done")
timer = 500
counter_interval = 1000
player_lives = 3
timer_up = False
game_started = False
score = 0
level = 1
difficulty_update_interval = 3
#Bullets
bullets = []
bullet_speed = 1
# Enemy properties
enemy_width, enemy_height = 50, 30
enemy_speed = .01  # Pixels per update
enemy_spawn_interval = 5  # Seconds
enemies = []
# Health levels for enemies
enemy_health_levels = [1, 2, 3]  # Easy, Medium, Hard
#Text initilization
font_setup = ("Arial",20,"normal")
#Turtles Setup
#Galaga
galaga = trtl.Turtle(shape=s_image)
galaga.hideturtle()
galaga.penup()
galaga.goto(0, -300)
galaga.setheading(90)
#Aliens
aliens = trtl.Turtle()
aliens.hideturtle()
#Score
score_writter = trtl.Turtle()
score_writter.hideturtle()
score_writter.penup()
score_writter.goto(-270,300)
score_writter.color("white")
#Counter
counter =  trtl.Turtle()
counter.hideturtle()
counter.penup()
counter.goto(260,300)
counter.color("white")
#Title writter
title_writter = trtl.Turtle()
title_writter.hideturtle()
title_writter.penup()
title_writter.goto(-350,300)
title_writter.color("white")
#Start
start_writter = trtl.Turtle()
start_writter.hideturtle()
start_writter.penup()
start_writter.color("white")
start_writter.write("Use a and d to move and use space to shoot", align="center", font=font_setup)
start_writter.goto(0,-50)
start_writter.write("Press space to start", align="center", font=font_setup)
# Life display
life_display = trtl.Turtle()
life_display.hideturtle()
life_display.penup()
life_display.goto(-350, 260)
life_display.color("white")

#Functions
#Player 
# Player Movement
def left():
    if galaga.xcor() <= -300:
        galaga.forward(0)
    else:
        galaga.goto(galaga.xcor() - 20, -300)

def right():
    if galaga.xcor() >= 300:
        galaga.forward(0)
    else:
        galaga.goto(galaga.xcor() + 20, -300)

# Player Shooting
def player_shoot():
    bullet = trtl.Turtle()
    bullet.shape("square")
    bullet.color("red")
    bullet.penup()
    bullet.goto(galaga.xcor(), galaga.ycor())
    bullet.setheading(90)
    bullets.append(bullet)
    s_sound.play()

# Bullet Movement and Collision Detection
def move_bullets():
    for bullet in bullets[:]:
        bullet.sety(bullet.ycor() + bullet_speed)
        if bullet.ycor() > 300:  # Remove bullets off-screen
            bullet.hideturtle()
            bullets.remove(bullet)
        else:
            # Check for collision with enemies
            for enemy in enemies[:]:
                if bullet.distance(enemy) < 25:  # Collision threshold
                    bullet.hideturtle()
                    bullets.remove(bullet)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        d_sound.play()
                        enemy.clear()
                        enemy.hideturtle()
                        enemies.remove(enemy)
                        update_score_for_galaga()
                    break
#Enemies
# Enemy Creation
def create_enemy(x, y, health):
    enemy = trtl.Turtle()
    enemy.penup()
    enemy.shape("square")
    enemy.shapesize(stretch_wid=1.5, stretch_len=2.5)
    enemy.shape(e_image if health == 1 else e2_image if health == 2 else e3_image)
    enemy.goto(x, y)
    enemy.health = health
    return enemy

# Enemy Spawning
def spawn_enemy():
    enemy_x = random.randint(-250, 250)
    enemy_y = 250  # Start near the top
    health = random.choice(enemy_health_levels)
    enemy = create_enemy(enemy_x, enemy_y, health)
    enemies.append(enemy)

# Enemy Movement and Player Collision Detection
def move_enemies():
    for enemy in enemies[:]:
        global player_lives
        enemy.sety(enemy.ycor() - enemy_speed)
        if enemy.ycor() < -300:  # If enemy moves off the bottom of the screen
            enemy.hideturtle()
            d_sound.play()
            enemies.remove(enemy)
            player_lives -= 1
            update_life()

# Player Collision with Enemy
def check_player_collision():
    global player_lives
    for enemy in enemies:
        if galaga.distance(enemy) < 20:
            player_lives -= 1
            enemy.clear()
            enemy.hideturtle()
            enemies.remove(enemy)
            update_life()
#Misc
# Game Management
def start_key_press():
    start_game()

def start_game():
    global game_started, timer, score, timer_up, player_lives

    if not game_started:
        # Reset variables
        timer = 500
        score = 0
        player_lives = 3
        timer_up = False
        game_started = True

        # Clear start text
        start_writter.clear()

        # Show turtle and start the game
        galaga.showturtle()
        score_writter.clear()
        title_writter.write("Score:", font=font_setup)
        score_writter.write(score, font=font_setup)
        life_display.write(f"Lives: {player_lives}", font=("Arial", 16, "normal"))
        countdown()

        # Main game loop
        last_enemy_spawn_time = time.time()
        while not timer_up and player_lives > 0:
            if time.time() - last_enemy_spawn_time > enemy_spawn_interval:
                spawn_enemy()
                last_enemy_spawn_time = time.time()

            move_enemies()
            move_bullets()
            check_player_collision()
            check_game_over()
            update_score_and_level()
            wn.update()

# Timer Countdown
def countdown():
    global timer, timer_up
    counter.clear()
    if timer == 0:
        timer_up = True
        counter.write("Time's Up", font=font_setup)

        # Hide and clear player and enemies
        galaga.hideturtle()
        galaga.clear()
        for enemy in enemies:
            enemy.hideturtle()
            enemy.clear()
        enemies.clear()
        wn.update()

        start_writter.write("GAME OVER!", align="center", font=font_setup)
        time.sleep(5)
        start_writter.clear()

        manage_leaderboard()
        time.sleep(5)
        show_restart_button()
    else:
        counter.write("Timer: " + str(timer), font=font_setup)
        timer -= 1
        counter.getscreen().ontimer(countdown, counter_interval)

# Score and Level Updates
def update_score_for_galaga():
    global score
    score += 1
    score_writter.clear()
    score_writter.write(score, font=font_setup)

def update_score_and_level():
    global enemy_speed, enemy_spawn_interval, level
    if score // 10 > level - 1:  # Level up every 10 points
        level += 1
        enemy_speed += .01
        enemy_spawn_interval += 0.3  # Faster spawn times

# Life Display Update
def update_life():
    life_display.clear()
    life_display.write(f"Lives: {player_lives}", font=("Arial", 16, "normal"))

# Check Game Over
def check_game_over():
    global timer_up
    if player_lives <= 0:
        timer_up = True
        counter.clear()
        counter.write("You Died!", font=font_setup)
        d2_sound.play()

        galaga.hideturtle()
        galaga.clear()
        for enemy in enemies:
            enemy.hideturtle()
            enemy.clear()
        enemies.clear()
        wn.update()

        start_writter.clear()
        start_writter.write("GAME OVER!", align="center", font=font_setup)
        time.sleep(5)
        start_writter.clear()

        manage_leaderboard()
        time.sleep(5)
        show_restart_button()
        return True
    return False

# Restart Game
def restart_game():
    global timer, timer_up, game_started, score, player_lives, enemies, bullets

    timer = 500
    score = 0
    player_lives = 3
    timer_up = False
    game_started = False

    galaga.hideturtle()
    galaga.goto(0, -300)
    galaga.showturtle()

    counter.clear()
    score_writter.clear()
    life_display.clear()
    clear_leaderboard(turtle_object=start_writter)

    wn.listen()
    start_game()

def show_restart_button():
    wn.textinput("Restart?", "Press 'OK' to Restart")
    restart_game()

# Leaderboard Management
def manage_leaderboard():
    global score
    spot = None

    leader_names_list = lb.get_names(leaderboard)
    leader_scores_list = lb.get_scores(leaderboard)

    if len(leader_scores_list) < 5 or score >= leader_scores_list[4]:
        lb.update_leaderboard(leaderboard, leader_names_list, leader_scores_list, name, score)
        lb.draw_leaderboard(True, leader_names_list, leader_scores_list, spot, score)
    else:
        lb.draw_leaderboard(False, leader_names_list, leader_scores_list, spot, score)

#Event
wn.listen()
wn.onkey(start_key_press, "space")
wn.onkeypress(left, "a")
wn.onkeypress(right, "d")
wn.onkeypress(player_shoot, "space")
wn.mainloop()