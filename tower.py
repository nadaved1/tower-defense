from enum import Enum
import math

class TowerColor(Enum):
	BLACK = 0
	RED = 1
	GREEN = 2
	ORANGE = 3
	PURPLE = 4

	def get_html_color(self) -> str:
		if self.name == "RED":    return "#C70039"
		if self.name == "GREEN":  return "#00A86B"
		if self.name == "ORANGE": return "#FF5733"
		if self.name == "PURPLE": return "#173F5F"
		return "#000000"
		
class Effect(Enum):
	NORMAL = 0
	SPLASH = 1
	SPEED  = 2 
	SLOW   = 3

class TowerArray():
	def __init__(self):
		self.towerList = []

class Shot():
	def __init__(self, tower, enemy, board, cellDim):
		self.targetEnemy = enemy
		self.originTower = tower
		self.rows = len(board)
		self.cols = len(board[0])
		self.cellDim = cellDim
		self.speed = 15
		self.color = self.originTower.color.get_html_color()
		self.location = self.calculateLocation(self.originTower)
		self.angle = self.calculateAngle(self.originTower, self.targetEnemy)
		self.dx = -1*math.cos(self.angle)*self.speed
		self.dy = -1*math.sin(self.angle)*self.speed
		self.center = self.calculateCenter(self.location)

	def __repr__(self):
		return "Shot(%r, %r, %r)" % (self.location, self.dx, self.dy)
		

	def calculateLocation(self, tower) -> list:
		startx = tower.center[0]-5
		starty = tower.center[1]-5
		endx = startx+10
		endy = starty+10
		return [startx, starty, endx, endy]
		

	def calculateAngle(self, tower, enemy) -> float:
		xDistance = tower.center[0] - enemy.center[0]
		yDistance = tower.center[1] - enemy.center[1]
		angle = math.atan2(yDistance, xDistance)
		return angle

	def calculateCenter(self, location) -> tuple:
		centerX = (location[2] - location[0])/2.0 + location[0]	
		centerY = (location[3] - location[1])/2.0 + location[1]
		return (centerX, centerY)

	def moveShot(self) -> None:
		self.location[0] += self.dx * self.originTower.shotSpeed
		self.location[1] += self.dy * self.originTower.shotSpeed
		self.location[2] += self.dx * self.originTower.shotSpeed
		self.location[3] += self.dy * self.originTower.shotSpeed
		self.center = self.calculateCenter(self.location)

	def isOffScreen(self):
		if (self.location[0] < 0 or 
		self.location[1] < 0 or 
		self.location[2] > (self.cols+1)*self.cellDim or 
		self.location[3] > (self.rows+1)*self.cellDim):
			return True
		return False

class Tower():
	def __init__(self, row : int, col : int, board, cellDim, color=TowerColor.BLACK):
		self.row = row
		self.col = col
		self.board = board
		self.cellDim = cellDim
		self.location = self.calculateLocation(self.row, self.col, cellDim)
		self.shotOnScreen = False
		self.radius = 70
		self.center = self.calculateCenter(self.location) 
		self.shots = []
		self.color = color
		self.cost = 1
		self.shotDamage = 0
		self.shotSpeed = 1.4
		self.effect = Effect.NORMAL
		self.slowDown = False
		if color == TowerColor.ORANGE:
			self.shotDamage = 1
			self.cost = 3
		elif color == TowerColor.RED:
			self.shotDamage = 2
			self.cost = 10
			self.effect = Effect.SPLASH
		elif color == TowerColor.GREEN:
			self.shotSpeed = 1.6
			self.shotDamage = 15
			self.radius = 90
			self.cost = 15
			self.effect = Effect.SPEED
		elif color == TowerColor.PURPLE:
			self.radius = 65 
			self.slowDown = True
			self.cost = 20
			self.effect = Effect.SLOW

	def __repr__(self):
		return "Tower(%r, %r, %r)" % (self.row, self.col, self.color)

	def calculateLocation(self, row, col, cellDim):	
		startx = col*cellDim
		starty = row*cellDim
		endx = startx + cellDim
		endy = starty + cellDim
		return [startx, starty, endx, endy]

	def calculateCenter(self, location): 
		centerX = (location[2] - location[0])/2.0 + location[0] 
		centerY = (location[3] - location[1])/2.0 + location[1]
		return [centerX, centerY]

	def fireShot(self, enemy):
		self.shotOnScreen = True
		shot = Shot(self, enemy, self.board, self.cellDim)
		self.shots.append(shot)   
