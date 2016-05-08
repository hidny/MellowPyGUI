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

import connect4Client
import button
import channelRoomGUI

#This is designed to be a singleton object

class Connect4GUI:
	
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
	
	TOP_LEFT_CORNERX = 160
	TOP_LEFT_CORNERY = 160
	BOTTOM_RIGHT_CORNERX = 975
	BOTTOM_RIGHT_CORNERY = 715
	RADIUS = 37
	X_DIST_BETWEEN_HOLES = 115
	Y_DIST_BETWEEN_HOLES = 90
	TOP_LEFT_HOLEX = 220
	TOP_LEFT_HOLEY = 210
	
	
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
		
		self.board =  [[0 for x in range(7)] for x in range(6)] 
		
		self.currentMsg = ''
		
		self.moveUserWantsToMake = -1
		
		self.lastFrameTime = int(round(time.time() * 1000))
		
		self.isAwaitingBid = 0
		self.currentBid = -1
		
		self.showBackToChannelButton = 0
		
		self.gameOver = 0
		
	
	def dropPeg(self, slot_num, colour):
		
		for x in range(0, len(self.board)):
			if self.board[len(self.board) - 1 - x][slot_num] == 0:
				self.board[len(self.board) - 1 - x][slot_num] = colour
				break
	
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
	def setMoveUserWantsToMake(self, moveIndex):
		self.moveUserWantsToMake = moveIndex
	
	def setMoveUserWantsToMakeToNull(self):
		self.moveUserWantsToMake = -1
	
	def getMoveUserWantsToMake(self):
		return self.moveUserWantsToMake
	
	
	
	def drawBoard(self):
		pygame.draw.rect(self.screen, self.BLUE, [self.TOP_LEFT_CORNERX, self.TOP_LEFT_CORNERY, self.BOTTOM_RIGHT_CORNERX - self.TOP_LEFT_CORNERX, self.BOTTOM_RIGHT_CORNERY - self.TOP_LEFT_CORNERY])
		
		for i in range(0, len(self.board)):
			for j in range(0, len(self.board[0])):
				if self.board[i][j] == 0:
					pygame.draw.circle(self.screen, self.WHITE, (self.TOP_LEFT_HOLEX + self.X_DIST_BETWEEN_HOLES*j, self.TOP_LEFT_HOLEY + self.Y_DIST_BETWEEN_HOLES * i), self.RADIUS)
				elif self.board[i][j] == self.RED:
					pygame.draw.circle(self.screen, (255, 0, 0), (self.TOP_LEFT_HOLEX + self.X_DIST_BETWEEN_HOLES*j, self.TOP_LEFT_HOLEY + self.Y_DIST_BETWEEN_HOLES * i), self.RADIUS)
				elif self.board[i][j] == self.YELLOW:
					pygame.draw.circle(self.screen, (255,255,0), (self.TOP_LEFT_HOLEX + self.X_DIST_BETWEEN_HOLES*j, self.TOP_LEFT_HOLEY + self.Y_DIST_BETWEEN_HOLES * i), self.RADIUS)
		
	
	def setMessage(self, message):
		self.currentMsg = message
	
	def displayGameMsg(self):
		myfont = pygame.font.SysFont("comicsansms", 30)
		xOffset = len(self.currentMsg)
		labelExample = myfont.render(str(self.currentMsg), 1, (0,0,255))
		self.screen.blit(labelExample, (self.width/2 - 10 * xOffset, (5*self.height)/6))
		
	def displayBackToChannelMessage(self):
		self.showBackToChannelButton = 1

