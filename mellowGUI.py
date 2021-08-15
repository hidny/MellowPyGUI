import sys
import time

import random
import pygame
from threading import Thread
import threading

from pygame.locals import *

import projectile
import mellowClient
import box
import clientContext

import math

# This is designed to be a singleton object


FIRST_ROUND = -999


class MellowGUI:
    pygame.init()

    gameOver = 0

    screen_width = 1300
    screen_height = 900

    size = width, height = screen_width, screen_height

    screen = pygame.display.set_mode(size)

    backgroundLayer = pygame.Surface(size)
    refreshRegions = []
    refreshScore = 0
    removeBidButtons = 0

    off_the_edgeX = 150
    off_the_edgeY = 150

    card_width = 79
    card_height = 123

    THROW_TIME = 200
    FRAME_WAIT_TIME = 40

    WHITE = (255, 255, 255)

    # Images:
    background_image_filename = 'Image/wood3.png'
    background = pygame.image.load(background_image_filename)

    cardz_image_file = 'Image/cardz.png'
    cardz = pygame.image.load(cardz_image_file)
    cardz_horizontal = pygame.transform.rotate(cardz, 270)

    backcard_image_file = 'Image/back.jpg'
    backcard = pygame.image.load(backcard_image_file)
    backcard_horizontal = pygame.transform.rotate(backcard, 270)

    dot_image_file = 'Image/dot.png'
    dot = pygame.image.load(dot_image_file).convert()

    red_dot_image_file = 'Image/reddot.png'
    reddot = pygame.image.load(red_dot_image_file).convert()

    green_dot_image_file = 'Image/greendot.png'
    greendot = pygame.image.load(green_dot_image_file).convert()
    

    def __init__(self):
        self.bidButtons = []

        self.bidButtons.append(box.Box(self.width / 2 - 180, self.height / 2 - 90, 110, 50))
        self.bidButtons.append(box.Box(self.width / 2 - 60, self.height / 2 - 90, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 - 0, self.height / 2 - 90, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 + 60, self.height / 2 - 90, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 + 120, self.height / 2 - 90, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 - 180, self.height / 2 - 30, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 - 120, self.height / 2 - 30, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 - 60, self.height / 2 - 30, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 - 0, self.height / 2 - 30, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 + 60, self.height / 2 - 30, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 + 120, self.height / 2 - 30, 50, 50))
        self.bidButtons.append(box.Box(self.width / 2 - 180, self.height / 2 + 30, 110, 50))
        self.bidButtons.append(box.Box(self.width / 2 - 60, self.height / 2 + 30, 110, 50))
        self.bidButtons.append(box.Box(self.width / 2 + 60, self.height / 2 + 30, 110, 50))

        self.southCardLock = threading.Lock()
        self.westCardLock = threading.Lock()
        self.northCardLock = threading.Lock()
        self.eastCardLock = threading.Lock()

        self.scoreLock = threading.Lock()

        self.tricks = 4 * [0]

        # Variable to handle the animation of thrown cards:
        self.projectiles = []

        self.southCards = 13 * [-1]
        self.westCards = 13 * [0]
        self.northCards = 13 * [0]
        self.eastCards = 13 * [0]

        self.currentMsg = ''

        self.cardUserWantsToPlay = ''
        self.yellowDotIndex = -1

        self.isAwaitingBid = 0
        self.currentBid = -1

        # Dealers:
        self.dealer = ''

        # if this is 1, the back is blue.
        # if this is 0, the back is red.
        # (I feel like this is a good way to troll people)
        self.backIsBlue = 0

        self.prevScoreForUs = 0
        self.prevScoreForThem = 0
        self.diffScoreUs = FIRST_ROUND
        self.diffScoreThem = FIRST_ROUND
        self.scoreForUs = 0
        self.scoreForThem = 0

        self.southBid = -1
        self.westBid = -1
        self.northBid = -1
        self.eastBid = -1

    def isStillRunning(self):
        if self.gameOver == 0:
            return 1
        else:
            print('GAME OVER according to isStillRunning(self)')
            return 0

    # Functions called by some controller file:
    def setupCardsForNewRound(self, southCardsInput):
        tempArray = []

        for index in range(0, len(southCardsInput)):
            tempArray.append(convertCardStringToNum(southCardsInput[index]))

        tempArray = sortCards(tempArray)

        # if the south cards haven't been set yet, setup the 4 players cards and reset the bids:
        if len(self.southCards) < 13 or self.southCards[0] == -1:
            self.southBid = -1
            self.westBid = -1
            self.northBid = -1
            self.eastBid = -1

            with self.southCardLock:
                with self.eastCardLock:
                    with self.westCardLock:
                        with self.northCardLock:
                            self.southCards = tempArray
                            self.westCards = 13 * [-1]
                            self.northCards = 13 * [-1]
                            self.eastCards = 13 * [-1]

                            self.tricks = 4 * [0]

    def setDealer(self, name):
        self.dealer = name

    def bidSouth(self, bid):
        # with self.bidLock:
        self.southBid = bid

    def bidWest(self, bid):
        # with self.bidLock:
        self.westBid = bid

    def bidNorth(self, bid):
        # with self.bidLock:
        self.northBid = bid

    def bidEast(self, bid):
        # with self.bidLock:
        self.eastBid = bid

    def addTrickSouth(self):
        self.tricks[0] = self.tricks[0] + 1

    def addTrickWest(self):
        self.tricks[1] = self.tricks[1] + 1

    def addTrickNorth(self):
        self.tricks[2] = self.tricks[2] + 1

    def addTrickEast(self):
        self.tricks[3] = self.tricks[3] + 1

    # 0: south, 1: west, 2: north, 3: east
    def throwSouthCard(self, cardString):
        with self.southCardLock:
            cardNum = convertCardStringToNum(cardString)
            indexCard = -1
            for x in range(0, len(self.southCards)):
                if self.southCards[x] == cardNum:
                    indexCard = x
                    break

            if indexCard == -1:
                print('AHHH!!!! IndexCard is -1 on throw card.')
                sys.exit(1)

            self.projectiles[0] = self.createSouthCardProjectile(self.southCards, indexCard)

    def throwWestCard(self, cardString):
        with self.westCardLock:
            cardNum = convertCardStringToNum(cardString)
            self.projectiles[1] = self.createWestCardProjectile(self.westCards, cardNum)

    def throwNorthCard(self, cardString):
        with self.northCardLock:
            cardNum = convertCardStringToNum(cardString)
            self.projectiles[2] = self.createNorthCardProjectile(self.northCards, cardNum)

    def throwEastCard(self, cardString):
        with self.eastCardLock:
            cardNum = convertCardStringToNum(cardString)
            self.projectiles[3] = self.createEastCardProjectile(self.eastCards, cardNum)

    ##START creating projectile functions.
    def createSouthCardProjectile(self, southCards, cardHeldIndex):
        if len(southCards) > 0:
            southStartX = self.getCardLocation(cardHeldIndex)
            southStartY = self.screen_height - self.off_the_edgeY - self.card_height / 4
            southEndX = self.screen_width / 2
            southEndY = self.screen_height / 2 + self.card_width + self.card_height / 4

            southprojectileId = southCards[cardHeldIndex]

            southCards.pop(cardHeldIndex)

            # params: (self, beingThrown, startX, startY, endX, endY, projectileId, rotation)
            return projectile.Projectile(1, southStartX, southStartY, southEndX, southEndY, southprojectileId, 0)
        else:
            return projectile.Projectile(0, 0, 0, 0, 0, 0, 0)

    def getCardEastWestPlayerYLocation(self, eastWestcards, indexCard):
        firstY = self.screen_height / 2
        if len(eastWestcards) % 2 == 0:
            firstY = firstY + self.card_width / 4

        firstY = firstY - int(len(eastWestcards) / 2) * (self.card_width / 2)

        ret = firstY + indexCard * (self.card_width / 2)
        return ret

    def createWestCardProjectile(self, westCards, cardNum):
        if len(westCards) > 0:
            indexThrow = random.randint(0, len(westCards) - 1)

            westStartX = self.off_the_edgeX
            westStartY = self.getCardEastWestPlayerYLocation(westCards, indexThrow)

            westEndX = self.screen_width / 2 - self.card_width - self.card_height / 4
            westEndY = self.screen_height / 2

            westCards.pop(indexThrow)

            return projectile.Projectile(1, westStartX, westStartY, westEndX, westEndY, cardNum, 1)
        else:
            return projectile.Projectile(0, 0, 0, 0, 0, 0, 0)

    def createNorthCardProjectile(self, northCards, cardNum):
        if len(northCards) > 0:
            indexThrow = random.randint(0, len(northCards) - 1)

            northStartX = self.getCardLocation(indexThrow)
            northStartY = self.off_the_edgeY + self.card_height / 2
            northEndX = self.screen_width / 2
            northEndY = self.screen_height / 2 - self.card_width - self.card_height / 4

            northCards.pop(indexThrow)

            return projectile.Projectile(1, northStartX, northStartY, northEndX, northEndY, cardNum, 0)
        else:
            return projectile.Projectile(0, 0, 0, 0, 0, 0, 0)

    def createEastCardProjectile(self, eastCards, cardNum):
        if len(eastCards) > 0:
            indexThrow = random.randint(0, len(eastCards) - 1)

            eastStartX = self.screen_width - self.off_the_edgeX
            eastStartY = self.getCardEastWestPlayerYLocation(eastCards, indexThrow)

            eastEndX = self.screen_width / 2 + self.card_width + self.card_height / 4
            eastEndY = self.screen_height / 2

            eastCards.pop(indexThrow)

            return projectile.Projectile(1, eastStartX, eastStartY, eastEndX, eastEndY, cardNum, 1)
        else:
            return projectile.Projectile(0, 0, 0, 0, 0, 0, 0)

    ##END creating projectile functions.

    def printThrownCards(self):
        for x in range(0, 4):
            self.projectiles[x].printThrownCard(self)

    # post: removes the 0-4 cards played/thrown from the game.
    def remove_Projectiles(self):
        if len(self.projectiles) >= 4:
            for x in range(0, 4):
                self.projectiles[x].endThrow(self)

    def isNewFightStarting(self):
        temp = 0
        with self.southCardLock:
            with self.westCardLock:
                with self.northCardLock:
                    with self.eastCardLock:
                        temp = len(self.southCards)
                        if temp == len(self.westCards) and temp == len(self.northCards) and temp == len(self.eastCards):
                            return 1
                        else:
                            return 0

    def updateScore(self, us, them):
        self.refreshScore = 1

        with self.scoreLock:
            self.prevScoreForUs = self.scoreForUs
            self.prevScoreForThem = self.scoreForThem

            self.diffScoreUs = us - self.prevScoreForUs
            self.diffScoreThem = them - self.prevScoreForThem

            self.scoreForUs = us
            self.scoreForThem = them

    # END CONTROL FUNCTIONS
    def printScore(self):

        pygame.draw.rect(self.backgroundLayer, (255, 255, 255, 0), ((1 * self.width) / 32, (4 * self.height) / 5 + 10, 300, 200))
        # Make summation lines:
        pygame.draw.rect(self.backgroundLayer, (0, 0, 255, 0),
                         ((1 * self.width) / 32, (4 * self.height) / 5 + 10 + 3 * 40, 60, 5))
        pygame.draw.rect(self.backgroundLayer, (0, 0, 255, 0),
                         ((1 * self.width) / 32 + 70, (4 * self.height) / 5 + 10 + 3 * 40, 60, 5))

        with self.scoreLock:
            myfont = pygame.font.SysFont("comicsansms", 30)

            labelExample1 = myfont.render("US       THEM", 1, (0, 0, 255))

            labelExample2 = myfont.render(str(self.prevScoreForUs) + "    " + str(self.prevScoreForThem), 1,
                                          (0, 0, 255))

            labelExample3 = myfont.render(" " + str(self.diffScoreUs) + "     " + str(self.diffScoreThem), 1,
                                          (0, 0, 255))

            labelExample4 = myfont.render(
                str(self.scoreForUs) + "    " + str(self.scoreForThem) + "  (" + self.dealer + ")", 1, (0, 0, 255))

            self.backgroundLayer.blit(labelExample1, ((1 * self.width) / 32, (4 * self.height) / 5 + 10))

            if self.diffScoreThem == FIRST_ROUND:
                # If it's the first round and don't put the previous scores up...
                pass
            else:
                self.backgroundLayer.blit(labelExample2, ((1 * self.width) / 32, (4 * self.height) / 5 + 10 + 1 * 40))
                self.backgroundLayer.blit(labelExample3, ((1 * self.width) / 32, (4 * self.height) / 5 + 10 + 2 * 40))
            self.backgroundLayer.blit(labelExample4, ((1 * self.width) / 32, (4 * self.height) / 5 + 10 + 3 * 40))

    TRICK_DISPLAY_SIZE = 60
    def printTricks(self):
        myfont = pygame.font.SysFont("comicsansms", 30)

        labelTricksSouth = myfont.render(str(self.tricks[0]) + "/" + str(self.southBid), 1, (0, 0, 255))
        labelTricksWest = myfont.render(str(self.tricks[1]) + "/" + str(self.westBid), 1, (0, 0, 255))
        labelTricksNorth = myfont.render(str(self.tricks[2]) + "/" + str(self.northBid), 1, (0, 0, 255))
        labelTricksEast = myfont.render(str(self.tricks[3]) + "/" + str(self.eastBid), 1, (0, 0, 255))

        #TODO: make 30 a constant...
        if int(self.westBid) >= 0:
            self.refreshRegions.append((5, self.height / 2, self.TRICK_DISPLAY_SIZE, self.TRICK_DISPLAY_SIZE))
            self.screen.blit(labelTricksWest, (5, self.height / 2))

        if int(self.eastBid) >= 0:
            self.refreshRegions.append((1 * self.width - 85, self.height / 2, self.TRICK_DISPLAY_SIZE, self.TRICK_DISPLAY_SIZE))
            self.screen.blit(labelTricksEast, (1 * self.width - 85, self.height / 2))

        if int(self.northBid) >= 0:
            self.refreshRegions.append((self.width / 2, self.height / 20, self.TRICK_DISPLAY_SIZE, self.TRICK_DISPLAY_SIZE))
            self.screen.blit(labelTricksNorth, (self.width / 2, self.height / 20))

        if int(self.southBid) >= 0:
            self.refreshRegions.append((self.width / 2, self.height - 90, self.TRICK_DISPLAY_SIZE, self.TRICK_DISPLAY_SIZE))
            self.screen.blit(labelTricksSouth, (self.width / 2, self.height - 90))

    def printcard(self, x, y, num, rotate90):
        if num >= 52:
            print('ERROR: card num is greater than 52!')
            num = 0
            sys.exit(1)

        if rotate90 == 0:

            self.refreshRegions.append((x, y, self.card_width, self.card_height))

            if num < 0:
                self.screen.blit(self.backcard, (x, y),
                                 (self.backIsBlue * self.card_width, 0, self.card_width, self.card_height))
            else:
                self.screen.blit(self.cardz, (x, y), (
                    (num % 13) * self.card_width, math.floor(num / 13) * self.card_height, self.card_width,
                    self.card_height))
        else:

            self.refreshRegions.append((x, y, self.card_height, self.card_width))

            if num < 0:
                self.screen.blit(self.backcard_horizontal, (x, y),
                                 (0, self.backIsBlue * self.card_width, self.card_height, self.card_width))
            else:
                self.screen.blit(self.cardz_horizontal, (x, y),
                                 (
                    ((4 - 1) - math.floor(num / 13)) * self.card_height,
                    (num % 13) * self.card_width,
                    self.card_height,
                    self.card_width)
                                 )

    # Implements If you want to use projectiles, this function must be there.
    def printProjectile(self, x, y, idNum, rotation):
        self.printcardFromCenter(x, y, idNum, rotation)

    def printcardFromCenter(self, centerX, centerY, num, rotate90):
        if rotate90 == 0:
            self.printcard(int(centerX - self.card_width / 2), int(centerY - self.card_height / 2), num, rotate90)
        else:
            self.printcard(int(centerX - self.card_height / 2), int(centerY - self.card_width / 2), num, rotate90)

    def getXCordFirstCardNorthSouth(self, cardList):
        if cardList != None:
            firstX = self.screen_width / 2
            if len(cardList) % 2 == 0:
                firstX = firstX + self.card_width / 4

            firstX = firstX - int(len(cardList) / 2) * (self.card_width / 2)

            return firstX
        else:
            return 0

    def isMouseHoveringOverCard(self, mx, my):
        firstX = self.getXCordFirstCardNorthSouth(self.southCards)

        if my > self.screen_height - self.off_the_edgeY - self.card_height / 2:
            if my < self.screen_height - self.off_the_edgeY + self.card_height / 2:
                firstX = self.getXCordFirstCardNorthSouth(self.southCards)
                if mx > firstX - self.card_width / 2:
                    if mx < firstX + len(self.southCards) * self.card_width / 2:
                        return 1
        return 0

    def printCardSuitNum(self, x, y, suit, num):
        self.printcard(x, y, 13 * suit + num, 1)

    def fill_background(self):
        #for y in range(0, self.screen_height, self.background.get_height()):
        #    for x in range(0, self.screen_width, self.background.get_width()):
        #        self.screen.blit(self.background, (x, y))
        self.backgroundLayer.blit(self.background, (0, 0))

    def printSouthCards(self, mx, my):
        currentX = self.getXCordFirstCardNorthSouth(self.southCards)

        indexOfMouseOnCard = self.getIndexCardHover(mx, my)
        mouseHoveringOverCard = self.isMouseHoveringOverCard(mx, my)

        with self.southCardLock:
            for index in range(0, len(self.southCards)):

                if mouseHoveringOverCard == 1 and indexOfMouseOnCard == index:
                    self.printcardFromCenter(currentX, self.screen_height - self.off_the_edgeY - self.card_height / 4,
                                             self.southCards[index], 0)
                else:
                    self.printcardFromCenter(currentX, self.screen_height - self.off_the_edgeY, self.southCards[index],
                                             0)
                
                if index == self.yellowDotIndex:
                    #yellow = FFFF00
                    pygame.draw.circle(self.screen, (255, 255, 100), (int(currentX - self.card_width/4), self.screen_height - self.off_the_edgeY), 20)
                    print('Yellow circle at index ' + str(index))
                
                currentX = currentX + (self.card_width / 2)

    def printWestCards(self):
        firstY = self.screen_height / 2
        if len(self.westCards) % 2 == 0:
            firstY = firstY + self.card_width / 4

        firstY = firstY - int(len(self.westCards) / 2) * (self.card_width / 2)
        currentY = firstY

        for x in range(0, len(self.westCards)):
            self.printcardFromCenter(self.off_the_edgeX, currentY, -1, 1)
            currentY = currentY + (self.card_width / 2)

    def printNorthCards(self):

        firstX = self.getXCordFirstCardNorthSouth(self.northCards)
        currentX = firstX

        for x in range(0, len(self.northCards)):
            self.printcardFromCenter(currentX, self.off_the_edgeY, -1, 0)
            currentX = currentX + (self.card_width / 2)

    def printEastCards(self):
        firstY = self.screen_height / 2
        if len(self.eastCards) % 2 == 0:
            firstY = firstY + self.card_width / 4

        firstY = firstY - int(len(self.eastCards) / 2) * (self.card_width / 2)
        currentY = firstY

        for x in range(0, len(self.eastCards)):
            self.printcardFromCenter(self.screen_width - self.off_the_edgeX, currentY, -1, 1)
            currentY = currentY + (self.card_width / 2)

    NOINDEX = -2

    def getIndexCardHover(self, mx, my):
        if my > self.screen_height - self.off_the_edgeY - self.card_height / 2:
            if my < self.screen_height - self.off_the_edgeY + self.card_height / 2:
                firstX = self.getXCordFirstCardNorthSouth(self.southCards)
                currentX = firstX
                for x in range(0, len(self.southCards)):
                    if mx < currentX - self.card_width / 2:
                        return x - 1

                    currentX = currentX + (self.card_width / 2)
                return len(self.southCards) - 1

        return self.NOINDEX

    # rearranges cards in the current players hand.
    def shiftSouthCards(self, origIndex, isLeft, numSpaces):
        # test some preconditions just in case
        if origIndex < len(self.southCards) and origIndex >= 0:
            if (origIndex + numSpaces < len(self.southCards) and isLeft == 0) or (
                    origIndex - numSpaces >= 0 and isLeft == 1):
                temp = self.southCards[origIndex]
                if isLeft == 1:
                    for x in range(0, numSpaces):
                        self.southCards[origIndex - x] = self.southCards[origIndex - x - 1]
                    self.southCards[origIndex - numSpaces] = temp
                else:
                    for x in range(0, numSpaces):
                        self.southCards[origIndex + x] = self.southCards[origIndex + x + 1]
                    self.southCards[origIndex + numSpaces] = temp

        return self.southCards

    def getCardLocation(self, cardHeldIndex):
        currentX = self.getXCordFirstCardNorthSouth(self.southCards)
        return currentX + cardHeldIndex * (self.card_width / 2)

    def setCardUserWantsToPlay(self, cardString):
        self.cardUserWantsToPlay = cardString

    def setCardUserWantsToPlayToNull(self):
        self.cardUserWantsToPlay = ''
        self.yellowDotIndex = -1

    def getCardUserWantsToPlay(self):
        return self.cardUserWantsToPlay

    def reorgSouthCards(self, mx, my, mouseJustPressed, mouseHeld, mouseJustRelease, cardHeldIndex, mPressX, mPressY):
        with self.southCardLock:
            indexOfMouseOnCard = self.getIndexCardHover(mx, my)

            mouseHoveringOverCard = self.isMouseHoveringOverCard(mx, my)

            if mouseJustPressed == 1:

                if mouseHoveringOverCard == 1:
                    cardHeldIndex = indexOfMouseOnCard

            if mouseJustRelease == 1:
                if self.isWaitingForBid() == 1:
                    self.checkIfUserBidAfterClick(mx, my)

                #After the user clicks, the card selection should go away:
                self.setCardUserWantsToPlayToNull()

                #Rough guess at the intentions of the player...
                #If player release card over edge or make a line with slope pointing up more than sideways, assume they want to play a card:
                if my < self.screen_height - self.off_the_edgeY - self.card_height / 2 \
                    or (my < mPressY and (mx == mPressX or abs((my - mPressY)/(mx - mPressX)) > 1)):

                    if cardHeldIndex >= 0:
                        if 0 <= cardHeldIndex < len(self.southCards):
                            # print('Trying to play: ' + str(convertCardNumToString(self.southCards[cardHeldIndex]))
                            self.setCardUserWantsToPlay(convertCardNumToString(self.southCards[cardHeldIndex]))
                            self.yellowDotIndex=cardHeldIndex
                            cardHeldIndex = self.NOINDEX
                            print('Yellow dot index: ' + str(self.yellowDotIndex))

            if mouseHeld == 1:
                if mouseHoveringOverCard == 1:
                    if cardHeldIndex > indexOfMouseOnCard:
                        shiftAmount = cardHeldIndex - indexOfMouseOnCard
                        self.southCards = self.shiftSouthCards(cardHeldIndex, 1, shiftAmount)
                        cardHeldIndex = indexOfMouseOnCard

                    elif cardHeldIndex < indexOfMouseOnCard:
                        shiftAmount = indexOfMouseOnCard - cardHeldIndex
                        self.southCards = self.shiftSouthCards(cardHeldIndex, 0, shiftAmount)
                        cardHeldIndex = indexOfMouseOnCard

            return cardHeldIndex

    def setMessage(self, message):
        self.currentMsg = message

    def displayCenterGameMsg(self):
        myfont = pygame.font.SysFont("comicsansms", 30)
        xOffset = len(self.currentMsg)
        labelExample = myfont.render(str(self.currentMsg), 1, (0, 0, 255))
        self.screen.blit(labelExample, (self.width / 2 - 10 * xOffset, self.height / 2 - 50))

    def displayBidChoices(self):

        pygame.draw.rect(self.screen, (255, 0, 255, 0), (self.width / 2 - 200, self.height / 2 - 100, 400, 200))

        myFont = pygame.font.SysFont("Bauhaus 93", 30)

        for i in range(0, len(self.bidButtons)):
            pygame.draw.rect(self.screen, (0, 0, 0, 0), self.bidButtons[i].getCoordBox())
            if i == 0:
                labelExample = myFont.render("Mellow", 1, (0, 255, 0))
            else:
                labelExample = myFont.render(str(i), 1, (0, 255, 0))

            self.screen.blit(labelExample, self.bidButtons[i].getTopLeftBox())

    def askUserForBid(self):
        self.isAwaitingBid = 1

    def isWaitingForBid(self):
        return self.isAwaitingBid

    def checkIfUserBidAfterClick(self, x, y):
        for i in range(0, len(self.bidButtons)):
            if self.bidButtons[i].isWithinBox(x, y):
                print('Clicked on ' + str(i))
                self.currentBid = i
        return -1

    # returns the bid if the user bid. Returns -1 otherwise.
    def consumeBid(self):
        if self.currentBid >= 0:
            self.isAwaitingBid = 0
            self.removeBidButtons = 1

        temp = self.currentBid
        self.currentBid = -1
        return temp


