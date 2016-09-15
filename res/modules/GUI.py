#TODO not finished yet.
import pygame;

#Constants
GREY = (150, 150, 150);
LIGHT_GREY = (230, 230, 230);
BLACK = (0, 0, 0);
BORDER_PERCENT = 5/100;

#Global Variables
openedPanel = None;
highscores = [];

def render(surf):
    if(openedPanel != None):
        openedPanel.render(surf);

def handleClick(pos):
    if(openedPanel != None):
        openedPanel.handleClick(pos);

class Button:

    def __init__(self, text, rect):
        self.text = text;
        self.rect = rect;

        self.surf = pygame.Surface((self.rect.width, self.rect.height));
        

    def render(self, surf):
        self.surf.fill(GREY);

        borderWidth = int(BORDER_PERCENT*self.rect.width);
        borderHeight = int(BORDER_PERCENT*self.rect.height);

        pygame.draw.rect(self.surf, LIGHT_GREY, pygame.Rect(borderWidth, borderHeight,
                                               self.rect.width-borderWidth*2,
                                               self.rect.height-borderHeight*2));
        font = pygame.font.Font(None, self.rect.height-borderHeight*4);
        fontArea = font.render(self.text, True, BLACK);
        fontRect = fontArea.get_rect();
        fontRect.center = (self.rect.width/2, self.rect.height/2);

        self.surf.blit(fontArea, fontRect);

        surf.blit(self.surf, self.rect);


class EndTurnButton:

    def __init__(self, pos, board):

        self.button = Button("End Turn", pygame.Rect(pos[0]-50, pos[1], 100, 25));
        self.board = board;

    def handleClick(self, pos):
        if(self.button.rect.collidepoint(pos)):
            self.click();

    def click(self):
        self.board.nextTurn();


class HUD:

    def __init__(self, board):
        self.board = board;

        self.surf = None;

    def render(self, surf):
        self.surf = pygame.Surface((surf.get_width(), 75));

        self.surf.fill(BLACK);

        font = pygame.font.Font(None, 60);

        fonts = [];
        fontArea = None;

        count = 1;
        for player in self.board.players:
            if(self.board.turn == player):
                font.set_bold(True);
            else:
                font.set_bold(False);
                
            fontArea = font.render(str(self.board.points[player]) + "sqs", True, player.getColor());
            fontRect = fontArea.get_rect();
            fontRect.center = (count*(surf.get_width()/(len(self.board.players)+1)), self.surf.get_height()/2);

            self.surf.blit(fontArea, fontRect);
            
            count += 1;

        surf.blit(self.surf, (0, 0));


class Panel:

    def __init__(self, board, surf):
        self.board = board;
        self.button = None;
        self.mainSurf = surf;

        self.surf = pygame.Surface((500, 400));

    def render(self, surf):

        self.surf.fill((200, 200, 200));

        font = pygame.font.Font(None, 50);
        fontArea = font.render("Player " + str(self.board.turn.number) + " wins the game.", True, BLACK);
        fontRect = fontArea.get_rect();

        fontRect.center = (self.surf.get_width()//2, self.surf.get_height()/4);

        self.button = Button("Close", pygame.Rect(self.surf.get_width()/2, self.surf.get_height()*2/3, 75, 30));
        self.button.render(self.surf);

        self.surf.blit(fontArea, fontRect);

        surf.blit(self.surf, (surf.get_width()/2 - self.surf.get_width()/2, surf.get_height()/2 - self.surf.get_height()/2));


    def handleClick(self, pos):
        if(self.button != None):
            if(self.button.rect.collidepoint(self.transPos(pos))):
                openedPanel = None;


    def transPos(self, pos):
        x = pos[0] - (self.mainSurf.get_width()-self.surf.get_width())/2;
        y = pos[1] - (self.mainSurf.get_height()-self.surf.get_height())/2;
        return (x, y);





    



