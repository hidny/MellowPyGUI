#!/usr/bin/env python
import sys
import time

import threading
import thread

import mellowGUI
import projectile
import clientContext

import random
import reversiGUI

#It's static because I only want one mellow client for the whole execution.

#Reversi specific constants:
START_MSG = 'From Reversi(public):'
YOUR_TURN = 'From Reversi(private): Your turn '

PUBLIC_SERVER_MSG = 'From Reversi(public): '

BOARD_INIT = "|"
TO_PLAY = 'to move'
VS = ' vs '

WIN = 'WINS!'
DRAW = 'It is a tie!'

OUT_OF_GAME_MSG = 'number of game rooms:'

#End Reversi specific constants

#Game specific variables:
gameStarted = 0


#http://stackoverflow.com/questions/419145/python-threads-critical-section
turn_lock = threading.Lock()
itsYourTurn = 0
#End game specific variables:


def isNumber(s):
	try:
		float(s)
		return 1
	except ValueError:
		return 0

def serverListener(connection, reversiGUIObject):

	global gameStarted
	global turn_lock
	global itsYourTurn
	
	isBlacksTurn = 1
	endOfRoundIndex = 0
	
	rowToInsert = 0
		
	#Red player is player one.
	blackPlayer = ''
	whitePlayer = ''
	
	try:
		#Sanity testing:
		print 'connect4 client in server Listener: '
		
		while reversiGUIObject.isGameOver() == 0:
			#print 'Trying to get message!'
			message = connection.getNextServerMessageInQueue()
			
			#print 'Message: ' + message
			#print '************'
			currentLines = message.split('\n')
			
			for currentLine in currentLines:
				if len(currentLine) > 1:
					#print '*****************************'
					#print "received message: " + str(currentLine)
					pass
				else:
					continue
				
				if currentLine.startswith(START_MSG):
					gameStarted = 1
				
				if gameStarted ==1:
					if currentLine.startswith(YOUR_TURN):
						with turn_lock:
							reversiGUIObject.setMoveUserWantsToMakeToNull()
							itsYourTurn=1
							if connection.getInteract() == 1:
								reversiGUIObject.setMessage('Your turn')
					
					elif currentLine.startswith(BOARD_INIT):
						rowToInsert = rowToInsert + 1
						
						getBoardInfoFromLine(reversiGUIObject, currentLine, rowToInsert)
						
						if rowToInsert == reversiGUI.BOARD_LENGTH:
							rowToInsert = 0
						
					elif currentLine.startswith(PUBLIC_SERVER_MSG):
					
						if currentLine.find(VS) != -1:
							#From Reversi(public): Michael vs Richard
							blackPlayer = currentLine.split(" ")[2]
							whitePlayer = currentLine.split(" ")[4]
					
						if currentLine.find(TO_PLAY) != -1:
							rowToInsert = 0
							if currentLine.find('black') != -1:
								isBlacksTurn = 0
							else:
								isBlacksTurn = 1
						
						
						if currentLine.find(WIN) != -1:
							print currentLine.split(" ")[2]
							if blackPlayer == currentLine.split(" ")[2]:
								reversiGUIObject.setMessage('Black(' + blackPlayer + ') wins!')
							elif whitePlayer == currentLine.split(" ")[2]:
								reversiGUIObject.setMessage('White(' + whitePlayer + ') wins!')
							
							connection.setInteract(1)
							reversiGUIObject.setGameOver()
							break
						
						if currentLine.find(DRAW) != -1:
							reversiGUIObject.setMessage('It\'s a draw')
							connection.setInteract(1)
							reversiGUIObject.setGameOver()
							break
		
		
		isDone = 0
		#This loop is here to get rid of 'From Reversi(public): 56 - 3'
		while isDone == 0:
			message = connection.getNextServerMessageInQueue()
			currentLines = message.split('\n')
			
			for currentLine in currentLines:
				if currentLine.startswith(PUBLIC_SERVER_MSG):
					if currentLine.find(' - ') != -1:
						isDone = 1
						
				
	except:
		print 'ERROR: in server listener'
		print 'ERROR: ' + currentLine
		reversiGUIObject.setMessage("ERROR: in reversi server listener")

def getBoardInfoFromLine(reversiGUIObject, line, rowNumber):
	for i in range(0, reversiGUI.BOARD_LENGTH):
		coord = str(chr(i + ord('a'))) + str(rowNumber)
		if line[1 + i*2] == 'W':
			reversiGUIObject.placePeg(coord, reversiGUI.WHITE)
		elif line[1 + i*2] == 'D':
			reversiGUIObject.placePeg( coord, reversiGUI.BLACK)
	
		
def clientListener(connection, reversiGUIObject):
	global gameStarted
	
	try:
		print 'Client Listener'
		
		connection.sendMessageToServer(connection.getCurrentPlayerName() + '\n')
		if connection.isHosting() == 1:
			connection.sendMessageToServer('/create reversi reversipy' + '\n')
		else:
			connection.sendMessageToServer('/join reversipy' + '\n')
		
		while reversiGUIObject.isGameOver() == 0:
			if connection.isHosting() == 1 and gameStarted == 0:
				time.sleep(1)
				connection.sendMessageToServer('/start' + '\n')
				print 'sent start msg'
			elif gameStarted == 1:
				break
			else:
				time.sleep(1)
		
		playMoveDefault(connection, reversiGUIObject)
		
		
	except:
		print 'ERROR: in client listener'
		reversiGUIObject.setMessage("ERROR: in reversi client listener")

def playMoveDefault(connection, reversiGUIObject):
	global turn_lock
	global itsYourTurn
	
	playedACardInFight = 0
	
	while reversiGUIObject.isGameOver() == 0:
		with turn_lock:
			if connection.getInteract() == 0:
				if itsYourTurn==1:
					move = 1
					connection.sendMessageToServer('/move ' + str(1) + '\n')
					itsYourTurn = 0
					
			elif connection.getInteract() == 1:
				if itsYourTurn==1:
					if reversiGUIObject.getMoveUserWantsToMake() != '':
						connection.sendMessageToServer('/move ' + str(reversiGUIObject.getMoveUserWantsToMake()) + '\n')
						reversiGUIObject.setMoveUserWantsToMakeToNull()
						itsYourTurn = 0
						reversiGUIObject.setMessage('')
		time.sleep(0.2)

#Pre: this should only get called from MellowGUI
def main(reversiGUIObject, args):
	
	random.seed()
	
	if len(args) > 1:
		connection = args[1]
	else:
		connection = clientContext.ClientContext('127.0.0.1', 6789, 'Michael')
	
	
	#start listening t server on a seperate thread:
	try:
		thread.start_new_thread( serverListener, (connection, reversiGUIObject) )
	except:
		print "Error: unable to start thread 1"
		reversiGUIObject.setMessage("Error: unable to start thread 1")
		exit(1)
	
	clientListener(connection, reversiGUIObject)

def slowDownIfInteract(connection, amountOfTime, gameStarted):
	if gameStarted == 1 and (connection.getSlowdown() == 1 or connection.getInteract() == 1):
		time.sleep(amountOfTime)
	
#You have to start it from mellowGUI because pygame has to be the main 
#thread.
if __name__ == "__main__":
	print 'Please use python reversiGUIObject.py to start.'
	exit(1)