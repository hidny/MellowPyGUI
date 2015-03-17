import sys, pygame
import time

import random, os
import time 
import pygame
from threading import Thread
import threading

from pygame import _view
from pygame.locals import *
from sys import exit

import projectile
import starterTest
import mellowClient


class MellowGUI:
	
	pygame.init()
	screen_width = 1300
	screen_height = 900
	
	size = width, height = screen_width, screen_height
	
	screen = pygame.display.set_mode(size)
	
	off_the_edgeX = 150
	off_the_edgeY = 150

	card_width = 79
	card_height = 123


	#TODO: make this as smooth as example 2

	#if this is 1, the back is blue.
	#if this is 0, the back is red.
	#(I feel like this is a good way to troll people)
	backIsBlue = 0


	southCards = 13 * [-1]
	westCards = 13 * [0]
	northCards= 13 * [0]
	eastCards = 13 * [0]

	scoreForUs = 0
	scoreForThem = 0

	#TODO: post the bid.
	southBid = -1
	westBid = -1
	northBid = -1
	eastBid = -1

	tricks = 4*[0]
	
	
	#Variable to handle the animation of thrown cards:
	projectiles = []

	THROW_TIME=1000
	FRAME_WAIT_TIME = 100
	
	
	WHITE = (255, 255, 255)

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
		#For now do nothing.
		pass
	
	#Functions called by some controller file:
	def setupCardsForNewRound(self, southCardsInput):
		tempArray = []
		
		print 'todo: setup cards for new round'
		print 'card indexes:'
		#TODO: make sure these are numbers.
		for index in range(0, len(southCardsInput)):
			tempArray.append(convertCardStringToNum(southCardsInput[index]))
			#print int(convertCardStringToNum(southCardsInput[index]))
		
		#for index in range(0, len(tempArray)):
		#	print tempArray[index]
		
		tempArray.sort()
		
		self.southCards = tempArray
		'''
		print 'South cards: '
		for index in range(0, len(southCards)):
			print southCards[index]
		'''
		with self.southCardLock:
			with self.westCardLock:
				with self.northCardLock:
					with self.eastCardLock:
						self.westCards  =  13* [-1]
						self.northCards =  13* [-1]
						self.eastCards  =  13* [-1]
						
						self.tricks = 4 *[0]


	
	def bidSouth(self, mellowGUI, bid):
		self.southBid = bid
		
	def bidWest(self, mellowGUI, bid):
		self.westBid = bid
		
	def bidNorth(self, mellowGUI, bid):
		self.northBid = bid
		
	def bidEast(self, mellowGUI, bid):
		self.eastBid = bid
	
	southCardLock = threading.Lock()
	westCardLock = threading.Lock()
	northCardLock = threading.Lock()
	eastCardLock = threading.Lock()
	scoreLock = threading.Lock()
	
	#0: south, 1: west, 2: north, 3: east
	#TODO: say which card is the one thrown
	def throwSouthCard(self, cardString):
		with self.southCardLock:
			cardNum = convertCardStringToNum(cardString)
			indexCard = -1
			for x in range(0, len(self.southCards)):
				if self.southCards[x] == cardNum:
					indexCard = x
					break
			
			if indexCard == -1:
				print 'AHHH!!!!'
			
			print 'TESTING' + str(indexCard)
			
			#TODO: get index of card num
			self.projectiles[0] = projectile.throwSouthCard(self, self.southCards, indexCard)
		
	def throwWestCard(self, cardString):#TODO: cardHeldIndex
		with self.westCardLock:
			cardNum = convertCardStringToNum(cardString)
			self.projectiles[1] = projectile.throwWestCard(self, self.westCards, cardNum)

	def throwNorthCard(self, cardString):
		with self.northCardLock:
			cardNum = convertCardStringToNum(cardString)
			self.projectiles[2] = projectile.throwNorthCard(self, self.northCards, cardNum)

	def throwEastCard(self, cardString):
		with self.eastCardLock:
			cardNum = convertCardStringToNum(cardString)
			self.projectiles[3] = projectile.throwEastCard(self, self.eastCards, cardNum)
	
	def printThrownCards(self):
		for x in range(0, 4):
			self.projectiles[x].printThrownCard(self)
	
		
	#pre: all projectiles are known.
	def remove_Projectiles(self, winnerIndex):
		for x in range(0, 4):
			self.projectiles[x].endThrow()
		
		#TODO: do something with the tricks thing.
		self.tricks[winnerIndex] = self.tricks[winnerIndex] + 1
	
	def updateScore(self, us, them):
		with self.scoreLock:
			diffUs  =    us  - self.scoreForUs
			diffThem =  them - self.scoreForThem
			
			#TODO: display score.
			
			self.scoreForUs = us
			self.scoreForThem = them
		
	#END CONTROL FUNCTIONS
	def printScore(self):	
		with self.scoreLock:
			myfont = pygame.font.SysFont("comicsansms", 30)
			
			#mellowGUI.screen.blit(labelExample, ((1*mellowGUI.width)/32, (4*mellowGUI.height)/5 + 10))
			#mellowGUI.screen.blit(labelExample, ((1*mellowGUI.width)/32, (4*mellowGUI.height)/5 + 10 + 1*40))
			#mellowGUI.screen.blit(labelExample, ((1*mellowGUI.width)/32, (4*mellowGUI.height)/5 + 10 + 2*40))
			#self.screen.blit(labelExample, ((1*mellowGUI.width)/32, (4*mellowGUI.height)/5 + 10 + 2*40))
			
			labelExample4 = myfont.render(str(self.scoreForUs) + "  " + str(self.scoreForThem) + "  (DEALER)", 1, (0,0,255))
			self.screen.blit(labelExample4, ((1*self.width)/32, (4*self.height)/5 + 10 + 2*40))
	
	
	def printcard(self, x, y, num, rotate90):
		if num >= 52:
			#crash
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

	def printcardFromCenter(self, centerX, centerY, num, rotate90):
		if rotate90 == 0:
			self.printcard(int(centerX - self.card_width/2), int(centerY - self.card_height/2), num, rotate90)
		else:
			self.printcard(int(centerX - self.card_height/2), int(centerY - self.card_width/2), num, rotate90)

	def getXCordFirstCardNorthSouth(self, cardList):
		firstX = self.screen_width/2
		if len(cardList) % 2 == 0:
			firstX = firstX + self.card_width/4
		
		firstX = firstX - int(len(cardList)/2)*(self.card_width/2)
		
		return firstX


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
		
		#print 'TO DELETE: Number of south cards: ' + str(len(southCards))
		with self.southCardLock:
			for x in range(0, len(self.southCards)):
				
				if mouseHoveringOverCard == 1 and indexOfMouseOnCard == x:
					self.printcardFromCenter(currentX, self.screen_height - self.off_the_edgeY - self.card_height/4, self.southCards[x], 0)
				else:
					self.printcardFromCenter(currentX, self.screen_height - self.off_the_edgeY,  self.southCards[x], 0)
				currentX = currentX + (self.card_width/2)
	
		

	def printWestCards(self, mx, my):
		firstY = self.screen_height/2
		if len(self.westCards) % 2 == 0:
			firstY = firstY + self.card_width/4
			
		firstY = firstY - int(len(self.westCards)/2)*(self.card_width/2)
		currentY = firstY
		
		for x in range(0, len(self.westCards)):
			self.printcardFromCenter(self.off_the_edgeX, currentY, -1, 1)
			currentY = currentY + (self.card_width/2)
		
		
	def printNorthCards(self, mx, my):
		
		firstX = self.getXCordFirstCardNorthSouth(self.northCards)
		currentX = firstX
		
		for x in range(0, len(self.northCards)):
			self.printcardFromCenter(currentX, self.off_the_edgeY, -1, 0)
			currentX = currentX + (self.card_width/2)
		
	def printEastCards(self, mx, my):
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


	def getCardLocation(self, cardHeldIndex):
		currentX = self.getXCordFirstCardNorthSouth(self.southCards)
		return currentX + cardHeldIndex* (self.card_width/2)


	def reorgSouthCards(self, mx, my, mouseJustPressed, mouseHeld, mouseJustRelease, cardHeldIndex):
		indexOfMouseOnCard = self.getIndexCardHover(mx, my)
		
		mouseHoveringOverCard = self.isMouseHoveringOverCard(mx, my)
		
		#no card held:
		if mouseJustPressed == 1:
			
			if mouseHoveringOverCard == 1:
				cardHeldIndex = indexOfMouseOnCard
		
		
		if mouseJustRelease == 1:
			if my < self.screen_height - self.off_the_edgeY - self.card_height/2:
				if cardHeldIndex >= 0:
					print '#TODO: if allowed to play....'
					if cardHeldIndex >=0 and cardHeldIndex < len(self.southCards):
						cardHeldIndex = self.NOINDEX
						#TODO: send command to controller about what card the user wants to play.
						
						
		
		if mouseHeld == 1:
			if mouseHoveringOverCard == 1:
				if cardHeldIndex > indexOfMouseOnCard:
					shiftAmount = cardHeldIndex - indexOfMouseOnCard
					self.southCards = shiftSouthCards(cardHeldIndex, 1, shiftAmount)
					cardHeldIndex = indexOfMouseOnCard
					#print southCards[0]
					
				elif cardHeldIndex < indexOfMouseOnCard:
					shiftAmount = indexOfMouseOnCard - cardHeldIndex
					self.southCards = shiftSouthCards(cardHeldIndex, 0, shiftAmount)
					cardHeldIndex = indexOfMouseOnCard
			
		return cardHeldIndex
		

		
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