def convertCardNumToString(num):
    if num < 0:
        return '??'

    suit = ''
    if num >= 0 and num < 13:
        suit = 'C'
    elif num >= 13 and num < 26:
        suit = 'D'
    elif num >= 26 and num < 39:
        suit = 'H'
    elif num >= 39 and num < 52:
        suit = 'S'
    else:
        print('ERROR: Trying to convert card with num ' + str(num) + ' in convertCardNumToString(num)')
        sys.exit(1)

    CardNumber = -1
    if num % 13 == 0:
        CardNumber = 'A'
    elif num % 13 == 9:
        CardNumber = 'T'
    elif num % 13 == 10:
        CardNumber = 'J'
    elif num % 13 == 11:
        CardNumber = 'Q'
    elif num % 13 == 12:
        CardNumber = 'K'
    else:
        CardNumber = str((num % 13) + 1)

    return str(CardNumber) + suit


# FUNCTIONS THAT OUTSIDE CLASSES SHOULD USE:
def convertCardStringToNum(card):
    row = 0
    if card[1:].find('C') != -1:
        row = 0
    elif card[1:].find('D') != -1:
        row = 1
    elif card[1:].find('H') != -1:
        row = 2
    elif card[1:].find('S') != -1:
        row = 3
    else:
        print(card)
        print(str(len(card)))
        print('ERROR: unknown suit!')
        sys.exit(1)

    if card[:1].find('A') != -1:
        column = 0
    elif card[:1].find('T') != -1:
        column = 9
    elif card[:1].find('J') != -1:
        column = 10
    elif card[:1].find('Q') != -1:
        column = 11
    elif card[:1].find('K') != -1:
        column = 12
    else:
        column = int(card[0]) - 1

    return 13 * row + column


