#!/usr/bin/env python
import sys
import time

import threading
import thread

import euchreGUI
import projectile
import clientContext

#It's static because I only want one euchre client for the whole execution.

#Euchre specific constants:
START_MSG = 'Starting Euchre!'
VARIATION = 'Variation:'

CALLING_ROUND1 = "Starting 1st calling round:"
CALLING_ROUND2 = "Starting 2nd calling round:"

YOUR_CALL = 'What\'s your call?'
YOUR_TURN = 'Play a card!'
YOUR_EXCHANGE = 'Pick a card to exchange with the trump card'
YOUR_NEW_HAND = 'Your new hand: '

PRIVATE_MSG = 'From Game(private):'
PUBLIC_MSG = 'From Game(public): '

#first dealer:
FIRST_DEALER = 'First dealer is '
DEALER_MSG = 'dealer is '
TRUMP_CARD = 'Trump card is '

PASSES = 'passes'
#1st round of calling:
ORDER_UP = 'orders up the dealer'
PICK_UP = 'picks up'
#2nd round of calling:
DECLARE = 'declares'
ALONE = ' and is going alone'


FIGHT_SUMMARY_MSG = 'Fight Winner:'

#From Game(private): JC KS 9C AC AH
STARTING_HAND_LENGTH = 5

TRICKS = 'trick(s).'

PLAYING_CARD = 'playing:'
WIN = 'win!'

END_OF_ROUND = 'END OF ROUND!'
END_OF_ROUND2 = 'Misdeal!'

#End Euchre specific constants

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


