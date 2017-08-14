import sys, pygame
import time

import random, os
import pygame
from threading import Thread
import threading

#from pygame import _view
from pygame.locals import *
from sys import exit

import starterTest
import mellowClient
import box
import clientContext

import reversiClient
import button
import channelRoomGUI

#This is designed to be a singleton object

BOARD_LENGTH = 8
BLACK = 'B'
WHITE = 'W'

class ReversiGUI:
	
	pygame.init()
	
	gameOver = 0
	
	screen_width = 1300
	screen_height = 900
	
	size = width, height = screen_width, screen_height
	
	screen = pygame.display.set_mode(size)
	
	off_the_edgeX = 150
	off_the_edgeY = 150


	THROW_TIME=100
	FRAME_WAIT_TIME = 40
	
	WHITE = (255, 255, 255)
	BLUE = (0, 178, 238)
	
	TOP_LEFT_CORNERX = 360
	TOP_LEFT_CORNERY = 160
	BOTTOM_RIGHT_CORNERX = 960
	BOTTOM_RIGHT_CORNERY = 760
	
	RADIUS = 27
	
	RED = 1
	YELLOW = 2
	
	#Images:
	background_image_filename = 'Image/wood3.png'
	background = pygame.image.load(background_image_filename)

	dot_image_file = 'Image/dot.png'
	dot = pygame.image.load(dot_image_file).convert()

	red_dot_image_file = 'Image/reddot.png'
	reddot = pygame.image.load(red_dot_image_file).convert()

	green_dot_image_file = 'Image/greendot.png'
	greendot = pygame.image.load(green_dot_image_file).convert()
	
	
	def __init__(self):
		
		self.boardLock = threading.Lock()
		
		self.board =  [['E' for x in range(BOARD_LENGTH)] for x in range(BOARD_LENGTH)] 
		
		self.currentMsg = ''
		
		
		self.lastFrameTime = int(round(time.time() * 1000))
		
		self.isAwaitingBid = 0
		self.currentBid = -1
		
		self.showBackToChannelButton = 0
		
		self.gameOver = 0
		
		self.moveCoord = ''
		
	
	#Example input: self.placePeg('a3', 'B')
	def placePeg(self, coord, colour):
		
		x = coord[0]
		y = coord[1]
		
		self.board[int(y) - 1][ord(x) - ord('a')] = colour
	
	def updateLastFrameTime(self):
		self.lastFrameTime = int(round(time.time() * 1000))
	
	def isGameOver(self):
		if self.gameOver == 0:
			return 0
		else:
			return 1
	
	
	def setGameOver(self):
		self.gameOver = 1
		self.displayBackToChannelMessage()
	
	def fill_background(self):
		for y in range(0, self.screen_height, self.background.get_height()):
			for x in range(0, self.screen_width, self.background.get_width()):
				self.screen.blit(self.background, (x, y))


	#moveUserWantsToMake = ''
	def setMoveUserWantsToMake(self, moveCoord):
		self.moveCoord = moveCoord
	
	def setMoveUserWantsToMakeToNull(self):
		self.moveCoord = ''
	
	def getMoveUserWantsToMake(self):
		return self.moveCoord
	
	
	def drawBoard(self):
		pygame.draw.rect(self.screen, (0, 255, 0), [self.TOP_LEFT_CORNERX, self.TOP_LEFT_CORNERY, self.BOTTOM_RIGHT_CORNERX - self.TOP_LEFT_CORNERX, self.BOTTOM_RIGHT_CORNERY - self.TOP_LEFT_CORNERY])
		
		X_DIST = (self.BOTTOM_RIGHT_CORNERX - self.TOP_LEFT_CORNERX) / BOARD_LENGTH
		Y_DIST = (self.BOTTOM_RIGHT_CORNERY - self.TOP_LEFT_CORNERY) / BOARD_LENGTH
		
		for i in range(0, BOARD_LENGTH+1):
			pygame.draw.line(self.screen, (0, 0, 0), (self.TOP_LEFT_CORNERX, self.TOP_LEFT_CORNERY + i* Y_DIST), (self.BOTTOM_RIGHT_CORNERX, self.TOP_LEFT_CORNERY + i* Y_DIST), 2)
			pygame.draw.line(self.screen, (0, 0, 0), (self.TOP_LEFT_CORNERX + i* X_DIST, self.TOP_LEFT_CORNERY), (self.TOP_LEFT_CORNERX + i* X_DIST, self.BOTTOM_RIGHT_CORNERY), 2)
		
		for i in range(0, BOARD_LENGTH):
			for j in range(0, BOARD_LENGTH):
				if self.board[i][j] == BLACK:
					pygame.draw.circle(self.screen, (0, 0, 0), (self.TOP_LEFT_CORNERX + j* X_DIST + X_DIST/2, self.TOP_LEFT_CORNERY + i* Y_DIST + Y_DIST/2), self.RADIUS)
				elif self.board[i][j] == WHITE:
					pygame.draw.circle(self.screen, (255, 255, 255), (self.TOP_LEFT_CORNERX + j* X_DIST + X_DIST/2, self.TOP_LEFT_CORNERY + i* Y_DIST + Y_DIST/2), self.RADIUS)
				else:
					pass
				
		
		
	def displayCurrentScore(self):
		X_DIST = (self.BOTTOM_RIGHT_CORNERX - self.TOP_LEFT_CORNERX) / BOARD_LENGTH
		Y_DIST = (self.BOTTOM_RIGHT_CORNERY - self.TOP_LEFT_CORNERY) / BOARD_LENGTH
		
		pygame.draw.rect(self.screen, (0, 255, 0), [150 - X_DIST, self.height/2, (self.BOTTOM_RIGHT_CORNERX - self.TOP_LEFT_CORNERX)/BOARD_LENGTH, (self.BOTTOM_RIGHT_CORNERY - self.TOP_LEFT_CORNERY)/BOARD_LENGTH])
		pygame.draw.rect(self.screen, (0, 255, 0), [150 - X_DIST, self.height/2 + Y_DIST + 15, (self.BOTTOM_RIGHT_CORNERX - self.TOP_LEFT_CORNERX)/BOARD_LENGTH, (self.BOTTOM_RIGHT_CORNERY - self.TOP_LEFT_CORNERY)/BOARD_LENGTH])
		
		pygame.draw.circle(self.screen, (0, 0, 0), (150 - X_DIST + X_DIST/2, self.height/2 + Y_DIST/2), self.RADIUS)
		pygame.draw.circle(self.screen, (255, 255, 255),       (150 - X_DIST + X_DIST/2, self.height/2 + Y_DIST + Y_DIST/2 + 15), self.RADIUS)
		
		
		myfont = pygame.font.SysFont("Bauhaus 93", 50)
		
		numBlackPegs = 0
		numWhitePegs = 0
		for i in range(0, BOARD_LENGTH):
			for j in range(0, BOARD_LENGTH):
				if self.board[i][j] == WHITE:
					numWhitePegs = numWhitePegs + 1
				elif self.board[i][j] == BLACK:
					numBlackPegs = numBlackPegs + 1
				else:
					pass
				
		labelExample = myfont.render('=' + str(numBlackPegs), 1, (0,0,255))
		self.screen.blit(labelExample, (155, self.height/2  + 10))
		labelExample = myfont.render('=' + str(numWhitePegs), 1, (0,0,255))
		
		self.screen.blit(labelExample, (155, self.height/2 + Y_DIST + 15  + 10))
	
	def setMessage(self, message):
		self.currentMsg = message
	
	def displayGameMsg(self):
		myfont = pygame.font.SysFont("comicsansms", 30)
		xOffset = len(self.currentMsg)
		labelExample = myfont.render(str(self.currentMsg), 1, (0,0,255))
		self.screen.blit(labelExample, (self.width/2 - 10 * xOffset, self.height-100))
		
	def displayBackToChannelMessage(self):
		self.showBackToChannelButton = 1

