#Game objects Module
import pygame;
import random;
import math;

class Player:

    def __init__(self, color, human=False):
        self.color = color;
        self.human = human;

    def getColor(self):
        return self.color;

#Constants
BLACK = (0, 0, 0);

P1BLUE = (124,216,247);
P2RED = (255, 0, 0);
P3GREEN = (17, 250, 87);
P4YELLOW = (231, 250, 17);

BORDER_PERCENT = 5/100;

BOARD_Y_OFFSET = 100;

PLAYERS = [Player(P1BLUE, True), Player(P2RED), Player(P3GREEN), Player(P4YELLOW)];

#Returns empty 2d list.
def createMultiDimList(size): #Stands for create multidimensional list.
    list1 = [];
    for i in range(size):
        list1.append([]);

    return list1;

class Square:

    def __init__(self, player, diceNumber, pos, size):

        self.player = player;
        self.pos = pos;
        self.size = size;
        self.dice = diceNumber;

        self.color = player.getColor();

    def render(self, surf):
        self.surf = pygame.Surface((self.size, self.size));
        self.surf.fill(BLACK);
        border = self.size * BORDER_PERCENT; #5% of the size of the square.
        pygame.draw.rect(self.surf, self.color, pygame.Rect(border, border,
                                                            self.size-BORDER_PERCENT*2*self.size,
                                                            self.size-BORDER_PERCENT*2*self.size));
        
        
        surf.blit(self.surf, (self.pos[0]*self.size, self.pos[1]*self.size));


class Board:

    def __init__(self, size, numberOfPlayers, maxDice):

        self.size = size;
        self.players = PLAYERS[0:numberOfPlayers];
        self.maxDice = maxDice;
        self.board = createMultiDimList(self.size);

        self.surf = None;

    def render(self, surf):
        mainSurfHeight = surf.get_height();

        size = mainSurfHeight-BOARD_Y_OFFSET*2;
        self.surf = pygame.Surface((size, size));

        for row in self.board:
            for col in row:
                col.render(self.surf);

        surf.blit(self.surf, (surf.get_width()/2-size/2, BOARD_Y_OFFSET));

    def generate(self, surfHeight):

        self.board = createMultiDimList(self.size);

        playerPoints = {};

        for player in self.players:
            playerPoints[player] = math.ceil(self.size**2/len(self.players));


        for y in range(self.size):
            for x in range(self.size):
                randomPlayer = random.choice(self.players);
                
                while(playerPoints[randomPlayer] <= 0):
                    randomPlayer = random.choice(self.players);
                    
                playerPoints[randomPlayer] -= 1;
                randomDice = random.randint(1, self.maxDice);

                self.board[y].append(Square(randomPlayer, randomDice, (x, y), (surfHeight-BOARD_Y_OFFSET*2)/self.size));








