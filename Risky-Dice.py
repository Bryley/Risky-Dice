#Imports
import pygame;
import sys;

sys.path.append("res/modules"); #Change path to the modules folder.
import GameObjects;
import GUI;

#Constant Variables
WIDTH = 800;
HEIGHT = 600;
WHITE = (255,255,255);

FPS = 30;

#Global Variables
running = True;

pygame.init();

screen = pygame.display.set_mode((WIDTH, HEIGHT));
pygame.display.set_caption("Risky Dice");

board = GameObjects.Board(6, 3, 12); #TEMP
board.generate(HEIGHT);

updater = pygame.time.Clock(); #Used to update game at a given FPS

class InGame:

    def __init__(self):
        self.board = GameObjects.Board(6, 3, 10);
        self.board.generate(HEIGHT);
        self.endButton = GUI.EndTurnButton((WIDTH/2, HEIGHT-50), self.board);

    def render(self, surf):
        self.board.render(surf);
        if(self.board.turn.human):
            self.endButton.button.render(surf);

    def handleClick(self, pos):
        self.board.handleClick(pos);
        self.endButton.handleClick(pos);

GAMESTATE = ["Main menu", InGame()];
gameState = GAMESTATE[1];

def render():
    screen.fill(WHITE);
    
    gameState.render(screen);
    pygame.display.update();

def update():
    board.ai.update();

while(running):

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
           running = False;

        elif(event.type == pygame.MOUSEBUTTONUP):
            pos = event.pos;
            gameState.handleClick(pos);

        elif(event.type == pygame.KEYDOWN):
            key = event.key;

            if(key == pygame.K_e):
                board.nextTurn();

    render();
    update();
    updater.tick(FPS); #Updates program at FPS time.

pygame.quit();
#quit();
