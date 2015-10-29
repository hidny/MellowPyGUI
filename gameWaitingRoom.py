#COPIED from channelRoom.py
#TODO: make a convincing game waiting room.

import sys
import time

import random, os


import threading
#from threading import Thread
import thread
'''
import pygame
from pygame import _view
from pygame.locals import *
'''

from sys import exit


import socket

#TODO: use constants from another file.
BUFFER_SIZE = 1024
END_OF_TRANSMISSION = '**end of transmission**'

HELLO_MSG = 'Hello'
PUBLIC_SERVER_MSG = 'From Game(public): '
#END TODO

sendMsgLock = threading.Lock()

serverSocket = []
gameOver = 1
currentPlayerName = ''

#I'm copy/pasting a lot of code from mellowClient.py. (I'll reduce the copy/paste later)
'''
class ChannelRoom:
	pygame.init()
	screen_width = 1300
	screen_height = 900
	
	size = width, height = screen_width, screen_height
	
	screen = pygame.display.set_mode(size)
	
	def printMsg():
		pass
'''
	

def endProgramCleanly():
	global gameOver
	gameOver = 0

def isStillRunning():
	global gameOver
	return gameOver

PUBLIC_SERVER_GAME_MSG = 'From Game(public): '
PUBLIC_SERVER_MSG = 'From server: '

def serverListener(name, isHostingGame, interact, slowdown, serverSocket):
	
	secondLastNumber = -1.0
	lastNumber = -1.0
	
	try:
		print 'serverListener in channel room activated'
		
		data =''
		while isStillRunning():
			time.sleep(1)
			
			if data != '':
				data = data + serverSocket.recv(BUFFER_SIZE)
			else:
				data = serverSocket.recv(BUFFER_SIZE)
			
			print 'DATA: ' + str(data)
			
			while END_OF_TRANSMISSION in data:
				message = data[0: data.index(END_OF_TRANSMISSION)]
				data = data[data.index(END_OF_TRANSMISSION) + len(END_OF_TRANSMISSION):]
				
				while len(data) > 0 and data[0] == '\n':
					data = data[1:]
				
				currentLines = message.split('\n')
				
				for currentLine in currentLines:
				
					print 'Current line received: '  + currentLine
					
					possibleNumber = currentLine.split(' ')[-1] 
					if isNumber(possibleNumber) == 1:
						
						secondLastNumber = float(lastNumber)
						lastNumber = float(possibleNumber)
						
						if secondLastNumber >= 0.0:
							time.sleep(2)
							print 'Sending: ' + str(float(lastNumber + secondLastNumber))
							sendMessageToServer(serverSocket, str(float(lastNumber + secondLastNumber)) + '\n')
						
						
					if len(currentLine) > 1:
						pass
					
					if currentLine.find(HELLO_MSG) != -1:
						#currentLine = currentLine[currentLine.index(HELLO_MSG) + len(HELLO_MSG):]
						#currentPlayerName = currentLine.split(' ')[1][0:-1]
						pass
					
					elif currentLine.find(PUBLIC_SERVER_MSG) != -1:
						pass
					
					else:
						#print currentLine
						pass
		
		
	except:
		print 'ERROR: in server listener'
		endProgramCleanly()
		#TODO: print error in GUI.
	
	
def clientListener(name, isHostingGame, interact, slowdown):
	global serverSocket
	
	try:
		print 'In clientListener in channel window.'
		
		#Fibonacci Testing:
		print 'Fibonacci Testing:'
		time.sleep(1)
		sendMessageToServer(serverSocket, '1' + '\n')
		time.sleep(1)	
		sendMessageToServer(serverSocket, '1' + '\n')
		time.sleep(5)
		#End Fibonacci Testing.
		
		#Sanity testing:
	
		if interact == 0:
			sendMessageToServer(serverSocket, name + '\n')
			
			if isHostingGame == 1:
				sendMessageToServer(serverSocket, '/create mellow mellowpy' + '\n')
			else:
				sendMessageToServer(serverSocket, '/join mellowpy' + '\n')
			
		
		while isStillRunning() == 1:
			time.sleep(1)
			
			if interact == 0 and isHostingGame == 1 and gameStarted == 0:
				time.sleep(0.2)
				sendMessageToServer(serverSocket, '/start' + '\n')
				
			if interact == 0:
				pass
				
			elif interact == 1:
				#TODO: Accept msgs sent.
				pass
		
		
	except:
		print 'ERROR: in client listener'
		#TODO: print error in GUI.
		endProgramCleanly()

def sendMessageToServer(serverSocket, msg):
	global sendMsgLock
	with sendMsgLock:
		serverSocket.send(str(msg))
		print 'Sent: ' + str(msg)
	
def slowDownIfInteract(amountOfTime, gameStarted, slowdown, interact):
	if gameStarted == 1 and (slowdown == 1 or interact == 1):
		time.sleep(amountOfTime)


#TODO: taken from mellowClient
def isNumber(s):
	try:
		float(s)
		return 1
	except ValueError:
		return 0

		
def main(name, args):
	global serverSocket
	
	alreadyConnected = 0
	#TODO: add this logic in mellow Client.py:
	print 'HELLO Channel Room CLIENT MAIN'
	if len(args) > 1:
		if args[1] == 'Already connected':
			name = args[2]
			serverSocket = args[3]
			
			alreadyConnected = 1
			
			print 'Channel Room: already connected!'
		else:
			name = args[1]
	else:
		name = 'Michael'
	#END TODO
	
	#default ip and port:
	tcpIP = '127.0.0.1'
	tcpPort = 6789
	
	isHostingGame = 0
	interact = 0
	slowdown = 0
	
	#parse arguments:
	for x in range (0, len(args)):
		print str(args[x])
		if args[x].find('host') != -1:
			isHostingGame = 1
		elif args[x].find('meatbag') != -1 or args[x].find('interact') != -1:
			interact = 1
		elif args[x].find('slow') != -1:
			slowdown = 1
		elif alreadyConnected == 0 and args[x].find('ip=') != -1:
			tcpIP = str(args[x][len('ip='):])
		elif alreadyConnected == 0 and args[x].find('p=') != -1:
			tcpPort = int(args[x][len('p='):])
	
	if alreadyConnected == 0:
		print 'IP: ' + str(tcpIP)
		print 'PORT: ' + str(tcpPort)
		print 'name: ' + str(name)
		
		#Connect to server:
		try:
			serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			serverSocket.connect((tcpIP, int(tcpPort)))
			
		except:
			print "ERROR: could not find server."
			#TODO: setGUIMessage("ERROR: could not find server.")
			exit(1)
	
	#Declare name:
	sendMessageToServer(serverSocket, name + "\n")
	
	#start listening to server on a seperate thread:
	try:
		thread.start_new_thread( serverListener, (name, isHostingGame, interact, slowdown, serverSocket) )
		print 'started thread'
		
	except:
		print "Error: unable to start server listener"
		exit(1)

	clientListener(name, isHostingGame, interact, slowdown)
	
if __name__ == "__main__":
	main('hello world', sys.argv)
	
#tansu

#Commands I can use:
#python channelRoom.py
#python channelRoom.py Michael slow interact p=6789 ip=127.0.0.1

#ctrl - > pause/break ftw!
