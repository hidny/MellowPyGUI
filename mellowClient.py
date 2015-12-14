#!/usr/bin/env python
import sys
import time

import socket
import threading
import thread

import mellowGUI
import projectile
#October 22, 2015: It's static because I only want one mellow client for the whole execution.

#TODO:
# DONE! 1) update scores
# DONE! 2) Sanity check tricks.
# 3) Send useful updates to a middleman that will then send variable to AI or GUI.
# 4) Make Middle man file that takes msgs from here and sends them to some player interface.
# 5) Implement the player interface with the GUI and with an AI.

#DONE: does turn lock even make sense? YES!
#DONE! Allow user to bid.

#Key: do multithread. (NOT: multiprocesses)

END_OF_TRANSMISSION = '**end of transmission**'

BUFFER_SIZE = 1024

#http://stackoverflow.com/questions/419145/python-threads-critical-section
turn_lock = threading.Lock()

sendMsgLock = threading.Lock()


gameStarted = 0
HELLO_MSG = 'Hello'
START_MSG = 'Starting Mellow!'
players = []
currentPlayerName = ''
itsYourBid = 0
itsYourTurn = 0

isBiddingPhase = 0
isPlayingPhase = 0

playerInTeamA = 1
teamAScore = 0
teamBScore = 0

tricks = []
endOfRoundIndex = 0

YOUR_BID = 'Game(private): What\'s your bid?'
YOUR_TURN = 'Game(private): Play a card!'
PRIVATE_MSG = 'From Game(private):'
PUBLIC_MSG = 'From Game(public): '
#first dealer:
FIRST_DEALER = 'From Game(public): First dealer is '
DEALER_MSG = 'dealer is '
FIGHT_SUMMARY_MSG = 'From Game(public): Fight Winner:'
#From Game(private): 7C KS 9C AC AH 2S 4D KC KH 2D 7H 9S 7S 
TRICKS = 'trick(s).'

cardsInHand = []

#playing
PLAYING_CARD = 'playing:'
PUBLIC_SERVER_MSG = 'From Game(public): '
WIN = 'win!'
END_OF_ROUND = 'END ROUND!'

serverSocket = []

#What's your bid?
#Dealer: Mom
#Game(private): Play a card!
#TODO: make sure messages are coming from the server and not some client.
#From Game(private): 6C AC JH 9H 7C 3H QS 4D AS 4S 8S 
#From Game(public): Michael playing: 9S

#From Game(public): Fight Winner: Mom (Take the server's word for it?)
#TODO: server bids and score are a bit unclear... meh.
#DECODE THIS:
#TODO: add "From Game(public): Michael & Dick vs Mom & Dad"
#TODO: do the same for the bids.
#From Game(public): 100    96
#From Game(public): 25    24
#From Game(public): 125    120

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

