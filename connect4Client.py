#!/usr/bin/env python
import sys
import time

import threading
import thread

import mellowGUI
import projectile
import clientContext

import random

#It's static because I only want one mellow client for the whole execution.

#Mellow specific constants:
START_MSG = 'From connect 4:'
YOUR_TURN = '0 or 1 or 2 or 3 or 4 or 5 or 6?'

PUBLIC_SERVER_MSG = 'From connect 4: '
MOVE_DESC = "has entered: "
BOARD_INIT = "|"
TO_PLAY = 'to play'

WIN = 'wins!'
DRAW = 'Tie Game!'

MISPLAYED = 'Play properly!'

OUT_OF_GAME_MSG = 'number of game rooms:'

#End Mellow specific constants

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

def serverListener(connection, connect4GUI):

	global gameStarted
	global turn_lock
	global itsYourTurn
	
	isRedsTurn = 1
	endOfRoundIndex = 0
	
	rowToInsert = 0
		
	#Red player is player one.
	redPlayer = ''
	blackPlayer = ''
	
	try:
		#Sanity testing:
		print 'connect4 client in server Listener: '
		
		while connect4GUI.isGameOver() == 0:
			message = connection.getNextServerMessageInQueue()
			
			currentLines = message.split('\n')
			
			for currentLine in currentLines:
				if len(currentLine) > 1:
					print '*****************************'
					print "received message: " + str(currentLine)
					
				if currentLine.startswith(START_MSG):
					gameStarted = 1
				
				if gameStarted ==1:
					if currentLine.startswith(YOUR_TURN):
						with turn_lock:
							connect4GUI.setCardUserWantsToMakeToNull()
							itsYourTurn=1
					
					elif currentLine.startswith(BOARD_INIT):
						rowToInsert = rowToInsert + 1
					
					elif currentLine.startswith(PUBLIC_SERVER_MSG):
						if currentLine.find(TO_PLAY) != -1:
							if currentLine.find('Black') != -1:
								isRedsTurn = 0
							else:
								isRedsTurn = 1
						
						if currentLine.find(MOVE_DESC) != -1:
							if isRedsTurn == 0:
								blackPlayer = currentLine.split(" ")[3]
							else:
								redPlayer  = currentLine.split(" ")[3]
							
							print 'HEY! ' + currentLine.split(" ")[6]
							slotNum = int(currentLine.split(" ")[6])
							
							print 'Dropping ' + str(slotNum)
							if isRedsTurn == 0:
								connect4GUI.dropPeg(slotNum, connect4GUI.YELLOW)
							else:
								connect4GUI.dropPeg(slotNum, connect4GUI.RED)
							
						
						if currentLine.find(WIN) != -1:
							if isRedsTurn == 1:
								connect4GUI.setMessage('Red(' + redPlayer + ') wins!')
							else:
								connect4GUI.setMessage('Yellow(' + blackPlayer + ') wins!')
							
							#TODO: highlight the 4 line(s)
							connection.setInteract(1)
							connect4GUI.setGameOver()
							break
							
						if currentLine.find(DRAW) != -1:
							connect4GUI.setMessage('It\'s a draw')
							connection.setInteract(1)
							connect4GUI.setGameOver()
							break
							
						if currentLine.find(MISPLAYED) != -1:
							itsYourTurn=1
			
			
	except:
		print 'ERROR: in server listener'
		print 'ERROR: ' + currentLine
		connect4GUI.setMessage("ERROR: in server listener")

def clientListener(connection, connect4GUI):
	global gameStarted
	
	try:
		print 'Client Listener'
		
		connection.sendMessageToServer(connection.getCurrentPlayerName() + '\n')
		if connection.isHosting() == 1:
			connection.sendMessageToServer('/create connect_four connect4py' + '\n')
		else:
			connection.sendMessageToServer('/join connect4py' + '\n')
		
		while connect4GUI.isGameOver() == 0:
			if connection.isHosting() == 1 and gameStarted == 0:
				time.sleep(0.2)
				connection.sendMessageToServer('/start' + '\n')
				print 'sent start msg'
			elif gameStarted == 1:
				break
			else:
				time.sleep(0.2)
		
		playMoveDefault(connection, connect4GUI)
		
		
	except:
		print 'ERROR: in client listener'
		connect4GUI.setMessage("ERROR: in client listener")

def playMoveDefault(connection, connect4GUI):
	global turn_lock
	global itsYourTurn
	
	playedACardInFight = 0
	
	while connect4GUI.isGameOver() == 0:
		with turn_lock:
			if connection.getInteract() == 0:
				if itsYourTurn==1:
					move = random.randint(0, 6)
					connection.sendMessageToServer('/move ' + str(move) + '\n')
					itsYourTurn = 0
					
			elif connection.getInteract() == 1:
				if itsYourTurn==1:
					if connect4GUI.getMoveUserWantsToMake() != -1:
						connection.sendMessageToServer('/move ' + str(connect4GUI.getMoveUserWantsToMake()) + '\n')
						connect4GUI.setCardUserWantsToMakeToNull()
						itsYourTurn = 0
		

#Pre: this should only get called from MellowGUI
def main(connect4GUI, args):
	
	random.seed()
	
	if len(args) > 1:
		connection = args[1]
	else:
		connection = clientContext.ClientContext('127.0.0.1', 6789, 'Michael')
	
	
	#start listening t server on a seperate thread:
	try:
		thread.start_new_thread( serverListener, (connection, connect4GUI) )
	except:
		print "Error: unable to start thread 1"
		connect4GUI.setMessage("Error: unable to start thread 1")
		exit(1)
	
	clientListener(connection, connect4GUI)

def slowDownIfInteract(connection, amountOfTime, gameStarted):
	if gameStarted == 1 and (connection.getSlowdown() == 1 or connection.getInteract() == 1):
		time.sleep(amountOfTime)
	
#You have to start it from mellowGUI because pygame has to be the main 
#thread.
if __name__ == "__main__":
	print 'Please use python connect4GUI.py to start.'
	exit(1)