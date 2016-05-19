import sys, pygame
import time

import random, os
import pygame
from threading import Thread
import threading

#from pygame import _view
from pygame.locals import *
from sys import exit

import projectile
import starterTest
import euchreClient
import box
import clientContext

import button
import channelRoomGUI


#This is designed to be a singleton object

	
FIRST_ROUND = -999
	
class EuchreGUI:
	
	pygame.init()
	
	gameOver = 0
	
	screen_width = 1300
	screen_height = 900
	
	size = width, height = screen_width, screen_height
	
	screen = pygame.display.set_mode(size)
	
	off_the_edgeX = 150
	off_the_edgeY = 150

	card_width = 79
	card_height = 123


	THROW_TIME=100
	FRAME_WAIT_TIME = 40
	
	WHITE = (255, 255, 255)
	
	STARTING_HAND_LENGTH = 5

	#Images:
	background_image_filename = 'Image/wood3.png'
	background = pygame.image.load(background_image_filename)

	cardz_image_file = 'Image/cardz.png'
	cardz = pygame.image.load(cardz_image_file)

	backcard_image_file = 'Image/back.jpg'
	backcard = pygame.image.load(backcard_image_file)

	dot_image_file = 'Image/dot.png'
	dot = pygame.image.load(dot_image_file).convert()

	red_dot_image_file = 'Image/reddot.png'
	reddot = pygame.image.load(red_dot_image_file).convert()

	green_dot_image_file = 'Image/greendot.png'
	greendot = pygame.image.load(green_dot_image_file).convert()
	
	
	
	
	def __init__(self):
		self.bidButtonsRound1 = []
		self.bidButtonsRound2 = []
		
		self.BUTTON_NUM_ROWS_1 = 1
		self.BUTTON_NUM_ROWS_2 = 2
		self.BUTTON_HEIGHT_ROW = 100
		
		
		self.BUTTON_NUM_COLUMNS_1 = 3
		self.BUTTON_NUM_COLUMNS_2 = 5
		self.BUTTON_WIDTH_ROW = 160
		
		self.BUTTON_OFFSET = 10
		
		for y in range(0, self.BUTTON_NUM_ROWS_1):
			for x in range(0, self.BUTTON_NUM_COLUMNS_1):
				self.bidButtonsRound1.append(box.Box(self.width/2 - (self.BUTTON_WIDTH_ROW*self.BUTTON_NUM_COLUMNS_1)/2 + self.BUTTON_WIDTH_ROW*x + self.BUTTON_OFFSET, self.height/2 - (self.BUTTON_HEIGHT_ROW*self.BUTTON_NUM_ROWS_1)/2 + self.BUTTON_HEIGHT_ROW*y + self.BUTTON_OFFSET, self.BUTTON_WIDTH_ROW - 2*self.BUTTON_OFFSET, self.BUTTON_HEIGHT_ROW - 2*self.BUTTON_OFFSET))
		
		for y in range(0, self.BUTTON_NUM_ROWS_2):
			for x in range(0, self.BUTTON_NUM_COLUMNS_2):
				self.bidButtonsRound2.append(box.Box(self.width/2 - (self.BUTTON_WIDTH_ROW*self.BUTTON_NUM_COLUMNS_2)/2 + self.BUTTON_WIDTH_ROW*x + self.BUTTON_OFFSET, self.height/2 - (self.BUTTON_HEIGHT_ROW*self.BUTTON_NUM_ROWS_2)/2 + self.BUTTON_HEIGHT_ROW*y + self.BUTTON_OFFSET, self.BUTTON_WIDTH_ROW - 2*self.BUTTON_OFFSET, self.BUTTON_HEIGHT_ROW - 2*self.BUTTON_OFFSET))
		
		
		self.variation = 'bicycle'
		
		self.southCardLock = threading.Lock()
		self.westCardLock = threading.Lock()
		self.northCardLock = threading.Lock()
		self.eastCardLock = threading.Lock()

		self.scoreLock = threading.Lock()
		
		
		self.tricks = 4*[0]
		
		#Variable to handle the animation of thrown cards:
		self.projectiles = []
		
			
		self.southCards = self.STARTING_HAND_LENGTH * [-1]
		self.westCards = self.STARTING_HAND_LENGTH * [0]
		self.northCards= self.STARTING_HAND_LENGTH * [0]
		self.eastCards = self.STARTING_HAND_LENGTH * [0]
		
		
		self.currentMsg = ''
		
		self.cardUserWantsToPlay = ''
		
		
		self.lastFrameTime = int(round(time.time() * 1000))
		
		self.isAwaitingBid = 0
		self.currentBid = ''
		
		
		#Dealers:
		self.dealer = ''
		self.trumpCard = ''
		self.isTrumpCovered = 0

		#if this is 1, the back is blue.
		#if this is 0, the back is red.
		#(I feel like this is a good way to troll people)
		self.backIsBlue = 0

		self.prevScoreForUs = 0
		self.prevScoreForThem = 0
		self.diffScoreUs =FIRST_ROUND
		self.diffScoreThem =FIRST_ROUND
		self.scoreForUs = 0
		self.scoreForThem = 0

		self.southBid = ''
		self.westBid = ''
		self.northBid = ''
		self.eastBid = ''
		
		self.biddingRound = 0
		
		self.showBackToChannelButton = 0
		self.gameOver = 0
		
	
	def updateLastFrameTime(self):
		self.lastFrameTime = int(round(time.time() * 1000))
	
	#Functions called by some controller file:
	def setupCardsForNewRound(self, southCardsInput):
		tempArray = []
		
		for index in range(0, len(southCardsInput)):
			tempArray.append(convertCardStringToNum(southCardsInput[index]))
		
		
		tempArray.sort()
		
		
		self.southBid = ''
		self.westBid = ''
		self.northBid = ''
		self.eastBid = ''
		
		self.trumpCard = ''
		self.isTrumpCovered = 0
	
		
		with self.southCardLock:
				with self.eastCardLock:
					with self.westCardLock:
						with self.northCardLock:
							self.setCardUserWantsToPlayToNull()
							self.southCards = tempArray
							
							self.westCards  =  self.STARTING_HAND_LENGTH* [-1]
							self.northCards =  self.STARTING_HAND_LENGTH* [-1]
							self.eastCards  =  self.STARTING_HAND_LENGTH* [-1]
							
							self.tricks = 4 *[0]

	def letDealerExchangeCard(self, southCardsInput):
		tempArray = []
		
		for index in range(0, len(southCardsInput)):
			tempArray.append(convertCardStringToNum(southCardsInput[index]))
		
		tempArray.sort()
		
		#TODO: wait for animation event #1
		self.isTrumpCovered = 1
		
		#TODO: wait for animation event #2
		with self.southCardLock:
			self.southCards = tempArray
		

	def setDealerString(self, name):
		self.dealer = name
		
	def setTrumpCard(self, trumpCard):
		self.trumpCard = trumpCard
	
	def getTrumpCard(self):
		return self.trumpCard
	
	
	def bidSouth(self, bid):
		#print it.
		self.southBid = bid
		
	def bidWest(self, bid):
		self.westBid = bid
		
	def bidNorth(self, bid):
		self.northBid = bid
		
	def bidEast(self, bid):
		self.eastBid = bid
	
	def coverTrumpCard(self):
		self.isTrumpCovered = 1
	
	def printBids(self):
		myfont = pygame.font.SysFont("Bauhaus 93", 30)
		
		printall = 0
		
		#print all:
		if (self.southBid == '' or self.southBid == 'p') and (self.westBid == '' or self.westBid == 'p') and (self.northBid == '' or self.northBid == 'p') and (self.eastBid == '' or self.eastBid == 'p'):
			printall = 1
			
		
		halfCharLength = 9
		
		if self.southBid != '' and (printall == 1 or self.southBid != 'p'):
			label = myfont.render(self.southBid, 1, (0,0,255))
			self.screen.blit(label, (self.screen_width/2                    - halfCharLength * len(self.southBid), self.screen_height - self.off_the_edgeY/2 + 30))
		
		if self.westBid != '' and (printall == 1 or self.westBid != 'p'):
			label = myfont.render(self.westBid, 1, (0,0,255))
			self.screen.blit(label, (20 + self.off_the_edgeX                     - halfCharLength * len(self.westBid), self.screen_height/2 - 30))
		
		if self.northBid != '' and (printall == 1 or self.northBid != 'p'):
			label = myfont.render(self.northBid, 1, (0,0,255))
			self.screen.blit(label, (self.screen_width/2                    - halfCharLength * len(self.northBid), self.off_the_edgeY/4 - 30))
		
		if self.eastBid != '' and (printall == 1 or self.eastBid != 'p'):
			label = myfont.render(self.eastBid, 1, (0,0,255))
			self.screen.blit(label, (self.screen_width - self.off_the_edgeX - halfCharLength * len(self.eastBid), self.screen_height/2 - 30))
		
			
	def addTrickSouth(self):
		self.tricks[0] = self.tricks[0] + 1
		
	def addTrickWest(self):
		self.tricks[1] = self.tricks[1] + 1
		
	def addTrickNorth(self):
		self.tricks[2] = self.tricks[2] + 1
		
	def addTrickEast(self):
		self.tricks[3] = self.tricks[3] + 1
		
	
	
	#0: south, 1: west, 2: north, 3: east
	def throwSouthCard(self, cardString):
		with self.southCardLock:
			cardNum = convertCardStringToNum(cardString)
			indexCard = -1
			for x in range(0, len(self.southCards)):
				if self.southCards[x] == cardNum:
					indexCard = x
					break
			
			if indexCard == -1:
				print 'AHHH!!!! IndexCard is -1 on throw card.'
				#exit(1)
			
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
			southStartY = self.screen_height - self.off_the_edgeY - self.card_height/4
			southEndX   = self.screen_width/2
			southEndY   = self.screen_height/2 + self.card_width + self.card_height/4
			
			southprojectileId = southCards[cardHeldIndex]
			
			southCards.pop(cardHeldIndex)
			
			#params: (self, beingThrown, startX, startY, endX, endY, projectileId, rotation)
			return projectile.Projectile(1, southStartX, southStartY, southEndX, southEndY, southprojectileId, 0)
		else:
			return projectile.Projectile(0, 0, 0, 0, 0, 0, 0)

	def getCardEastWestPlayerYLocation(self, eastWestcards, indexCard):
		firstY = self.screen_height/2
		if len(eastWestcards) % 2 == 0:
			firstY = firstY + self.card_width/4
			
		firstY = firstY - int(len(eastWestcards)/2)*(self.card_width/2)
		
		ret = firstY + indexCard * (self.card_width/2)
		return ret

	def createWestCardProjectile(self, westCards, cardNum):
		if len(westCards) > 0:
			indexThrow = random.randint(0,len(westCards) - 1)
			
			westStartX = self.off_the_edgeX
			westStartY = self.getCardEastWestPlayerYLocation(westCards, indexThrow)
			
			westEndX= self.screen_width/2 - self.card_width - self.card_height/4
			westEndY= self.screen_height/2
			
			westCards.pop(indexThrow)
			
			return projectile.Projectile(1, westStartX, westStartY, westEndX, westEndY, cardNum, 1)
		else:
			return projectile.Projectile(0, 0, 0, 0, 0, 0, 0)
	
	def createNorthCardProjectile(self, northCards, cardNum):
		if len(northCards) > 0:
			indexThrow = random.randint(0,len(northCards) - 1)
			
			northStartX = self.getCardLocation(indexThrow)
			northStartY = self.off_the_edgeY + self.card_height/2
			northEndX   = self.screen_width/2
			northEndY   = self.screen_height/2 - self.card_width - self.card_height/4
			
			northCards.pop(indexThrow)
			
			return projectile.Projectile(1, northStartX, northStartY, northEndX, northEndY, cardNum, 0)
		else:
			return projectile.Projectile(0, 0, 0, 0, 0, 0, 0)
	
	def createEastCardProjectile(self, eastCards, cardNum):
		if len(eastCards) > 0:
			indexThrow = random.randint(0,len(eastCards) - 1)
			
			eastStartX = self.screen_width -  self.off_the_edgeX
			eastStartY = self.getCardEastWestPlayerYLocation(eastCards, indexThrow)
			
			eastEndX= self.screen_width/2 + self.card_width + self.card_height/4
			eastEndY= self.screen_height/2
			
			eastCards.pop(indexThrow)
			
			return projectile.Projectile(1, eastStartX, eastStartY, eastEndX, eastEndY, cardNum, 1)
		else:
			return projectile.Projectile(0, 0, 0, 0, 0, 0, 0)
	##END creating projectile functions.
	
	
	def printThrownCards(self):
		for x in range(0, 4):
			self.projectiles[x].printThrownCard(self)
	
	#post: removes the 0-4 cards played/thrown from the game.
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
	
		with self.scoreLock:
			self.prevScoreForUs = self.scoreForUs
			self.prevScoreForThem = self.scoreForThem
		
			self.diffScoreUs  =    us - self.prevScoreForUs
			self.diffScoreThem =  them - self.prevScoreForThem
			
			self.scoreForUs = us
			self.scoreForThem = them
		
	#END CONTROL FUNCTIONS
	def printScore(self):
	
		pygame.draw.rect(self.screen, (255, 255, 255, 0), ((1*self.width)/32, (4*self.height)/5 + 10, 300, 200))
		#Make summation lines:
		pygame.draw.rect(self.screen, (0, 0, 255, 0), ((1*self.width)/32, (4*self.height)/5 + 10 + 3*40, 60, 5))
		pygame.draw.rect(self.screen, (0, 0, 255, 0), ((1*self.width)/32 + 70, (4*self.height)/5 + 10 + 3*40, 60, 5))
		
		
		with self.scoreLock:
			myfont = pygame.font.SysFont("comicsansms", 30)
			
			
			labelExample1 = myfont.render("US       THEM", 1, (0,0,255))
			
			labelExample2 = myfont.render(str(self.prevScoreForUs) + "    " + str(self.prevScoreForThem), 1, (0,0,255))
			
			labelExample3 = myfont.render(" " + str(self.diffScoreUs) + "     " + str(self.diffScoreThem), 1, (0,0,255))
			
			labelExample4 = myfont.render(str(self.scoreForUs) + "    " + str(self.scoreForThem) + "  (" + self.dealer + ")", 1, (0,0,255))
			
			self.screen.blit(labelExample1, ((1*self.width)/32, (4*self.height)/5 + 10))
			
			if self.diffScoreThem == FIRST_ROUND:
				#If it's the first round and don't put the previous scores up...
				pass
			else:
				self.screen.blit(labelExample2, ((1*self.width)/32, (4*self.height)/5 + 10 + 1*40))
				self.screen.blit(labelExample3, ((1*self.width)/32, (4*self.height)/5 + 10 + 2*40))
			self.screen.blit(labelExample4, ((1*self.width)/32, (4*self.height)/5 + 10 + 3*40))
	
	def printTricks(self):
		myfont = pygame.font.SysFont("comicsansms", 30)
		
		labelTricksSouth = myfont.render(str(self.tricks[0]) + "/" + str(self.STARTING_HAND_LENGTH), 1, (0,0,255))
		labelTricksWest = myfont.render(str(self.tricks[1]) + "/" + str(self.STARTING_HAND_LENGTH), 1, (0,0,255))
		labelTricksNorth = myfont.render(str(self.tricks[2]) + "/" + str(self.STARTING_HAND_LENGTH), 1, (0,0,255))
		labelTricksEast = myfont.render(str(self.tricks[3]) + "/" + str(self.STARTING_HAND_LENGTH), 1, (0,0,255))
		
		self.screen.blit(labelTricksWest, (5, self.height/2))
		
		self.screen.blit(labelTricksEast, (1*self.width - 85, self.height/2))
		
		self.screen.blit(labelTricksNorth, (self.width/2, self.height/20))
		
		self.screen.blit(labelTricksSouth, (self.width/2, self.height - 90))
		
	
	
	def printDeck(self):
		
		if self.isTrumpCovered == 1:
			cardShown = -1
		else:
			if self.trumpCard != "":
				cardShown = convertCardStringToNum(self.trumpCard)
			else:
				cardShown = -1
		
		if self.dealer.find('North(') != -1:
			x = self.screen_width/2 - 3*self.card_width
			y = self.off_the_edgeY
			
			self.printcardFromCenter(x+3, y+5, -1, 0)
			self.printcardFromCenter(x, y, cardShown, 0)
			
		elif self.dealer.find('East(') != -1:
			x = self.screen_width    - self.off_the_edgeX
			y = self.screen_height/2  - 3*self.card_width
			
			self.printcardFromCenter(x-5, y+5, -1, 1)
			self.printcardFromCenter(x, y, cardShown, 1)
			
		elif self.dealer.find('South(') != -1:
			x = self.screen_width/2 + 3*self.card_width
			y = self.screen_height   - self.off_the_edgeY
			
			self.printcardFromCenter(x-5, y+5, -1, 0)
			self.printcardFromCenter(x, y, cardShown, 0)
			
		elif self.dealer.find('West(') != -1:
			x = self.off_the_edgeX
			y = self.screen_height/2 + 3*self.card_width
			
			self.printcardFromCenter(x+5, y, -1, 1)
			self.printcardFromCenter(x, y, cardShown, 1)
		
		'''
		firstY = self.screen_height/2
		if len(self.westCards) % 2 == 0:
			firstY = firstY + self.card_width/4
			
		firstY = firstY - int(len(self.westCards)/2)*(self.card_width/2)
		currentY = firstY
		
		for x in range(0, len(self.westCards)):
			self.printcardFromCenter(self.off_the_edgeX, currentY, -1, 1)
			currentY = currentY + (self.card_width/2)
		'''
	
	def printcard(self, x, y, num, rotate90):
		if num >= 52:
			print 'ERROR: card num is greater than 52!'
			num = 0
			sys.exit(1)
		
		if num < 0:
			if rotate90 ==0:
				self.screen.blit(self.backcard, (x, y), (self.backIsBlue*self.card_width, 0, self.card_width, self.card_height))
			else:
				temp = pygame.transform.rotate(self.backcard, 270)
				self.screen.blit(temp, (x, y), (0, self.backIsBlue * self.card_width, self.card_height, self.card_width))
		else:
			if rotate90 ==0:
				self.screen.blit(self.cardz, (x, y), ((num%13) * self.card_width, (num/13) * self.card_height, self.card_width, self.card_height))
			else:
				temp = pygame.transform.rotate(self.cardz, 270)
				self.screen.blit(temp, (x, y), (((4-1) - num/13) * self.card_height, (num%13) * self.card_width, self.card_height, self.card_width))

	#Implements If you want to use projectiles, this function must be there.
	def printProjectile(self, x, y, idNum, rotation):
		self.printcardFromCenter(x, y, idNum, rotation)
		
	
	def printcardFromCenter(self, centerX, centerY, num, rotate90):
		if rotate90 == 0:
			self.printcard(int(centerX - self.card_width/2), int(centerY - self.card_height/2), num, rotate90)
		else:
			self.printcard(int(centerX - self.card_height/2), int(centerY - self.card_width/2), num, rotate90)

	def getXCordFirstCardNorthSouth(self, cardList):
		if cardList != None:
			firstX = self.screen_width/2
			if len(cardList) % 2 == 0:
				firstX = firstX + self.card_width/4
			
			firstX = firstX - int(len(cardList)/2)*(self.card_width/2)
			
			return firstX
		else:
			return 0


	def isMouseHoveringOverCard(self, mx, my):
		firstX = self.getXCordFirstCardNorthSouth(self.southCards)
		
		if my > self.screen_height - self.off_the_edgeY - self.card_height/2:
			if my< self.screen_height - self.off_the_edgeY + self.card_height/2:
				firstX = self.getXCordFirstCardNorthSouth(self.southCards)
				if mx > firstX - self.card_width/2:
					if mx < firstX + len(self.southCards) * self.card_width/2:
						return 1
		return 0

	def printcardSuitNum(self, x, y, suit, num):
		printcard(x, y, 13*suit + num, 1)

	def fill_background(self):
		for y in range(0, self.screen_height, self.background.get_height()):
			for x in range(0, self.screen_width, self.background.get_width()):
				self.screen.blit(self.background, (x, y))

	def printSouthCards(self, mx, my):
		currentX = self.getXCordFirstCardNorthSouth(self.southCards)
		
		indexOfMouseOnCard = self.getIndexCardHover(mx, my)
		mouseHoveringOverCard = self.isMouseHoveringOverCard(mx, my)
		
		with self.southCardLock:
			for x in range(0, len(self.southCards)):
				
				if mouseHoveringOverCard == 1 and indexOfMouseOnCard == x:
					self.printcardFromCenter(currentX, self.screen_height - self.off_the_edgeY - self.card_height/4, self.southCards[x], 0)
				else:
					self.printcardFromCenter(currentX, self.screen_height - self.off_the_edgeY,  self.southCards[x], 0)
				currentX = currentX + (self.card_width/2)
	
		

	def printWestCards(self):
		firstY = self.screen_height/2
		if len(self.westCards) % 2 == 0:
			firstY = firstY + self.card_width/4
			
		firstY = firstY - int(len(self.westCards)/2)*(self.card_width/2)
		currentY = firstY
		
		for x in range(0, len(self.westCards)):
			self.printcardFromCenter(self.off_the_edgeX, currentY, -1, 1)
			currentY = currentY + (self.card_width/2)
		
		
	def printNorthCards(self):
		
		firstX = self.getXCordFirstCardNorthSouth(self.northCards)
		currentX = firstX
		
		for x in range(0, len(self.northCards)):
			self.printcardFromCenter(currentX, self.off_the_edgeY, -1, 0)
			currentX = currentX + (self.card_width/2)
		
	def printEastCards(self):
		firstY = self.screen_height/2
		if len(self.eastCards) % 2 == 0:
			firstY = firstY + self.card_width/4
			
		firstY = firstY - int(len(self.eastCards)/2)*(self.card_width/2)
		currentY = firstY
		
		for x in range(0, len(self.eastCards)):
			self.printcardFromCenter(self.screen_width - self.off_the_edgeX, currentY, -1, 1)
			currentY = currentY + (self.card_width/2)
		
	

	NOINDEX = -2
	def getIndexCardHover(self, mx, my):
		if my > self.screen_height - self.off_the_edgeY - self.card_height/2:
			if my< self.screen_height - self.off_the_edgeY + self.card_height/2:
				firstX = self.getXCordFirstCardNorthSouth(self.southCards)
				currentX = firstX
				for x in range(0, len(self.southCards)):
					if mx < currentX - self.card_width/2:
						return x-1
					
					currentX = currentX + (self.card_width/2)
				return len(self.southCards) - 1
				
		return self.NOINDEX

	#rearranges cards in the current players hand.
	def shiftSouthCards(self, origIndex, isLeft, numSpaces):
		#test some preconditions just in case
		if origIndex < len(self.southCards) and origIndex >= 0:
			if (origIndex + numSpaces < len(self.southCards) and isLeft == 0) or (origIndex - numSpaces >= 0 and isLeft == 1):
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
		return currentX + cardHeldIndex* (self.card_width/2)

	#cardUserWantsToPlay = ''
	
	def setCardUserWantsToPlay(self, cardString):
		self.cardUserWantsToPlay = cardString
	
	def setCardUserWantsToPlayToNull(self):
		self.cardUserWantsToPlay = ''
	
	def getCardUserWantsToPlay(self):
		return self.cardUserWantsToPlay
	
	
	def reorgSouthCards(self, mx, my, mouseJustPressed, mouseHeld, mouseJustRelease, cardHeldIndex):
		with self.southCardLock:
			indexOfMouseOnCard = self.getIndexCardHover(mx, my)
			
			mouseHoveringOverCard = self.isMouseHoveringOverCard(mx, my)
			
			#no card held:
			if mouseJustPressed == 1:
				
				if mouseHoveringOverCard == 1:
					cardHeldIndex = indexOfMouseOnCard
			
			
			if mouseJustRelease == 1:
				if self.isWaitingForBid() == 1:
					self.checkIfUserBidAfterClick(mx, my)
				
				if my < self.screen_height - self.off_the_edgeY - self.card_height/2:
					if cardHeldIndex >= 0:
						if cardHeldIndex >=0 and cardHeldIndex < len(self.southCards):
							print 'Trying to play: ' + str(convertCardNumToString(self.southCards[cardHeldIndex]))
							self.setCardUserWantsToPlay(convertCardNumToString(self.southCards[cardHeldIndex]))
							cardHeldIndex = self.NOINDEX
							
			
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
		labelExample = myfont.render(str(self.currentMsg), 1, (0,0,255))
		self.screen.blit(labelExample, (self.width/2 - 10 * xOffset, self.height/2 - 50))
	
	#This could be 1 or 2. (because there are 2 bidding rounds in Euchre.)
	def setBiddingRound(self, roundNumber):
		self.biddingRound = roundNumber
		if roundNumber != 1:
			#TODO: make a covering animation.
			self.isTrumpCovered = 1
	
	
	def displayBidChoices(self):
		
		'''
		self.BUTTON_NUM_ROWS_2 = 2
		self.BUTTON_HEIGHT_ROW = 100
		
		self.BUTTON_NUM_COLUMNS_2 = 5
		self.BUTTON_WIDTH_ROW = 160
		
		self.BUTTON_OFFSET = 10
		'''
		if self.biddingRound == 1:
			pygame.draw.rect(self.screen, (255, 0, 255, 0), (self.width/2 - self.BUTTON_WIDTH_ROW*self.BUTTON_NUM_COLUMNS_1/2, self.height/2 - self.BUTTON_HEIGHT_ROW*self.BUTTON_NUM_ROWS_1/2, self.BUTTON_WIDTH_ROW*self.BUTTON_NUM_COLUMNS_1, self.BUTTON_HEIGHT_ROW*self.BUTTON_NUM_ROWS_1))
			
			myfont = pygame.font.SysFont("Bauhaus 93", 30)
			
			labelAlone = myfont.render("Alone", 1, (0,255,0))
			
			for i in range(0, len(self.bidButtonsRound1)):
				
				if self.variation == 'ontarian' and i== 1 and self.dealer.find('North(') != -1:
					pygame.draw.rect(self.screen, (170, 183, 184, 0), self.bidButtonsRound1[i].getCoordBox())
					#Draw an x:
					pygame.draw.line(self.screen, (255, 0, 0, 0), (self.bidButtonsRound1[i].getX(), self.bidButtonsRound1[i].getY()), (self.bidButtonsRound1[i].getX() + self.bidButtonsRound1[i].getWidth(), self.bidButtonsRound1[i].getY()+ self.bidButtonsRound1[i].getHeight()), 2)
					pygame.draw.line(self.screen, (255, 0, 0, 0), (self.bidButtonsRound1[i].getX(), self.bidButtonsRound1[i].getY()+ self.bidButtonsRound1[i].getHeight()), (self.bidButtonsRound1[i].getX() + self.bidButtonsRound1[i].getWidth(), self.bidButtonsRound1[i].getY()), 2)
					
				else:
					pygame.draw.rect(self.screen, (0, 0, 0, 0), self.bidButtonsRound1[i].getCoordBox())
				
				command = "Order Up"
				if self.dealer.find('South(') != -1:
					command = "Pick It Up"
				
				if i == 0:
					labelExample = myfont.render("Pass", 1, (0,255,0))
					self.screen.blit(labelExample, self.bidButtonsRound1[i].getTopLeftBox())
					
				elif  i == 1:
					
					labelExample = myfont.render(command, 1, (0,255,0))
					self.screen.blit(labelExample, self.bidButtonsRound1[i].getTopLeftBox())
					
				elif  i == 2:
					labelExample = myfont.render(command, 1, (0,255,0))
					self.screen.blit(labelExample, self.bidButtonsRound1[i].getTopLeftBox())
					
					nextLine = self.BUTTON_HEIGHT_ROW/2 - self.BUTTON_OFFSET
					self.screen.blit(labelAlone, (self.bidButtonsRound1[i].getX(), self.bidButtonsRound1[i].getY() + nextLine))
			
		elif self.biddingRound == 2:
		
			pygame.draw.rect(self.screen, (255, 0, 255, 0), (self.width/2 - self.BUTTON_WIDTH_ROW*self.BUTTON_NUM_COLUMNS_2/2, self.height/2 - self.BUTTON_HEIGHT_ROW*self.BUTTON_NUM_ROWS_2/2, self.BUTTON_WIDTH_ROW*self.BUTTON_NUM_COLUMNS_2, self.BUTTON_HEIGHT_ROW*self.BUTTON_NUM_ROWS_2))
			
			myfont = pygame.font.SysFont("Bauhaus 93", 30)
			
			labelAlone = myfont.render("Alone", 1, (0,255,0))
			
			
			initialTrump = (self.trumpCard[1:]).upper()
			
			for i in range(0, len(self.bidButtonsRound2)):
				
				if i != 5:
					if (i%5 == 1 and 'S' == initialTrump) or (i%5 == 2 and 'H' == initialTrump) or (i%5 == 3 and 'C' == initialTrump) or (i%5 == 4 and 'D' == initialTrump):
						pygame.draw.rect(self.screen, (170, 183, 184, 0), self.bidButtonsRound2[i].getCoordBox())
						
						#Draw an x:
						pygame.draw.line(self.screen, (255, 0, 0, 0), (self.bidButtonsRound2[i].getX(), self.bidButtonsRound2[i].getY()), (self.bidButtonsRound2[i].getX() + self.bidButtonsRound2[i].getWidth(), self.bidButtonsRound2[i].getY()+ self.bidButtonsRound2[i].getHeight()), 2)
						pygame.draw.line(self.screen, (255, 0, 0, 0), (self.bidButtonsRound2[i].getX(), self.bidButtonsRound2[i].getY()+ self.bidButtonsRound2[i].getHeight()), (self.bidButtonsRound2[i].getX() + self.bidButtonsRound2[i].getWidth(), self.bidButtonsRound2[i].getY()), 2)
					else:
						pygame.draw.rect(self.screen, (0, 0, 0, 0), self.bidButtonsRound2[i].getCoordBox())
				
				if i == 0:
					labelExample = myfont.render("Pass", 1, (0,255,0))
					self.screen.blit(labelExample, self.bidButtonsRound2[i].getTopLeftBox())
					
				elif  i%5 == 1:
					labelExample = myfont.render("Spades", 1, (0,255,0))
					self.screen.blit(labelExample, self.bidButtonsRound2[i].getTopLeftBox())
					
				elif  i%5 == 2:
					labelExample = myfont.render("Hearts", 1, (0,255,0))
					self.screen.blit(labelExample, self.bidButtonsRound2[i].getTopLeftBox())
					
				elif  i%5 == 3:
					labelExample = myfont.render("Clubs", 1, (0,255,0))
					self.screen.blit(labelExample, self.bidButtonsRound2[i].getTopLeftBox())
					
				elif  i%5 == 4:
					labelExample = myfont.render("Diamonds", 1, (0,255,0))
					self.screen.blit(labelExample, self.bidButtonsRound2[i].getTopLeftBox())
					
				elif  i == 5:
					pass
				
				if i >= 6:
					nextLine = self.BUTTON_HEIGHT_ROW/2 - self.BUTTON_OFFSET
					self.screen.blit(labelAlone, (self.bidButtonsRound2[i].getX(), self.bidButtonsRound2[i].getY() + nextLine))
				
	def askUserForBid(self):
		self.isAwaitingBid = 1
	
	def isWaitingForBid(self):
		return self.isAwaitingBid

	
	def isGameOver(self):
		if self.gameOver == 0:
			return 0
		else:
			return 1
	
	def setGameOver(self):
		self.gameOver = 1
		self.displayBackToChannelMessage()

	def setVariation(self, variation):
		self.variation = variation
	
	def displayBackToChannelMessage(self):
		self.showBackToChannelButton = 1
		
	def checkIfUserBidAfterClick(self, x, y):
		if self.biddingRound == 1:
			for i in range(0, len(self.bidButtonsRound1)):
				if self.bidButtonsRound1[i].isWithinBox(x, y):
					print 'Clicked on ' + str(i)
					if i == 0:
						self.currentBid = 'P'
					elif i == 1:
						self.currentBid = str(self.trumpCard[1:])
					elif i == 2:
						self.currentBid = str(self.trumpCard[1:]) + ' a'
					
					print 'Bid ' + str(self.currentBid)
		
		elif self.biddingRound == 2:
			for i in range(0, len(self.bidButtonsRound2)):
				if self.bidButtonsRound2[i].isWithinBox(x, y):
					print 'Clicked on ' + str(i)
					if i == 0:
						self.currentBid = 'P'
					elif i%5 == 1:
						self.currentBid = 'S'
					elif i%5 == 2:
						self.currentBid = 'H'
					elif i%5 == 3:
						self.currentBid = 'C'
					elif i%5 == 4:
						self.currentBid = 'D'
					
					#Going alone
					if i>5:
						self.currentBid = self.currentBid + ' a'
					
					print 'Bid ' + str(self.currentBid)
	
	#returns the bid if the user bid. Returns -1 otherwise.
	def consumeBid(self):
		if self.currentBid != '':
			self.isAwaitingBid = 0
		temp = self.currentBid
		self.currentBid = ''
		return temp
	
