#!/usr/bin/env python
import sys
import time

import threading
import thread

import mellowGUI
import projectile
import clientContext

#It's static because I only want one mellow client for the whole execution.

#Mellow specific constants:
START_MSG = 'From Game(public): Starting Mellow!'
YOUR_BID = 'From Game(private): What\'s your bid?'
YOUR_TURN = 'From Game(private): Play a card!'
PRIVATE_MSG = 'From Game(private):'
PUBLIC_MSG = 'From Game(public): '
#first dealer:
FIRST_DEALER = 'From Game(public): First dealer is '
DEALER_MSG = 'dealer is '
FIGHT_SUMMARY_MSG = 'From Game(public): Fight Winner:'
#From Game(private): 7C KS 9C AC AH 2S 4D KC KH 2D 7H 9S 7S 
STARTING_HAND_LENGTH = 13

TRICKS = 'trick(s).'

PLAYING_CARD = 'playing:'
PUBLIC_SERVER_MSG = 'From Game(public): '
WIN = 'win!'
END_OF_ROUND = 'END ROUND!'
#End Mellow specific constants

#Game specific variables:
gameStarted = 0
players = []
#http://stackoverflow.com/questions/419145/python-threads-critical-section
turn_lock = threading.Lock()
itsYourBid = 0
itsYourTurn = 0
#End game specific variables:


def isNumber(s):
	try:
		float(s)
		return 1
	except ValueError:
		return 0
		
def isACard(card):
	if len(card) != 2:
		return 0
	else:
		if card[0] == '2' or card[0] == '3' or card[0] == '4' or card[0] == '5' or card[0] == '6' or card[0] == '7' or card[0] == '8' or card[0] == '9'  or card[0] == 'T'  or card[0] == 'J' or card[0] == 'Q'  or card[0] == 'K'   or card[0] == 'A':
			if card[1] == 'S' or card[1] == 'H' or card[1] == 'C' or card[1] == 'D':
				return 1
	
def shiftArrayByOne(array):
	temp = array[0]
	for i in range (0, len(array) -1):
		array[i] = array[i+1]
	array[len(array) - 1] = temp
	return array


