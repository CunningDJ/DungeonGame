from math import sqrt
from random import random, randint
import random

class Monster:
	
    def __init__(self, x, y, targeting=False, target=0):
		self.x = x
		self.y = y
    
    def seek(self, players):
        closestDistance = 100000000
        closestPlayer = Player()
        for player in players:
            if player.alive == True:
                distance = self.playerDistance(player)
                if distance < closestDistance:
                    closestDistance = distance
                    closestPlayer = player
        self.targeting = True
        self.target = closestPlayer.pID
        self.advance(closestPlayer)
        

    def advance(self,player):
        if player.x > self.x:
            self.x += 1
        elif player.x < self.x:
            self.x -=1
        
        if player.y > self.y:
            self.y += 1
        elif player.y < self.y:
            self.y -=1
        
    
    def playerDistance(self,player):
        return sqrt((self.x-player.x)**2 + (self.y-player.y)**2)
        
    def shout(self):
        print('{} {}! RARR!'.format(self.x, self.y))
        

class Player:
    
    def __init__(self,x=0,y=0,pID=999):
        self.x = x
        self.y = y
        self.pID = pID
        self.alive = True
    
    def shout(self,signout):
        print('I, p{}, am excited about being in x{} y{}!'.format(self.pID,self.x,self.y))
        print(signout)
        
class World:
    
    def __init__(self,wall=True):
        print("'Hello!' - World")
        self.players = []
        self.monsters = []
        self.x_space = 0
        self.y_space = 0
        self.wall = wall
        self.end = False
        
    def genesis(self,numPlayers,numMonsters,x_space,y_space):
        self.x_space = x_space
        self.y_space = y_space
        
        for count in range(numPlayers):
            #Initializes each player at a random spot in the "center quarter" of the stage.
            startPointX, startPointY = randint(self.x_space*1/4,self.x_space*3/4), randint(self.y_space*1/4,self.y_space*3/4)
            print('startX: {} startY: {}'.format(startPointX, startPointY))
            self.players.append(Player(startPointX, startPointY, count+1))
        
        monsterStartPoints = ((0, 0), (0, y_space-1), (x_space-1, y_space-1), (x_space-1, 0))
        
        for count in range(numMonsters):
            startPointX, startPointY = random.choice(monsterStartPoints)
            self.monsters.append(Monster(startPointX, startPointY))
            
        print('Let there be light! I am a {}x{} world, with {} players and {} monsters.'.format(self.x_space,self.y_space,len(self.players),len(self.monsters)))    # TODO Remove print check
    
    # Sets self.wall to True (keeps characters of the wall)
    # or False (loops the characters around the opposite end)
    def setWall(self,bool):
        self.wall = bool
            
    def check(self):
        livingPlayers = False
        
        
        xMax = self.x_space-1
        yMax = self.y_space-1
        for player in self.players:
            if player.alive == True:
                # Checks wall/loop boundaries
                if self.wall == True:
                    if player.x > xMax:
                        player.x = xMax
                    elif player.x < 0:
                        player.x = 0
                    
                    if player.y > yMax:
                        player.y = yMax
                    elif player.y < 0:
                        player.y = 0
                else:
                    if player.x > xMax:
                        player.x = 0
                    elif player.x < 0:
                        player.x = xMax
                    
                    if player.y > yMax:
                        player.y = 0
                    elif player.y < 0:
                        player.y = yMax
                # Checks if monster has caught them
                for monster in self.monsters:
                    if (monster.x,monster.y) == (player.x,player.y):
                        player.alive = False
                        break
            
            # Running check if any player is still alive
            if player.alive == True:
                livingPlayers = True        
        
        if livingPlayers == False:
            self.end = True
            print('World Ended!')
    
    def agentTest(self):
        for player in self.players:
            print('Player: {} X: {} Y: {}'.format(player.pID,player.x,player.y))
        
        count = 0
        for monster in self.monsters:
            print('Monster: {} X: {} Y: {}'.format(count,monster.x,monster.y))
            count +=1
    