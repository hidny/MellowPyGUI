from pygame import _view
from pygame.locals import *

import pygame
import box
import time
import math
import textBox

#TODO: note down if shift is pressed or not and act accordingly.
#FIXME: if you hold tab, the repeat typed logic goes on...
#TODO: move connect to server button and make it work like pressing enter

class TextBoxList:
	listOfTextBoxes = []
	selectedBoxIndex = 0
	
	def __init__(self, listOfTextBoxes):
		self.listOfTextBoxes = listOfTextBoxes
	
	def addTextbox(self, textbox, index = -1):
		if len(self.listOfTextBoxes) == 0 or index == 0:
			for element in self.listOfTextBoxes:
				element.setUnFocussed()
			textbox.setFocussed()
		
		if index >=0:
			self.listOfTextBoxes.insert(index, textbox)
		else:
			self.listOfTextBoxes.append(textbox)
		
	def deleteTextBox(self, index = 0 ):
		self.listOfTextBoxes.remove(index)
		if self.selectedBoxIndex >= len(self.listOfTextBoxes):
			self.selectedBoxIndex = self.selectedBoxIndex - 1
	
	def drawTextBoxes(self, screen):
		for element in self.listOfTextBoxes:
			element.drawTextBox(screen)
		
	
	def checkClickForTextBoxes(self, x, y, mouseJustPressed):
		shouldFocusBasedOnMouse = 0
		for i in range (0, len(self.listOfTextBoxes)):
			shouldFocusBasedOnMouse = self.listOfTextBoxes[i].shouldFocusBasedOnMouse(x, y, mouseJustPressed)
			if shouldFocusBasedOnMouse == 1:
				self.selectedBoxIndex = i
				break
		
		if shouldFocusBasedOnMouse == 1:
			for element in self.listOfTextBoxes:
				element.updateFocusBasedOnMouse(x, y, mouseJustPressed)
				
			
		
	def dealWithShiftTextBox(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_TAB:
				self.shiftSelectedToNextBex()
	
	def shiftSelectedToNextBex(self):
		self.selectedBoxIndex = (self.selectedBoxIndex + 1) % len(self.listOfTextBoxes)
		for element in self.listOfTextBoxes:
			element.setUnFocussed()
		
		self.listOfTextBoxes[self.selectedBoxIndex].setFocussed()
	
	def shiftSelectedToPrevBox(self):
		self.selectedBoxIndex = (self.selectedBoxIndex - 1 + len(self.listOfTextBoxes) ) % len(self.listOfTextBoxes)
		for element in self.listOfTextBoxes:
			element.setUnFocussed()
		
		self.listOfTextBoxes[self.selectedBoxIndex].setFocussed()
	
	#TODO: test these
	def handleKeyboardButtonHeldDown(self):
		self.listOfTextBoxes[self.selectedBoxIndex].handleKeyboardButtonHeldDown()
	
	def dealWithKeyboard(self, event):
		self.dealWithShiftTextBox(event)
		self.listOfTextBoxes[self.selectedBoxIndex].dealWithKeyboard(event)
	
	def checkIfEnterPressed(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_KP_ENTER or  event.key == pygame.K_RETURN:
				return 1
		
		return 0
	
	def getText(self, index):
		return self.listOfTextBoxes[index].getCurrentText