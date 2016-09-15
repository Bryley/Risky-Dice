#TODO not finished yet.
import pygame;

#Constants
GREY = (150, 150, 150);
LIGHT_GREY = (230, 230, 230);
BLACK = (0, 0, 0);
BORDER_PERCENT = 5/100;

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

        self.button = Button("End Turn", pygame.Rect(pos[0]-50, pos[1]-12, 100, 25));
        self.board = board;

    def handleClick(self, pos):
        if(self.button.rect.collidepoint(pos)):
            self.click();

    def click(self):
        self.board.nextTurn();





    



