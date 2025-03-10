import pygame
import time
import random
#to use text we need to initialize font module
pygame.font.init()
FONT = pygame.font.SysFont("Times New Roman" , 30)#size and font name SysFont means system fonts


#projectiels details in this case bullets details
BULLET_WIDTH = 10
BULLET_HEIGHT = 20


#pLayers details
#PLAYER_WIDTH = 40
#PLAYER_HEIGHT = 60

#HOW much to move per press player velocity
PLAYER_VEL = 5
#speed of the bullet
BULLET_VEL = 5


#Windows width and height 
WIDTH , HEIGHT =  1000,700
#WIN stands for window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#name to diplay for the game
pygame.display.set_caption("Rectangle Dodge")

#Setting background image for the game
#BG stands for background
BG = pygame.image.load("image.jpg")
#if image does not fit the window
#we can transform the width and height of image to match the windows width and height by the following code below:
#BG = pygame.transform.scale(pygame.image.load("image.jpg"), (WIDTH, HEIGHT))

SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

SPACESHIP = pygame.image.load("image2.png")
SPACESHIP1 = pygame.transform.scale(SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

BULLET = pygame.image.load("image3.jpg")
BULLET1 = pygame.transform.scale(BULLET, (BULLET_WIDTH, BULLET_HEIGHT))

# drawing image on screen
def draw(player , elapsed_time, bullets):
    
    WIN.blit(BG ,(0,0))#blit is used to draw image on the application
    #0 , 0 starts from the top left corner of the screen and top right is then the width you specified
    
    
    #to insert text in python we use fstring 
    time_text = FONT.render(f"Score: {round(elapsed_time)}" , 1 , "white")#1 makes the text better and white is the color
    # {round(elapsed_time)} round the times to nearest 1 sec
    WIN.blit(time_text, (10 , 10))
    
    
    #Drawing a rectangle which is our player in this case 
    WIN.blit(SPACESHIP1 , (player.x , player.y))#also can use rgb(255, 0 , 0)
    
    
    #drawing bullets
    #if we draw after the players they will appear on top of the player 
    #if we draw them before the player they will appear behind the player
    
    for bullet in bullets:
        WIN.blit(BULLET1 , (bullet.x , bullet.y))
    
    
   
    pygame.display.update()#update applies everything to the screen 
    #if no update nothing happens to the screen 
    
    
#main Game Loop specifically while loop 
def main():
    run = True# controls when to quit
    #creating a player 
    player = pygame.Rect(400 , 100 , SPACESHIP_WIDTH, SPACESHIP_HEIGHT)#the coordinates tell where the player will span
    
    clock = pygame.time.Clock()#determines how fast the while loop runs 
    #which eventually controls the movement of the charcters etc
    
    start_time = time.time()#stores the current time
    elapsed_time = 0 #how much time has passed 
    
    #adding projectiles
    bullet_add_increment = 2000#first bullet will be added at 2000 mili second 
    bullet_count = 0#tells us when another star adds after the first one
    
    bullets = []#storing stars in the list to draw
    #storing the stars on the screen
    
    hit = False#to prevent errors we define the variable
    
    while run:
        
        bullet_count += clock.tick(60) #clock.tick() counts how much miliseconds have passed till the last clock.tick()
        #clock.tick(60)#Delays the loop to run 60 seconds
        elapsed_time = time.time() - start_time
        
        #adds bullets to the screen 
        if bullet_count > bullet_add_increment:
            for _ in range(3):#don't need a variable just want to run the loop 3 times 
                bullet_x = random.randint(0,WIDTH - BULLET_WIDTH)#rand int randomly returns a value between the upper and lower limit including the limits 
                bullet = pygame.Rect(bullet_x , -BULLET_HEIGHT, BULLET_WIDTH,BULLET_HEIGHT)#NEGATIVE  to make it look like it is falling from above
                bullets.append(bullet)#adding the bullet to the list    

            bullet_add_increment = max(200 , bullet_add_increment -50)#max()selects the max value out of the two 
            bullet_count = 0# to control the bullets so they don't spawn infinitly
        
        #Quits the game when close is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()#stores the list of keys pressed by the user 
        #(player.x - PLAYER_VEL) >= 0 THIS is used so that we remain in the fourth coordinate
        if keys[pygame.K_LEFT] and (player.x - PLAYER_VEL) >=0:#K_LEFT code for left key for a K_a is used is pygame library
            player.x -= PLAYER_VEL #moves left
        if keys[pygame.K_RIGHT] and (player.x + PLAYER_VEL) <= (WIDTH-SPACESHIP_WIDTH):
            player.x += PLAYER_VEL#moves right 
        if keys[pygame.K_UP] and (player.y - PLAYER_VEL) >=0:
            player.y -= PLAYER_VEL#moves up 
        if keys[pygame.K_DOWN] and (player.y + PLAYER_VEL) <= (HEIGHT-SPACESHIP_HEIGHT):
            player.y += PLAYER_VEL#moves down
        
        #moving down the bullets
        #a copy of the bullets[] list is being created
        for bullet in bullets[:]:#removing the bullet that hit the bottom
                bullet.y += BULLET_VEL
                if bullet.y > HEIGHT:
                    bullets.remove(bullet)
                elif (bullet.y + bullet.height >= player.y )and bullet.colliderect(player):#basically it checks if the star has collided with the player then it is removed
                    #colliderect checks weather two rectangles have collieded or not 
                    bullets.remove(bullet)
                    hit = True
                    break
        
        if hit:
            lost_text = FONT.render("You Lost!" , 1 , "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))#lost_text.getwidth() gets the width of the text
            pygame.display.update()
            pygame.time.delay(4000)#pause for 4 seconds
            break
        draw(player , elapsed_time , bullets)
            
    pygame.quit()
    
if __name__ == "__main__":
    main()
    