#TODO: use starts with instead of find to avoid hacking.
#aString.startswith("hello")
def serverListener(name, isHostingGame, mellowGUIVars, interact, slowdown):
	global gameStarted
	global players
	global currentPlayerName
	
	global turn_lock
	global itsYourBid
	global itsYourTurn
	global playerInTeamA
	
	global endOfRoundIndex
	global serverSocket
	
	try:
	
		#Sanity testing:
		print 'Card height in server Listener: ' + str(mellowGUIVars.card_height)
		
		data =''
		while mellowGUIVars.isStillRunning() == 1:
			if data != '':
				data = data + serverSocket.recv(BUFFER_SIZE)
			else:
				data = serverSocket.recv(BUFFER_SIZE)
			
			#print 'DATA: ' + str(data)
			while END_OF_TRANSMISSION in data:
				message = data[0: data.index(END_OF_TRANSMISSION)]
				data = data[data.index(END_OF_TRANSMISSION) + len(END_OF_TRANSMISSION):]
				
				while len(data) > 0 and data[0] == '\n':
					data = data[1:]
				
				currentLines = message.split('\n')
				
				for currentLine in currentLines:
					if len(currentLine) > 1:
						print '*****************************'
						print "received message: " + str(currentLine)
						
					if currentLine.find(HELLO_MSG) != -1:
						currentLine = currentLine[currentLine.index(HELLO_MSG) + len(HELLO_MSG):]
						currentPlayerName = currentLine.split(' ')[1][0:-1]
						
					elif currentLine.find(START_MSG) != -1:
						gameStarted = 1
						#Starting Mellow! Michael & Dick vs Dad & Mom
						#team A
						#Trying to send: From Game(public): Starting Mellow! Michael & Dick vs Dad & Mom
						currentLine = currentLine[currentLine.index(START_MSG) + len(START_MSG):]
						players.append(currentLine.split(' ')[1])
						players.append(currentLine.split(' ')[5])
						players.append(currentLine.split(' ')[3])
						players.append(currentLine.split(' ')[7])
						
						while players[0] != currentPlayerName:
							players = shiftArrayByOne(players)
							if playerInTeamA == 0:
								playerInTeamA = 1
							else:
								playerInTeamA = 0
						
						
					elif currentLine.find(YOUR_BID) != -1:
						currentLine = currentLine[currentLine.index(YOUR_BID) + len(YOUR_BID):]
						with turn_lock:
							itsYourBid=1
							print 'Its my bid!'
							if interact == 1:
								mellowGUIVars.askUserForBid()
						
					
					elif currentLine.find(YOUR_TURN) != -1:
						currentLine = currentLine[currentLine.index(YOUR_TURN) + len(YOUR_TURN):]
						with turn_lock:
							itsYourTurn=1
					
					elif currentLine.find(PUBLIC_SERVER_MSG) != -1:
						if currentLine.find(PLAYING_CARD) != -1:
							#From Game(public): Michael playing: 9S
							player = currentLine.split(' ')[2]
							card = currentLine.split(' ')[4]
							
							if isACard(card) == 0:
								print 'UH OH! Could not find card: ' + str(card)
								sys.exit(1)
							
							if players[0] != player:
								slowDownIfInteract(0.25, gameStarted, slowdown, interact)
							
							if players[0] == player:
								print 'South(' + player + ') plays ' + card
								mellowGUIVars.throwSouthCard(card)
							elif players[1] == player:
								print 'West(' + player + ') plays ' + card
								mellowGUIVars.throwWestCard(card)
							elif players[2] == player:
								print 'North(' + player + ') plays ' + card
								mellowGUIVars.throwNorthCard(card)
							elif players[3] == player:
								print 'East(' + player + ') plays ' + card
								mellowGUIVars.throwEastCard(card)
							else:
								print 'ERROR: unknown player plays card!'
								sys.exit(1)
							#TODO: send this fact to some AI or GUI program so it could think.
							
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
										print 'South(' + bidder + ') bids ' + bid
										
									elif players[1] == bidder:
										mellowGUIVars.bidWest(bid)
										print 'West(' + bidder + ') bids ' + bid
										
									elif players[2] == bidder:
										mellowGUIVars.bidNorth(bid)
										print 'North(' + bidder + ') bids ' + bid
										
									elif players[3] == bidder:
										mellowGUIVars.bidEast(bid)
										print 'East(' + bidder + ') bids ' + bid
										
									else:
										print 'ERROR: unknown player bids'
										sys.exit(1)
						#TODO: send this fact to some AI or GUI program so it could think.
							
						
					if currentLine.find(PRIVATE_MSG) != -1:
						currentLine = currentLine[currentLine.index(PRIVATE_MSG) + len(PRIVATE_MSG):]
						currentLine = currentLine.strip()
						cardsTemp = currentLine.split(' ')
						
						
						if len(cardsTemp) > 0 and isACard(cardsTemp[0]) == 1:
							if len(cardsTemp) == 13:
								mellowGUIVars.setupCardsForNewRound(cardsTemp)
							
							print 'Printing cards:'
							for card in cardsTemp:
								print card
							print 'Done printing cards'
				
					if currentLine.find(PUBLIC_MSG) != -1 and currentLine.find(DEALER_MSG) != -1:
						#From Game(public): First dealer is Mom
						#From Game(public): Dealer: Michael
						dealer = message.split(' ')[len(message.split(' ')) - 1]
						while dealer[len(dealer) -1] == '\n':
							dealer = dealer[0:-1]
						
						if players[0]  == dealer:
							print 'Dealer is South(' + dealer + ')'
							mellowGUIVars.setDealer("South(" + dealer + ")")
							
						elif players[1] == dealer:
							print 'Dealer is West(' + dealer + ')'
							mellowGUIVars.setDealer("West(" + dealer + ")")
							
						elif players[2] == dealer:
							print 'Dealer is North(' + dealer + ')'
							mellowGUIVars.setDealer("North(" + dealer + ")")
							
						elif players[3] == dealer:
							print 'Dealer is East(' + dealer + ')'
							mellowGUIVars.setDealer("East(" + dealer + ")")
							
						else:
							print 'current dealer: ' + dealer
							print 'ERROR: unknown dealer'
							sys.exit(1)
					
					if currentLine.find(PUBLIC_MSG) != -1 and currentLine.find(FIGHT_SUMMARY_MSG) != -1:
						slowDownIfInteract(1, gameStarted, slowdown, interact)
						mellowGUIVars.remove_Projectiles()
						
						#copy of dealer logic:
						fightWinner = message.split(' ')[len(message.split(' ')) - 1]
						while fightWinner[len(fightWinner) -1] == '\n':
							fightWinner = fightWinner[0:-1]
						
						if players[0]  == fightWinner:
							mellowGUIVars.addTrickSouth()
							print 'Fight Winner is South(' + fightWinner + ')'
							#mellowGUIVars.setMessage('Fight Winner is South(' + fightWinner + ')')
							
						elif players[1] == fightWinner:
							mellowGUIVars.addTrickWest()
							print 'Fight Winner is West(' + fightWinner + ')'
							#mellowGUIVars.setMessage('Fight Winner is West(' + fightWinner + ')')
							
						elif players[2] == fightWinner:
							mellowGUIVars.addTrickNorth()
							print 'Fight Winner is North(' + fightWinner + ')'
							#mellowGUIVars.setMessage('Fight Winner is North(' + fightWinner + ')')
							
						elif players[3] == fightWinner:
							mellowGUIVars.addTrickEast()
							print 'Fight Winner is East(' + fightWinner + ')'
							#mellowGUIVars.setMessage('Fight Winner is East(' + fightWinner + ')')
							
						else:
							print 'current fightWinner: ' + fightWinner
							print 'ERROR: unknown fight winner'
							sys.exit(1)
						#End copy
					
					if currentLine.find(PUBLIC_MSG) != -1 and currentLine.find(WIN) != -1:
						print message[message.index(PUBLIC_MSG) + len(PUBLIC_MSG):]
						#TODO: make a better msg.
					
					if currentLine.find(PUBLIC_MSG) != -1 and currentLine.find(TRICKS) != -1:
						#From Game(public): ALL: Mom got 4 trick(s).
						slowDownIfInteract(1, gameStarted, slowdown, interact)
						
						#TODO: send this update somewhere.
						#Trying to send: From Game(public): ALL: Michael got 1 trick(s).
						player = message.split(' ')[3]
						number = message.split(' ')[5]
						
						if players[0]  == player:
							print 'python South(' + player + ') has ' + number + ' tricks.'
						elif players[1] == player:
							print 'West(' + player + ') has ' + number + ' tricks.'
						elif players[2] == player:
							print 'North(' + player + ') has ' + number + ' tricks.'
						elif players[3] == player:
							print 'East(' + player + ') has ' + number + ' tricks.'
						else:
							print 'current player: ' + player
							print 'ERROR: unknown player has tricks.'
							sys.exit(1)
					
						#End copy
					#TODO:
					#At round end, update score
					#and sanity check tricks.
					
					if currentLine.find(PUBLIC_MSG) != -1 and currentLine.find(END_OF_ROUND) != -1:
						endOfRoundIndex = 0
					
					if currentLine.find(PUBLIC_MSG) != -1:# and endOfRoundIndex < 3:
						
						currentScores = currentLine[currentLine.find(PUBLIC_MSG) + len(PUBLIC_MSG):]
						currentScores = currentScores.strip()
						tokens = currentScores.split(' ')
						if len(tokens) > 1 and isNumber(tokens[0]) == 1 and isNumber(tokens[len(tokens) - 1]) == 1:
							endOfRoundIndex = endOfRoundIndex + 1
							print '***'
							print '**TESTING: in getting current Score if cond'
							print '**'
							if endOfRoundIndex == 1:
								print 'previous scores: '
							elif endOfRoundIndex == 2:
								print 'Scores added: '
							else:
								print 'Current Total:'
							
							if playerInTeamA == 1:
								print 'US(team A): ' + tokens[0]
								print 'THEM(team B): ' + tokens[len(tokens) - 1]
								mellowGUIVars.updateScore(int(tokens[0]), int(tokens[len(tokens) - 1]))
							else:
								print 'THEM(team A): ' + tokens[0]
								print 'US(team B): ' + tokens[len(tokens) - 1]
								mellowGUIVars.updateScore(int(tokens[len(tokens) - 1]), int(tokens[0]))
			
	except:
		print 'ERROR: in server listener'
		mellowGUIVars.setMessage("ERROR: in server listener")

