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

#TODO: maybe this is redundant? MT: who cares?
import socket

#TODO (optional): make  a config file for server name, port and desired name.

#TODO: add a title and put your name on it.

import chatBox

def main(name, args):
	
	pygame.init()
	
	screen_width = 1300
	screen_height = 900
	
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
	
	startServer = button.Button(900, 800, 300, 50, "Send Message", (0, 255 ,0), (255, 0 ,255))
	
	colourDatBox = 0
	
	onScreenText = ''
	
	# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
	#myfont2 = pygame.font.SysFont("monospace", 15)

	
	enterPressed = 0
	textBox1 = textBox.TextBox((1*screen_width)/32, (4*screen_height)/5 + 10 + 40, 800, 100, '', (255, 255, 255), (23,128,0), str(name))
	
	serverConnectionBoxes = textBoxList.TextBoxList([])
	
	serverConnectionBoxes.addTextbox(textBox1)
	
	#The extremely lame chatbox.
	#TODO: be able to initialize more variables to declare it.
	myChatBox = chatBox.chatBox(24)
	
	#				(self, x, y, width, height, firstOptionText, labelColour, bkColour, list):
	list = []
	#One Fish Two Fish Red Fish Blue Fish
	list.append("One Fish")
	list.append("Two Fish")
	list.append("Red Fish")
	list.append("Blue Fish")
	
	drop = dropDown.DropDown(500, 300, 300, 50, "Dropping down.", (0, 255 ,0), (255, 0 ,255),list)
	
	
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
				#textBox1.dealWithKeyboard(event)
				serverConnectionBoxes.dealWithKeyboard(event)
				frameHasKeyboardEvent = 1
				
				if serverConnectionBoxes.checkIfEnterPressed(event) == 1:
					enterPressed = 1
					
		
		
		mx,my = pygame.mouse.get_pos()
		
		drop.updateSelected(mx, my, screen)
		
		if mouseJustRelease == 1:
			drop.updateClicked(mx, my, mouseJustRelease, screen)
		
		
		if frameHasKeyboardEvent == 0:
			#textBox1.handleKeyboardButtonHeldDown()
			serverConnectionBoxes.handleKeyboardButtonHeldDown()
		
		#print the chatbox:
		myChatBox.printChat(screen)
		
		#print the dropdown:
		drop.printDropDown(screen)
		
		#textBox1.drawTextBox(screen)
		serverConnectionBoxes.drawTextBoxes(screen)
		
		#paintMouseMarkers(screen, mouseJustPressed, mouseJustRelease, mouseHeld, mx, my, greendot, reddot, dot)
		
		if mouseJustRelease==1:
			serverConnectionBoxes.checkClickForTextBoxes(mx, my, 1)
		#print str(mx) + ' ' + str(my)
		
		if enterPressed == 0:
			enterPressed = startServer.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		startServer.printButton(pygame, screen)
		
		if enterPressed == 1:
			print 'You pressed enter!'
			#TODO: take whatever is in the chatbox.
			myChatBox.setNewChatMessage(textBox1.getCurrentText())
			textBox1.setCurrentTextEmpty()
			
			enterPressed = 0
			#mellowGUI.main('hello', ['start.py', name, str('ip=' + tcpIP), str('p=' + str(tcpPort)), 'host'])
		
		
		pygame.display.update()
		
		screen.fill(0)
		
		clock.tick(30)
		
	print "bye"
	
PERIOD = 1000
SHOWCURSONTIME = 500
	

def shouldBlinkTextCursor():
	partOfCycle = round(time.time() * 1000) % PERIOD
	
	if partOfCycle < SHOWCURSONTIME:
		return 1
	else:
		return 0

def paintMouseMarkers(screen, mouseJustPressed, mouseJustRelease, mouseHeld, mx, my, greendot, reddot, dot):
	#print mouse cursor:
	if mouseJustPressed == 1 or mouseJustRelease==1:
		screen.blit(greendot, (mx-5, my-5), (0, 0, 10, 10))
		print 'green'
	elif mouseHeld == 1:
		print 'red'
		screen.blit(reddot, (mx-5, my-5), (0, 0, 10, 10))
	else:
		screen.blit(dot, (mx-5, my-5), (0, 0, 10, 10))

if __name__ == "__main__":
	main('hello world', sys.argv)
	

#start server
#python channelRoomGUI.py