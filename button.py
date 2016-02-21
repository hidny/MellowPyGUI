from pygame import _view
from pygame.locals import *



class Button:
	
	def __init__(self, x, y, width, heigth, labelMessage, labelColour, bkColour):
		self.x = x
		self.y = y
		self.width = width
		self.heigth = heigth
		
		self.labelMessage = labelMessage
		self.labelColour = labelColour
		self.colour = bkColour
		
		self.label = 0
		
		self.isFocussed = 0
		self.isPressedDown = 0
		self.pressTime = 0
	
	def getTopLeftBox(self):
		return (self.x, self.y)
	
	def getCoordBox(self):
		return (self.x, self.y, self.width, self.heigth)
	
	def isWithinBox(self, x, y):
		if x >= self.x and x<= self.x + self.width:
			if y >= self.y and y <= self.y + self.heigth:
				return 1
		
		return 0
	
	def updateButtonAndCheckIfPressed(self, x, y, mouseJustPressed, mouseJustRelease):
		if self.isWithinBox(x, y) == 0:
			self.isFocussed = 0
			self.isPressedDown = 0
		else:
			self.isFocussed = 1
			if mouseJustPressed == 1:
				self.isPressedDown = 1
		
		if mouseJustRelease == 1 and self.isFocussed == 1 and self.isPressedDown == 1 and self.isWithinBox(x, y) == 1:
			self.isPressedDown = 0
			return 1
		else:
			if  mouseJustRelease == 1:
				self.isPressedDown = 0
			return 0
		
	def printButton(self, pygame, screen):
		if self.isPressedDown == 1:
			pygame.draw.rect(screen, (0, 0, 0), self.getCoordBox())
		else:
			pygame.draw.rect(screen, self.colour, self.getCoordBox())
		
		BUTTON_FONT = pygame.font.SysFont("comicsansms", 30)
		labelExample = BUTTON_FONT.render(self.labelMessage, 1, self.labelColour)
		screen.blit(labelExample, self.getTopLeftBox())
		