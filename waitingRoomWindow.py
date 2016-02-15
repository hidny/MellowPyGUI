#TODO: make the waiting room.
import sys, pygame
from pygame import _view
from pygame.locals import *
from sys import exit

import channelRoomGUI

import time

import dropDown
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
		connection.setWaitingRoomChatBox(chatBox.chatBox(24, 400 ,20, 500))
		
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
	
	
	gameSlots = []
	sendMessageButton = button.Button(900, 800, 300, 50, "Send Message", (0, 255 ,0), (255, 0 ,255))
	
	cancelButton =      button.Button(900, 700, 300, 50, "Cancel", (0, 255 ,0), (255, 0 ,255))
	
	colourDatBox = 0
	
	enterPressed = 0
	cancelPressed = 0
	waitingForLeaveMsg = 0
	textBox1 = textBox.TextBox((1*screen_width)/32, (4*screen_height)/5 + 10 + 40, 800, 100, '', (255, 255, 255), (23,128,0), '')
	
	serverConnectionBoxes = textBoxList.TextBoxList([])
	
	serverConnectionBoxes.addTextbox(textBox1)
	
	gameSlots = []
	
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
		
		cancelPressed = cancelButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		if enterPressed == 1:
			if len(textBox1.getCurrentText()) > 0:
				#Send whatever is in the input box to server:
				connection.sendMessageToServer(textBox1.getCurrentText()  + "\n")
				textBox1.setCurrentTextEmpty()
			
			enterPressed = 0
		
		#Print slots:
		#TODO: please put this into a function...
		
		
		opened = -1
		for i in range(0, len(gameSlots)):
			if gameSlots[i].getIsOpen() == 1:
				opened = i
			elif opened >= 0:
				gameSlots[i].close()
		
		for i in range(0, len(gameSlots)):
			if i != opened:
				gameSlots[i].printDropDown(screen)
		
		if opened >= 0:
			gameSlots[i].printDropDown(screen)
		
		
		for i in range(0, len(gameSlots)):
			playerName = gameSlots[i].getMainText()
			
			gameSlots[i].updateSelected(mx, my, screen)
			
			ret = gameSlots[i].updateClicked(mx, my, mouseJustRelease, screen)
			
			if ret >= 0:
				if opened >= 0:
					print 'AHAHA!'
					exit(1)
					gameSlots[opened].close()
					gameSlots[ret].open()
			
			
			gameSlots[i].setMainText(playerName)
			
			if ret != -1:
				break
			
			#IF drop down open, close the other drop downs!
			#TODO: Make the functions that react to client wishes here.
			#TODO2: show the open slots first. ( don't cover the open drop downs.)
		
		
		#END TODO
		
		sendMessageButton.printButton(pygame, screen)
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
			
			
			elif temp.startswith(connection.getCurrentGameName()):
				print 'REFRESH DUDE!'
				
				lines = temp.split('\n')
				host = lines[0].split(' ')[4][0:-1]
				print 'Host: ' + host
				numSlots = len(lines) - 1
				
				createSlots = 0
				if len(gameSlots) == 0:
					createSlots = 1
					
				#if game slots defined...
				listWhatever = []
				listWhatever.append("one")
				listWhatever.append("two")
				listWhatever.append("three")
				for x in range(0, numSlots):
					print 'Slot: ' + lines[1 + x].split(' ')[2]
					if createSlots == 1:
						gameSlots.append(dropDown.DropDown(100, 100 + 100 * x, 300, 50, lines[1 + x].split(' ')[2], (0, 255 ,0), (255, 0 ,255),listWhatever))
					else:
						gameSlots[x].setMainText(lines[1 + x].split(' ')[2])
					
				
				
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