#Imports
import pygame;
import sys;

sys.path.append("res/modules"); #Change path to the modules folder.
import GameObjects;

#Constant Variables
WIDTH = 800;
HEIGHT = 600;
WHITE = (255,255,255);

GAMESTATE = ["Main menu", "In Game"];

#Global Variables
running = True;
gameState = GAMESTATE[1];

pygame.init();

screen = pygame.display.set_mode((WIDTH, HEIGHT));
pygame.display.set_caption("Risky Dice");

board = GameObjects.Board(6, 3, 12); #TEMP
board.generate(HEIGHT);

def render():
    screen.fill(WHITE);
    
    board.render(screen);
    pygame.display.update();

while(running):

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
           running = False;

        elif(event.type == pygame.MOUSEBUTTONUP):
            pos = event.pos;
            board.handleClick(pos);

    render();

pygame.quit();
#quit();