def sortCards(tempArray):
    # Ace values should increase so they can be properly sorted.
    for x in range(0, len(tempArray)):
        if tempArray[x] % 13 == 0:
            tempArray[x] = tempArray[x] + 13

    tempArray.sort()

    # put the ace values back to the way they were
    for x in range(0, len(tempArray)):
        if tempArray[x] % 13 == 0:
            tempArray[x] = tempArray[x] - 13

    return tempArray


def main(connection):
    mellowGUI = MellowGUI()

    print('Inside Mellow GUI main!')

    try:
        t = Thread(name='Testing', target=mellowClient.main, args=(mellowGUI, ['MellowGUI.py', connection]))
        t.start()
    except:
        print("Error: unable to start thread")

    for x in range(0, 4):  # mellowGUI.projectiles.
        temp = projectile.Projectile(0, 0, 0, 0, 0, 0, 0)
        mellowGUI.projectiles.append(temp)

    # texting adding
    myfont = pygame.font.SysFont("comicsansms", 30)

    clock = pygame.time.Clock()

    mellowLogo = pygame.image.load("MellowLogo.png").convert()
    transColor = mellowLogo.get_at((0, 0))
    mellowLogo.set_colorkey(transColor)

    versNumber = pygame.image.load("versNumber.png").convert()
    transColor = versNumber.get_at((0, 0))
    versNumber.set_colorkey(transColor)

    mouseJustPressed = 0
    mouseHeld = 0
    mouseJustRelease = 0
    cardHeldIndex = mellowGUI.NOINDEX

    mPressX = 0
    mPressY = 0

    pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    #print background:

    mellowGUI.fill_background()

    mellowGUI.backgroundLayer.blit(mellowLogo, (0, 0, 500, 500), (0, 0, 500, 500))
    mellowGUI.backgroundLayer.blit(versNumber, (20, 50, 500, 500), (0, 0, 500, 500))

    # No Chat box:
    #pygame.draw.rect(mellowGUI.backgroundLayer, mellowGUI.WHITE,
    #                 [(6 * mellowGUI.width) / 8, (4 * mellowGUI.height) / 5 + 10, 300, 200])

    mellowGUI.printScore()
    #end print background

    mellowGUI.screen.blit(mellowGUI.backgroundLayer, (0, 0, mellowGUI.width, mellowGUI.height), (0, 0, mellowGUI.width, mellowGUI.height))

    iter = 0

    while 1:

        iter = iter + 1

        # React to user events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mellowGUI.gameOver = 1
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseHeld = 1
                    mouseJustPressed = 1
                    mPressX, mPressY = pygame.mouse.get_pos()

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouseHeld = 0
                    mouseJustRelease = 1

        mx, my = pygame.mouse.get_pos()

        cardHeldIndex = mellowGUI.reorgSouthCards(mx, my, mouseJustPressed, mouseHeld, mouseJustRelease, cardHeldIndex, mPressX, mPressY)

        # END React to user events:

        # print Stuff:

        if mellowGUI.refreshScore == 1:
            #TODO: put refreshRegions dimensions in a constant:
            mellowGUI.refreshRegions.append(((1 * mellowGUI.width) / 32, (4 * mellowGUI.height) / 5 + 10, 300, 200))
            mellowGUI.printScore()
            mellowGUI.refreshScore = 0

        if mellowGUI.removeBidButtons == 1:
            #TODO: put refreshRegions dimensions in a constant:
            mellowGUI.refreshRegions.append((mellowGUI.width / 2 - 200, mellowGUI.height / 2 - 100, 400, 200))
            mellowGUI.removeBidButtons = 0

        #TODO: fill in refresh regions:
        for region in mellowGUI.refreshRegions:
            mellowGUI.screen.blit(mellowGUI.backgroundLayer, (region[0], region[1], region[2], region[3]),
                                                        (region[0], region[1], region[2], region[3]))
        mellowGUI.refreshRegions = []
        # END fill in background regions

        mellowGUI.printSouthCards(mx, my)
        mellowGUI.printWestCards()
        mellowGUI.printNorthCards()
        mellowGUI.printEastCards()

        mellowGUI.printThrownCards()

        mellowGUI.printTricks()

        mellowGUI.displayCenterGameMsg()

        # print colour of cursor depending on what user does:
        if mouseJustPressed == 1 or mouseJustRelease == 1:
            mellowGUI.screen.blit(mellowGUI.greendot, (mx - 5, my - 5), (0, 0, 10, 10))
        elif mouseHeld == 1:
            mellowGUI.screen.blit(mellowGUI.reddot, (mx - 5, my - 5), (0, 0, 10, 10))
        else:
            mellowGUI.screen.blit(mellowGUI.dot, (mx - 5, my - 5), (0, 0, 10, 10))
        # end print colour of cursor.

        mellowGUI.refreshRegions.append((mx - 5, my - 5, 10, 10))

        if mellowGUI.isWaitingForBid() == 1:
            mellowGUI.displayBidChoices()

        mouseJustPressed = 0
        mouseJustRelease = 0

        pygame.display.update()
        # End print stuff.

        # Update to next frame:
        clock.tick_busy_loop(1000 / mellowGUI.FRAME_WAIT_TIME)



