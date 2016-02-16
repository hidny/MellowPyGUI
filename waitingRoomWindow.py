#For testing:
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

import joinGameWindow
import createGameWindow
#End for testing.

from pygame import _view
from pygame.locals import *

import dropDown

import clientContext
import channelRoomGUI
#import pygame
#import box
#import time
#import math


NOT_SELECTED = -1

class WaitingRoomPlayerList:
	
		def __init__(self, players, textbox, connection):
			
			self.connection = connection
			
			self.gameSlots = []
			self.indexSelected = NOT_SELECTED
			self.textbox = textbox
			
			self.listEmptySlot = []
			self.listPlayerSlot = []
			
			#TODO: change the server to allow the host to swap players.
			
			if connection.isHosting() == 1:
			#TODO: make a convincing list of options that are also available to the command line interface.
				self.listEmptySlot.append("Open")
				self.listEmptySlot.append("Close")
				self.listPlayerSlot.append("Open")
				self.listPlayerSlot.append("Close")
			
			self.listEmptySlot.append("Move")
			self.listPlayerSlot.append("Whisper")
			
			for x in range(0, len(players)):
				if players[x] == 'Open' or players[x] == 'Close':
					listToUse = self.listEmptySlot
				else:
					listToUse = self.listPlayerSlot
				self.gameSlots.append(dropDown.DropDown(200, 100 + 100 * x, 300, 50, players[x], (0, 255 ,0), (255, 0 ,255), listToUse, 0))
				
			self.selected = -1
		
		def printGameSlots(self, mx, my, screen):
			
			if self.indexSelected != NOT_SELECTED:
				self.gameSlots[self.indexSelected].updateSelected(mx, my, screen)
			
			for x in range(0, len(self.gameSlots)):
				#go backwards so the the dropdowns won't cover each other in the wrong way:
				self.gameSlots[len(self.gameSlots) - 1 - x].printDropDown(screen)
		
		#pre: len(players) == len(self.gameSlots)
		def updatePlayerList(self, players):
		
			if len(players) != len(self.gameSlots):
				print 'ERROR: number of slots is inconsistant!'
				print str(len(players)) + ' vs ' + str(len(self.gameSlots))
				exit(1)
			
				
			if players[self.indexSelected] != self.gameSlots[self.indexSelected].getMainText():
				self.indexSelected = NOT_SELECTED
			
			for x in range(0, len(players)):
				if players[x] != self.gameSlots[x].getMainText():
					if players[x] == 'Open' or players[x] == 'Closed':
						listToUse = self.listEmptySlot
					else:
						listToUse = self.listPlayerSlot
					self.gameSlots[x] = dropDown.DropDown(200, 100 + 100 * x, 300, 50, players[x], (0, 255 ,0), (255, 0 ,255),listToUse, 0)
				
			
		def clickEvent(self, mx, my, screen):
			
			if self.indexSelected != NOT_SELECTED:
				temp = self.gameSlots[self.indexSelected].updateClicked(mx, my, 1, screen)
				#reopen the slot So I could close it later. (outside updateClicked)
				if self.gameSlots[self.indexSelected].getIsOpen() == 0:
					self.gameSlots[self.indexSelected].open()
				
				if temp >=0:
					#print 'Pressed something!'
					#print self.gameSlots[self.indexSelected].listOfOptions[temp]
					textPressed = self.gameSlots[self.indexSelected].listOfOptions[temp]
					if textPressed == 'Open':
						if self.gameSlots[self.indexSelected].getMainText() == 'Closed' or self.gameSlots[self.indexSelected].getMainText() == 'Open' :
							self.connection.sendMessageToServer("/open " + str(self.indexSelected + 1) + "\n")
						else:
							self.connection.sendMessageToServer("/kick " + self.gameSlots[self.indexSelected].getMainText() + "\n")
							#TODO: Warning: my server might not be able to handle 2 messages at once:
							self.connection.sendMessageToServer("/open " + str(self.indexSelected + 1)  + "\n")
					
					if textPressed == 'Close':
						if self.gameSlots[self.indexSelected].getMainText() == 'Closed' or self.gameSlots[self.indexSelected].getMainText() == 'Open' :
							self.connection.sendMessageToServer("/close " + str(self.indexSelected + 1) + "\n")
						else:
							self.connection.sendMessageToServer("/kick " + self.gameSlots[self.indexSelected].getMainText() + "\n")
							#TODO: Warning: my server might not be able to handle 2 messages at once:
							self.connection.sendMessageToServer("/close " + str(self.indexSelected + 1)  + "\n")
					
					if textPressed == 'Whisper':
						self.textbox.setCurrentText("/m " + self.gameSlots[self.indexSelected].getMainText() + " ")
					
					if textPressed == 'Move':
						self.connection.sendMessageToServer("/move " + str(self.indexSelected + 1) + "\n")
					
					self.gameSlots[self.indexSelected].close()
					self.indexSelected = NOT_SELECTED
					
					#TODO: Make the client talk to the server to service the commands!
					#TODO: some options don't make sense like moving into closed slot
					#Or reopeing slot.
					
					#DO IT HERE!
					return
			
			
			for x in range(0, len(self.gameSlots)):
				tempBox =  box.Box(200, 100 + 100 * x, 300, 50)
				
				if tempBox.isWithinBox(mx, my):
					#print 'You clicked a box!'
					
					for y in range(0, len(self.gameSlots)):
						if x != y:
							self.gameSlots[y].close()
						
					if self.gameSlots[x].getIsOpen() == 1:
						self.gameSlots[x].close()
						self.indexSelected = NOT_SELECTED
					else:
						self.gameSlots[x].open()
						self.indexSelected = x
						
						
