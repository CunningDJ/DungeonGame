from msvcrt import getch, getwch
import time
from threading import Thread
import os
import random
from math import sqrt
from queue import Queue

players = []
monster = {}
squareDim =  60
y_space = squareDim
x_space = squareDim

wall = {'wallVersion' : False}

endProgram = object
killQ = Queue()

def main():        
    # Setting initial position of monster
    monster['x'],monster['y'] = (0,0)

    numPlayers = int(input('Number of players?: '))
    wallInput = input('Solid Wall (Y/N)? ').upper()
    print('Wall Version {}'.format(wallInput))
    if wallInput == 'Y':
        wall['wallVersion'] = True

    for player in range(numPlayers):
        #Setting initial player positions
        players.append({'x' : random.choice(range(int(x_space/4),int(3*x_space/4))), 'y' : random.choice(range(int(y_space/4),int(3*y_space/4))), 'alive' : True})

    #for player in players:     # TODO Test Print
        #print('Player {}: X {} | Y {}'.format(players.index(player),player['x'],player['y']))

    # For Python 3.3+:    
    #drawThread = Thread(target=draw, daemon=True)
    #monsterThread = Thread(target=monsterEngine, daemon=True)

    # For older Python versions:
    drawThread = Thread(target=draw)
    drawThread.setDaemon(True)
    
    monsterThread = Thread(target=monsterEngine)
    monsterThread.setDaemon(True)
    
    # Start the monster engine, draw engine, and player input engine
    drawThread.start()
    monsterThread.start()
    playerInput(drawThread)
    drawThread.join()
    
def playerInput(drawThread):

    
    while True:
        key = ord(getwch())
        if key == 27: #ESC
            killQ.put(endProgram)
            break
            
        if key == 224: # Special keys (arrows, f keys, ins, del, etc.)
            key = ord(getwch())
            if key == 80: #Down arrow
                players[0]['y'] -= 1
            elif key == 72: #Up arrow
                players[0]['y'] += 1
            elif key == 77: #right arrow
                players[0]['x'] += 1
            elif key == 75: #left arrow
                players[0]['x'] -= 1
        
        if len(players) >= 2:
            #P2 CONTROLS
            if key == 119: # W (p2 up)
                players[1]['y'] += 1
            elif key == 115: # S (p2 down)
                players[1]['y'] -= 1
            elif key == 100: # D (p2 right)
                players[1]['x'] += 1
            elif key == 97: # A (p2 left)
                players[1]['x'] -= 1
                
        if len(players) == 3:
            # P3 CONTROLS
            if key == 105: # I (p3 up)
                players[2]['y'] += 1
            elif key == 107: # K (p3 down)
                players[2]['y'] -= 1
            elif key == 108: # L (p3 right)
                players[2]['x'] += 1
            elif key == 106: # J (p3 left)
                players[2]['x'] -= 1
        
        
        

     
            
            
def monsterEngine():
    time.sleep(2)
    restCount = 0
    monsterSpeed = 2    # Initial Speed
    while True:
        # Rests between monster seeking & moving
        monsterRest = 1/float(monsterSpeed)
        # print('Monster Rest: {}'.format(monsterRest))        # TODO Print Check
        time.sleep(monsterRest)
        # Speeds up the monster every 20 rests
        restCount +=1
        if int(monsterRest * restCount) % 7 == 0:
            monsterSpeed = monsterSpeed * 1.05
        
        closestID = -1
        closestDistance = 1000000000
        playersCopy = getPlayersCopy()
        for player in playersCopy:
            if players[playersCopy.index(player)]['alive'] == True:
                distance = sqrt((monster['x'] - player['x'])**2 + (monster['y'] - player['y'])**2)
                if distance < closestDistance:
                    closestDistance = distance
                    closestID = playersCopy.index(player)
        
        #print('Closest Player: {} DISTANCE: {}'.format(closestID,distance))    # TODO Remove
        # Moving the monster toward the closest player
        if playersCopy[closestID]['x'] < monster['x']:
            monster['x'] -= 1
        elif playersCopy[closestID]['x'] > monster['x']:
            monster['x'] += 1
        if playersCopy[closestID]['y'] < monster['y']:
            monster['y'] -= 1
        elif playersCopy[closestID]['y'] > monster['y']:
            monster['y'] += 1
        
        
def getPlayersCopy():
    playersCopy = []
    for player in players:
        playersCopy.append(player)
    
    return playersCopy

def worldChecker(playersCopy, monsterCopy,currentTime):
    # Checks if the monster has eaten any players (same location)
    livingPlayers = 0
    for player in playersCopy:
        if player['alive'] == True:
            if player['x'] == monsterCopy['x'] and player['y'] == monsterCopy['y']:
                players[playersCopy.index(player)]['alive'] = False
            else:
                livingPlayers += 1
    
    if killQ.empty() != True:
        item = killQ.get()
        print('NOT EMPTY!')
        #exit()
        if item == endProgram:
            os.system('cls')    # for windows
            #os.system('clear') # for linux
            print('################\nGAME OVER!\nTime: {0:.1f}\n################\n'.format(currentTime))
            exit()
    
    # Ends the game if all of the players have been eaten
    if livingPlayers == 0:
        os.system('cls')    # for windows
        #os.system('clear') # for linux
        print('################\nGAME OVER!\nTime: {0:.1f}\n(Esc to Exit)\n################\n'.format(currentTime))
        exit()
    
    # Pulls the players back in the range of the map if they've gone outside of the borders
    
    for player in playersCopy:
        if player['x'] > x_space-1:
            if wall['wallVersion']:
                players[playersCopy.index(player)]['x'] = x_space-1 # WALL VERSION
            else:
                players[playersCopy.index(player)]['x'] = 0         # LOOP VERSION
        elif player['x'] < 0:
            if wall['wallVersion']:
                players[playersCopy.index(player)]['x'] = 0         # WALL VERSION
            else:
                players[playersCopy.index(player)]['x'] = x_space-1 # LOOP VERSION
        
        if player['y'] > y_space-1:
            if wall['wallVersion']:
                players[playersCopy.index(player)]['y'] = y_space-1 # WALL VERSION
            else:
                players[playersCopy.index(player)]['y'] = 0         # LOOP VERSION
        elif player['y'] < 0:
            if wall['wallVersion']:
                players[playersCopy.index(player)]['y'] = 0         # WALL VERSION
            else:
                players[playersCopy.index(player)]['y'] = y_space-1 # LOOP VERSION
    
    return
            
            
def draw():
    startTime = time.time()
    while True:
        playersCopy = getPlayersCopy()
        monsterCopy = monster
        os.system('cls')    # for windows
        #os.system('clear') # for linux
        #print('WALL: {}'.format(wall['wallVersion']))
        currentTime = time.time() - startTime
        print('Time: {0:.1f}'.format(currentTime))      # Prints the current game time
        for y in range(y_space)[y_space::-1]:
            rowString = ''
            for x in range(x_space):
                occupied = False
                if x == monster['x'] and y == monster['y']:
                    rowString += 'M'
                    occupied = True
                
                for player in playersCopy:
                    if player['alive'] == True and occupied == False:
                        if x == player['x'] and y == player['y']:
                            rowString += '{}'.format(playersCopy.index(player)+1)
                            occupied = True
                            continue
                if occupied == False:
                    rowString += '+'
                if x < x_space-1:
                    rowString += '-'
            
            print('{}'.format(rowString))

        worldChecker(playersCopy,monsterCopy,currentTime)


main()