def convertCardNumToString(num):
	if num < 0:
		return '??'
	
	suit = ''
	if num >=0 and num <13:
		suit = 'C'
	elif num >=13 and num <26:
		suit = 'D'
	elif num >=26 and num <39:
		suit = 'H'
	elif num >=39 and num <52:
		suit = 'S'
	else:
		print 'ERROR: Trying to convert card with num ' + str(num) + ' in convertCardNumToString(num)'
	
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
	
#FUNCTIONS THAT OUTSIDE CLASSES SHOULD USE:
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
		print card
		print str(len(card))
		print 'ERROR: unknown suit!'

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
	
	return 13*row + column


def main(connection):
	euchreGUI = EuchreGUI()
	#keep track of the last frame/heartbeat so we can throw projectiles smoothly.
	euchreGUI.updateLastFrameTime()
	
	print 'Inside Euchre GUI main!'
	
	try:
		t = Thread(name = 'Testing', target=euchreClient.main, args=(euchreGUI, ['euchreGUI.py', connection]))
		t.start()
	except:
		print "Error: unable to start thread"
	
	
	for x in range(0, 4):#euchreGUI.projectiles.
		temp = projectile.Projectile(0, 0, 0, 0, 0, 0, 0)
		euchreGUI.projectiles.append(temp)
	
	#texting adding 
	myfont = pygame.font.SysFont("comicsansms", 30)
	
	clock = pygame.time.Clock()
	
	euchreLogo = pygame.image.load("EuchreLogo.png").convert()
	transColor = euchreLogo.get_at((0,0))
	euchreLogo.set_colorkey(transColor)
	
	versNumber = pygame.image.load("versNumber1.png").convert()
	transColor = versNumber.get_at((0,0))
	versNumber.set_colorkey(transColor)
	

	mouseJustPressed = 0
	mouseHeld = 0
	mouseJustRelease = 0
	cardHeldIndex = euchreGUI.NOINDEX
	
	returnToChannelButton = button.Button(600, 600, 300, 50, "Return to channel", (0, 255 ,0), (255, 0 ,255))
	returnToChannelPressed = 0
	
	while 1:
		
		#React to user events:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				euchreGUI.gameOver = 1
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					mouseHeld=1
					mouseJustPressed = 1
			
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					mouseHeld = 0
					mouseJustRelease = 1
		
		mx,my = pygame.mouse.get_pos()
		
		cardHeldIndex = euchreGUI.reorgSouthCards(mx, my, mouseJustPressed, mouseHeld, mouseJustRelease, cardHeldIndex)
		
		
		if euchreGUI.showBackToChannelButton == 1:
			returnToChannelPressed = returnToChannelButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		#END React to user events:
		
		#Print Stuff:
		
		euchreGUI.fill_background()
		
		euchreGUI.screen.blit(euchreLogo, (0, 0, 500, 500), (0, 0, 500, 500))
		euchreGUI.screen.blit(versNumber, (20, 50, 500, 500), (0, 0, 500, 500))
		
		
		#TODO: Chat box:
		pygame.draw.rect(euchreGUI.screen, euchreGUI.WHITE, [(6*euchreGUI.width)/8, (4*euchreGUI.height)/5 + 10, 300, 200])
		
		euchreGUI.printScore()
		
		euchreGUI.printSouthCards(mx, my)
		euchreGUI.printWestCards()
		euchreGUI.printNorthCards()
		euchreGUI.printEastCards()

		euchreGUI.printThrownCards()
		
		euchreGUI.printTricks()
		euchreGUI.printDeck()
		euchreGUI.printBids()
		
		euchreGUI.displayCenterGameMsg()
		
		
		#Print colour of cursor depending on what user does:
		if mouseJustPressed == 1 or mouseJustRelease==1:
			euchreGUI.screen.blit(euchreGUI.greendot, (mx-5, my-5), (0, 0, 10, 10))
		elif mouseHeld == 1:
			euchreGUI.screen.blit(euchreGUI.reddot, (mx-5, my-5), (0, 0, 10, 10))
		else:
			euchreGUI.screen.blit(euchreGUI.dot, (mx-5, my-5), (0, 0, 10, 10))
		#end print colour of cursor.
		
		
		if euchreGUI.isWaitingForBid() == 1:
			euchreGUI.displayBidChoices()
		
		if euchreGUI.showBackToChannelButton ==1:
				returnToChannelButton.printButton(pygame, euchreGUI.screen)
		
		pygame.display.update()
		
		
		mouseJustPressed = 0
		mouseJustRelease = 0
		
		#End print stuff.
		
		#go back to channel after game is over:
		if euchreGUI.isGameOver() == 1 and returnToChannelPressed ==1:
			channelRoomGUI.main('', ['from euchreGUI.py', connection])
		#End go back to channel
		
		#Update to next frame:
		
		euchreGUI.updateLastFrameTime()
		clock.tick(1000/euchreGUI.FRAME_WAIT_TIME)
	
	
	euchreGUI.gameOver = 1