def serverListener(connection, mellowGUIVars):

	global gameStarted
	global players
	global turn_lock
	global itsYourBid
	global itsYourTurn
	
	playerInTeamA = 1
	endOfRoundIndex = 0
	
	try:
	
		#Sanity testing:
		#print 'Card height in server Listener: ' + str(mellowGUIVars.card_height)
		
		while mellowGUIVars.isStillRunning() == 1:
			message = connection.getNextServerMessageInQueue()
			
			currentLines = message.split('\n')
			
			for currentLine in currentLines:
				if len(currentLine) > 1:
					#print '*****************************'
					#print "received message: " + str(currentLine)
					pass
				if currentLine.startswith(START_MSG):
					gameStarted = 1
					#Starting Mellow! Michael & Dick vs Dad & Mom
					#team A
					#Trying to send: From Game(public): Starting Mellow! Michael & Dick vs Dad & Mom
					currentLine = currentLine[currentLine.index(START_MSG) + len(START_MSG):]
					players.append(currentLine.split(' ')[1])
					players.append(currentLine.split(' ')[5])
					players.append(currentLine.split(' ')[3])
					players.append(currentLine.split(' ')[7])
					
					while players[0] != connection.getCurrentPlayerName():
						players = shiftArrayByOne(players)
						if playerInTeamA == 0:
							playerInTeamA = 1
						else:
							playerInTeamA = 0
					
					
				elif currentLine.startswith(YOUR_BID):
					currentLine = currentLine[currentLine.index(YOUR_BID) + len(YOUR_BID):]
					with turn_lock:
						itsYourBid=1
						#print 'Its my bid!'
						if connection.getInteract() == 1:
							mellowGUIVars.askUserForBid()
					
				
				elif currentLine.startswith(YOUR_TURN):
					currentLine = currentLine[currentLine.index(YOUR_TURN) + len(YOUR_TURN):]
					with turn_lock:
						itsYourTurn=1
				
				elif currentLine.startswith(PUBLIC_SERVER_MSG):
					if currentLine.find(PLAYING_CARD) != -1:
						#From Game(public): Michael playing: 9S
						player = currentLine.split(' ')[2]
						card = currentLine.split(' ')[4]
						
						if isACard(card) == 0:
							#print 'UH OH! Could not find card: ' + str(card)
							sys.exit(1)
						
						if players[0] != player:
							slowDownIfInteract(connection, 0.25, gameStarted)
						
						if players[0] == player:
							#print 'South(' + player + ') plays ' + card
							mellowGUIVars.throwSouthCard(card)
						elif players[1] == player:
							#print 'West(' + player + ') plays ' + card
							mellowGUIVars.throwWestCard(card)
						elif players[2] == player:
							#print 'North(' + player + ') plays ' + card
							mellowGUIVars.throwNorthCard(card)
						elif players[3] == player:
							#print 'East(' + player + ') plays ' + card
							mellowGUIVars.throwEastCard(card)
						else:
							#print 'ERROR: unknown player plays card!'
							sys.exit(1)
						
						#get relative player direction
						#make it print: west plays x
						#or north plays y
						#Let some other class deal with this.
					
					#Check if it's a bid:
					#From Game(public): Dad: 1
					msgTokens = message.split(' ')
					if len(msgTokens) > 3:
						isBid = 0
						for i in range(0, len(players)):
							if(msgTokens[2] == players[i] + ':'):
								isBid = 1
						
						bidder = msgTokens[2][0:-1]
						if isBid == 1:
							bid = msgTokens[3]
							if bid[len(bid) - 1] == '\n':
								bid = bid[0:-1]
							
							if bid.isdigit():
								if players[0]  == bidder:
									mellowGUIVars.bidSouth(bid)
									#print 'South(' + bidder + ') bids ' + bid
									
								elif players[1] == bidder:
									mellowGUIVars.bidWest(bid)
									#print 'West(' + bidder + ') bids ' + bid
									
								elif players[2] == bidder:
									mellowGUIVars.bidNorth(bid)
									#print 'North(' + bidder + ') bids ' + bid
									
								elif players[3] == bidder:
									mellowGUIVars.bidEast(bid)
									#print 'East(' + bidder + ') bids ' + bid
									
								else:
									#print 'ERROR: unknown player bids'
									sys.exit(1)
						
				if currentLine.startswith(PRIVATE_MSG):
					currentLine = currentLine[currentLine.index(PRIVATE_MSG) + len(PRIVATE_MSG):]
					currentLine = currentLine.strip()
					cardsTemp = currentLine.split(' ')
					
					
					if len(cardsTemp) > 0 and isACard(cardsTemp[0]) == 1:
						if len(cardsTemp) == STARTING_HAND_LENGTH:
							mellowGUIVars.setupCardsForNewRound(cardsTemp)
						
						#print 'Printing cards:'
						#for card in cardsTemp:
						#	print card
						#print 'Done printing cards'
				
				
				if currentLine.startswith(PUBLIC_MSG) and currentLine.find(DEALER_MSG) != -1:
					#From Game(public): First dealer is Mom
					#From Game(public): Dealer: Michael
					dealer = message.split(' ')[len(message.split(' ')) - 1]
					while dealer[len(dealer) -1] == '\n':
						dealer = dealer[0:-1]
					
					if players[0]  == dealer:
						#print 'Dealer is South(' + dealer + ')'
						mellowGUIVars.setDealer("South(" + dealer + ")")
						
					elif players[1] == dealer:
						#print 'Dealer is West(' + dealer + ')'
						mellowGUIVars.setDealer("West(" + dealer + ")")
						
					elif players[2] == dealer:
						#print 'Dealer is North(' + dealer + ')'
						mellowGUIVars.setDealer("North(" + dealer + ")")
						
					elif players[3] == dealer:
						#print 'Dealer is East(' + dealer + ')'
						mellowGUIVars.setDealer("East(" + dealer + ")")
						
					else:
						#print 'current dealer: ' + dealer
						#print 'ERROR: unknown dealer'
						sys.exit(1)
				
				
				if currentLine.startswith(FIGHT_SUMMARY_MSG):
					slowDownIfInteract(connection, 1, gameStarted)
					mellowGUIVars.remove_Projectiles()
					
					fightWinner = message.split(' ')[len(message.split(' ')) - 1]
					while fightWinner[len(fightWinner) -1] == '\n':
						fightWinner = fightWinner[0:-1]
					
					if players[0]  == fightWinner:
						mellowGUIVars.addTrickSouth()
						#print 'Fight Winner is South(' + fightWinner + ')'
						
					elif players[1] == fightWinner:
						mellowGUIVars.addTrickWest()
						#print 'Fight Winner is West(' + fightWinner + ')'
						
					elif players[2] == fightWinner:
						mellowGUIVars.addTrickNorth()
						#print 'Fight Winner is North(' + fightWinner + ')'
						
					elif players[3] == fightWinner:
						mellowGUIVars.addTrickEast()
						#print 'Fight Winner is East(' + fightWinner + ')'
						
					else:
						#print 'current fightWinner: ' + fightWinner
						#print 'ERROR: unknown fight winner'
						sys.exit(1)
				
				if currentLine.startswith(PUBLIC_MSG) and currentLine.find(WIN) != -1:
					#print message[message.index(PUBLIC_MSG) + len(PUBLIC_MSG):]
					mellowGUIVars.setMessage(message[message.index(PUBLIC_MSG) + len(PUBLIC_MSG):-1])
				
				if currentLine.startswith(PUBLIC_MSG) and currentLine.find(TRICKS) != -1:
					#From Game(public): ALL: Mom got 4 trick(s).
					slowDownIfInteract(connection, 1, gameStarted)
					
					#Trying to send: From Game(public): ALL: Michael got 1 trick(s).
					player = message.split(' ')[3]
					number = message.split(' ')[5]
					
					#if players[0]  == player:
					#	print 'python South(' + player + ') has ' + number + ' tricks.'
					#elif players[1] == player:
					#	print 'West(' + player + ') has ' + number + ' tricks.'
					#elif players[2] == player:
					#	print 'North(' + player + ') has ' + number + ' tricks.'
					#elif players[3] == player:
					#	print 'East(' + player + ') has ' + number + ' tricks.'
					#else:
					#	print 'current player: ' + player
					#	print 'ERROR: unknown player has tricks.'
					#	sys.exit(1)
				
				
				if currentLine.startswith(PUBLIC_MSG) and currentLine.find(END_OF_ROUND) != -1:
					endOfRoundIndex = 0
				
				
				if currentLine.startswith(PUBLIC_MSG):
					currentScores = currentLine[currentLine.find(PUBLIC_MSG) + len(PUBLIC_MSG):]
					currentScores = currentScores.strip()
					tokens = currentScores.split(' ')
					if len(tokens) > 1 and isNumber(tokens[0]) == 1 and isNumber(tokens[len(tokens) - 1]) == 1:
						endOfRoundIndex = endOfRoundIndex + 1
						
						if endOfRoundIndex == 1:
						#	print 'previous scores: '
							pass
						elif endOfRoundIndex == 2:
						#	print 'Scores added: '
							pass
						#else:
						#	print 'Current Total:'
							
						#	print 'Tell Mellow GUI about current total and let it figure everything else out:'
							if playerInTeamA == 1:
								#print 'US(team A): ' + tokens[0]
								#print 'THEM(team B): ' + tokens[len(tokens) - 1]
								mellowGUIVars.updateScore(int(tokens[0]), int(tokens[len(tokens) - 1]))
							else:
								#print 'THEM(team A): ' + tokens[0]
								#print 'US(team B): ' + tokens[len(tokens) - 1]
								mellowGUIVars.updateScore(int(tokens[len(tokens) - 1]), int(tokens[0]))
			
	except:
		#print 'ERROR: in server listener'
		#print 'ERROR: ' + currentLine
		mellowGUIVars.setMessage("ERROR: in server listener")

