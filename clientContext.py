
#This file holds variables applicable to how the client connects to the server
#and will be used in almost every client python file.

import socket

import threading
import thread

import time

END_OF_TRANSMISSION = '**end of transmission**'
BUFFER_SIZE = 1024

#This is designed to be a singleton object
#This class holds all info the client should know about
#it's relationship with the server.

class ClientContext:
	
	def __init__(self, tcpIP, tcpPort, currentPlayerName):
		self.data = ''
		self.tcpIP = tcpIP
		self.tcpPort = tcpPort
		self.currentPlayerName = currentPlayerName
		self.currentPlayerLocation = ''
		
		self.serverSocket = []
		self.sendMsgLock = threading.Lock()
	
		self.recvMsgLock = threading.Lock()
	
		self.currentPlayerName = ''
		
		self.channelChatBox = ''
		self.waitingRoomChatBox = ''
		
		self.currentGameName = ''
		self.isHost = 0
		
		self.interact = 1
		self.slowdown = 1
		
		try:
			self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.serverSocket.connect((self.tcpIP, int(self.tcpPort)))
			print 'Connected'
			
			print currentPlayerName
			
			#Sending name:
			self.sendMessageToServer(currentPlayerName + '\n')
			print 'Message sent'
			
			print 'Start server listener thread:'
			thread.start_new_thread(self.getServerMessages, ())
			
			print 'Get client name according to server:'
			message = ''
			while message == '':
				message = self.getNextServerMessageInQueue()
				time.sleep(0.5)
			
			self.currentPlayerName = message.split(' ')[1]
			self.currentPlayerName = self.currentPlayerName[0:-1]
			
			print 'Your name is now: ' + self.currentPlayerName
			
			print 'Done starting client-server context'
			
		except:
			print "ERROR: could not find server. tcpIP: " + str(self.tcpIP) + " tcpPort: " + str(self.tcpPort)
			exit(1)
	

	def sendMessageToServer(self, msg):
		with self.sendMsgLock:
			self.serverSocket.send(str(msg))
			print 'Sent: ' + str(msg)
	
	
	messageFromServerQueue = []
	
	#consume messages from queue:
	def getNextServerMessageInQueue(self):
		with self.recvMsgLock:
			if len(self.messageFromServerQueue) == 0:
				return ''
			else:
				ret = self.messageFromServerQueue[0]
				del self.messageFromServerQueue[0]
				return ret
	
	def reinsertMessageAtFrontOfQueue(self, message):
		with self.recvMsgLock:
			self.messageFromServerQueue.insert(0, message + '\n')
			
	
	#get messages from server and produce them on queue:
	def getServerMessages(self):
		global END_OF_TRANSMISSION
		
		try:
			
			while 1 == 1:
				if END_OF_TRANSMISSION in self.data:
					message = self.data[0: self.data.index(END_OF_TRANSMISSION)]
					self.data = self.data[self.data.index(END_OF_TRANSMISSION) + len(END_OF_TRANSMISSION):]
					
					#print 'Received in clientContext: ' + message
					with self.recvMsgLock:
						self.messageFromServerQueue.append(message)
						
					
					while len(self.data) > 0 and self.data[0] == '\n':
						self.data = self.data[1:]
					
				else:
					if self.data == '':
						self.data = self.serverSocket.recv(BUFFER_SIZE)
					else:
						self.data = self.data + self.serverSocket.recv(BUFFER_SIZE)
		except:
			print 'ERROR: in server listener (ClientContext.py)'
	
	def setChannelChatBox(self, channelChatBox):
		self.channelChatBox = channelChatBox
		
	def getChannelChatBox(self):
		return self.channelChatBox
	
	def setWaitingRoomChatBox(self, waitingRoomChatBox):
		self.waitingRoomChatBox = waitingRoomChatBox
		
	def getWaitingRoomChatBox(self):
		return self.waitingRoomChatBox
	
	def setCurrentGameName(self, gameName):
		self.currentGameName = gameName
		
	def getCurrentGameName(self):
		return self.currentGameName
	
	
	def setHost(self):
		self.isHost = 1
		
	def setJoiner(self):
		self.isHost = 0
	
	def isHosting(self):
		return self.isHost
	
	
	def setInteract(self, interact):
		self.interact = interact
	
	def getInteract(self):
		return self.interact
	
	
	def setSlowdown(self, slowdown):
		self.slowdown = slowdown
	
	def getSlowdown(self):
		return self.interact
	
	def getCurrentPlayerName(self):
		return self.currentPlayerName
		