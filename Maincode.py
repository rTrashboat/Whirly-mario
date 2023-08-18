import math
from random import randint
import random
import pygame
import winsound
from sys import exit
import time
#from level.py import Level

def heighest_obstacle():
    y = 0
    for obstacle in obstacle_group:
        if obstacle.rect.y < y:
            y = obstacle.rect.y
    return y

def lowest_obstacle():
    x = 0
    y = 0
    for obstacle in obstacle_group:
        if obstacle.rect.y > y:
            x = obstacle.rect.x
            y = obstacle.rect.y
    return x,y


movement = 3
# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        x,y = lowest_obstacle()
        self.image = pygame.image.load("Graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x,y))
        self.gravity = 0
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3

    def apply_gravity(self,movement):
        global game_active
        self.gravity += 0.8
        self.rect.y += self.gravity

        # Collision detection with obstacles

        for obstacle_spiky in obstacle_spiky_group:
            if self.rect.colliderect(obstacle_spiky.rect):
                game_active = False
                #print(game_active)

        for obstacle in obstacle_group:
            if self.rect.colliderect(obstacle.rect):
                print("touching")
                if floating:
                    if self.rect.top >= obstacle.rect.bottom - 5 or self.gravity < 0:
                        self.rect.top = obstacle.rect.bottom 
                        print("down")
                        self.gravity = 0
                else:
                    if self.gravity < 0 :
                        self.rect.top = obstacle.rect.bottom + 6
                        self.gravity = 0
                if self.gravity > 0  and floating == False:
                    self.rect.bottom = obstacle.rect.top + 7
                    self.gravity = 0
#                elif self.gravity < 0 :
#                    self.rect.top = obstacle.rect.bottom
#                    self.gravity = 0
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= obstacle.rect.top + 1 and self.rect.colliderect(obstacle.rect):
                #if self.rect.colliderect(obstacle.rect):
                #    self.rect.bottom = obstacle.rect.top - 50
                self.gravity = -15

    def input(self):
        keys = pygame.key.get_pressed()
#        if keys[pygame.K_SPACE] or (keys[pygame.K_UP] and self.rect.bottom >= obstacle.rect.top + 1 and self.gravity > 0 and self.rect.colliderect(obstacle.rect)):
#            if self.rect.colliderect(obstacle.rect):
#                self.rect.bottom = obstacle.rect.top - 2
#            self.gravity = -20
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1.5
        elif keys[pygame.K_LEFT] or keys[pygame.K_q]  or keys[pygame.K_a]:
            self.direction.x = -1.5
        else:
            self.direction.x = 0

    def update(self,movement):
        self.apply_gravity(movement)
        self.rect.x += self.direction.x * self.speed
        self.input()

        #print(self.rect.x)

class Obstacles(pygame.sprite.Sprite):
    # 94 width and 7 height
    def __init__(self, obstacle_x, obstacle_y):
        super().__init__()
        self.image = pygame.image.load("Graphics/Simpleground.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(obstacle_x, obstacle_y))

class Obstacles_spiky(pygame.sprite.Sprite):
    def __init__(self, obstacle_x, obstacle_y):
        super().__init__()
        self.image = pygame.image.load("Graphics/Spikedground.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(obstacle_x, obstacle_y))

class Powerup_speed(pygame.sprite.Sprite):
    def __init__(self, speed_x, speed_y):
        super().__init__()
        self.image = pygame.image.load("Graphics/speedpowerup.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(speed_x, speed_y))

class Powerup_jetpack(pygame.sprite.Sprite):
    def __init__(self, jetpack_x, jetpack_y):
        super().__init__()
        self.image = pygame.image.load("Graphics/jetpackpowerup.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(jetpack_x, jetpack_y))

class level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Graphics/Background.png")
        self.rect = self.image.get_rect()
        self.world_shift = 0

    def scroll_x(self,p,o):
        player_y = p.rect.y
        player_y += 20
        for obstacle in obstacle_group:
            obstacle_y = obstacle.rect.y
            obstacle_y += 20
        

    def update(self,p,o):
        self.scroll_x(p,o)

obstacle_num = 0

def generate_obstacles(num,obstacle_num, up):
    global obstacle_spiky
    global obstacle
    global obstacle_x
    global obstacle_y
#    obstacle_group.empty()
    ten_obstacles = False
    generating = True
    spacing = 20
    max_spacing = 40
    obstacle_number = 0
    while generating:
        if ten_obstacles:
            break
        #print(obstacle_num)
        else:
            if not up:
                obstacle_x = randint(94, Width - 94)
                obstacle_y = randint(spacing, max_spacing)
                obstacle = Obstacles(obstacle_x, obstacle_y)
                obstacle_group.add(obstacle)
            else: 
                if random.randint(1,2) !=0:
                    obstacle_x = randint(94, Width - 94) 
                    obstacle_y = randint(-50, -9)
                    obstacle = Obstacles(obstacle_x, obstacle_y)
                    obstacle_group.add(obstacle)
                else:
                    obstacle_x = randint(94, Width - 94)
                    obstacle_y = randint(-50, -9)
                    obstacle_spiky = Obstacles_spiky(obstacle_x, obstacle_y)
                    obstacle_spiky_group.add(obstacle_spiky)

        if len(obstacle_group.sprites()) > obstacle_number:
                obstacle_num += 1
                spacing += 20
                max_spacing += 20
        obstacle_number = len(obstacle_group.sprites())
        if obstacle_num == num:
            ten_obstacles = True
    #       print(10)
            return obstacle_num
            break
            #print("cool")

def generate_powerup(powerup):
    if powerup == "speed":
        speed_y = randint(-50,-26)
        speed_x = randint(28, Width - 28)
        speed = Powerup_speed(speed_x,speed_y)
        speed_group.add(speed)
    elif powerup == "jetpack":
        jetpack_y = randint(-50,-26)
        jetpack_x = randint(28, Width - 28)
        jetpack = Powerup_jetpack(jetpack_x,jetpack_y)
        jetpack_group.add(jetpack)

    #print("added")

# Initialize pygame
pygame.init()


# Screen
Width = 500
Height = 600
screen = pygame.display.set_mode((Width, Height))
test_font = pygame.font.Font("fonts/Pixels.ttf", 90)
test_font2 = pygame.font.Font("fonts/Pixels.ttf", 150)

# Texts
gameover = test_font.render("GAME OVER", False, "Red")
ptr = test_font.render("Press r to retry", False, "Red")

# Clock
clock = pygame.time.Clock()

# Title
pygame.display.set_caption("Whirly mario")

# Icon
icon = pygame.image.load("Graphics/icon.ico").convert_alpha()
pygame.display.set_icon(icon)

# Groups
obstacle_spiky_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
obstacle_num = generate_obstacles(1,obstacle_num,False)
print(obstacle_num)

# Player
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

# Obstacles

level = level()
level_group = pygame.sprite.Group()
level_group.add(level)

speed_group = pygame.sprite.Group()
jetpack_group = pygame.sprite.Group()

# Keys
keys = pygame.key.get_pressed()

# Loop
game_active = True
running = True
last_action_time2 = time.time()
last_action_time3 = time.time()
last_action_time4 = time.time()
last_action_time = time.time()
score = test_font.render("0", False, "Red")
spawn_time = 0.6
floating = False
sped_up = False
powerups = ["speed","jetpack"]
while running:
    if game_active:
        #print(game_active)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if player.rect.y >= 600:
            game_active = False
        if player.rect.y <= 0:
            player.rect.y == 3

        if player.rect.x <= 0:
            player.rect.x = 3
        elif player.rect.x >= 470:
            player.rect.x = 470 
        for jetpack in jetpack_group:
            jetpack.rect.y += 4
            if player.rect.colliderect(jetpack.rect):
                last_action_time4 = current_time
                elapsed_time4 = 0
                floating = True
                jetpack_group.empty()

        for speed in speed_group:
            if player.rect.colliderect(speed.rect):
                print("touched")
                last_action_time3  = current_time
                elapsed_time3 = 0
                movement = movement / 2
                spawn_time = spawn_time * 2.5
                print(movement)
                speed_group.empty()
                sped_up = True



        if randint(1,300) == 1:
            random.shuffle(powerups)
            generate_powerup(powerups[1])

        level_group.draw(screen)
        player_group.draw(screen)
        obstacle_group.draw(screen)
        obstacle_spiky_group.draw(screen)
        speed_group.draw(screen)
        jetpack_group.draw(screen)
        screen.blit(score,(5,-30))

        player.update(movement)

        current_time = time.time()
        elapsed_time = current_time - last_action_time
        elapsed_time2 = current_time - last_action_time2
        if sped_up:
            if int(elapsed_time3) == 10:
                spawn_time = spawn_time / 2.5
                movement = 3.5
                #print("cool")
                # Update the last action time
                last_action_time3  = current_time
                sped_up = False
            elapsed_time3 = current_time - last_action_time3
            print(elapsed_time3)
        score = test_font.render(str(int(elapsed_time2)), False, "grey")

        if elapsed_time >= spawn_time:
            generate_obstacles(obstacle_num + 1,obstacle_num,True)
            #print("cool")
            # Update the last action tim e
            last_action_time = current_time

        if floating == True:
            print("cool")
            player.gravity = 0
            player.rect.y -= 0.000000000001
            elapsed_time4 = current_time - last_action_time4
            if int(elapsed_time4) == 10:
                last_action_time4 = current_time
                floating = False


        for speed in speed_group:
            speed.rect.y += 4
        for obstacle in obstacle_group:
            obstacle.rect.y += movement
        for obstacle_spiky in obstacle_spiky_group:
            obstacle_spiky.rect.y += movement
#            if obstacle.rect.y == 600:
#                obstacle_group.remove(obstacle)
#                generate_obstacles(obstacle_num + 1,obstacle_num)

        pygame.display.flip()
        pygame.display.update()

        clock.tick(60)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.key.get_pressed()[pygame.K_r]:
            floating = False
            spawn_time = 0.6
            movement = 3.5
            last_action_time2 = time.time()
            current_time = time.time()
            speed_group.empty()
            obstacle_spiky_group.empty()
            obstacle_group.empty()
            obstacle_num = 0
            generate_obstacles(1,obstacle_num,False)
            player.gravity = 0
            player.rect.x,player.rect.y = lowest_obstacle() 
            game_active = True

        screen.blit(gameover, (145,100))
        screen.blit(ptr, (55,300))

        pygame.display.flip()
        pygame.display.update()

        clock.tick(60)

pygame.quit()
