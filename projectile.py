import random

#This class deals with the animation of cards being thrown into the middle of the table.
#Pre: the GUI must have a function named: printProjectile(x, y, id, rotation)

class Projectile:

	def __init__(self, beingThrown, startX, startY, endX, endY, projectileId, rotation, percStop = 0):
		self.beingThrown=beingThrown
		self.startX = startX
		self.startY = startY
		self.endX   = endX
		self.endY   = endY
		self.projectileId = projectileId
		self.rotation = rotation
		
		self.perc = 0
		#Controls the randomness of where the card lands. This should make it seem more real...
		self.percStop = 100 + random.randint(0, percStop)
	
	#TODO: generalize: guiVar
	#guiVar.printProjectile()
	def printThrownCard(self, guiVars):
		
		#THROW_TIME=100
		#FRAME_WAIT_TIME = 40
		if self.beingThrown == 1:
			currentX = int((self.perc * (self.endX) + (100 - self.perc) * (self.startX))/100)
			currentY = int((self.perc * (self.endY) + (100 - self.perc) * (self.startY))/100)
			
			guiVars.printProjectile(currentX, currentY, self.projectileId, self.rotation)
			
			if self.perc < self.percStop:
				jump = (100*guiVars.FRAME_WAIT_TIME)/guiVars.THROW_TIME
				self.perc = self.perc + jump
				
				if self.perc > self.percStop:
					self.perc = self.percStop
	
	def endThrow(self, guiVars):
		self.beingThrown=0
		self.startX=0
		self.startY=0
		self.endX=0
		self.endY=0
		self.perc = 0
		self.projectileId = -1
		self.rotation = 0