def clientListener(name, isHostingGame, mellowGUIVars, interact, slowdown):
	global gameStarted
	global players
	
	global serverSocket
	
	try:
		#Sanity testing:
		print 'Card height in client Listener2: ' + str(mellowGUIVars.card_height)
	
		sendMessageToServer(serverSocket, name + '\n')
		if isHostingGame == 1:
			sendMessageToServer(serverSocket, '/create mellow mellowpy' + '\n')
		else:
			sendMessageToServer(serverSocket, '/join mellowpy' + '\n')
		
		#TODO: PUT THIS INTO FUNCTION
		while mellowGUIVars.isStillRunning() == 1:
			if isHostingGame == 1 and gameStarted == 0:
				time.sleep(0.2)
				sendMessageToServer(serverSocket, '/start' + '\n')
				print 'sent start msg'
			elif gameStarted == 1:
				break
			
		'''
		playedACardInFight = 0
			
		while mellowGUIVars.isStillRunning() == 1:
			if isHostingGame == 1 and gameStarted == 0:
				time.sleep(0.2)
				sendMessageToServer(serverSocket, '/start' + '\n')
				print 'sent start msg'
			
			if interact == 0:
				if mellowGUIVars.isNewFightStarting() and playedACardInFight == 1:
					playedACardInFight = 0
				
				if itsYourBid==1:
					print 'Your bid'
					with turn_lock:
						#TODO: put this back!
						sendMessageToServer(serverSocket, '/move 1' + '\n')
						itsYourBid = 0
						itsYourTurn = 0
						print 'sent msg'
					
				elif itsYourTurn==1:
					print 'Your turn'
					with turn_lock:
						sendMessageToServer(serverSocket, '/move 1' + '\n')
						playedACardInFight = 1
						itsYourBid = 0
						itsYourTurn = 0
					
			elif interact == 1:
				if mellowGUIVars.isNewFightStarting() and playedACardInFight == 1:
					playedACardInFight = 0
					
				if itsYourBid==1:
					temp = mellowGUIVars.consumeBid()
					if temp >=0:
						with turn_lock:
							sendMessageToServer(serverSocket, '/move ' + str(temp) + '\n')
							itsYourBid = 0
							itsYourTurn = 0
				elif itsYourTurn==1:
					if mellowGUIVars.getCardUserWantsToPlay() != '':
						with turn_lock:
							sendMessageToServer(serverSocket, '/move ' + str(mellowGUIVars.getCardUserWantsToPlay()) + '\n')
							mellowGUIVars.setCardUserWantsToPlayToNull()
							playedACardInFight = 1
							itsYourBid = 0
							itsYourTurn = 0
		'''
		playCardDefault(name, isHostingGame, mellowGUIVars, interact, slowdown, serverSocket)
		#ENDTODO: PUT THIS INTO FUNCTION
		
			
	except:
		print 'ERROR: in client listener'
		mellowGUIVars.setMessage("ERROR: in client listener")