if __name__ == "__main__":
	args = sys.argv
	if len(args) > 1:
		name = args[1]
	else:
		name = 'Michael'
	
	#default ip and port:
	tcpIP = '127.0.0.1'
	tcpPort = 6789
	
	isHostingGame = 0
	interact = 0
	slowdown = 0
	
	#parse arguments:
	for x in range (0, len(args)):
		print str(args[x])
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
	
	print 'IP: ' + str(tcpIP)
	print 'PORT: ' + str(tcpPort)
	print 'name: ' + str(name)
	
	connection = clientContext.ClientContext(tcpIP, tcpPort, name)
	
	if isHostingGame ==1:
		connection.setHost()
	else:
		connection.setJoiner()
	
	connection.setInteract(interact)
	connection.setSlowdown(slowdown)
	main(connection)
	
'''
cd C:\Users\Michael\Desktop\cardGamePython\euchreGUI

cd desktop\cardGamePython\pythoninternet
For autogame:
python euchreGUI.py Michael host > output1.txt
python euchreGUI.py Phil
python euchreGUI.py Richard
python euchreGUI.py Doris

For game played by user:
python euchreGUI.py Michael host slow interact > output1.txt
python euchreGUI.py Phil slow
python euchreGUI.py Richard slow
python euchreGUI.py Doris slow


'''