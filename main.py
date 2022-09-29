import pygame
import os

# Inits for text and sound
pygame.font.init()
pygame.mixer.init()


# Set value of const to window
RESOLUTION = (1280,720)
WIN = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("MOW THE LAWN!")
# Colors Values
GRASS = (98,158,0)
MOWED_GRASS_COLOR = (122,175,5)
BROWN = (77,55,40)
WHITE = (255, 255, 255)
# Borders rects
BORDER_UP = pygame.Rect(0, 0, 1280, 20)
BORDER_LEFT = pygame.Rect(0, 0, 20, 720)
BORDER_RIGHT = pygame.Rect(1260, 0, 20, 720)
BORDER_DOWN = pygame.Rect(0, 700, 1280, 20)
# Set value of const to game properties
FPS = 60
VEL = 10
mowed_grass_list = []

LAWNMOVER_IMAGE = pygame.image.load(os.path.join('Assets', 'lawnmover.png'))
LAWNMOVER = pygame.transform.rotate(pygame.transform.scale(LAWNMOVER_IMAGE, (150, 150)), 90)

LAWNMOVER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'lawn-mower.mp3'))

SCORE_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)


def draw_window(lawnmover, mowed_grass_list, score):
    # Display changes on window
    WIN.fill(GRASS)
    pygame.draw.rect(WIN, BROWN, BORDER_UP)
    pygame.draw.rect(WIN, BROWN, BORDER_LEFT)
    pygame.draw.rect(WIN, BROWN, BORDER_RIGHT)
    pygame.draw.rect(WIN, BROWN, BORDER_DOWN)
    for MOVED_GRASS in mowed_grass_list:
        # Display all moved blocks
        pygame.draw.rect(WIN,MOWED_GRASS_COLOR, MOVED_GRASS)
    score_text = SCORE_FONT.render("SCORE: "+ str(score), 1, WHITE)
    WIN.blit(score_text, (20 + score_text.get_width() - 10, 40))
    # Create score text and dispaly in window
    WIN.blit(LAWNMOVER, (lawnmover.x, lawnmover.y))
    pygame.display.update()


def mow_the_grass(lawnmover):
    # Create mowed block and cheks if already in list
    MOWED_GRASS_BLOCK = pygame.Rect(lawnmover.x, lawnmover.y, 150, 150)
    if MOWED_GRASS_BLOCK not in mowed_grass_list:
        mowed_grass_list.append(MOWED_GRASS_BLOCK)


def handle_movement(keys_pressed, lawnmover):
    # Change position of lawnmover
    if keys_pressed[pygame.K_a] and lawnmover.x - VEL > BORDER_LEFT.x + 15 : 
        # LEFT KEY
        lawnmover.x -= VEL
    if keys_pressed[pygame.K_d] and lawnmover.x + VEL + 100 < BORDER_RIGHT.x - 45 : 
        # RIGHT KEY
        lawnmover.x += VEL
    if keys_pressed[pygame.K_w] and lawnmover.y - VEL > BORDER_UP.y + 15: 
        # UP KEY
        lawnmover.y -= VEL
    if keys_pressed[pygame.K_s] and lawnmover.y + VEL + 100 < BORDER_DOWN.y - 45: 
        # DOWN KEY
        lawnmover.y += VEL
    mow_the_grass(lawnmover)
    # Add changes to grass
    

def draw_winner(text):
    # Display text in center of window
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (1280/2 - draw_text.get_width()/2, 720/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)


def main():
    # Main function
    lawnmover = pygame.Rect(100, 300, 100, 100)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        score = len(mowed_grass_list) -1
        keys_pressed = pygame.key.get_pressed()  
        handle_movement(keys_pressed, lawnmover)
        draw_window(lawnmover, mowed_grass_list, score)
        winner_text = ''
        if score == 1:
            # When game starts sound is played
            LAWNMOVER_SOUND.play()
        if score > 600 :
            # Check if game is done
            LAWNMOVER_SOUND.stop()
            winner_text="YOU CLEARED GRASS GOOD JOB!" 
            draw_winner(winner_text)
            mowed_grass_list.clear()
            main()
    

if __name__ == "__main__":
    main()