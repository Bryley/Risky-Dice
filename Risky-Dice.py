#Imports
import pygame;

#Global Variables
running = True;

#Constant Variables
WIDTH = 800;
HEIGHT = 600;
WHITE = (255,255,255);

pygame.init();

screen = pygame.display.set_mode((WIDTH, HEIGHT));
pygame.display.set_caption("Risky Dice");

def render():
    screen.fill(WHITE);
    pygame.display.update();

while(running):

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
           running = False;

    render();

pygame.quit();
quit();
