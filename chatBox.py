from pygame import _view
from pygame.locals import *

import pygame
import sys
EMPTY_LINE = -1

class chatBox:

	
	
	#TODO: add more params to customize the chat.
	def __init__(self, numLines, x, y, xLimit):
		#OMG: https://docs.python.org/2/tutorial/classes.html
		self.listOfLines = []
		self.numLines = numLines
		for i in range(0, self.numLines):
			self.listOfLines.append(EMPTY_LINE)
		
		self.x = x
		self.y = y
		self.xLimit = xLimit
		self.currentIndex = 0
		
	   
	def printChat(self, screen):
		#pygame.draw.rect(screen, self.bkColour, self.box.getCoordBox() )
		pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.xLimit, self.y + 20 + 30*self.numLines) )
		
		myfont = pygame.font.SysFont("comicsansms", 25)
		for i in range(0, len(self.listOfLines)):
			if self.listOfLines[i] == EMPTY_LINE:
				pass
			else:
				#TODO: undo change
				label =  myfont.render(str(self.listOfLines[i]), 1, (255, 255, 255))
				screen.blit(label, (self.x + 20, self.y + 20 + 30*i))
				
		
	
	def printChatConsole(self):
		print '*************************'
		for i in range(0, len(self.listOfLines)):
			if self.listOfLines[i] == EMPTY_LINE:
				print ''
			else:
				print '' + str(self.listOfLines[i])
		print '*************************'
	
	def setNewChatMessage(self, msg):
		if(self.currentIndex >= self.numLines):
			for i in range(1, len(self.listOfLines)):
				self.listOfLines[i - 1] = self.listOfLines[i]
			self.listOfLines[self.numLines - 1] = msg
		else:
			#print str(self.currentIndex)
			#print str(self.listOfLines)
			
			self.listOfLines[self.currentIndex] = msg
			self.currentIndex = self.currentIndex + 1
	
	
def main(args):
	print 'What is up!'
	myBox = chatBox(30)
	print '1'
	myBox.printChatConsole()
	print '2'
	myBox.setNewChatMessage('hello')
	myBox.printChatConsole()
	myBox.setNewChatMessage('world')
	myBox.printChatConsole()
	myBox.setNewChatMessage('1')
	myBox.printChatConsole()
	myBox.setNewChatMessage('2')
	myBox.printChatConsole()
	myBox.setNewChatMessage('3')
	myBox.printChatConsole()
	myBox.setNewChatMessage('4')
	myBox.printChatConsole()
	myBox.setNewChatMessage('5')
	myBox.printChatConsole()
	myBox.setNewChatMessage('6')
	myBox.printChatConsole()
	myBox.setNewChatMessage('7')
	myBox.printChatConsole()
	
	for i in range(30):
		myBox.setNewChatMessage(str( i + 102))
	myBox.printChatConsole()
	

	
if __name__ == "__main__":
	main( sys.argv)