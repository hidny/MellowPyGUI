from pygame import _view
from pygame.locals import *

import pygame
import box
import time
import math

#For now: the deletion rate = repeating rate.
#I hope I don't have to change that.

# ?? don't appear. Why not?

#wait REPEAT_DELAY_TIME to start repeating the same character.
REPEAT_DELAY_TIME = 500
#wait REPEAT_PERIOD between 
REPEAT_PERIOD = 20

class TextBox:
	
	def __init__(self, x, y, width, height, currentText, labelColour, bkColour, text = ''):
		self.box = box.Box(x, y, width, height)
		
		self.currentText = currentText
		self.labelColour = labelColour
		self.bkColour = bkColour
		self.currentText = text
		
		self.isFocussed = 0
		self.isPressedDown = 0
		
		self.isKeyHeldDown = 0
		self.isDeletingText = 0
		self.numRepeatedCharacters = 0
		self.timePressed = 0
		self.currentKeyPressed = 0
			
	
	def getTopLeftBox(self):
		return self.box.getTopLeftBox(self.x, self.y)
	
	def getCoordBox(self):
		return self.box.getCoordBox()
	
	def isWithinBox(self, x, y):
		return self.box.isWithinBox(x, y)
	
	#TODO: have a variable for the currently selected textbox.
	def shouldFocusBasedOnMouse(self, x, y, mouseJustPressed):
		if mouseJustPressed == 1:
			if self.isWithinBox(x, y) == 1:
				return 1
			else:
				return 0
	
	def updateFocusBasedOnMouse(self, x, y, mouseJustPressed):
		if mouseJustPressed == 1:
			if self.isWithinBox(x, y) == 1:
				self.setFocussed()
			else:
				self.setUnFocussed()
			
	
	#TODO: autoprint and auto delete when button is held.
	def dealWithKeyboard(self, event):
		
		#Check if a button was pressed down for the first time:
		if event.type == pygame.KEYDOWN:
			if pygame.key.get_mods() & pygame.KMOD_LSHIFT or pygame.key.get_mods() & pygame.KMOD_RSHIFT:
				if event.key == pygame.K_a:
					self.currentText = self.currentText + 'A'
				if event.key == pygame.K_b:
					self.currentText = self.currentText + 'B'
				if event.key == pygame.K_c:
					self.currentText = self.currentText + 'C'
				if event.key == pygame.K_d:
					self.currentText = self.currentText + 'D'
				if event.key == pygame.K_e:
					self.currentText = self.currentText + 'E'
				
				if event.key == pygame.K_f:
					self.currentText = self.currentText + 'F'
				if event.key == pygame.K_g:
					self.currentText = self.currentText + 'G'
				if event.key == pygame.K_h:
					self.currentText = self.currentText + 'H'
				if event.key == pygame.K_i:
					self.currentText = self.currentText + 'I'
				if event.key == pygame.K_j:
					self.currentText = self.currentText + 'J'
				
				if event.key == pygame.K_k:
					self.currentText = self.currentText + 'K'
				if event.key == pygame.K_l:
					self.currentText = self.currentText + 'L'
				if event.key == pygame.K_m:
					self.currentText = self.currentText + 'M'
				if event.key == pygame.K_n:
					self.currentText = self.currentText + 'N'
				if event.key == pygame.K_o:
					self.currentText = self.currentText + 'O'
				
				if event.key == pygame.K_p:
					self.currentText = self.currentText + 'P'
				if event.key == pygame.K_q:
					self.currentText = self.currentText + 'Q'
				if event.key == pygame.K_r:
					self.currentText = self.currentText + 'R'
				if event.key == pygame.K_s:
					self.currentText = self.currentText + 'S'
				if event.key == pygame.K_t:
					self.currentText = self.currentText + 'T'
				
				if event.key == pygame.K_u:
					self.currentText = self.currentText + 'U'
				if event.key == pygame.K_v:
					self.currentText = self.currentText + 'V'
				if event.key == pygame.K_w:
					self.currentText = self.currentText + 'W'
				if event.key == pygame.K_x:
					self.currentText = self.currentText + 'X'
				if event.key == pygame.K_y:
					self.currentText = self.currentText + 'Y'
				if event.key == pygame.K_z:
					self.currentText = self.currentText + 'Z' 
					
				
				if event.key == pygame.K_0:
					self.currentText = self.currentText + ')' 
				if event.key == pygame.K_1:
					self.currentText = self.currentText + '!' 
				if event.key == pygame.K_2:
					self.currentText = self.currentText + '@' 
				if event.key == pygame.K_3:
					self.currentText = self.currentText + '#' 
				if event.key == pygame.K_4:
					self.currentText = self.currentText + '$' 
				if event.key == pygame.K_5:
					self.currentText = self.currentText + '%' 
				if event.key == pygame.K_6:
					self.currentText = self.currentText + '^' 
				if event.key == pygame.K_7:
					self.currentText = self.currentText + '&' 
				if event.key == pygame.K_8:
					self.currentText = self.currentText + '*' 
				if event.key == pygame.K_9:
					self.currentText = self.currentText + '('
				
				if event.key == pygame.K_MINUS:
					self.currentText = self.currentText + '_'
					
				if event.key == pygame.K_PLUS:
					self.currentText = self.currentText + '='
					
					
				if event.key == pygame.K_COMMA:
					self.currentText = self.currentText + '<'
				if event.key == pygame.K_PERIOD:
					self.currentText = self.currentText + '>'
				if event.key == K_SEMICOLON:
					self.currentText = self.currentText + ':'
				
				if event.key == K_BACKSLASH:
					self.currentText = self.currentText + '|'
				
				if event.key == K_SLASH:
					self.currentText = self.currentText + '?'
				
				if event.key == K_BACKQUOTE:
					self.currentText = self.currentText + '~'
				
				
				if event.key == K_LEFTBRACKET:
					self.currentText = self.currentText + '{'
				
				if event.key == K_RIGHTBRACKET:
					self.currentText = self.currentText + '}'
				
				if event.key == K_QUOTE:
					self.currentText = self.currentText + '"'
				
			else:
				#self.isKeyHeldDown == 0 or self.currentKeyPressed != event.key:
				if event.key == pygame.K_a:
					self.currentText = self.currentText + 'a'
				if event.key == pygame.K_b:
					self.currentText = self.currentText + 'b'
				if event.key == pygame.K_c:
					self.currentText = self.currentText + 'c'
				if event.key == pygame.K_d:
					self.currentText = self.currentText + 'd'
				if event.key == pygame.K_e:
					self.currentText = self.currentText + 'e'
				
				if event.key == pygame.K_f:
					self.currentText = self.currentText + 'f'
				if event.key == pygame.K_g:
					self.currentText = self.currentText + 'g'
				if event.key == pygame.K_h:
					self.currentText = self.currentText + 'h'
				if event.key == pygame.K_i:
					self.currentText = self.currentText + 'i'
				if event.key == pygame.K_j:
					self.currentText = self.currentText + 'j'
				
				if event.key == pygame.K_k:
					self.currentText = self.currentText + 'k'
				if event.key == pygame.K_l:
					self.currentText = self.currentText + 'l'
				if event.key == pygame.K_m:
					self.currentText = self.currentText + 'm'
				if event.key == pygame.K_n:
					self.currentText = self.currentText + 'n'
				if event.key == pygame.K_o:
					self.currentText = self.currentText + 'o'
				
				if event.key == pygame.K_p:
					self.currentText = self.currentText + 'p'
				if event.key == pygame.K_q:
					self.currentText = self.currentText + 'q'
				if event.key == pygame.K_r:
					self.currentText = self.currentText + 'r'
				if event.key == pygame.K_s:
					self.currentText = self.currentText + 's'
				if event.key == pygame.K_t:
					self.currentText = self.currentText + 't'
				
				if event.key == pygame.K_u:
					self.currentText = self.currentText + 'u'
				if event.key == pygame.K_v:
					self.currentText = self.currentText + 'v'
				if event.key == pygame.K_w:
					self.currentText = self.currentText + 'w'
				if event.key == pygame.K_x:
					self.currentText = self.currentText + 'x'
				if event.key == pygame.K_y:
					self.currentText = self.currentText + 'y'
				if event.key == pygame.K_z:
					self.currentText = self.currentText + 'z' 
					
				
				if event.key == pygame.K_0:
					self.currentText = self.currentText + '0' 
				if event.key == pygame.K_1:
					self.currentText = self.currentText + '1' 
				if event.key == pygame.K_2:
					self.currentText = self.currentText + '2' 
				if event.key == pygame.K_3:
					self.currentText = self.currentText + '3' 
				if event.key == pygame.K_4:
					self.currentText = self.currentText + '4' 
				if event.key == pygame.K_5:
					self.currentText = self.currentText + '5' 
				if event.key == pygame.K_6:
					self.currentText = self.currentText + '6' 
				if event.key == pygame.K_7:
					self.currentText = self.currentText + '7' 
				if event.key == pygame.K_8:
					self.currentText = self.currentText + '8' 
				if event.key == pygame.K_9:
					self.currentText = self.currentText + '9' 
			
			
				if event.key == pygame.K_ASTERISK:
					self.currentText = self.currentText + '*'
				if event.key == pygame.K_PLUS:
					self.currentText = self.currentText + '+'
				if event.key == pygame.K_COMMA:
					self.currentText = self.currentText + ','
				if event.key == pygame.K_PERIOD:
					self.currentText = self.currentText + '.'
				if event.key == pygame.K_MINUS:
					self.currentText = self.currentText + '-'
				if event.key == pygame.K_EXCLAIM:
					self.currentText = self.currentText + '-'
				if event.key == pygame.K_QUESTION:
					self.currentText = self.currentText + '/'
					
				if event.key == pygame.K_HASH:
					self.currentText = self.currentText + '#'
				
				if event.key == K_SEMICOLON:
					self.currentText = self.currentText + ';'
				
				if event.key == K_BACKSLASH:
					self.currentText = self.currentText + '\\'
				
				if event.key == K_SLASH:
					self.currentText = self.currentText + '/'
					
				if event.key == K_BACKQUOTE:
					self.currentText = self.currentText + '`'
				
				if event.key == K_LEFTBRACKET:
					self.currentText = self.currentText + '['
				
				if event.key == K_RIGHTBRACKET:
					self.currentText = self.currentText + ']'
		
				if event.key == K_QUOTE:
					self.currentText = self.currentText + '\''
		
			if event.key == pygame.K_BACKSPACE:
				#if len(currentText) >= 1:
				self.currentText = self.currentText[0:-1]
				self.isDeletingText = 1
			
			if event.key == pygame.K_SPACE:
					self.currentText = self.currentText + ' '
					
			
			self.currentKeyPressed = event.key
			self.isKeyHeldDown = 1
			self.timePressed = round(time.time() * 1000)
		
		#check if the key was raised:
		elif event.type == pygame.KEYUP:
				self.setFingerLiftedOffKey()
		
		self.handleKeyboardButtonHeldDown()
	
	def handleKeyboardButtonHeldDown(self):
		#Check for keys being held down:
		if(self.shouldRepeatTypeCommand()):
			self.numRepeatedCharacters = self.numRepeatedCharacters + 1
			if self.isDeletingText == 0:
				self.currentText = self.currentText + self.currentText[-1]
			elif self.isDeletingText == 1:
				self.currentText = self.currentText[0:-1]
		
	def shouldRepeatTypeCommand(self):
		if self.isKeyHeldDown == 1 and len(self.currentText) > 0:
			
			currentTime = round(time.time() * 1000)
			timeDiff = currentTime - self.timePressed
			numExpectedRepeats = 0
			if timeDiff > REPEAT_DELAY_TIME:
				numExpectedRepeats = 1 + math.floor((timeDiff-REPEAT_DELAY_TIME)/REPEAT_PERIOD)
				
				if numExpectedRepeats > self.numRepeatedCharacters:
					return 1
			
		return 0
	
	def setCurrentText(self, text):
		self.currentText = text

	def getCurrentText(self):
		return self.currentText

	def setCurrentTextEmpty(self):
		self.currentText = ''
	
	
	#TODO: get rid of screen_width and screen height params.
	def drawTextBox(self, screen):
		#TODO: make this customizable.
		myfont = pygame.font.SysFont("comicsansms", 30)
	
		labelExample3 = myfont.render(str(self.currentText), 1, self.labelColour)
		#pygame.draw.rect()
		#draw a rectangle shape
		#pygame.draw.rect(screen, (23,128,0), ((1*screen_width)/32, (4*screen_height)/5 + 10 + 3*40, 1000, 100 ))
		
		if self.isFocussed == 1:
			pygame.draw.rect(screen, (255,255,255), self.box.getCoordBoxOffset(10) )
		else: #TODO: don't assume  a black background.
			pygame.draw.rect(screen, (0,0,0), self.box.getCoordBoxOffset(10) )
			
		pygame.draw.rect(screen, self.bkColour, self.box.getCoordBox() )
		
		#TODO: use X offset and y offset.
		screen.blit(labelExample3, (self.box.x + 10, self.box.y + 10))
	
	#TODO: make the background change if focused... or something...
	def setFocussed(self):
		#print 'FOCUS on textbox'
		self.isFocussed = 1
	
	def setUnFocussed(self):
		print 'UNfOCUS on textbox'
		self.isFocussed = 0
		self.setFingerLiftedOffKey()
	
	def setFingerLiftedOffKey(self):
		self.isKeyHeldDown = 0
		self.isDeletingText = 0
		self.numRepeatedCharacters = 0
	
	#Check if the textbox is focused.
	def isFocussed(self):
		return self.isFocussed
		
	