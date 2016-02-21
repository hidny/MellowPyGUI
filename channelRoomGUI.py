import sys, pygame
from pygame import _view
from pygame.locals import *
from sys import exit

import time

import textBox
import textBoxList
import box
import button
import mellowGUI
import chatBox
import clientContext

import joinGameWindow
import createGameWindow
import start

def main(threadName, args):
	
	if len(args) > 1:
		connection = args[1]
	else:
		connection = clientContext.ClientContext('127.0.0.1', 6789, 'Barney')
	
	if connection.getChannelChatBox() == '':
		connection.setChannelChatBox(chatBox.chatBox(24, 100 ,20, 500))
		
	pygame.init()
	
	screen_width = 1300
	screen_height = 900
	USER_REFRESH_TIME = 2000
	lastRefreshTime = round(time.time() * 1000) - USER_REFRESH_TIME
	REFRESH_MSG = 'number of game rooms:'
	PLAYERS_IN_CHANNEL_HEADER = 'players in channel:'
	DISCONNECT = 'Goodbye!'
	
	listOfPlayerInChannel = []
	
	clock = pygame.time.Clock()
	
	size = width, height = screen_width, screen_height
	screen = pygame.display.set_mode(size)
	
	#Variable declaration for cursor
	dot_image_file = 'Image/dot.png'
	dot = pygame.image.load(dot_image_file).convert()

	red_dot_image_file = 'Image/reddot.png'
	reddot = pygame.image.load(red_dot_image_file).convert()

	green_dot_image_file = 'Image/greendot.png'
	greendot = pygame.image.load(green_dot_image_file).convert()
	#End variable declaration for cursor.
	
	
	WHITE = (255, 255, 255)
	myfont = pygame.font.SysFont("comicsansms", 30)
	
	mouseJustPressed = 0
	mouseHeld = 0
	mouseJustRelease = 0
	
	joinButton = button.Button(10, 120, 100, 50, "Join", (0, 255 ,0), (255, 0 ,255))
	createButton = button.Button(10,240, 100, 50, "Create", (0, 255 ,0), (255, 0 ,255))
	sendMessageButton = button.Button(900, 800, 300, 50, "Send Message", (0, 255 ,0), (255, 0 ,255))
	disconnectButton=   button.Button(900, 700, 300, 50, "Disconnect", (0, 255 ,0), (255, 0 ,255))
	disconnectPressed = 0
	
	colourDatBox = 0
	
	enterPressed = 0
	textBox1 = textBox.TextBox((1*screen_width)/32, (4*screen_height)/5 + 10 + 40, 800, 100, '', (255, 255, 255), (23,128,0), '')
	
	serverConnectionBoxes = textBoxList.TextBoxList([])
	
	serverConnectionBoxes.addTextbox(textBox1)
	
	
	while 1==1:
		
		#Get mouse events:
		mouseJustPressed = 0
		mouseJustRelease = 0
		frameHasKeyboardEvent = 0
		
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
			
			elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				serverConnectionBoxes.dealWithKeyboard(event)
				frameHasKeyboardEvent = 1
				
				if serverConnectionBoxes.checkIfEnterPressed(event) == 1:
					enterPressed = 1
		
		mx,my = pygame.mouse.get_pos()
		
		
		if frameHasKeyboardEvent == 0:
			#textBox1.handleKeyboardButtonHeldDown()
			serverConnectionBoxes.handleKeyboardButtonHeldDown()
		
		#print the chatbox:
		connection.getChannelChatBox().printChat(screen)
		
		
		
		#textBox1.drawTextBox(screen)
		serverConnectionBoxes.drawTextBoxes(screen)
		
		if mouseJustRelease==1:
			serverConnectionBoxes.checkClickForTextBoxes(mx, my, 1)
		
		if enterPressed == 0:
			enterPressed = sendMessageButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		joinPressed =  joinButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		createPressed = createButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		if disconnectPressed == 0:
			disconnectPressed = disconnectButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		if enterPressed == 1:
			if len(textBox1.getCurrentText()) > 0:
				#Send whatever is in the chatbox to server:
				connection.sendMessageToServer(textBox1.getCurrentText()  + "\n")
				textBox1.setCurrentTextEmpty()
			
			enterPressed = 0
		
		#Enter join window:
		if joinPressed == 1:
			print 'Join pressed!'
			joinGameWindow.main('', ['from channelRoomGUI.py', connection])
		
		
		if createPressed == 1:
			print 'Create pressed!'
			createGameWindow.main('', ['from channelRoomGUI.py', connection])
		
		if disconnectPressed == 1:
			connection.sendMessageToServer("/disc" + "\n")
			
		
		#Print buttons:
		sendMessageButton.printButton(pygame, screen)
		joinButton.printButton(pygame, screen)
		createButton.printButton(pygame, screen)
		disconnectButton.printButton(pygame, screen)
		
		if round(time.time() * 1000)  - lastRefreshTime > USER_REFRESH_TIME:
			connection.sendMessageToServer("/refresh" + "\n")
			lastRefreshTime = round(time.time() * 1000)
	
		
		temp = connection.getNextServerMessageInQueue()
		
		
		#Print players in channel:
		for i in range(0, len(listOfPlayerInChannel)):
			myfont = pygame.font.SysFont("comicsansms", 25)
			label =  myfont.render(listOfPlayerInChannel[i], 1, (255, 255, 255))
			screen.blit(label, (1000, 30 + 30*i))
		
		if temp != '':
			if temp.endswith('\n'):
				temp = temp[0:-1]
				
			while temp.startswith('\n'):
				temp = temp[1:]
			
			#Receive answer from server: (sent /refresh message)...
			
			if temp.startswith(REFRESH_MSG):
				lines = temp.split('\n')
				foundListOfUsers = 0
				
				print 'Getting users:'
				listOfPlayerInChannel = []
				for line in lines:
					if foundListOfUsers == 1:
						listOfPlayerInChannel.append(line)
					elif line.startswith(PLAYERS_IN_CHANNEL_HEADER):
						listOfPlayerInChannel.append(line)
						foundListOfUsers = 1
						
				foundListOfUsers = 0
			
			elif temp.startswith(DISCONNECT) and disconnectPressed == 1:
				start.main('From channel room', ['start.py'])
			else:
				lines = temp.split('\n')
				for line in lines:
					connection.getChannelChatBox().setNewChatMessage(line)
			
		
		pygame.display.update()
		screen.fill(0)
		clock.tick(30)
		
	
PERIOD = 1000
SHOWCURSONTIME = 500
	

#Template for a blinking cursor that I didn't implement:
def shouldBlinkTextCursor():
	partOfCycle = round(time.time() * 1000) % PERIOD
	if partOfCycle < SHOWCURSONTIME:
		return 1
	else:
		return 0


if __name__ == "__main__":
	main('main thread', sys.argv)
	

#start server
#python channelRoomGUI.py