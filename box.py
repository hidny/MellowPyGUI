
class Box:
	x = 0
	y = 0
	width = 0
	heigth = 0
	
	def __init__(self, x, y, width, heigth):
		self.x = x
		self.y = y
		self.width = width
		self.heigth = heigth
	
	def getTopLeftBox(self):
		return (self.x, self.y)
	
	def getCoordBox(self):
		return (self.x, self.y, self.width, self.heigth)
	
	def isWithinBox(self, x, y):
		if x >= self.x and x<= self.x + self.width:
			if y >= self.y and y <= self.y + self.heigth:
				return 1
		
		return 0