def clientListener(connection, mellowGUIVars):
	global gameStarted
	global players
	
	
	try:
		#Sanity testing:
		print 'Card height in client Listener2: ' + str(mellowGUIVars.card_height)
	
		connection.sendMessageToServer(connection.getCurrentPlayerName() + '\n')
		if connection.isHosting() == 1:
			connection.sendMessageToServer('/create mellow mellowpy' + '\n')
		else:
			connection.sendMessageToServer('/join mellowpy' + '\n')
		
		while mellowGUIVars.isStillRunning() == 1:
			if connection.isHosting() == 1 and gameStarted == 0:
				time.sleep(0.2)
				connection.sendMessageToServer('/start' + '\n')
				print 'sent start msg'
			elif gameStarted == 1:
				break
		
		playCardDefault(connection, mellowGUIVars)
		
			
	except:
		print 'ERROR: in client listener'
		mellowGUIVars.setMessage("ERROR: in client listener")

def playCardDefault(connection, mellowGUIVars):
	global players	
	global turn_lock
	global itsYourBid
	global itsYourTurn
	
	playedACardInFight = 0
	
	while mellowGUIVars.isStillRunning() == 1:
		with turn_lock:
			if connection.getInteract() == 0:
				if mellowGUIVars.isNewFightStarting() and playedACardInFight == 1:
					playedACardInFight = 0
				
				if itsYourBid==1:
					print 'Your bid'
					connection.sendMessageToServer('/move 1' + '\n')
					itsYourBid = 0
					itsYourTurn = 0
					print 'sent msg'
					
				elif itsYourTurn==1:
					print 'Your turn'
					connection.sendMessageToServer('/move 1' + '\n')
					playedACardInFight = 1
					itsYourBid = 0
					itsYourTurn = 0
					
			elif connection.getInteract() == 1:
				if mellowGUIVars.isNewFightStarting() and playedACardInFight == 1:
					playedACardInFight = 0
					
				if itsYourBid==1:
					temp = mellowGUIVars.consumeBid()
					if temp >=0:
						connection.sendMessageToServer('/move ' + str(temp) + '\n')
						itsYourBid = 0
						itsYourTurn = 0
				elif itsYourTurn==1:
					if mellowGUIVars.getCardUserWantsToPlay() != '':
						connection.sendMessageToServer('/move ' + str(mellowGUIVars.getCardUserWantsToPlay()) + '\n')
						mellowGUIVars.setCardUserWantsToPlayToNull()
						playedACardInFight = 1
						itsYourBid = 0
						itsYourTurn = 0
		time.sleep(0.2)

#Pre: this should only get called from MellowGUI
def main(mellowGUIVars, args):
	
	if len(args) > 1:
		connection = args[1]
	else:
		connection = clientContext.ClientContext('127.0.0.1', 6789, 'Michael')
	
	print 'HELLO MELLOW CLIENT MAIN'
	
	#start listening t server on a seperate thread:
	try:
		thread.start_new_thread( serverListener, (connection, mellowGUIVars) )
	except:
		print "Error: unable to start thread 1"
		mellowGUIVars.setMessage("Error: unable to start thread 1")
		exit(1)
	
	clientListener(connection, mellowGUIVars)

def slowDownIfInteract(connection, amountOfTime, gameStarted):
	if gameStarted == 1 and (connection.getSlowdown() == 1 or connection.getInteract() == 1):
		time.sleep(amountOfTime)
	
#You have to start it from mellowGUI because pygame has to be the main 
#thread.
if __name__ == "__main__":
	exit(1)