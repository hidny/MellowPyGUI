
#This file holds variables applicable to how the client connects to the server
#and will be used in almost every client python file.

import socket

import time

END_OF_TRANSMISSION = '**end of transmission**'
BUFFER_SIZE = 1024

#This is designed to be a singleton object
#This class holds all info the client should know about
#it's relationship with the server.

class ClientContextTest:
	
	def __init__(self, tcpIP, tcpPort, currentPlayerName):
		self.data = ''
		self.tcpIP = '127.0.0.1'
		self.tcpPort = 6789
		self.currentPlayerName = 'testPlayer'
		self.currentPlayerLocation = ''
		
		self.serverSocket = []
	
		
		self.channelChatBox = ''
		self.waitingRoomChatBox = ''
		
		self.currentGameName = ''
		self.isHost = 0
		
		self.interact = 1
		self.slowdown = 1
		
		try:
			self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.serverSocket.connect((self.tcpIP, int(self.tcpPort)))
			print('Connected')
			
			print(currentPlayerName)
			
			#Sending name:
			self.sendMessageToServer(currentPlayerName + '\n')
			print('Message sent')
			
			print('Debug for 10 seconds')
			time.sleep(10)
			
			serverSocket.close()
		except Exception as e:
			print("ERROR: could not find server. tcpIP: " + str(self.tcpIP) + " tcpPort: " + str(self.tcpPort))
			print("Exception message: " + str(e))
			exit(1)
	

	def sendMessageToServer(self, msg):
		print('Sending: ' + str(msg))
	
		self.serverSocket.send(str(msg).encode())
		print('Sent: ' + str(msg))
	
if __name__ == "__main__":
	ClientContextTest('127.0.0.1', 6789, 'TestPlayer')