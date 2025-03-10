import pygame
import os#loading os to take path of images

#good practice to create constants in upper case
WIDTH , HEIGHT = 900 , 500#scale if on low display
WIN = pygame.display.set_mode((WIDTH , HEIGHT))#window is called the surface
pygame.display.set_caption("Third Game!")

WHITE = (255, 255, 255)
BLACK = (0 , 0 , 0)
RED = (255 , 0 , 0)
YELLOW = (255 , 255 , 0)

#we can't have floating points while creating a pygame rectangle
BORDER = pygame.Rect((WIDTH//2)-5 , 0 , 10 , HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH , SPACESHIP_HEIGHT = 55 , 40

#creating a new user event 
YELLOW_HIT = pygame.USEREVENT + 1 #unique event id = 1
RED_HIT = pygame.USEREVENT + 2 #unique event id = 1


YELLOW_SPACE_IMGAE = pygame.image.load("image1.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACE_IMGAE , (SPACESHIP_WIDTH , SPACESHIP_HEIGHT)) , 90)#making the space ship smaller


RED_SPACE_IMGAE = pygame.image.load("image2.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACE_IMGAE ,  (SPACESHIP_WIDTH , SPACESHIP_HEIGHT)), 270)#making space ship smaller

#Used to draw stuff on the screen 
def draw_window(red , yellow , red_bullets , yellow_bullets):
    WIN.fill(WHITE)#colors the screen/Window RGB
   
    pygame.draw.rect(WIN , BLACK , BORDER)#drawing shapes etc this method is used not images on the screen 

    WIN.blit(YELLOW_SPACESHIP, (yellow.x , yellow.y))#blit is used to draw surface on screen
    #first parameter is height and second is width 
        
    WIN.blit(RED_SPACESHIP , (red.x , red.y))
    

    for bullet in red_bullets:
        pygame.draw.rect(WIN , RED , bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN , YELLOW , bullet)


    pygame.display.update()#needs to update every time to draw something on the screen

#player movements

#yellow ship movement 
def yellow_handle_movement(keys_pressed , yellow):
    if keys_pressed[pygame.K_a] and (yellow.x - VEL) > 0:  #a is used to go left 
         yellow.x -= VEL
    if keys_pressed[pygame.K_d] and (yellow.x + VEL) < BORDER.x - SPACESHIP_WIDTH:#used to go right
         yellow.x += VEL
    if keys_pressed[pygame.K_w] and (yellow.y - VEL) > 0 :#used to go up
         yellow.y -= VEL
    if keys_pressed[pygame.K_s] and (yellow.y + VEL) < (HEIGHT-SPACESHIP_HEIGHT-15):#used to come down
         yellow.y += VEL


#red movements
def red_handle_movement(keys_pressed , red):
        if keys_pressed[pygame.K_LEFT] and (red.x - VEL) > BORDER.x + BORDER.width :# a is used to go left 
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and (red.x + VEL) < WIDTH - SPACESHIP_WIDTH:#used to go right
            red.x += VEL
        if keys_pressed[pygame.K_UP]  and  (red.y - VEL) > 0:#used to go up
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and (red.y + VEL) < (HEIGHT-SPACESHIP_HEIGHT-15):#used to come down
            red.y += VEL

#move bullets , handle collision of the bullets and removing the bullets after collision
def handle_bullets(yellow_bullets, red_bullets , yellow ,red):
    #coming from the character on the left 
    for bullet in yellow_bullets:#moving towards the right
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):#checks for collision if yellow bullets hits red
            yellow_bullets.remove(bullet)
            #creating an event
            pygame.event.post(pygame.event.Event(RED_HIT))
    
    for bullet in red_bullets:#moving towards the right
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):#checks for collision if yellow bullets hits red
            red_bullets.remove(bullet)
            #creating an event
            pygame.event.post(pygame.event.Event(YELLOW_HIT))





#collisions , redrawing window , updating the score, game logic
#main loop

def main():
    red = pygame.Rect(400, 100 , SPACESHIP_WIDTH , SPACESHIP_HEIGHT )
    yellow = pygame.Rect(300, 100 , SPACESHIP_WIDTH  , SPACESHIP_HEIGHT)#

    red_bullets = []# add a bullet to list then draw it on screen and then move it 
    yellow_bullets = []


    clock = pygame.time.Clock()
    run = True

    #event loop 
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            #We want the bullet to come out each time the player presses the key
            #not when he is holding the key

            if event.type == pygame.KEYDOWN:# KEYDOWN when the key is pressed
                 #when left CTRL is pressed 
                 if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:# ( len(yellow_bullets) < MAX_BULLETS) limits the number of the bullets 
                    bullet = pygame.Rect(yellow.x+yellow.width , yellow.y+yellow.height//2 - 2          , 10 , 5)#yellow.y+yellow.height/2 -2  so bullet comes out from the middle of the character 
                      #yellow.x+yellow.width so the bullet comes out front of the space ship
                    yellow_bullets.append(bullet)
                 if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y+red.height//2 - 2          , 10 , 5)#red.y+red.height/2 -2  so bullet comes out from the middle of the character 
                      #red.x     ( (red.width) is removed because it is facing ot left of the screen  )   so the bullet comes out front of the space ship
                    red_bullets.append(bullet)



        #after every 60 times a second it checks what keys are being pressed 
        keys_pressed = pygame.key.get_pressed()#what keys are currently being pressed 
        #we check if the keys stayed pressed down it will registered as pressed
        
        yellow_handle_movement(keys_pressed , yellow)
        red_handle_movement(keys_pressed , red)
        

        handle_bullets(yellow_bullets , red_bullets , yellow , red)



        draw_window(red, yellow , red_bullets , yellow_bullets)
            
    
    pygame.quit()

#only want to run the game when this file is runned not when it is imported
if __name__ == "__main__":
    main()







