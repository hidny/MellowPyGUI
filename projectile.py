import random
import mellowGUI

#This class deals with the animation of cards being thrown into the middle of the table.

class Projectile:
	beingThrown=0
	startX=0
	startY=0
	endX=0
	endY=0
	perc = 0
	throwCardNum = -1
	rotation = 0

	def __init__(self, beingThrown, startX, startY, endX, endY, throwCardNum, rotation):
		self.beingThrown=beingThrown
		self.startX = startX
		self.startY = startY
		self.endX   = endX
		self.endY   = endY
		self.throwCardNum = throwCardNum
		self.rotation = rotation
		
		self.percStop = 100 + random.randint(0, 20)
		
	def printThrownCard(self, mellowVars):
		
		#THROW_TIME=100
		#FRAME_WAIT_TIME = 40
		if self.beingThrown == 1:
			currentX = (self.perc * (self.endX) + (100 - self.perc) * (self.startX))/100
			currentY = (self.perc * (self.endY) + (100 - self.perc) * (self.startY))/100
			mellowVars.printcardFromCenter(currentX, currentY, self.throwCardNum, self.rotation)
			if self.perc < self.percStop:
				jump = (100*mellowVars.FRAME_WAIT_TIME)/mellowVars.THROW_TIME
				self.perc = self.perc + jump
				#make it boring:
				#TODO: take this line away to get cooler projectiles.
				if self.perc > self.percStop:
					self.perc = self.percStop
	
	def endThrow(self, mellowVars):
		self.beingThrown=0
		self.startX=0
		self.startY=0
		self.endX=mellowVars.screen_width/2
		self.endY=mellowVars.screen_height/2 + mellowVars.card_width + mellowVars.card_height/2
		self.perc = 0
		self.throwCardNum = -1
		self.rotation = 0

def throwSouthCard(mellowVars, southCards, cardHeldIndex):
	if len(southCards) > 0:
		southStartX = mellowVars.getCardLocation(cardHeldIndex)
		southStartY = mellowVars.screen_height - mellowVars.off_the_edgeY - mellowVars.card_height/4
		southEndX   = mellowVars.screen_width/2
		southEndY   = mellowVars.screen_height/2 + mellowVars.card_width + mellowVars.card_height/4
		
		southThrowCardNum = southCards[cardHeldIndex]
		
		southCards.pop(cardHeldIndex)
		
		#beingThrown, startX, startY, endX, endY, throwCardNum)
		return Projectile(1, southStartX, southStartY, southEndX, southEndY, southThrowCardNum, 0)
	else:
		return Projectile(0, 0, 0, 0, 0, 0, 0)

def getCardYLocation(mellowVars, eastWestcards, indexCard):
	firstY = mellowVars.screen_height/2
	if len(eastWestcards) % 2 == 0:
		firstY = firstY + mellowVars.card_width/4
		
	firstY = firstY - int(len(eastWestcards)/2)*(mellowVars.card_width/2)
	
	ret = firstY + indexCard * (mellowVars.card_width/2)
	return ret

def throwWestCard(mellowVars, westCards, cardNum):
	if len(westCards) > 0:
		indexThrow = random.randint(0,len(westCards) - 1)
		
		westStartX = mellowVars.off_the_edgeX
		westStartY = getCardYLocation(mellowVars, westCards,indexThrow)
		
		westEndX= mellowVars.screen_width/2 - mellowVars.card_width - mellowVars.card_height/4
		westEndY= mellowVars.screen_height/2
		
		westCards.pop(indexThrow)
		
		return Projectile(1, westStartX, westStartY, westEndX, westEndY, cardNum, 1)
	else:
		return Projectile(0, 0, 0, 0, 0, 0, 0)
	
def throwEastCard(mellowVars, eastCards, cardNum):
	if len(eastCards) > 0:
		indexThrow = random.randint(0,len(eastCards) - 1)
		
		eastStartX = mellowVars.screen_width -  mellowVars.off_the_edgeX
		eastStartY = getCardYLocation(mellowVars, eastCards, indexThrow)
		
		eastEndX= mellowVars.screen_width/2 + mellowVars.card_width + mellowVars.card_height/4
		eastEndY= mellowVars.screen_height/2
		
		eastCards.pop(indexThrow)
		
		return Projectile(1, eastStartX, eastStartY, eastEndX, eastEndY, cardNum, 1)
	else:
		return Projectile(0, 0, 0, 0, 0, 0, 0)
		
	
def throwNorthCard(mellowVars, northCards, cardNum):
	if len(northCards) > 0:
		indexThrow = random.randint(0,len(northCards) - 1)
		
		northStartX = mellowVars.getCardLocation(indexThrow)
		northStartY = mellowVars.off_the_edgeY + mellowVars.card_height/2
		northEndX   = mellowVars.screen_width/2
		northEndY   = mellowVars.screen_height/2 - mellowVars.card_width - mellowVars.card_height/4
		
		northCards.pop(indexThrow)
		
		return Projectile(1, northStartX, northStartY, northEndX, northEndY, cardNum, 0)
	else:
		return Projectile(0, 0, 0, 0, 0, 0, 0)

	
def main():
	print 'what is up?'
	x = Projectile(0, 0, 0, 0, 0, 0,0)
	print 'nothing bad happened yet.'
	throwSouthCard([0,0,0,0], 3)
	print 'Still nothing bad.'
	y = []
	y.append(x)
	y.append(30)
	print y[1]
	
				
if __name__ == "__main__":
    main()