#TODO:
def playCardDefault(name, isHostingGame, mellowGUIVars, interact, slowdown, serverSocketInput):
	global currentPlayerName
	global players
	
	global turn_lock
	global itsYourBid
	global itsYourTurn
	global serverSocket
	
	serverSocket = serverSocketInput
	playedACardInFight = 0
	
	while mellowGUIVars.isStillRunning() == 1:
		with turn_lock:
			if interact == 0:
				if mellowGUIVars.isNewFightStarting() and playedACardInFight == 1:
					playedACardInFight = 0
				
				if itsYourBid==1:
					print 'Your bid'
					sendMessageToServer(serverSocket, '/move 1' + '\n')
					itsYourBid = 0
					itsYourTurn = 0
					print 'sent msg'
					
				elif itsYourTurn==1:
					print 'Your turn'
					sendMessageToServer(serverSocket, '/move 1' + '\n')
					playedACardInFight = 1
					itsYourBid = 0
					itsYourTurn = 0
					
			elif interact == 1:
				if mellowGUIVars.isNewFightStarting() and playedACardInFight == 1:
					playedACardInFight = 0
					
				if itsYourBid==1:
					temp = mellowGUIVars.consumeBid()
					if temp >=0:
						sendMessageToServer(serverSocket, '/move ' + str(temp) + '\n')
						itsYourBid = 0
						itsYourTurn = 0
				elif itsYourTurn==1:
					if mellowGUIVars.getCardUserWantsToPlay() != '':
						sendMessageToServer(serverSocket, '/move ' + str(mellowGUIVars.getCardUserWantsToPlay()) + '\n')
						mellowGUIVars.setCardUserWantsToPlayToNull()
						playedACardInFight = 1
						itsYourBid = 0
						itsYourTurn = 0
		

