#Made from a copy from channelRoomGUI:

import sys, pygame
from pygame import _view
from pygame.locals import *
from sys import exit

import time

import textBox
import textBoxList
import box
import button
import dropDown

import mellowGUI
import sys

import chatBox
import clientContext
import channelRoomGUI

import waitingRoomWindow

def main(threadName, args):
	
	if len(args) > 1:
		connection = args[1]
	else:
		connection = clientContext.ClientContext('127.0.0.1', 6789, 'Lenny')

	pygame.init()
	
	screen_width = 1300
	screen_height = 900
	
	USER_ERROR_MSG_TIME = 5000
	
	
	REFRESH_MSG = 'number of game rooms:'
	BADROOMNAME1 = 'ERROR: a game called'
	BADROOMNAME2 = 'already exists.'
	DIST_ABOVE_FIELD = 50
	
	
	listOfGamesInChannel = []
	
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
	
	createButton =        button.Button(900, 600, 300, 50, "Create", (0, 255 ,0), (255, 0 ,255))
	cancelButton =      button.Button(900, 700, 300, 50, "Cancel", (0, 255 ,0), (255, 0 ,255))
	
	enterPressed = 0
	
	roomNameTextBox = textBox.TextBox((21*screen_width)/32, (1*screen_height)/5, 350, 50, '', (255, 255, 255), (23,128,0), '')
	passwordTextBox = textBox.TextBox((21*screen_width)/32, (2*screen_height)/5, 350, 50, '', (255, 255, 255), (23,128,0), '')
	askForOtherNameStartTime = 0
	printAskForOtherRoomName = 0
	
	serverConnectionBoxes = textBoxList.TextBoxList([])
	
	serverConnectionBoxes.addTextbox(roomNameTextBox)
	serverConnectionBoxes.addTextbox(passwordTextBox)
	
	
	
	#List of game choices:
	#TODO: implement mellow, connectfour, and chess.
	list = []
	list.append("chess")
	list.append("connectfour")
	list.append("mellow")
	
	
	gameChoices = dropDown.DropDown(100, 300, 300, 50, "mellow", (0, 255 ,0), (255, 0 ,255),list)
	tryingToCreate = 0
	
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
				#textBox1.dealWithKeyboard(event)
				serverConnectionBoxes.dealWithKeyboard(event)
				frameHasKeyboardEvent = 1
				
				if serverConnectionBoxes.checkIfEnterPressed(event) == 1:
					enterPressed = 1
		
		
		mx,my = pygame.mouse.get_pos()
		
		
		#Take care of drop down:
		
		myfont = pygame.font.SysFont("comicsansms", 25)
		label =  myfont.render("Game name:", 1, (255, 255, 255))
		screen.blit(label, (100, 300 - DIST_ABOVE_FIELD))
		
		gameChoices.updateSelected(mx, my, screen)
		
		if mouseJustRelease == 1:
			gameChoices.updateClicked(mx, my, mouseJustRelease, screen)
			
		
		gameChoices.printDropDown(screen)
		#End take care of drop down.
		
		if frameHasKeyboardEvent == 0:
			serverConnectionBoxes.handleKeyboardButtonHeldDown()
		
		serverConnectionBoxes.drawTextBoxes(screen)
		
		if mouseJustRelease==1:
			serverConnectionBoxes.checkClickForTextBoxes(mx, my, 1)
		
		#Print buttons:
		if enterPressed == 0:
			enterPressed = createButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		cancelPressed = cancelButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		createButton.printButton(pygame, screen)
		cancelButton.printButton(pygame, screen)
		
		#Print gamename/password labels:
		myfont = pygame.font.SysFont("comicsansms", 25)
		label =  myfont.render("room name:", 1, (255, 255, 255))
		screen.blit(label, ((21*screen_width)/32, (1*screen_height)/5 - DIST_ABOVE_FIELD))
		label =  myfont.render("password:", 1, (255, 255, 255))
		screen.blit(label, ((21*screen_width)/32, (2*screen_height)/5 - DIST_ABOVE_FIELD))
		#End print gamename/password labels.
		
		#PRINT ERROR MSG:
		if printAskForOtherRoomName == 1:
			if round(time.time() * 1000) < askForOtherNameStartTime + USER_ERROR_MSG_TIME:
				myfont = pygame.font.SysFont("comicsansms", 25)
				label =  myfont.render("ERROR: The room name is already taken! ", 1, (255, 0, 0))
				screen.blit(label, ((19*screen_width)/32, (1*screen_height)/5 - 150))
			else:
				printAskForOtherRoomName = 0
		#END PRINT ERR MSG
		
		temp = connection.getNextServerMessageInQueue()
		
		if temp != '':
			if temp.endswith('\n'):
				temp = temp[0:-1]
				
			if temp.startswith('\n'):
				temp = temp[1:]
			
			#Receive answer from server: (sent /refresh message)...
			
			#Check if you're in game!
			if tryingToCreate == 1 and temp.startswith('Game created:'):
				#Move to game room as host.
				#AND go in as host.
				connection.setHost()
				connection.setCurrentGameName(gameChoices.getSelectedLabel())
				
				waitingRoomWindow.main('', ['from createGameWindow.py', connection])
			
			elif temp.startswith(BADROOMNAME1) and BADROOMNAME2 in temp:
				serverConnectionBoxes.shiftSelectedToIndex(0)
				printAskForOtherRoomName = 1
				askForOtherNameStartTime = round(time.time() * 1000)
				tryingToCreate = 0
			
			elif temp.startswith(REFRESH_MSG):
				#Do nothing:
				pass
				
			else:
				lines = temp.split('\n')
				for line in lines:
					connection.getChannelChatBox().setNewChatMessage(line)
			
		
		
		if enterPressed == 1:
			if gameChoices.getSelectedLabel() != '':
				connection.sendMessageToServer('/create ' + gameChoices.getSelectedLabel() + ' ' + roomNameTextBox.getCurrentText() + ' ' + passwordTextBox.getCurrentText() + '\n')
				
				tryingToCreate = 1
			else:
				pass
			enterPressed = 0
		
		
		if cancelPressed == 1:
			channelRoomGUI.main('', ['from createGameWindow.py', connection])
			cancelPressed = 0
		
		pygame.display.update()
		screen.fill(0)
		clock.tick(30)


if __name__ == "__main__":
	main('main', sys.argv)
	

#start server
#python channelRoomGUI.py