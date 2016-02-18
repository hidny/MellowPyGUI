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
		#TODO: put these vars in args...
		connection = clientContext.ClientContext('127.0.0.1', 6789, 'Moe')

	pygame.init()
	
	screen_width = 1300
	screen_height = 900
	
	USER_PASSWORD_MSG_TIME = 5000
	
	USER_REFRESH_TIME = 2000
	lastRefreshTime = round(time.time() * 1000) - USER_REFRESH_TIME
	REFRESH_MSG = 'number of game rooms:'
	PLAYERS_IN_CHANNEL_HEADER = 'players in channel:'
	BADPASSWORD = 'ERROR: Bad password.'
	ERROR = 'ERROR:'
	
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
	
	joinButton =        button.Button(900, 600, 300, 50, "Join", (0, 255 ,0), (255, 0 ,255))
	cancelButton =      button.Button(900, 700, 300, 50, "Cancel", (0, 255 ,0), (255, 0 ,255))
	
	enterPressed = 0
	
	roomNameTextBox = textBox.TextBox((21*screen_width)/32, (1*screen_height)/5, 350, 50, '', (255, 255, 255), (23,128,0), '')
	passwordTextBox = textBox.TextBox((21*screen_width)/32, (2*screen_height)/5, 350, 50, '', (255, 255, 255), (23,128,0), '')
	errorMessageDisplayStart = 0
	printAskForPassword = 0
	printError = 0
	
	serverConnectionBoxes = textBoxList.TextBoxList([])
	
	serverConnectionBoxes.addTextbox(roomNameTextBox)
	serverConnectionBoxes.addTextbox(passwordTextBox)
	
	tryingToJoin = 0
	tryingToJoinRoom = ''
	
	while 1==1:
		
		#React to user events:
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
			serverConnectionBoxes.handleKeyboardButtonHeldDown()
		
		
		if mouseJustRelease==1:
			serverConnectionBoxes.checkClickForTextBoxes(mx, my, 1)
		
		serverConnectionBoxes.drawTextBoxes(screen)
		
		
		if enterPressed == 0:
			enterPressed = joinButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		if enterPressed == 1:
			tryingToJoinRoom = roomNameTextBox.getCurrentText()
			connection.sendMessageToServer('/join ' + tryingToJoinRoom + ' ' + passwordTextBox.getCurrentText() + '\n')
			enterPressed = 0
			tryingToJoin = 1
		
		
		cancelPressed = cancelButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		if cancelPressed == 1:
			channelRoomGUI.main('', ['from joinGameWindow.py', connection])
			cancelPressed = 0
		
		
		#END React to user events:
		
		#Print Stuff:
		
		joinButton.printButton(pygame, screen)
		cancelButton.printButton(pygame, screen)
		
		
	
		#Print gamename/password labels:
		myfont = pygame.font.SysFont("comicsansms", 25)
		label =  myfont.render("room name:", 1, (255, 255, 255))
		screen.blit(label, ((21*screen_width)/32, (1*screen_height)/5 - 50))
		label =  myfont.render("password:", 1, (255, 255, 255))
		screen.blit(label, ((21*screen_width)/32, (2*screen_height)/5 - 50))
		#End print gamename/password labels.
		
		#PRINT ERROR MSG:
		if printAskForPassword == 1:
			if round(time.time() * 1000) < errorMessageDisplayStart + USER_PASSWORD_MSG_TIME:
				myfont = pygame.font.SysFont("comicsansms", 25)
				label =  myfont.render("Please Enter Password!", 1, (255, 0, 0))
				screen.blit(label, ((21*screen_width)/32, (1*screen_height)/5 - 150))
			else:
				printAskForPassword = 0
		elif printError == 1:
			if round(time.time() * 1000) < errorMessageDisplayStart + USER_PASSWORD_MSG_TIME:
				myfont = pygame.font.SysFont("comicsansms", 25)
				label =  myfont.render("Error trying to join the game.", 1, (255, 0, 0))
				screen.blit(label, ((21*screen_width)/32, (1*screen_height)/5 - 150))
			else:
				printError = 0
		#END PRINT ERR MSG
		
		
		#Print open games in channel:
		for i in range(0, len(listOfGamesInChannel)):
			myfont = pygame.font.SysFont("comicsansms", 25)
			label =  myfont.render(listOfGamesInChannel[i], 1, (255, 255, 255))
			screen.blit(label, (100, 30 + 30*i))
		
			if i > 0:
				if mouseJustRelease == 1:
					if mx > 100 and mx < 800 and my > 30 + 30*i and my < 30 + 30*i + 30:
						print 'BUTTON pressed: ' + str(i)
						roomNameTextBox.setCurrentText(listOfGamesInChannel[i].split(' ')[1] )
						connection.sendMessageToServer('/join ' + roomNameTextBox.getCurrentText() + ' ' + passwordTextBox.getCurrentText() + '\n')
			else:
				if mouseJustRelease == 1:
					if mx > 100 and mx < 800 and my > 30 + 30*i and my < 30 + 30*i + 30:
						print 'Pressed number of games message.'
		
		#End print stuff.
		
		#React to server messages:
		temp = connection.getNextServerMessageInQueue()
		
		if temp != '':
			if temp.endswith('\n'):
				temp = temp[0:-1]
				
			if temp.startswith('\n'):
				temp = temp[1:]
			
			#Receive answer from server: (sent /refresh message)...
			
			#check if you're in game!
			if tryingToJoin == 1 and temp.startswith('Game joined:'):
				#TODO: move to game room as joiner
				connection.setJoiner()
				
				connection.setCurrentGameName(roomToGameDict[tryingToJoinRoom])
				
				waitingRoomWindow.main('', ['from createGameWindow.py', connection])
				
			if temp.startswith(BADPASSWORD):
				serverConnectionBoxes.shiftSelectedToIndex(1)
				printAskForPassword = 1
				printError = 0
				errorMessageDisplayStart = round(time.time() * 1000)
				tryingToJoin = 0
			
			elif temp.startswith(ERROR):
				printError = 1
				printAskForPassword = 0
				errorMessageDisplayStart = round(time.time() * 1000)
				tryingToJoin = 0
				
			elif temp.startswith(REFRESH_MSG):
				lines = temp.split('\n')
				foundListOfUsers = 0
				
				roomToGameDict = {};
				
				#print 'Getting game room waiting for players:'
				listOfGamesInChannel = []
				
				for line in lines:
					if foundListOfUsers == 1 and line.strip(' ') == '':
						break
					elif foundListOfUsers == 1 or line.startswith(REFRESH_MSG):
						if line.startswith(REFRESH_MSG):
							foundListOfUsers = 1
						
						listOfGamesInChannel.append(line)
						
						roomToGameDict[line.split(' ')[1]] = line.split(' ')[0][0:-1]
						
						
				foundListOfUsers = 0
			
			else:
				print 'DEBUG: ' + temp
				#lines = temp.split('\n')
				#for line in lines:
				#	connection.getChannelChatBox().setNewChatMessage(line)
			
		
		#End React to server messages
		
		
		#Ask server for a periodic update.
		if round(time.time() * 1000)  - lastRefreshTime > USER_REFRESH_TIME:
			connection.sendMessageToServer("/refresh" + "\n")
			lastRefreshTime = round(time.time() * 1000)
		#end ask server for a periodic update.
		
		pygame.display.update()
		screen.fill(0)
		clock.tick(30)


if __name__ == "__main__":
	main('main', sys.argv)
	

#start server
#python channelRoomGUI.py