#TODO: make it display the bid.


def main(name):
	mellowGUI = MellowGUI()
	
	print 'Inside Mellow GUI main!'
	
	try:
		#t = Thread(name = 'Testing', target=starterTest.main, args=('Michael', ))
		t = Thread(name = 'Testing', target=mellowClient.main, args=(mellowGUI, ))
		#t = Thread(name = 'Testing', target=melloClient.main, args=('Michael',))
		t.start()
	except:
		print "Error: unable to start thread"
	
	
	for x in range(0, 4):#mellowGUI.projectiles.
		temp = projectile.Projectile(0, 0, 0, 0, 0, 0, 0)
		mellowGUI.projectiles.append(temp)
	
	#texting adding 
	myfont = pygame.font.SysFont("comicsansms", 30)

	# render text
	labelExample = myfont.render("Do not renege!", 1, (0,0,255))
	labelExample = myfont.render("  US        THEM", 1, (0,0,255))
	labelExample2 = myfont.render("     0        0 (SOUTH)", 1, (0,0,255))
	labelExample3 = myfont.render(" 1 4      1 5 ", 1, (0,0,255))
	labelExample4 = myfont.render(" 1 4 0    1 5 0 (WEST)", 1, (0,0,255))
	
	clock = pygame.time.Clock()
	
	ballspeed = [2, 2]
	
	
	ball = pygame.image.load("ball.png").convert()
	transColor = ball.get_at((0,0))
	ball.set_colorkey(transColor)
	
	mellowLogo = pygame.image.load("MellowLogo.png").convert()
	transColor = mellowLogo.get_at((0,0))
	mellowLogo.set_colorkey(transColor)
	
	versNumber = pygame.image.load("versNumber.png").convert()
	transColor = versNumber.get_at((0,0))
	versNumber.set_colorkey(transColor)
	
	ball = pygame.image.load("ball.png").convert()
	transColor = ball.get_at((0,0))
	ball.set_colorkey(transColor)
	
	ballrect = ball.get_rect()

	mouseJustPressed = 0
	mouseHeld = 0
	mouseJustRelease = 0
	cardHeldIndex = mellowGUI.NOINDEX
	
	
	while 1:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					mouseHeld=1
					mouseJustPressed = 1
			
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					mouseHeld = 0
					mouseJustRelease = 1
		
		ballrect = ballrect.move(ballspeed)
		if ballrect.left < 0 or ballrect.right > mellowGUI.width:
			ballspeed[0] = -ballspeed[0]
		if ballrect.top < 0 or ballrect.bottom > mellowGUI.height:
			ballspeed[1] = -ballspeed[1]

		mellowGUI.fill_background()
		
		mellowGUI.screen.blit(mellowLogo, (0, 0, 500, 500), (0, 0, 500, 500))
		mellowGUI.screen.blit(versNumber, (20, 50, 500, 500), (0, 0, 500, 500))
		
		mellowGUI.screen.blit(labelExample, (mellowGUI.width/2, mellowGUI.height/2))
		
		#TODO: Score screen:
		pygame.draw.rect(mellowGUI.screen, mellowGUI.WHITE, [(6*mellowGUI.width)/8, (4*mellowGUI.height)/5 + 10, 300, 200])
		#mellowGUI.screen.blit(labelExample, ((6*mellowGUI.width)/8, (4*mellowGUI.height)/5 + 10))
		#mellowGUI.screen.blit(labelExample2, ((6*mellowGUI.width)/8, (4*mellowGUI.height)/5 + 10 + 1*40))
		#mellowGUI.screen.blit(labelExample3, ((6*mellowGUI.width)/8, (4*mellowGUI.height)/5 + 10 + 2*40))
		#mellowGUI.screen.blit(labelExample4, ((6*mellowGUI.width)/8, (4*mellowGUI.height)/5 + 10 + 3*40))
		
		pygame.draw.rect(mellowGUI.screen, mellowGUI.WHITE, [(1*mellowGUI.width)/32, (4*mellowGUI.height)/5 + 10, 300, 200])
		#mellowGUI.screen.blit(labelExample, ((1*mellowGUI.width)/32, (4*mellowGUI.height)/5 + 10))
		#mellowGUI.screen.blit(labelExample, ((1*mellowGUI.width)/32, (4*mellowGUI.height)/5 + 10 + 1*40))
		#mellowGUI.screen.blit(labelExample, ((1*mellowGUI.width)/32, (4*mellowGUI.height)/5 + 10 + 2*40))
		#mellowGUI.screen.blit(labelExample, ((1*mellowGUI.width)/32, (4*mellowGUI.height)/5 + 10 + 3*40))
		mellowGUI.printScore()
		
		mellowGUI.screen.blit(ball, ballrect)
		mx,my = pygame.mouse.get_pos()
		
		cardHeldIndex = mellowGUI.reorgSouthCards(mx, my, mouseJustPressed, mouseHeld, mouseJustRelease, cardHeldIndex)
		
		mellowGUI.printSouthCards(mx, my)
		mellowGUI.printWestCards(mx, my)
		mellowGUI.printNorthCards(mx, my)
		mellowGUI.printEastCards(mx, my)

		mellowGUI.printThrownCards()
		
		if mouseJustPressed == 1 or mouseJustRelease==1:
			mellowGUI.screen.blit(mellowGUI.greendot, (mx-5, my-5), (0, 0, 10, 10))
		elif mouseHeld == 1:
			mellowGUI.screen.blit(mellowGUI.reddot, (mx-5, my-5), (0, 0, 10, 10))
		else:
			mellowGUI.screen.blit(mellowGUI.dot, (mx-5, my-5), (0, 0, 10, 10))
		
		pygame.display.update()
		mouseJustPressed = 0
		mouseJustRelease = 0
		
		#print 'Done frame'
		clock.tick(mellowGUI.FRAME_WAIT_TIME)
		

if __name__ == "__main__":
	main('hello world')
	
'''
cd desktop\cardGamePython\pythoninternet

python mellowGUI.py Michael host > output1.txt
python mellowGUI.py Phil
python mellowGUI.py Richard
python mellowGUI.py Doris

#Starting game in
'''