#TODO: make the waiting room.
import sys, pygame
from pygame import _view
from pygame.locals import *
from sys import exit

import channelRoomGUI

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

def main(threadName, args):
	
	
	if len(args) > 1:
		connection = args[1]
		connection.setWaitingRoomChatBox(chatBox.chatBox(24, 100 ,20, 500))
		
	else:
		print 'AAAHAHAHA'
		exit(1)
		#TODO: put these vars in args...
		connection = clientContext.ClientContext('127.0.0.1', 6789, 'Doris')
		

	pygame.init()
	
	screen_width = 1300
	screen_height = 900
	USER_REFRESH_TIME = 2000
	lastRefreshTime = round(time.time() * 1000) - USER_REFRESH_TIME
	REFRESH_MSG = 'number of game rooms:'
	PLAYERS_IN_CHANNEL_HEADER = 'players in channel:'
	
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
	LEAVE_MESSAGE = 'number of game rooms:'
	
	joinButton = button.Button(10, 120, 100, 50, "WAITING ROOM!", (0, 255 ,0), (255, 0 ,255))
	createButton = button.Button(10,240, 100, 50, "Create", (0, 255 ,0), (255, 0 ,255))
	sendMessageButton = button.Button(900, 800, 300, 50, "Send Message", (0, 255 ,0), (255, 0 ,255))
	
	cancelButton =      button.Button(900, 700, 300, 50, "Cancel", (0, 255 ,0), (255, 0 ,255))
	
	colourDatBox = 0
	
	enterPressed = 0
	cancelPressed = 0
	waitingForLeaveMsg = 0
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
			
		#TODO: get the textbox that's focused on if possible, then update it!
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
		connection.getWaitingRoomChatBox().printChat(screen)
		
		
		#textBox1.drawTextBox(screen)
		serverConnectionBoxes.drawTextBoxes(screen)
		
		if mouseJustRelease==1:
			serverConnectionBoxes.checkClickForTextBoxes(mx, my, 1)
		
		if enterPressed == 0:
			enterPressed = sendMessageButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		joinPressed =  joinButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		createPressed = createButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		cancelPressed = cancelButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		if enterPressed == 1:
			if len(textBox1.getCurrentText()) > 0:
				#Send whatever is in the input box to server:
				connection.sendMessageToServer(textBox1.getCurrentText()  + "\n")
				textBox1.setCurrentTextEmpty()
			
			enterPressed = 0
		
		#Enter join window:
		if joinPressed == 1:
			print 'Join pressed!'
			#TODO: save chat box.
			joinGameWindow.main('', ['from channelRoomGUI.py', connection])
		
		
		if createPressed == 1:
			#TODO: save chat box and send to create window.'
			print 'Create pressed!'
			createGameWindow.main('', ['from channelRoomGUI.py', connection])
		
		#Print buttons:
		#TODO DELETE
		sendMessageButton.printButton(pygame, screen)
		joinButton.printButton(pygame, screen)
		createButton.printButton(pygame, screen)
		cancelButton.printButton(pygame, screen)
		
		
		
		if round(time.time() * 1000)  - lastRefreshTime > USER_REFRESH_TIME:
			connection.sendMessageToServer("/refresh" + "\n")
			lastRefreshTime = round(time.time() * 1000)
			print 'TESTING: ' + connection.getCurrentGameName()
	
		
		temp = connection.getNextServerMessageInQueue()
		
		
		#Print players in channel:
		for i in range(0, len(listOfPlayerInChannel)):
			myfont = pygame.font.SysFont("comicsansms", 25)
			label =  myfont.render(listOfPlayerInChannel[i], 1, (255, 255, 255))
			screen.blit(label, (1000, 30 + 30*i))
		
		if temp != '':
			if temp.endswith('\n'):
				temp = temp[0:-1]
				
			if temp.startswith('\n'):
				temp = temp[1:]
			
			#Receive answer from server: (sent /refresh message)...
			if waitingForLeaveMsg == 1 and temp.startswith(LEAVE_MESSAGE):
				channelRoomGUI.main('', ['from waitRoomWindow.py', connection])
			
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
			
			#TODO: make this react to the refresh message that shows the slots.
			elif temp.startswith(REFRESH_MSG):
				pass
			
			elif temp.startswith(connection.getCurrentGameName()):
				print 'REFRESH DUDE!'
				lines = temp.split('\n')
				host = lines[0].split(' ')[4][0:-1]
				print 'Host: ' + host
				numSlots = len(lines) - 1
				
				for x in range(0, numSlots):
					print 'Slot: ' + lines[1 + x].split(' ')[2]
			
			else:
				lines = temp.split('\n')
				for line in lines:
					connection.getWaitingRoomChatBox().setNewChatMessage(line)
			
		if cancelPressed == 1:
			connection.sendMessageToServer('/leave' + '\n')
			waitingForLeaveMsg = 1
		
		
		pygame.display.update()
		screen.fill(0)
		clock.tick(30)
		
	
PERIOD = 1000
SHOWCURSONTIME = 500
	

if __name__ == "__main__":
	main('main thread', sys.argv)
	

#start server
#python channelRoomGUI.py