def main(mellowGUIVars, args):
	global serverSocket
	print 'HELLO MELLOW CLIENT MAIN'
	if len(args) > 1:
		name = args[1]
	else:
		name = 'Michael'
	
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
		elif args[x].find('ip=') != -1:
			tcpIP = str(args[x][len('ip='):])
		elif args[x].find('p=') != -1:
			tcpPort = int(args[x][len('p='):])
	
	print 'IP: ' + str(tcpIP)
	print 'PORT: ' + str(tcpPort)
	print 'name: ' + str(name)
	
	#Connect to server:
	try:
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverSocket.connect((tcpIP, int(tcpPort)))
	except:
		print "ERROR: could not find server."
		mellowGUIVars.setMessage("ERROR: could not find server.")
		exit(1)
	
	#start listening t server on a seperate thread:
	try:
		thread.start_new_thread( serverListener, (name, isHostingGame, mellowGUIVars, interact, slowdown) )
	except:
		print "Error: unable to start thread 1"
		mellowGUIVars.setMessage("Error: unable to start thread 1")
		exit(1)
	
	clientListener(name, isHostingGame, mellowGUIVars, interact, slowdown)

def sendMessageToServer(serverSocket, msg):
	global sendMsgLock
	with sendMsgLock:
		serverSocket.send(str(msg))
	
def slowDownIfInteract(amountOfTime, gameStarted, slowdown, interact):
	if gameStarted == 1 and (slowdown == 1 or interact == 1):
		time.sleep(amountOfTime)
	
if __name__ == "__main__":
	main('testing', sys.argv)