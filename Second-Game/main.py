import pygame
import time
import random

pygame.font.init()
FONT = pygame.font.SysFont("Times New Roman" , 30)

pygame.display.set_caption("Snake Game")
BG = pygame.image.load("image2.jpg")

BUBBLE_WIDTH = 20
BUBBLE_HEIGHT = 20

SNAKE_WIDTH = 25
SNAKE_HEIGHT = 25

SNAKE_VEL = 5


WIDTH , HEIGHT = 1000 , 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(snake,snake2 , elapsed_time , bubbles):
    WIN.blit(BG, (0 , 0))
    
    time_text = FONT.render(f"Time:{round(elapsed_time)}s" , 1 , "white")
    WIN.blit(time_text , (10, 10))
    
    
    pygame.draw.rect(WIN , "Red" , snake)
    pygame.draw.rect(WIN , "Red" , snake2)
    
    for bubble in bubbles:
        pygame.draw.rect(WIN , "white" , bubble)
        
    pygame.display.update()
    
def main():
    
    run = True
    
    snake = pygame.Rect(WIDTH/2, HEIGHT - SNAKE_HEIGHT,SNAKE_WIDTH , SNAKE_HEIGHT )
    snake2 = pygame.Rect(WIDTH/2 - SNAKE_WIDTH -1, HEIGHT - SNAKE_HEIGHT,SNAKE_WIDTH , SNAKE_HEIGHT )
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    
    bubble_add_increment = 5000
    bubble_count = 0
    bubbles = []
    
    hit = False
    
    
    while run:
        bubble_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        if bubble_count > bubble_add_increment:
            for _ in range(1):
                bubbles.clear()
                bubble_x = random.randint(0, WIDTH - BUBBLE_WIDTH)
                bubble_y = random.randint(0 , HEIGHT - BUBBLE_HEIGHT)
                bubble = pygame.Rect(bubble_x , bubble_y , BUBBLE_WIDTH , BUBBLE_HEIGHT)
                bubbles.append(bubble)
               
                
           
            bubble_add_increment = max(200 , bubble_add_increment)
            bubble_count = 0
            
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and (snake.x - SNAKE_VEL) >= 0:
            snake.x -= SNAKE_VEL
            snake2.x -= SNAKE_VEL
        if keys[pygame.K_RIGHT] and (snake.x + SNAKE_VEL) <= (WIDTH - SNAKE_WIDTH):
            snake.x += SNAKE_VEL
            snake2.x = snake.x - SNAKE_WIDTH-1
            snake2.y = snake.y 
        if keys[pygame.K_UP] and (snake.y - SNAKE_VEL) >= 0:
            snake.y -= SNAKE_VEL  # Move first triangle up
            snake2.y = snake.y + SNAKE_HEIGHT+1
            snake2.x = snake.x 
            
            
        if keys[pygame.K_DOWN] and (snake.y + SNAKE_VEL) <= (HEIGHT - SNAKE_HEIGHT):
            snake.y += SNAKE_VEL
            snake2.y += SNAKE_VEL
        
        
        for bubble in bubbles[:]:
            if bubble.y > HEIGHT:
                bubbles.remove(bubble)
            elif (bubble.y + bubble.height >= snake.y) and bubble.colliderect(snake):
                bubbles.remove(bubble)
                hit = True
                break
        
        draw(snake,snake2, elapsed_time, bubbles)
    pygame.quit()
    
if __name__ == "__main__":
    main()
