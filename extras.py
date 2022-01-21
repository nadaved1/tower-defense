
from tower import TowerColor

class TowerButton():
	def __init__(self, buttonNum : int, canvas, boardDim, color : TowerColor):
		self.buttonNum = buttonNum
		self.canvas = canvas
		self.towerName = color.name + ' Tower'
		self.statsBarWidth = 200
		self.towerBarTopPad = 60
		self.iconColor = color
		startx, endx = boardDim+10, (boardDim+
		self.statsBarWidth-10)
		starty = (self.towerBarTopPad+10+
		(buttonNum*60+10)+self.buttonNum*10) 
		endy = starty + 60
		self.location = [startx, starty, endx, endy]

	def __repr__(self):
		return "Button(%r, %r)" % (self.location, self.iconColor)

	def drawButton(self, pressed):
		if pressed == False:
			self.canvas.create_rectangle(self.location[0],
			self.location[1], self.location[2], self.location[3],
			fill="#333333", outline="white")
		elif pressed == True:
			self.canvas.create_rectangle(self.location[0],
			self.location[1], self.location[2], self.location[3],
			fill="#333333", outline=self.iconColor.get_html_color())	
		self.canvas.create_text(self.location[0] + 120, 
		self.location[1]+(self.location[3]-self.location[1])/2, 
		text=self.towerName, fill="white")
		self.drawTowerIcon()
		
	def drawTowerIcon(self):
		startx = self.location[0] + 20
		starty = self.location[1] + ((self.location[3]-
		self.location[1])-40)/2
		endx = startx + 40
		endy = starty + 40
		self.iconLocation = [startx, starty, endx, endy]
		self.canvas.create_oval(startx, starty, endx, endy, fill=self.iconColor.get_html_color())	
