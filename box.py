
class Box:
	x = 0
	y = 0
	width = 0
	height = 0
	
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	
	def getTopLeftBox(self):
		return (self.x, self.y)
	
	def getCoordBox(self):
		return (self.x, self.y, self.width, self.height)
	
	def getCoordBoxOffset(self, outset):
		return (self.x - outset, self.y - outset, self.width + 2 * outset, self.height + 2 * outset)
	
	def getX(self):
		return self.x
	
	def getY(self):
		return self.y
	
	def getHeight(self):
		return self.height
	
	def getWidth(self):
		return self.width
	
	def isWithinBox(self, x, y):
		if x >= self.x and x<= self.x + self.width:
			if y >= self.y and y <= self.y + self.height:
				return 1
		
		return 0
		