if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        name = args[1]
    else:
        name = 'Michael'

    # default ip and port:
    tcpIP = '127.0.0.1'
    tcpPort = 6789

    isHostingGame = 0
    interact = 0
    slowdown = 0

    # parse arguments:
    for x in range(0, len(args)):
        print(str(args[x]))
        if args[x].find('host') != -1:
            isHostingGame = 1
        elif args[x].find('meatbag') != -1 or args[x].find('interact') != -1:
            interact = 1
        elif args[x].find('slow') != -1:
            slowdown = 1
        elif args[x].find('ip=') != -1:
            tcpIP = str(args[x][len('ip='):])
        elif args[x].find('p=') != -1:
            tcpPort = int(args[x][len('p='):])

    print('IP: ' + str(tcpIP))
    print('PORT: ' + str(tcpPort))
    print('name: ' + str(name))

    conn = clientContext.ClientContext(tcpIP, tcpPort, name)

    if isHostingGame == 1:
        conn.setHost()
    else:
        conn.setJoiner()

    conn.setInteract(interact)
    conn.setSlowdown(slowdown)
    main(conn)

# cd C:\Users\Michael\Desktop\cardGamePython\MellowPyGUI

# cd desktop\cardGamePython\pythoninternet
# For autogame:
# python mellowGUI.py Michael host > output1.txt
# python mellowGUI.py Phil
# python mellowGUI.py Richard
# python mellowGUI.py Doris

# For game played by user:
# python mellowGUI.py Michael host slow interact > output1.txt
# python mellowGUI.py Phil slow
# python mellowGUI.py Richard slow
# python mellowGUI.py Doris slow


# python mellowGUI.py Michael host slow interact p=6789 ip=127.0.0.1