def main(connection):
	reversiGUI = ReversiGUI()
	
	reversiGUI.updateLastFrameTime()
	
	print 'Inside Connect 4 GUI main!'
	
	
	try:
		t = Thread(name = 'Testing', target=reversiClient.main, args=(reversiGUI, ['ReversiGUI.py', connection]))
		t.start()
	except:
		print "Error: unable to start thread"
	
	
	#texting adding 
	myfont = pygame.font.SysFont("comicsansms", 30)
	
	clock = pygame.time.Clock()
	
	
	#Uses Bauhaus 93 font.
	reversiLogo = pygame.image.load("ReversiLogo.png").convert()
	transColor = reversiLogo.get_at((0,0))
	reversiLogo.set_colorkey(transColor)
	
	
	returnToChannelButton = button.Button(reversiGUI.BOTTOM_RIGHT_CORNERX + 10, 600, 300, 50, "Return to channel", (0, 255 ,0), (255, 0 ,255))
	
	mouseJustPressed = 0
	mouseHeld = 0
	mouseJustRelease = 0
	returnToChannelPressed = 0
	
	try:
		while 1:
			
			#React to user events:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					reversiGUI.gameOver = 1
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
			
			if mouseJustRelease == 1:
				
				
				#Find the slot the player clicked on:
				if my > reversiGUI.TOP_LEFT_CORNERY and my < reversiGUI.BOTTOM_RIGHT_CORNERY:
					if  mx > reversiGUI.TOP_LEFT_CORNERX and mx < reversiGUI.BOTTOM_RIGHT_CORNERX:
						pressedX = 1 + (BOARD_LENGTH*(mx - reversiGUI.TOP_LEFT_CORNERX)) / (  reversiGUI.BOTTOM_RIGHT_CORNERX - reversiGUI.TOP_LEFT_CORNERX)
						pressedY = 1 + (BOARD_LENGTH*(my - reversiGUI.TOP_LEFT_CORNERY)) / (  reversiGUI.BOTTOM_RIGHT_CORNERY - reversiGUI.TOP_LEFT_CORNERY)
						
						pressedX = chr(pressedX + ord('a') - 1)
						
						desiredMove = str(pressedX) + str(pressedY)
						reversiGUI.setMoveUserWantsToMake(desiredMove)
						
			
			if reversiGUI.showBackToChannelButton ==1:
				returnToChannelPressed = returnToChannelButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
			
			#END React to user events:
			
			#Print Stuff:
			
			reversiGUI.fill_background()
			
			reversiGUI.drawBoard()
			
			reversiGUI.displayCurrentScore()
			
			reversiGUI.screen.blit(reversiLogo, (0, 0, 500, 500), (0, 0, 500, 500))
			
			#TODO: Chat box:
			pygame.draw.rect(reversiGUI.screen, reversiGUI.WHITE, [(6*reversiGUI.width)/8, (4*reversiGUI.height)/5 + 10, 300, 200])
			
			reversiGUI.displayGameMsg()
			
			#Print colour of cursor depending on what user does:
			if mouseJustPressed == 1 or mouseJustRelease==1:
				reversiGUI.screen.blit(reversiGUI.greendot, (mx-5, my-5), (0, 0, 10, 10))
			elif mouseHeld == 1:
				reversiGUI.screen.blit(reversiGUI.reddot, (mx-5, my-5), (0, 0, 10, 10))
			else:
				reversiGUI.screen.blit(reversiGUI.dot, (mx-5, my-5), (0, 0, 10, 10))
			#end print colour of cursor.
			
			if reversiGUI.showBackToChannelButton ==1:
				returnToChannelButton.printButton(pygame, reversiGUI.screen)
			
			pygame.display.update()
			
			
			mouseJustPressed = 0
			mouseJustRelease = 0
			
			#End print stuff.
			
			#go back to channel after game is over:
			if reversiGUI.isGameOver() == 1 and returnToChannelPressed ==1:
				channelRoomGUI.main('', ['from ReversiGUI.py', connection])
			#End go back to channel
			
			#Update to next frame:
			
			reversiGUI.updateLastFrameTime()
			clock.tick(1000/reversiGUI.FRAME_WAIT_TIME)
		
		
		reversiGUI.gameOver = 1
	except:
		#print 'ERROR: in reversi gui'
		reversiGUI.setMessage("ERROR: in server listener")
		exit(1)

#WARNING: Below is copied from mellow GUI.
#TODO: put this in a util function.
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
cd C:\Users\Michael\Desktop\cardGamePython\MellowPyGUI

cd desktop\cardGamePython\pythoninternet
For autogame:
python reversiGUI.py Michael host > output1.txt
python reversiGUI.py Phil
python reversiGUI.py Richard
python reversiGUI.py Doris

For game played by user:
python reversiGUI.py Michael host slow interact > output1.txt
python reversiGUI.py Phil slow
python reversiGUI.py Richard slow
python reversiGUI.py Doris slow


python reversiGUI.py Michael host slow interact p=6789 ip=127.0.0.1
'''