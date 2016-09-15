#Imports
import pygame;
import sys;

sys.path.append("res/modules"); #Change path to the modules folder.
import GameObjects;
import GUI;

#Constant Variables

NUMBER_OF_PLAYERS = 3;
NUMBER_OF_SQUARES = 8;
MAX_DICE = 10;

WIDTH = 800;
HEIGHT = 600;
WHITE = (255,255,255);

FPS = 30;

#Global Variables
running = True;

pygame.init();

screen = pygame.display.set_mode((WIDTH, HEIGHT));
pygame.display.set_caption("Risky Dice");

updater = pygame.time.Clock(); #Used to update game at a given FPS
    
class InGame:

    def __init__(self):
        self.board = GameObjects.Board(NUMBER_OF_SQUARES, NUMBER_OF_PLAYERS, MAX_DICE);
        self.board.generate(HEIGHT);
        self.board.findPoints();
        self.endButton = GUI.EndTurnButton((WIDTH/2, HEIGHT-50), self.board);

        self.hud = GUI.HUD(self.board);

    def render(self, surf):
        self.hud.render(surf);
        self.board.render(surf);
        if(self.board.turn.human):
            self.endButton.button.render(surf);

    def update(self):
        self.board.ai.update();

    def handleClick(self, pos):
        self.board.handleClick(pos);
        self.endButton.handleClick(pos);
        

GAMESTATE = ["Main menu", InGame()];
gameState = GAMESTATE[1];

def load():
    file = open("res/highscore.txt");

    for line in file:
        GAMESTATE[1].board.record = int(line);
    
    file.close();

def save():
    file = open("res/highscore.txt", "w");
    file.write(str(GAMESTATE[1].board.record));
    file.close();

def render():
    screen.fill(WHITE);
    
    gameState.render(screen);
    
    GUI.render(screen);
    pygame.display.update();

def update():
    gameState.update();


load();

while(running):

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
           running = False;

        elif(event.type == pygame.MOUSEBUTTONUP):
            pos = event.pos;
            gameState.handleClick(pos);
            GUI.handleClick(pos);

        elif(event.type == pygame.KEYDOWN):
            key = event.key;

            if(key == pygame.K_e):
                board.nextTurn();

    render();
    update();
    updater.tick(FPS); #Updates program at FPS time.

save();
pygame.quit();
#quit();
