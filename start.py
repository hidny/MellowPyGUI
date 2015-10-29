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
import sys

#TODO: maybe this is redundant? MT: who cares?
import socket

#TODO (optional): make  a config file for server name, port and desired name.

#TODO: add a title and put your name on it.
	
def main(name, args):
	#default values:
	tcpIP = '127.0.0.1'
	tcpPort = 6789
	name = 'Michael'
	
	numArgsSet = 0
	
	if len(args) > 1:
		name = args[1]
		numArgsSet = numArgsSet+1
	
	for x in range (0, len(args)):
		print str(args[x])
		#if args.find('host') != -1:
		#	isHostingGame = 1
		#elif args.find('meatbag') != -1 or args.find('interact') != -1:
		#	interact = 1
		#elif args.find('slow') != -1:
		#	slowdown = 1
		if args[x].find('ip=') != -1:
			tcpIP = str(args[x][len('ip='):])
			numArgsSet = numArgsSet+1
			
		elif args[x].find('p=') != -1:
			tcpPort = int(args[x][len('p='):])
			numArgsSet = numArgsSet+1
	
	if numArgsSet == 3:
		mellowGUI.main('hello', [name, str('ip=' + tcpIP), str('p=' + str(tcpPort))])
	
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
	enterPressed = 0
	
	startServer = button.Button(900, 800, 300, 50, "Connect to Server", (0, 255 ,0), (255, 0 ,255))
	
	colourDatBox = 0
	
	onScreenText = ''
	
	# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
	#myfont2 = pygame.font.SysFont("monospace", 15)

	# render text
	labelHost = myfont.render("Host:", 1, (255,255,0))
	labelPort = myfont.render("Port:", 1, (255,255,0))
	labelDesiredName = myfont.render("Desired Name:", 1, (255,255,0))
	
	screen.blit(labelHost, ((1*screen_width)/32, (2*screen_height)/5 + 10 + 40 -50))
	screen.blit(labelPort, ((1*screen_width)/32, (3*screen_height)/5 + 10 + 40 -50))
	screen.blit(labelDesiredName, ((1*screen_width)/32, (4*screen_height)/5 + 10 + 40 -50))
	
	textBox1 = textBox.TextBox((1*screen_width)/32, (2*screen_height)/5 + 10 + 40, 800, 100, '', (255, 255, 255), (128,128,0), str(tcpIP))
	textBox2 = textBox.TextBox((1*screen_width)/32, (3*screen_height)/5 + 10 + 40, 800, 100, '', (255, 255, 255), (200,128,0), str(tcpPort))
	textBox3 = textBox.TextBox((1*screen_width)/32, (4*screen_height)/5 + 10 + 40, 800, 100, '', (255, 255, 255), (23,128,0), str(name))
	
	serverConnectionBoxes = textBoxList.TextBoxList([])
	serverConnectionBoxes.addTextbox(textBox1, 0)
	serverConnectionBoxes.addTextbox(textBox2, 1)
	serverConnectionBoxes.addTextbox(textBox3)
	
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
		
		if frameHasKeyboardEvent == 0:
			#textBox1.handleKeyboardButtonHeldDown()
			serverConnectionBoxes.handleKeyboardButtonHeldDown()
		
		#textBox1.drawTextBox(screen)
		serverConnectionBoxes.drawTextBoxes(screen)
		
		#paintMouseMarkers(screen, mouseJustPressed, mouseJustRelease, mouseHeld, mx, my, greendot, reddot, dot)
		
		if mouseJustRelease==1:
			serverConnectionBoxes.checkClickForTextBoxes(mx, my, 1)
		#print str(mx) + ' ' + str(my)
		
		'''
		#Print ugly Mellow label
		labelExample = myfont.render("Mellow", 1, (0,255,0))
		goToServer = box.Box(100, 200, 250, 50)
		pygame.draw.rect(screen, (255, 0 ,255), goToServer.getCoordBox())
		screen.blit(dot, goToServer.getTopLeftBox(), goToServer.getCoordBox())
		screen.blit(labelExample, goToServer.getTopLeftBox())
		'''
		
		if enterPressed == 0:
			enterPressed = startServer.updateButtonAndCheckIfPressed(mx, my, mouseJustPressed, mouseJustRelease)
		
		startServer.printButton(pygame, screen)
		
		if enterPressed == 1:
			colourDatBox = colourDatBox + 1
			print 'TESTING ENTRIES!'
			print str(textBox1.getCurrentText())
			print str(textBox2.getCurrentText())
			print str(textBox3.getCurrentText())
			print 'TODO: actually have something done'
			tcpIP = str(textBox1.getCurrentText())
			tcpPort = str(textBox2.getCurrentText())
			NAME = str(textBox3.getCurrentText())
			print 'starting main'
			
			#pygame.display.quit()
			#pygame.quit()
			
			mellowGUI.main('hello', ['start.py', name, 'slow', 'interact', str('ip=' + tcpIP), str('p=' + str(tcpPort)), 'host'])
			
		
		'''
		#Sample interactions:
		#Button reaction:
		if colourDatBox % 2 == 1:
			screen.blit(dot, (50, 50), (0, 0, 10, 10))
		else:
			pygame.draw.rect(screen, (0, 0 ,0), (50, 50, 10, 10))
		
		#Blinking:
		if shouldBlinkTextCursor() == 1:
			#TODO: make this a nice vertical line.
			screen.blit(dot, (100, 50), (0, 0, 10, 10))
		else:
			screen.blit(reddot, (100, 50), (0, 0, 10, 10))
		'''
		#pygame.draw.rect()
		
		pygame.display.update()
		clock.tick(40)
		
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
#python start.py michael host
#then click start.
#python mellowGUI.py Phil
#python mellowGUI.py Richard
#python mellowGUI.py Doris

#alt1:
#start server
#python start.py michael host
#then click start.
#python mellowGUI.py Phil slow
#python mellowGUI.py Richard slow
#python mellowGUI.py Doris slow

#alt2:
#start server
#python start.py michael host
#then click start.
#python mellowGUI.py Phil slow
#start java rich
#python mellowGUI.py Doris slow