def main(threadName, args):
	
	if len(args) > 1:
		connection = args[1]
	else:
		#TODO: put these vars in args...
		connection = clientContext.ClientContext('127.0.0.1', 6789, 'Doris')
		
		#The extremely lame chatbox.
		#TODO: be able to initialize more variables to declare it.
		connection.sendMessageToServer("/create mellow test" + "\n")
		connection.setCurrentGameName("mellow")
		connection.setHost()
	
	connection.setWaitingRoomChatBox(chatBox.chatBox(24, 500 ,20, 200))
	
	screen_width = 1300
	screen_height = 900
	USER_REFRESH_TIME = 2000
	lastRefreshTime = round(time.time() * 1000) - USER_REFRESH_TIME
	size = width, height = screen_width, screen_height
	screen = pygame.display.set_mode(size)
	
	
	
	FIRST_MSG_TO_IGNORE = 'Game created:'
	BANNED_MSG = 'You have been banned from the game.'
	waitingForLeaveMsg = 0
	waitingForGameMessage = 0
	LEAVE_MESSAGE = 'number of game rooms:'
	
	
	
	
	clock = pygame.time.Clock()
	pygame.init()
	
	#TODO: put the user textbox init into a utility function.
	textBox1 = textBox.TextBox((1*screen_width)/32, (4*screen_height)/5 + 10 + 40, 800, 100, '', (255, 255, 255), (23,128,0), '')
	sendMessageButton = button.Button(900, 800, 300, 50, "Send Message", (0, 255 ,0), (255, 0 ,255))
	cancelButton =      button.Button(900, 700, 300, 50, "Cancel", (0, 255 ,0), (255, 0 ,255))
	startButton =       button.Button(900, 600, 300, 50, "Start", (0, 255 ,0), (255, 0 ,255))
	
	waitingList = WaitingRoomPlayerList( ["Michael", "Richard", "Open", "Open"], textBox1, connection)
	
	serverConnectionBoxes = textBoxList.TextBoxList([])
	serverConnectionBoxes.addTextbox(textBox1)

	while 1==1:
		
		#React to user events:
		enterPressed = 0
		cancelPressed = 0
		mouseJustRelease = 0
		mouseJustPressed = 0
		frameHasKeyboardEvent = 0
		startPressed = 0
		
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
		
		if enterPressed == 0:
			enterPressed = sendMessageButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		if enterPressed == 1:
			if len(textBox1.getCurrentText()) > 0:
				#Send whatever is in the chatbox to server:
				connection.sendMessageToServer(textBox1.getCurrentText()  + "\n")
				textBox1.setCurrentTextEmpty()
			
			enterPressed = 0
		
		cancelPressed = cancelButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		if connection.isHosting() == 1:
			startPressed   = startButton.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		if mouseJustRelease == 1:
			waitingList.clickEvent(mx, my, screen)
		
		if cancelPressed == 1:
			connection.sendMessageToServer('/leave' + '\n')
			waitingForLeaveMsg = 1
		
		if connection.isHosting() == 1 and startPressed == 1:
			connection.sendMessageToServer('/start' + '\n')
			waitingForGameMessage = 1
		#END React to user events:
		
		#Print Stuff:
		connection.getWaitingRoomChatBox().printChat(screen)
		
		serverConnectionBoxes.drawTextBoxes(screen)
		
		sendMessageButton.printButton(pygame, screen)
		
		cancelButton.printButton(pygame, screen)
		
		if connection.isHosting() == 1:
			startButton.printButton(pygame, screen)
		
		pygame.draw.circle(screen, (255, 0, 255), (mx, my), 5)
		
		waitingList.printGameSlots(mx, my, screen)
		
		#End print stuff.
		
		#React to server messages:
		#Copied from channel Room GUI:
		#Code to get response from server:
		temp = connection.getNextServerMessageInQueue()
		
		if temp != '':
			if temp.endswith('\n'):
				temp = temp[0:-1]
				
			while temp.startswith('\n'):
				temp = temp[1:]
			
			if waitingForLeaveMsg == 1 and temp.startswith(LEAVE_MESSAGE):
				channelRoomGUI.main('', ['from waitRoomPWindow.py', connection])
				
			#Receive answer from server: (sent /refresh message)...
			elif temp.startswith(FIRST_MSG_TO_IGNORE):
				print 'Skip it!'
			
			elif temp.startswith(BANNED_MSG):
				waitingForLeaveMsg = 1
				
			elif temp.startswith(connection.getCurrentGameName()):
				print 'REFRESH DUDE!'
				
				#Parse refresh message to get info about who's waiting and who's host:
				lines = temp.split('\n')
				host = lines[0].split(' ')[4][0:-1]
				print 'Host: ' + host
				numSlots = len(lines) - 1
				
				listOfPlayers = []
				for x in range(0, numSlots):
					listOfPlayers.append(lines[1 + x].split(' ')[2])
				
				#Call waiting list to update list of players waiting:
				waitingList.updatePlayerList(listOfPlayers)
				
				
			else:
				lines = temp.split('\n')
				for line in lines:
					connection.getWaitingRoomChatBox().setNewChatMessage(line)
		
		
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
	main('main thread', sys.argv)

		
	
	