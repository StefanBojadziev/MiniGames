# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys, time
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
BLUE      = (135, 203, 243) #Барање 1: боја на вториот црв
DARKBLUE  = (  0,   0, 255) #Барање 1: боја на вториот црв
LIGHTPURPLE = (224, 176, 255) #Барање 2: боја на нов објект
DARKPURPLE = (145, 95, 109) #Барање 2: боја на нов објект
YELLOW    = (255, 255,   0) #Барање 2: боја на нов објект
ORANGE    = (248, 157,   12) #Барање 2: боја на нов објект
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head
score= 0


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, score

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    global secondWormDirection, score
    start = time.time()
    # Set a random start point.
    startX = random.randint(5, CELLWIDTH - 6)
    startY = random.randint(5, CELLHEIGHT - 6)
    #Барање 1
    startSecondX = random.randint(5, CELLWIDTH - 6)
    startSecondY = random.randint(5, CELLHEIGHT - 6)

    wormCoords = [{'x': startX,     'y': startY},
                  {'x': startX - 1, 'y': startY},
                  {'x': startX - 2, 'y': startY}]
    direction = random.choice([UP, DOWN, RIGHT, LEFT])

    #Барање 1
    secondWormCoords = [{'x': startSecondX, 'y': startSecondY},
                  {'x': startSecondX - 1, 'y': startSecondY},
                  {'x': startSecondX - 2, 'y': startSecondY}]
    secondWormDirection = random.choice([UP, DOWN, RIGHT, LEFT])

    # Start the apple in a random place.
    apple = getRandomLocation()
    #Барање 2
    yellowLemon = getRandomLocation()
    purpleGrape = getRandomLocation()
    extraPoints = 0 #нова променлива за броење на екстра поени

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        #Барање 1
        #Сите можности за правец се валидни освен спротивниот, затоа што не може црвот да се сврти 180 степени
        if secondWormDirection == RIGHT:
            secondWormDirection = random.choice([UP, DOWN, RIGHT])
        elif secondWormDirection == LEFT:
            secondWormDirection = random.choice([UP, DOWN, LEFT])
        elif secondWormDirection == DOWN:
            secondWormDirection = random.choice([LEFT, RIGHT, DOWN])
        elif secondWormDirection == UP:
            secondWormDirection = random.choice([RIGHT, UP, LEFT])

        if secondWormDirection == UP:
            newSecondHead = {'x': secondWormCoords[HEAD]['x'], 'y': secondWormCoords[HEAD]['y'] - 1}
        elif secondWormDirection == DOWN:
            newSecondHead = {'x': secondWormCoords[HEAD]['x'], 'y': secondWormCoords[HEAD]['y'] + 1}
        elif secondWormDirection == LEFT:
            newSecondHead = {'x': secondWormCoords[HEAD]['x'] - 1, 'y': secondWormCoords[HEAD]['y']}
        elif secondWormDirection == RIGHT:
            newSecondHead = {'x': secondWormCoords[HEAD]['x'] + 1, 'y': secondWormCoords[HEAD]['y']}

        #Барање 1
        if ((time.time() - start) > 20):
            if secondWormCoords[HEAD]['x'] == wormCoords[HEAD]['x'] and secondWormCoords[HEAD]['y'] == wormCoords[HEAD]['y']:
                pass
            else:
                del secondWormCoords[-1]

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        elif secondWormCoords[HEAD]['x'] == wormCoords[HEAD]['x'] and secondWormCoords[HEAD]['y'] == wormCoords[HEAD]['y'] and ((time.time() - start) > 20):
            pass
        else:
            del wormCoords[-1] # remove worm's tail segment

        #Барање 1
        if wormCoords[HEAD]['x'] == purpleGrape['x'] and wormCoords[HEAD]['y'] == purpleGrape['y']:
            purpleGrape = {'x': -1, 'y': -1} #Го поместуваме објектот надвор од полето за игра
            extraPoints += 3 #Додаваме по 3 поени
        if wormCoords[HEAD]['x'] == yellowLemon['x'] and wormCoords[HEAD]['y'] == yellowLemon['y']:
            yellowLemon = {'x': -1, 'y': -1} #Го поместуваме објектот надвор од полето за игра
            extraPoints += 3 #Додаваме по 3 поени

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        #Барање 2
        baseLength = len(wormCoords)-3
        score = baseLength + extraPoints
        drawScore(score)
        #Барање 1
        if time.time() - start > 20:
            secondWormCoords.insert(0, newSecondHead)
            drawSecondWorm(secondWormCoords)
        #Барање 2
        if time.time() - start % 10 > 5:
            drawPurpleGrape(purpleGrape)
        #Барање 2
        if time.time() - start < 7:
            drawYellowLemon(yellowLemon)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    global score
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)

    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()

    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    #Барање 2
    scoreFont = pygame.font.Font('freesansbold.ttf', 20)
    scoreText = 'Score: ' + str(score)
    scoreSurf = scoreFont.render(scoreText, True, YELLOW)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (WINDOWWIDTH / 2, 500)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    #Барање 3
    buttonFont = pygame.font.Font('freesansbold.ttf', 35)
    startText = 'Start from the beggining'
    quitText = 'Quit'
    startSurf = buttonFont.render(startText, True, GREEN, DARKGRAY)
    quitSurf = buttonFont.render(quitText, True, GREEN, DARKGRAY)
    startRect = startSurf.get_rect()
    quitRect = quitSurf.get_rect()
    startRect.midtop = (WINDOWWIDTH / 2, 400)
    quitRect.midtop = (WINDOWWIDTH / 2, 450)
    DISPLAYSURF.blit(startSurf, startRect)
    DISPLAYSURF.blit(quitSurf, quitRect)

    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        #Барање 3
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if startRect.collidepoint(mouse_pos):
                    return
                if quitRect.collidepoint(mouse_pos):
                    terminate()

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

#Барање 1
def drawSecondWorm(secondWormCoords):
    for coord in secondWormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKBLUE, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, BLUE, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


#Барање 2
def drawYellowLemon(coord):
    color1 = YELLOW
    color2 = ORANGE
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    for i in range(3):
        color1, color2 = color2, color1
        lemonYellowRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, color1, lemonYellowRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPurpleGrape(coord):
    color1 = LIGHTPURPLE
    color2 = DARKPURPLE
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    for i in range(3):
        color1, color2 = color2, color1
        grapePurpleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, color1, grapePurpleRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()