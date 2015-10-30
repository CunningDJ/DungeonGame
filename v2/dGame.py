from dGameMod import World
import time
from threading import Thread
from msvcrt import getwch
import os

def main():

    newWorld = World()
    time.sleep(1)
    newWorld.genesis(*getParams())

    #monsterThread = Thread(target=monsterEngine, args=(newWorld.monsters,))
    #drawThread = Thread(target=draw, args=(newWorld,))
    #engineThread = Thread(target=gameEngine, args=(newWorld,))
    #monsterThread.setDaemon(True)
    #drawThread.setDaemon(True)
    #engineThread.start()
    #engineThread.join()
    gameEngine(newWorld)

# Determines how the intial parameters of the World object are decided
def getParams():
    numPlayers = 3
    numMonsters = 2
    squareDim = 40
    
    return numPlayers, numMonsters, squareDim, squareDim

def gameEngine(world):
    drawThread = Thread(target=drawEngine, args=(world,))
    monsterThread = Thread(target=monsterEngine, args=(world,))
    monsterThread.setDaemon(True)
    drawThread.setDaemon(True)
    drawThread.start()
    monsterThread.start()
    
    world.agentTest()
    exitCode = False
    while world.end == False:
        exitCode = playerInput(world.players)
        if exitCode == True:
            break

    #drawThread.join()
    print('Done! (Escaped)')
    
def monsterEngine(world):
    time.sleep(2)
    while True:
        time.sleep(1)
        for monster in world.monsters:
            monster.seek(world.players)
            
def drawEngine(world):
    count = 1
    while world.end == False:
        draw(world)
        world.check()
    print('Draw Done!')
    
def playerInput(players):
    exitCode = False
    
    key = ord(getwch())
    if key == 27: #ESC
        os.system('cls')
        exitCode = True
    #P1 (players[0]) controls
    elif key == 224: # Special keys (arrows, f keys, ins, del, etc.)
        key = ord(getwch())
        if key == 80: #Down arrow
            players[0].y -= 1
        elif key == 72: #Up arrow
            players[0].y += 1
        elif key == 77: #right arrow
            players[0].x += 1
        elif key == 75: #left arrow
            players[0].x -= 1
    #P2 (players[1]) controls
    elif key == 119: # W (p2 up)
        players[1].y += 1
    elif key == 115: # S (p2 down)
        players[1].y -= 1
    elif key == 100: # D (p2 right)
        players[1].x += 1
    elif key == 97: # A (p2 left)
        players[1].x -= 1
    #P3 (players[2])  controls
    elif key == 105: # I (p3 up)
        players[2].y += 1
    elif key == 107: # K (p3 down)
        players[2].y -= 1
    elif key == 108: # L (p3 right)
        players[2].x += 1
    elif key == 106: # J (p3 left)
        players[2].x -= 1
    
    return exitCode
    
def draw(world):
    
    playersCopy, monstersCopy = copyAgents(world)
    os.system('cls')
    for y in range(world.y_space)[world.y_space::-1]:
        rowString = ''
        for x in range(world.x_space):
            occupied = False
            for monster in monstersCopy:
                if x == monster.x and y == monster.y and occupied == False:
                    rowString += 'M'
                    occupied=True
                    
            for player in playersCopy:
                if player.alive == True and occupied == False:
                    if x == player.x and y == player.y and occupied == False:
                        rowString += str(player.pID)
                        occupied=True
            
            if occupied == False:
                rowString += '+'
            
            if x < world.x_space-1:
                rowString += '-'
            
        print('{}'.format(rowString))
        
# Returns a copy of (1) the list of Player objects and (2) the list of Monster objects
def copyAgents(world):
    monstersCopy = []
    playersCopy = []
    for monster in world.monsters:
        monstersCopy.append(monster)
    
    for player in world.players:
        playersCopy.append(player)
        
    return playersCopy, monstersCopy
main()
