from pygame import _view
from pygame.locals import *

import pygame
import box
import time
import math

class DropDown:
	
	
	
	def __init__(self, x, y, width, height, firstOptionText, labelColour, bkColour, listOfOptions):
		self.firstOptionBox = box.Box(x, y, width, height)
		
		self.labelColour = labelColour
		self.bkColour = bkColour
		self.firstOptionText = firstOptionText
		self.listOfOptions = listOfOptions
		self.isOpen = 0
		for i in range(0, len(self.listOfOptions)):
			if self.listOfOptions[i]  == firstOptionText:
				self.indexSelected = i
		
		
	def printDropDown(self, screen):
		if self.isOpen == 1:
			self.printOpen(screen)
		else:
			self.printClosed(screen)
	
	def printClosed(self, screen):
		#TODO: make this customizable.
		myfont = pygame.font.SysFont("comicsansms", 30)
		
		labelExample3 = myfont.render(str(self.firstOptionText), 1, self.labelColour)
		
		pygame.draw.rect(screen, (255,0,255), self.firstOptionBox.getCoordBox() )
		
		#TODO: draw triangle.
		
		pygame.draw.rect(screen, self.bkColour, self.firstOptionBox.getCoordBox() )
		
		#TODO: use X offset and y offset.
		screen.blit(labelExample3, (self.firstOptionBox.x, self.firstOptionBox.y))
		
		
	def printOpen(self, screen):
		#TODO: make this customizable.
		myfont = pygame.font.SysFont("comicsansms", 30)
		
		labelExample3 = myfont.render(str(self.firstOptionText), 1, self.labelColour)
		
		pygame.draw.rect(screen, (255,0,255), self.firstOptionBox.getCoordBox() )
		
		#TODO: use X offset and y offset ?? (REDO the logic)
		screen.blit(labelExample3, (self.firstOptionBox.getX(), self.firstOptionBox.getY()))
		
		y = self.firstOptionBox.getY()
		height = self.firstOptionBox.getHeight()
		
		tempBox = self.firstOptionBox
		for i in range(0, len(self.listOfOptions)):
		
			y = y + tempBox.getHeight()
			labelExample3 = myfont.render(str(self.listOfOptions[i]), 1, (255, 0, 255))
		
			tempBox = box.Box(tempBox.getX(), y, tempBox.getWidth(), height)
			
			if self.indexSelected != i:
				pygame.draw.rect(screen, (0,255,255), tempBox.getCoordBox() )
			else:
				pygame.draw.rect(screen, (0,0,255), tempBox.getCoordBox() )
			
			screen.blit(labelExample3, (tempBox.getX(), tempBox.getY()))
			
		
		#TODO: draw triangle.
		
		
	
	def updateSelected(self, mouseX, mouseY, screen):
		
		if self.isOpen == 1:
			y = self.firstOptionBox.getY()
			height = self.firstOptionBox.getHeight()
			
			tempBox = self.firstOptionBox
			for i in range(0, len(self.listOfOptions)):
			
				y = y + tempBox.getHeight()
				
				tempBox = box.Box(tempBox.getX(), y, tempBox.getWidth(), height)
				
				if tempBox.isWithinBox(mouseX, mouseY):
					self.indexSelected = i
					self.firstOptionText = self.listOfOptions[i]
					return
				
		
	
	def getSelectedLabel(self):
		if self.indexSelected >= 0:
			return self.listOfOptions[self.indexSelected]
		else:
			return ''
			
	def getIndexSelected(self):
		return self.indexSelected
		
	def updateClicked(self, mx, my, mouseReleased, screen):
		
		if mouseReleased == 1:
			if self.firstOptionBox.isWithinBox(mx, my) and self.isOpen == 0:
				self.isOpen = 1
			else:
				self.updateSelected(mx, my, screen)
				if self.getIndexSelected() >= 0:
					#TODO: return this so the gui class could do logic on it!
					print str(self.getSelectedLabel())
				
				self.isOpen = 0
				
	