def serverListener(connection, euchreGUIVars):

	global gameStarted
	global players
	global turn_lock
	global itsYourBid
	global itsYourTurn
	
	playerInTeamA = 1
	isRoundSetup = 0
	
	try:
	
		#Sanity testing:
		print 'Card height in server Listener: ' + str(euchreGUIVars.card_height)
		
		while euchreGUIVars.isGameOver() == 0:
			message = connection.getNextServerMessageInQueue()
			
			currentLines = message.split('\n')
			
			for currentLine in currentLines:
				if len(currentLine) > 1:
					print '*****************************'
					print "received message2: " + str(currentLine)
					
				
				
				if currentLine.startswith(PUBLIC_MSG):
					if currentLine.find(START_MSG) != -1:
						gameStarted = 1
						#Starting Euchre! Michael & Dick vs Dad & Mom
						#team A
						#Trying to send: From Game(public): Starting Euchre! Michael & Dick vs Dad & Mom
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
						
						print 'Euchre Client test: game starting'
					
					elif currentLine.find(VARIATION) != -1:
						euchreGUIVars.setVariation(currentLine.split(' ')[3])
				
					elif currentLine.find(TRUMP_CARD) != -1:
						card = currentLine.split(' ')[5]
						#From Game(public): Trump card is 9H
						euchreGUIVars.setTrumpCard(card)
					
					
					elif currentLine.find(CALLING_ROUND1) != -1:
						print 'Setting bidding round to 1'
						euchreGUIVars.setBiddingRound(1)
						
					elif currentLine.find(CALLING_ROUND2) != -1:
						print 'Setting bidding round to 2'
						euchreGUIVars.setBiddingRound(2)
						
					elif currentLine.find(PLAYING_CARD) != -1:
						#From Game(public): Michael playing: 9S
						player = currentLine.split(' ')[2]
						card = currentLine.split(' ')[4]
						
						if isACard(card) == 0:
							print 'UH OH! Could not find card: ' + str(card)
							sys.exit(1)
						
						if players[0] != player:
							slowDownIfInteract(connection, 0.25, gameStarted)
						
						if players[0] == player:
							print 'South(' + player + ') plays ' + card
							euchreGUIVars.throwSouthCard(card)
						elif players[1] == player:
							print 'West(' + player + ') plays ' + card
							euchreGUIVars.throwWestCard(card)
						elif players[2] == player:
							print 'North(' + player + ') plays ' + card
							euchreGUIVars.throwNorthCard(card)
						elif players[3] == player:
							print 'East(' + player + ') plays ' + card
							euchreGUIVars.throwEastCard(card)
						else:
							print 'ERROR: unknown player plays card!'
							sys.exit(1)
						
						#get relative player direction
						#make it print: west plays x
						#or north plays y
						#Let some other class deal with this.
						
					
					elif currentLine.find(DEALER_MSG) != -1:
						#From Game(public): First dealer is Mom
						#From Game(public): Dealer: Michael
						dealer = message.split(' ')[len(message.split(' ')) - 1]
						while dealer[len(dealer) -1] == '\n':
							dealer = dealer[0:-1]
						
						if players[0]  == dealer:
							print 'Dealer is South(' + dealer + ')'
							euchreGUIVars.setDealerString("South(" + dealer + ")")
							
						elif players[1] == dealer:
							print 'Dealer is West(' + dealer + ')'
							euchreGUIVars.setDealerString("West(" + dealer + ")")
							
						elif players[2] == dealer:
							print 'Dealer is North(' + dealer + ')'
							euchreGUIVars.setDealerString("North(" + dealer + ")")
							
						elif players[3] == dealer:
							print 'Dealer is East(' + dealer + ')'
							euchreGUIVars.setDealerString("East(" + dealer + ")")
							
						else:
							print 'current dealer: ' + dealer
							print 'ERROR: unknown dealer'
							sys.exit(1)
						
					
					
					elif currentLine.find(FIGHT_SUMMARY_MSG) != -1:
						slowDownIfInteract(connection, 1, gameStarted)
						euchreGUIVars.remove_Projectiles()
						
						fightWinner = message.split(' ')[len(message.split(' ')) - 1]
						while fightWinner[len(fightWinner) -1] == '\n':
							fightWinner = fightWinner[0:-1]
						
						if players[0]  == fightWinner:
							euchreGUIVars.addTrickSouth()
							print 'Fight Winner is South(' + fightWinner + ')'
							
						elif players[1] == fightWinner:
							euchreGUIVars.addTrickWest()
							print 'Fight Winner is West(' + fightWinner + ')'
							
						elif players[2] == fightWinner:
							euchreGUIVars.addTrickNorth()
							print 'Fight Winner is North(' + fightWinner + ')'
							
						elif players[3] == fightWinner:
							euchreGUIVars.addTrickEast()
							print 'Fight Winner is East(' + fightWinner + ')'
							
						else:
							print 'current fightWinner: ' + fightWinner
							print 'ERROR: unknown fight winner'
							sys.exit(1)
				
					elif currentLine.find(WIN) != -1:
						print message[message.index(PUBLIC_MSG) + len(PUBLIC_MSG):]
						euchreGUIVars.setMessage(message[message.index(PUBLIC_MSG) + len(PUBLIC_MSG):-1])
						euchreGUIVars.setGameOver()
				
					elif currentLine.find(TRICKS) != -1:
						#From Game(public): ALL: Mom got 4 trick(s).
						slowDownIfInteract(connection, 1, gameStarted)
						
						#Trying to send: From Game(public): ALL: Michael got 1 trick(s).
						player = message.split(' ')[3]
						number = message.split(' ')[5]
						
						if players[0]  == player:
							print 'python South(' + player + ') has ' + number + ' trick(s).'
						elif players[1] == player:
							print 'West(' + player + ') has ' + number + ' trick(s).'
						elif players[2] == player:
							print 'North(' + player + ') has ' + number + ' trick(s).'
						elif players[3] == player:
							print 'East(' + player + ') has ' + number + ' trick(s).'
						else:
							print 'current player: ' + player
							print 'ERROR: unknown player has tricks.'
							sys.exit(1)
				
				
					elif currentLine.find(END_OF_ROUND) != -1 or currentLine.find(END_OF_ROUND2) != -1:
						isRoundSetup = 0
					
					if currentLine.find(PASSES) != -1 or currentLine.find(ORDER_UP) != -1 or currentLine.find(PICK_UP) != -1 or currentLine.find(DECLARE) != -1:
					#Euchre ack received: From Game(public): Dad orders up the dealer and is going alone.
						
						#GET Bidder:
						#Check if it's a bid:
						#From Game(public): Dad: 1
						msgTokens = message.split(' ')
						bidder = msgTokens[2]
						
						if currentLine.find(PASSES) != -1:
							bid = 'p'
						elif currentLine.find(ORDER_UP) != -1:
							bid = 'order up (' + euchreGUIVars.getTrumpCard() + ')'
							if dealer != players[0]:
								euchreGUIVars.coverTrumpCard()
							
						elif currentLine.find(PICK_UP) != -1:
							bid = 'picks up (' + euchreGUIVars.getTrumpCard() + ')'
							if dealer != players[0]:
								euchreGUIVars.coverTrumpCard()
							
						elif currentLine.find(DECLARE) != -1:
						
							if currentLine.find('spades') != -1:
								#bid = 'declares spade'
								bid = 'spades'
							elif currentLine.find('clubs') != -1:
								#bid = 'declares clubs'
								bid = 'clubs'
							elif currentLine.find('hearts') != -1:
								#bid = 'declares hearts'
								bid = 'hearts'
							elif currentLine.find('diamonds') != -1:
								#bid = 'declares diamonds'
								bid = 'diamonds'
							else:
								print 'ERROR: unknown trump! CurrentLine:' + currentLine
								sys.exit(1)
						
						if currentLine.find(ALONE) != -1:
							bid = bid + ' alone'
						'''
						PASSES = 'passes'
						#1st round of calling:
						ORDER_UP = 'orders up the dealer'
						PICK_UP = 'picks up'
						#2nd round of calling:
						DECLARE = 'declares'
						ALONE = ' and is going alone'
						'''
						
						
						if players[0]  == bidder:
							euchreGUIVars.bidSouth(bid)
							print 'South(' + bidder + ') bids :' + bid
						
						elif players[1] == bidder:
							euchreGUIVars.bidWest(bid)
							print 'West(' + bidder + ') bids :' + bid
						
						elif players[2] == bidder:
							euchreGUIVars.bidNorth(bid)
							print 'North(' + bidder + ') bids :' + bid
						
						elif players[3] == bidder:
							euchreGUIVars.bidEast(bid)
							print 'East(' + bidder + ') bids :' + bid
						
						else:
							print 'ERROR: unknown player bids'
							sys.exit(1)
				
					
					#if all other public messages are false, go here:
					else:
						
						currentScores = currentLine[currentLine.find(PUBLIC_MSG) + len(PUBLIC_MSG):]
						currentScores = currentScores.strip()
						tokens = currentScores.split(' ')
						if len(tokens) > 1 and isNumber(tokens[0]) == 1 and isNumber(tokens[len(tokens) - 1]) == 1 and isRoundSetup == 0:
							
							print 'Current Total:'
							
							print 'Tell Euchre GUI about current total and let it figure everything else out:'
							if playerInTeamA == 1:
								print 'US(team A): ' + tokens[0]
								print 'THEM(team B): ' + tokens[len(tokens) - 1]
								euchreGUIVars.updateScore(int(tokens[0]), int(tokens[len(tokens) - 1]))
							else:
								print 'THEM(team A): ' + tokens[0]
								print 'US(team B): ' + tokens[len(tokens) - 1]
								euchreGUIVars.updateScore(int(tokens[len(tokens) - 1]), int(tokens[0]))
					
						
				
				#DONE public message handling
				
				#Start private message handling
				elif currentLine.startswith(PRIVATE_MSG):
					currentLine = currentLine[currentLine.index(PRIVATE_MSG) + len(PRIVATE_MSG):]
					currentLine = currentLine.strip()
					cardsTemp = currentLine.split(' ')
					
					if currentLine.find(YOUR_CALL) != -1:
						currentLine = currentLine[currentLine.index(YOUR_CALL) + len(YOUR_CALL):]
						with turn_lock:
							itsYourBid=1
							print 'Its my bid!'
							if connection.getInteract() == 1:
								euchreGUIVars.askUserForBid()
						
					
					elif currentLine.find(YOUR_TURN) != -1:
						currentLine = currentLine[currentLine.index(YOUR_TURN) + len(YOUR_TURN):]
						with turn_lock:
							itsYourTurn=1
					
					elif currentLine.find(YOUR_EXCHANGE) != -1:
						with turn_lock:
							itsYourTurn=1
					
					elif currentLine.find(YOUR_NEW_HAND) != -1:
						currentLine = currentLine[currentLine.index(YOUR_NEW_HAND) + len(YOUR_NEW_HAND):]
						currentLine = currentLine.strip()
						cardsTemp = currentLine.split(' ')
						euchreGUIVars.letDealerExchangeCard(cardsTemp)
						
						print 'Printing cards:'
						for card in cardsTemp:
							print card
						print 'Done printing cards'
					
					elif isACard(cardsTemp[0]) == 1:
						if len(cardsTemp) == STARTING_HAND_LENGTH and isRoundSetup ==0:
							euchreGUIVars.setupCardsForNewRound(cardsTemp)
							isRoundSetup = 1
						
						print 'Printing cards:'
						for card in cardsTemp:
							print card
						print 'Done printing cards'
				
				
				#Done private message handling
				
				
				
			
	except:
		print 'ERROR: in server listener'
		print 'ERROR: ' + currentLine
		euchreGUIVars.setMessage("ERROR: in server listener")

