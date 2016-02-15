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
import clientContext

import joinGameWindow
import createGameWindow
#End for testing.

from pygame import _view
from pygame.locals import *

import dropDown
#import pygame
#import box
#import time
#import math


NOT_SELECTED = -1

class WaitingRoomPlayerList:
	
		def __init__(self, players, isHost):
		
			self.numSlots = len(players) - 1
			self.lines = players
			
			self.gameSlots = []
			self.indexSelected = NOT_SELECTED
			
			#if game slots defined...
			self.listWhatever = []
			#TODO: make a convincing list of options that are also available to the command line interface.
			self.listWhatever.append("one")
			self.listWhatever.append("two")
			self.listWhatever.append("three")
			
			for x in range(0, self.numSlots):
				#print 'Slot: ' + self.lines[1 + x].split(' ')[2]
				self.gameSlots.append(dropDown.DropDown(100, 100 + 100 * x, 300, 50, self.lines[1 + x].split(' ')[2], (0, 255 ,0), (255, 0 ,255),self.listWhatever, 0))
				
				
			
			self.selected = -1
		
		def printGameSlots(self, mx, my, screen):
			
			if self.indexSelected != NOT_SELECTED:
				self.gameSlots[self.indexSelected].updateSelected(mx, my, screen)
			
			for x in range(0, self.numSlots):
				#print 'Slot: ' + self.lines[1 + x].split(' ')[2]
				
				#go backwards so the the dropdowns won't cover each other in the wrong way:
				self.gameSlots[self.numSlots - 1 - x].printDropDown(screen)
				
		def clickEvent(self, mx, my, screen):
			
			if self.indexSelected != NOT_SELECTED:
				temp = self.gameSlots[self.indexSelected].updateClicked(mx, my, 1, screen)
				#reopen the slot So I could close it later. (outside updateClicked)
				if self.gameSlots[self.indexSelected].getIsOpen() == 0:
					self.gameSlots[self.indexSelected].open()
				
				if temp >=0:
					#print 'Pressed something!'
					#print self.gameSlots[self.indexSelected].listOfOptions[temp]
					self.gameSlots[self.indexSelected].close()
					self.indexSelected = NOT_SELECTED
					
					#TODO: Make the client talk to the server to service the commands!
					#DO IT HERE!
					return
			
			
			for x in range(0, self.numSlots):
				tempBox =  box.Box(100, 100 + 100 * x, 300, 50)
				
				if tempBox.isWithinBox(mx, my):
					
					#print 'You clicked a box!'
					
					for y in range(0, self.numSlots):
						if x != y:
							self.gameSlots[y].close()
						
					if self.gameSlots[x].getIsOpen() == 1:
						self.gameSlots[x].close()
						self.indexSelected = NOT_SELECTED
					else:
						self.gameSlots[x].open()
						self.indexSelected = x
						
					

def main(threadName, args):
	print 'I forgot how to python!'
	
	screen_width = 1300
	screen_height = 900
	size = width, height = screen_width, screen_height
	screen = pygame.display.set_mode(size)
	
	clock = pygame.time.Clock()
	
	createButton = button.Button(10,240, 100, 50, "Create", (0, 255 ,0), (255, 0 ,255))
	
	
	waitingList = WaitingRoomPlayerList( ["list of players:", "player slot: Michael", "player slot: Richard"], 0)
	
	pygame.init()
	
	
	while 1==1:
		
		#update mouse events:
		mouseJustRelease = 0
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
			
		mx,my = pygame.mouse.get_pos()
		
		if mouseJustRelease == 1:
			waitingList.clickEvent(mx, my, screen)
		
		pygame.draw.circle(screen, (255, 0, 255), (mx, my), 50)
		
		'''
		pygame.draw.circle(screen, (255, 0, 255), (screen_width - mx, my), 50)
		pygame.draw.circle(screen, (255, 0, 255), (mx, screen_height - my), 50)
		pygame.draw.circle(screen, (255, 0, 255), (screen_width - mx, screen_height - my), 50)
		'''
		createButton.printButton(pygame, screen)
		
		waitingList.printGameSlots(mx, my, screen)
		
		#print 'refresh'
		pygame.display.update()
		screen.fill(0)
		clock.tick(30)
		

if __name__ == "__main__":
	main('main thread', sys.argv)

		
	
	