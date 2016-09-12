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
P4ORANGE = (245, 182, 10);

SELECT = (235, 255, 13); #The color for selected squares.

BORDER_PERCENT = 5/100;

BOARD_Y_OFFSET = 100;

PLAYERS = [Player(P1BLUE, True), Player(P2RED), Player(P3GREEN), Player(P4ORANGE)];

#Returns empty 2d list.
def createMultiDimList(size): #Stands for create multidimensional list.
    list1 = [];
    for i in range(size):
        list1.append([]);

    return list1;

class Square:

    def __init__(self, board, player, diceNumber, pos, size):

        self.board = board; #Instance of parent;
        self.player = player;
        self.pos = pos;
        self.size = size;
        self.dice = diceNumber;

        self.font = pygame.font.Font(None, int(self.size-(7*self.size)/100));

        self.rect = pygame.Rect(self.pos[0]*self.size, self.pos[1]*self.size, self.size, self.size);

    def render(self, surf):
        self.surf = pygame.Surface((self.size, self.size));
        if(self.board.selected == self):
            self.surf.fill(SELECT);
        else:
            self.surf.fill(BLACK);
        border = self.size * BORDER_PERCENT; #5% of the size of the square.
        pygame.draw.rect(self.surf, self.player.getColor(), pygame.Rect(border, border,
                                                            self.size-BORDER_PERCENT*2*self.size,
                                                            self.size-BORDER_PERCENT*2*self.size));
        
        
        fontArea = self.font.render(str(self.dice), True, BLACK);

        fontRect = fontArea.get_rect();

        fontRect.center = (self.size/2, self.size/2);

        self.surf.blit(fontArea, fontRect);
        
        surf.blit(self.surf, self.rect);

    def rollDice(self):
        total = 0;
        for roll in range(self.dice):
            total += random.randint(1, 6);

        return total;


class Board:

    def __init__(self, size, numberOfPlayers, maxDice):

        self.size = size;
        self.players = PLAYERS[0:numberOfPlayers];
        self.maxDice = maxDice;
        self.board = createMultiDimList(self.size);

        self.turn = self.players[0];

        self.points = {};

        self.selected = None;

        self.surf = None;

    def render(self, surf):
        self.mainSurf = surf; #main surf is the main screen instance.

        size = self.mainSurf.get_height()-BOARD_Y_OFFSET*2;
        self.surf = pygame.Surface((size, size));

        for row in self.board:
            for col in row:
                col.render(self.surf);

        surf.blit(self.surf, (self.mainSurf.get_width()/2-size/2, BOARD_Y_OFFSET));

    def takeOverSquare(self, domSquare, square):
        #domSquare stands for dominate square which is the square that will take over the 'square'.

        #TODO make animation showing roll numbers.
        
        dRoll = domSquare.rollDice();
        roll = square.rollDice();

        if(dRoll > roll):
            square.player = domSquare.player;
            square.dice = domSquare.dice-1;

            domSquare.dice = 1;

        else:
            domSquare.dice = 1;

    #Gets the number of adjacent avalable squares
    def getAvalableAdjacentSquares(self, x, y, targetPlayer):
        #targetPlayer is the target player the function will count.
        count = 0;

        if(x > 0):
            if(self.board[y][x-1].player != targetPlayer):
                count += 1;
        if(x < self.size-1):
            if(self.board[y][x+1].player != targetPlayer):
                count += 1;

        if(y > 0):
            if(self.board[y-1][x].player != targetPlayer):
                count += 1;

        if(y < self.size-1):
            if(self.board[y+1][x].player != targetPlayer):
                count += 1;

        return count;
        

    #Handles validation of square selection.
    def handleClick(self, pos):
        x = 0;
        y = 0;
        for row in self.board:
            for col in row:
                if(col.rect.collidepoint(self.transPos(pos))):

                    #If the square clicked is already selected...
                    if(col == self.selected):
                        #Unselect it
                        self.selected = None;
                        return;

                    #If picking atacking square.
                    if(self.selected != None):
                        #If the clicked squares player is not the current player...
                        if(col.player != self.turn):
                            count = 0;
                            if(x > 0):
                                if(self.board[y][x-1] == self.selected):
                                    count += 1;
                            if(x < self.size-1):
                                if(self.board[y][x+1] == self.selected):
                                    count += 1;
                            if(y > 0):
                                if(self.board[y-1][x] == self.selected):
                                    count += 1;
                            if(y < self.size-1):
                                if(self.board[y+1][x] == self.selected):
                                    count += 1;

                            if(count > 0):

                                self.takeOverSquare(self.selected, col);
                                if(col.player == self.turn and col.dice != 1):
                                    self.selected = col;
                                else:
                                    self.selected = None;

                        return;
                            
                    if(col.dice == 1):
                        return;
                    
                    if(col.player == self.turn):
                        
                        if(self.getAvalableAdjacentSquares(x, y, self.turn) > 0):
                            self.selected = col;
                
                x += 1;
            x = 0;
            y += 1;

    def findPoints(self):
        for player in self.players:
            values = [];
            for y in range(self.size):
                for x in range(self.size):
                    self.check = [];
                    self.count = 0;
                    self.floodFillCheck(x, y, player);
                    values.append(self.count);

            self.points[player] = max(values);
            print("FINISHED: " + str(max(values)));

        

    #Looping function for findingPoints algorithm.
    def floodFillCheck(self, x, y, player):
        #Do this statement but look for an IndexError.
        try:
            if(self.board[y][x].player != player or (x, y) in self.check):
                return;
        except IndexError:
            return;

        self.count += 1;
        self.check.append((x,y));
        
        if((x >= self.size) == False):
            self.floodFillCheck(x+1, y, player);
        if((x <= 0) == False):
            self.floodFillCheck(x-1, y, player);

        if((y >= self.size) == False):
            self.floodFillCheck(x, y+1, player);
        if((y <= 0) == False):
            self.floodFillCheck(x, y-1, player);
            

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

                self.board[y].append(Square(self, randomPlayer, randomDice, (x, y), (surfHeight-BOARD_Y_OFFSET*2)/self.size));


    def transPos(self, pos):
        y = pos[1] - BOARD_Y_OFFSET;
        x = pos[0] - (self.mainSurf.get_width()-self.surf.get_width())/2;

        return (x,y);