def main(connection):
	connect4GUI = Connect4GUI()
	
	connect4GUI.updateLastFrameTime()
	
	print 'Inside Connect 4 GUI main!'
	
	
	try:
		t = Thread(name = 'Testing', target=connect4Client.main, args=(connect4GUI, ['Connect4GUI.py', connection]))
		t.start()
	except:
		print "Error: unable to start thread"
	
	
	#texting adding 
	myfont = pygame.font.SysFont("comicsansms", 30)
	
	clock = pygame.time.Clock()
	
	
	#Uses Bauhaus 93 font.
	connect4Logo = pygame.image.load("Connect4Logo.png").convert()
	transColor = connect4Logo.get_at((0,0))
	connect4Logo.set_colorkey(transColor)
	
	
	returnToChannelButton = button.Button(Connect4GUI.BOTTOM_RIGHT_CORNERX + 10, 600, 300, 50, "Return to channel", (0, 255 ,0), (255, 0 ,255))
	
	mouseJustPressed = 0
	mouseHeld = 0
	mouseJustRelease = 0
	returnToChannelPressed = 0
	
	try:
		while 1:
			
			#React to user events:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					connect4GUI.gameOver = 1
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
				print str(mx) + ',' +  str(my)
				
				#Find the slot the player clicked on:
				if my > connect4GUI.TOP_LEFT_HOLEY - connect4GUI.RADIUS and my < connect4GUI.TOP_LEFT_HOLEY + connect4GUI.Y_DIST_BETWEEN_HOLES * (len(connect4GUI.board)-1) + connect4GUI.RADIUS:
					if connect4GUI.TOP_LEFT_HOLEX > connect4GUI.TOP_LEFT_HOLEX - connect4GUI.RADIUS and connect4GUI.TOP_LEFT_HOLEX < connect4GUI.TOP_LEFT_HOLEX + connect4GUI.X_DIST_BETWEEN_HOLES*(len(connect4GUI.board[0])-1) + connect4GUI.RADIUS:
						if (mx -  (connect4GUI.TOP_LEFT_HOLEX - connect4GUI.RADIUS)) / connect4GUI.X_DIST_BETWEEN_HOLES >= 0 and (mx -  (connect4GUI.TOP_LEFT_HOLEX - connect4GUI.RADIUS)) / connect4GUI.X_DIST_BETWEEN_HOLES < len(connect4GUI.board[0]):
							connect4GUI.setMoveUserWantsToMake((mx -  (connect4GUI.TOP_LEFT_HOLEX - connect4GUI.RADIUS)) / connect4GUI.X_DIST_BETWEEN_HOLES)
			
			if connect4GUI.showBackToChannelButton ==1:
				returnToChannelPressed = returnToChannelButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
			
			#END React to user events:
			
			#Print Stuff:
			
			connect4GUI.fill_background()
			
			connect4GUI.drawBoard()
			
			connect4GUI.screen.blit(connect4Logo, (0, 0, 500, 500), (0, 0, 500, 500))
			
			#TODO: Chat box:
			pygame.draw.rect(connect4GUI.screen, connect4GUI.WHITE, [(6*connect4GUI.width)/8, (4*connect4GUI.height)/5 + 10, 300, 200])
			
			connect4GUI.displayGameMsg()
			
			#Print colour of cursor depending on what user does:
			if mouseJustPressed == 1 or mouseJustRelease==1:
				connect4GUI.screen.blit(connect4GUI.greendot, (mx-5, my-5), (0, 0, 10, 10))
			elif mouseHeld == 1:
				connect4GUI.screen.blit(connect4GUI.reddot, (mx-5, my-5), (0, 0, 10, 10))
			else:
				connect4GUI.screen.blit(connect4GUI.dot, (mx-5, my-5), (0, 0, 10, 10))
			#end print colour of cursor.
			
			if connect4GUI.showBackToChannelButton ==1:
				returnToChannelButton.printButton(pygame, connect4GUI.screen)
			
			pygame.display.update()
			
			
			mouseJustPressed = 0
			mouseJustRelease = 0
			
			#End print stuff.
			
			#go back to channel after game is over:
			if connect4GUI.isGameOver() == 1 and returnToChannelPressed ==1:
				channelRoomGUI.main('', ['from connect4GUI.py', connection])
			#End go back to channel
			
			#Update to next frame:
			
			connect4GUI.updateLastFrameTime()
			clock.tick(1000/connect4GUI.FRAME_WAIT_TIME)
		
		
		connect4GUI.gameOver = 1
	except:
		print 'ERROR: in connect4 gui'
		connect4GUI.setMessage("ERROR: in server listener")
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
python connect4GUI.py Michael host > output1.txt
python connect4GUI.py Phil
python connect4GUI.py Richard
python connect4GUI.py Doris

For game played by user:
python connect4GUI.py Michael host slow interact > output1.txt
python connect4GUI.py Phil slow
python connect4GUI.py Richard slow
python connect4GUI.py Doris slow


python connect4GUI.py Michael host slow interact p=6789 ip=127.0.0.1
'''