def clientListener(connection, euchreGUIVars):
	global gameStarted
	global players
	
	
	try:
		#Sanity testing:
		print 'Card height in client Listener2: ' + str(euchreGUIVars.card_height)
	
		connection.sendMessageToServer(connection.getCurrentPlayerName() + '\n')
		if connection.isHosting() == 1:
			connection.sendMessageToServer('/create euchre euchrepy' + '\n')
		else:
			connection.sendMessageToServer('/join euchrepy' + '\n')
		
		while euchreGUIVars.isGameOver() == 0:
			if connection.isHosting() == 1 and gameStarted == 0:
				time.sleep(0.2)
				connection.sendMessageToServer('/start' + '\n')
				print 'sent start msg'
			elif gameStarted == 1:
				break
		
		playCardDefault(connection, euchreGUIVars)
		
			
	except:
		print 'ERROR: in client listener'
		euchreGUIVars.setMessage("ERROR: in client listener")

def playCardDefault(connection, euchreGUIVars):
	global players	
	global turn_lock
	global itsYourBid
	global itsYourTurn
	
	playedACardInFight = 0
	
	while euchreGUIVars.isGameOver() == 0:
		with turn_lock:
			if connection.getInteract() == 0:
				if euchreGUIVars.isNewFightStarting() and playedACardInFight == 1:
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
				if euchreGUIVars.isNewFightStarting() and playedACardInFight == 1:
					playedACardInFight = 0
					
				if itsYourBid==1:
					temp = euchreGUIVars.consumeBid()
					if temp != '':
						print 'TESTING: ' + '/move ' + str(temp)
						connection.sendMessageToServer('/move ' + str(temp) + '\n')
						itsYourBid = 0
						itsYourTurn = 0
				elif itsYourTurn==1:
					if euchreGUIVars.getCardUserWantsToPlay() != '':
						connection.sendMessageToServer('/move ' + str(euchreGUIVars.getCardUserWantsToPlay()) + '\n')
						euchreGUIVars.setCardUserWantsToPlayToNull()
						playedACardInFight = 1
						itsYourBid = 0
						itsYourTurn = 0
		

#Pre: this should only get called from EuchreGUI
def main(euchreGUIVars, args):
	
	if len(args) > 1:
		connection = args[1]
	else:
		connection = clientContext.ClientContext('127.0.0.1', 6789, 'Michael')
	
	print 'HELLO MELLOW CLIENT MAIN'
	
	#start listening t server on a seperate thread:
	try:
		thread.start_new_thread( serverListener, (connection, euchreGUIVars) )
	except:
		print "Error: unable to start thread 1"
		euchreGUIVars.setMessage("Error: unable to start thread 1")
		exit(1)
	
	clientListener(connection, euchreGUIVars)

def slowDownIfInteract(connection, amountOfTime, gameStarted):
	if gameStarted == 1 and (connection.getSlowdown() == 1 or connection.getInteract() == 1):
		time.sleep(amountOfTime)
	
#You have to start it from euchreGUI because pygame has to be the main 
#thread.
if __name__ == "__main__":
	exit(1)