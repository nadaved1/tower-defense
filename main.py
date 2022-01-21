from pip import main
from animation import Animation
from enemy import Enemy, EnemyWave
from tower import Tower, TowerArray, TowerColor
from extras import TowerButton
from tkinter import PhotoImage, ALL
import math

class towerDefense(Animation):
	def init(self):
		self.makeBoard()
		self.initGameConstants()
		self.initButtonLocations()
		self.towers = TowerArray()
		self.gameOver = False
		self.isEnemyWave = False
		self.towerButtonClicked = False
		self.startScreenHelpMode = False
		self.pause = False
		self.youWon = False
		self.ffdPressed = False
		self.clickedButton = None
		self.towerButtons = []
		self.slowEnemies = []
		self.loadImages()
		self.createInitTowers()
		self.createTowerButtons()
		self.setStartLocation()
		self.setStartScreen()
		
	def setStartScreen(self):
		self.startScreen = True

	def makeBoard(self):
		board = [ [0,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
					[0,1,1,1,1,1,1,1,1,1,1,0,0,1,0],
					[0,1,0,0,0,0,0,0,0,0,1,0,0,1,0],
					[0,1,0,0,0,0,0,0,0,0,1,0,0,1,0],
					[0,1,1,1,1,1,1,1,1,0,1,1,1,1,0],
					[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,1,0,1,1,1,0,0],
					[0,1,1,1,1,1,1,1,1,0,1,0,1,0,0],
					[0,1,0,0,0,0,0,0,0,0,1,0,1,0,0],
					[0,1,1,1,1,1,1,1,1,1,1,0,1,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,1,1,3]  ]
		self.rows, self.cols = len(board), len(board[0])
		self.cellDim = 40
		self.board = board

	def initGameConstants(self) -> None:
		self.numEnemies = 10
		self.counter = 1
		self.lives = 5
		self.score = 0
		self.waveNum = 0
		self.numWaves = 10
		self.money = 15
		self.enemyHealth = 5

	def initButtonLocations(self) -> None:
		self.sendWaveButton    = [self.boardDim+10,  10, self.width-10, 70]
		self.infoButton        = [self.boardDim+210, self.sendWaveButton[3]+10, self.width-10, self.sendWaveButton[3]+140]
		self.fastForwardButton = [self.boardDim+210, self.sendWaveButton[3]+460, self.width-10, self.height-10]
						
	def loadImages(self) -> None:	
		self.gameOverImage 			= PhotoImage(file="img/gameOver.gif")
		self.gameOverHelpImage  	= PhotoImage(file="img/gameOverHelp.gif")
		self.instructionsImage  	= PhotoImage(file="img/instructions.gif")
		self.startImage 			= PhotoImage(file="img/towerDefense.gif")
		self.startHelpImage 		= PhotoImage(file="img/startHelp.gif")
		self.instructionsHelpImage  = PhotoImage(file="img/instructionsHelp.gif")
		self.pauseImage 			= PhotoImage(file="img/pauseImage.gif")
		self.youWinImage 			= PhotoImage(file="img/youWin.gif")
		self.youWinHelpImage 		= PhotoImage(file="img/youWinHelp.gif")
		self.towerImage 			= PhotoImage(file="img/tower.gif")
	
	def createInitTowers(self) -> None:
		self.orangeTower = Tower(0, 0, self.board, self.cellDim, color=TowerColor.ORANGE)
		self.redTower 	 = Tower(0, 0, self.board, self.cellDim, color=TowerColor.RED)
		self.greenTower  = Tower(0, 0, self.board, self.cellDim, color=TowerColor.GREEN)
		self.purpleTower = Tower(0, 0, self.board, self.cellDim, color=TowerColor.PURPLE) 

	def createTowerButtons(self) -> None:
		orangeTowerButton = TowerButton(0, self.canvas, self.boardDim, TowerColor.ORANGE)
		redTowerButton 	  = TowerButton(1, self.canvas, self.boardDim, TowerColor.RED)
		greenTowerButton  = TowerButton(2, self.canvas, self.boardDim, TowerColor.GREEN)
		purpleTowerButton = TowerButton(3, self.canvas, self.boardDim, TowerColor.PURPLE)
		self.towerButtons.append(orangeTowerButton)
		self.towerButtons.append(redTowerButton)
		self.towerButtons.append(greenTowerButton)
		self.towerButtons.append(purpleTowerButton)

	def setStartLocation(self) -> None:
		for row in range(self.rows):
			for col in range(self.cols):
				if self.board[row][col] == 2:
					self.startLocation = (row, col)
	
	def keyPressed(self, event):
		if (self.gameOver == False and 
		self.startScreen == True and 
		self.youWon == False):
			if event.char == "r":
				self.init()
			if self.startScreenHelpMode == False:
				if event.char == "h":
					self.startScreenHelpMode = True
			elif self.startScreenHelpMode == True:
				if event.char == 'h':
					self.startScreenHelpMode = False
		elif (self.gameOver == False and 
		self.startScreen == False and 
		self.youWon == False):
			if event.char == "r":
				self.init()
			if event.char == "p":
				if self.pause == False:
					self.pause = True
				elif self.pause == True:
					self.pause = False
		elif self.youWon == True:
			if event.char == "r":
				self.init()
		else: 
			if event.char == "r":
				self.init()
	
	def mousePressed(self, event):
		if (self.gameOver == False and self.startScreen and self.startScreenHelpMode == False and self.youWon == False):
			if (event.x > 50 and event.x < self.width-50 and event.y > 50 and event.y < self.height - 50):
				self.startScreen = False
		if (self.gameOver == False and self.startScreen == False and self.youWon == False):
			if self.towerButtonClicked:
				(row, col) = self.getRowCol((event.x, event.y))
				canBuyTower = self.checkCanBuyTower(self.clickedButton.iconColor, row, col)
				if (self.legalTowerClick(row, col) and canBuyTower == True):
					self.newTower(row, col, self.clickedButton.iconColor)
					self.towerButtonClicked = False
					self.clickedButton = None
				elif (self.whichButton(event.x, event.y) == 'sendwave' and self.isEnemyWave == False):
					self.newEnemyWave()
					self.towerButtonClicked = False
				elif (self.whichButton(event.x, event.y) == 'ffd'):
					self.ffdPressed = not self.ffdPressed
					
				elif (self.whichButton(event.x, event.y) != None and self.clickedButton != True):
					self.clickedButton = self.whichButton(event.x, event.y)
					canBuyTower = self.checkCanBuyTower(self.clickedButton.iconColor)
					if canBuyTower == True:
						self.towerButtonClicked = True
					else:
						self.towerButtonClicked = False	
			else:
				self.clickedButton = self.whichButton(event.x, event.y)
				if (self.clickedButton == 'sendwave' and not self.isEnemyWave):
					self.newEnemyWave()
					self.clickedButton = None
				elif (self.clickedButton == 'ffd'):
					self.ffdPressed = not self.ffdPressed
				elif (self.clickedButton != None and not isinstance(self.clickedButton, str)):
					canBuyTower = self.checkCanBuyTower(self.clickedButton.iconColor)
					if canBuyTower == True:
						self.towerButtonClicked = True
					else:
						self.towerButtonClicked = False
		elif (self.gameOver == True and 
		self.startScreen == False and 
		self.youWon == False):
			if (event.x > 50 and event.x < self.width-50 and 
			event.y > 50 and event.y < self.height - 50):
				self.init()			
	
	def getRowCol(self, location):
		row = int(round(location[1]/self.cellDim))
		col = int(round(location[0]/self.cellDim))
		return (row, col)
	
	def checkCanBuyTower(self, towerDetails, row=0, col=0):
		canBuyTower = False
		for tower in self.towers.towerList:
			if (tower.row, tower.col) == (row, col):
				return canBuyTower
		if towerDetails   == TowerColor.ORANGE: canBuyTower = (self.money >= self.orangeTower.cost)
		elif towerDetails == TowerColor.RED:    canBuyTower = (self.money >= self.redTower.cost)
		elif towerDetails == TowerColor.GREEN:  canBuyTower = (self.money >= self.greenTower.cost)
		elif towerDetails == TowerColor.PURPLE: canBuyTower = (self.money >= self.purpleTower.cost)  
		return canBuyTower

	def legalTowerClick(self, row, col):
		if row <= self.rows-1 and row >= 0:
			if col <= self.cols-1 and col >= 0:
				if self.board[row][col] == 0:
					return True
		return False
		
	def newTower(self, row, col, towerButton):
		tower = Tower(row, col, self.board, self.cellDim, color=towerButton)
		self.money -= tower.cost
		self.towers.towerList.append(tower)

	def whichButton(self, x, y):
		for button in self.towerButtons:
			if (button.location[0] < x < button.location[2] and button.location[1] < y < button.location[3]):
				return button
		if (self.sendWaveButton[0] < x < self.sendWaveButton[2] and self.sendWaveButton[1] < y < self.sendWaveButton[3]):
			return 'sendwave'
		if (self.fastForwardButton[0] < x < self.fastForwardButton[2] and self.fastForwardButton[1] < y < self.fastForwardButton[3]):
			return 'ffd'
		return None
	
	def newEnemyWave(self):
		self.isEnemyWave = True
		self.waveNum += 1
		self.enemyHealth += 2
		self.enemyWave = EnemyWave(self.numEnemies, self.rows, self.cols, self.cellDim, self.startLocation, self.board)
		self.startWave = True
		self.numEnemiesOnBoard = 0
		
	def youWin(self):
		self.youWon = True		 
		
	def timerFired(self):
		if (self.gameOver == False and 
		self.startScreen == False and 
		self.pause == False and 
		self.youWon==False):
			self.slowEnemies = []
			self.counter += 1
			if self.isEnemyWave == True:
				if (self.counter % 20 == 0 and 
				self.numEnemiesOnBoard < self.numEnemies):
					self.addEnemyToWave()
					self.startWave = False
				for enemy in self.enemyWave.wave:
					(row, col) = self.getRowCol(enemy.location)
					if (row, col) == (self.rows-1, self.cols-1):
						self.loseLife(enemy)
					enemy.moveEnemy()
				for tower in self.towers.towerList:
					if tower.slowDown == True:
						self.doSlowDown(tower)
					else:
						enemy = self.findNearestEnemy(tower)
						if (enemy[1] < tower.radius  and 
						tower.shotOnScreen == False and 
						self.counter % 10 == 0):
							tower.fireShot(enemy[0])
						self.performShotMaint(tower, enemy[0])
				if self.startWave == False and self.enemyWaveIsEmpty():
					self.isEnemyWave = False
					self.numEnemiesOnBoard = 0
			else:
				for tower in self.towers.towerList:
					for shot in tower.shots:
						shot.moveShot()
						if shot.isOffScreen():
							tower.shots.remove(shot)
							tower.shotOnScreen = False
			self.redrawAll()

	def addEnemyToWave(self):
		self.numEnemiesOnBoard += 1
		color = "white"
		if self.waveNum > 2:
			color = "pink"
		if self.waveNum > 4:
			color = "yellow"
		if self.waveNum > 6:
			color = "cyan"
		if self.waveNum > 8:
			color = "maroon" 
		self.enemyWave.wave.append(Enemy(self.rows, self.cols, 
		self.cellDim, self.startLocation, self.board, self.enemyHealth, 
		color))
		
	def doSlowDown(self, tower):
		for enemy in self.enemyWave.wave:
			if self.findDistance(tower, enemy) < tower.radius:
				self.slowEnemies += [enemy]
		for enemy in self.slowEnemies:
			enemy.slowSpeed()
			
	def loseLife(self, enemy):
		self.lives -=1
		self.enemyWave.wave.remove(enemy)
		if self.lives == 0:
			self.makeGameOver()

	def makeGameOver(self):
		self.canvas.delete(ALL)
		self.gameOver = True
		self.redrawAll()

	def performShotMaint(self, tower, enemy):	
		for shot in tower.shots:
			shot.moveShot()
			if self.shotHitEnemy(shot, enemy):
				if tower.color.RED:
					enemy1 = self.findNearestEnemy(enemy)
					if enemy1[1] < 200:
						enemy1[0].health -= 1
						if enemy1[0].health <= 0:
							self.score += 1
							self.money += 1
							self.enemyWave.wave.remove(enemy1[0])
							if (self.waveNum == self.numWaves and 
							len(self.enemyWave.wave) == 0):
								self.youWin()
				tower.shots.remove(shot)
				tower.shotOnScreen = False
				enemy.health -= tower.shotDamage
				if enemy.health < 0:
					self.score += 1
					self.money += 1
					self.enemyWave.wave.remove(enemy)
					if (self.waveNum == self.numWaves and 
					len(self.enemyWave.wave) == 0):
						self.youWin()
			elif shot.isOffScreen():
				tower.shots.remove(shot)
				tower.shotOnScreen = False
			else:
				for enemy in self.enemyWave.wave:
					if self.shotHitEnemy(shot, enemy):
						tower.shots.remove(shot)
						tower.shotOnScreen = False
						enemy.health -= tower.shotDamage
						if enemy.health <= 0:
							self.score += 1
							self.money += 1
							self.enemyWave.wave.remove(enemy)
							if (self.waveNum == self.numWaves and 
							len(self.enemyWave.wave) == 0):
								self.youWin()

	def findNearestEnemy(self, tower):
		nearest = [800, 800]
		for enemy in self.enemyWave.wave:
			distance = self.findDistance(tower, enemy)
			if distance < nearest[1] and distance != 0:
				nearest[0] = enemy
				nearest[1] = distance
		return nearest			

	def findDistance(self, thing1, thing2):
		distanceDifferences = [thing1.center[0]-thing2.center[0], 
		thing1.center[1]-thing2.center[1]]
		distance = math.sqrt(distanceDifferences[0]**2 + 
		distanceDifferences[1]**2)
		return distance

	def shotHitEnemy(self, shot, enemy):
		if type(enemy) != Enemy:
			return False
		if self.findDistance(shot, enemy) < self.cellDim/2:	
			return True
		return False

	def enemyWaveIsEmpty(self):
		return (len(self.enemyWave.wave) == 0)
		
	def redrawAll(self):
		self.canvas.delete(ALL)
		if (self.gameOver == False and 
		self.startScreen == False and 
		self.pause == False and 
		self.youWon == False):
			self.drawGame()
			if self.isEnemyWave:
				self.drawEnemy()
			self.drawTowers()
			self.drawShots()
			self.drawStatistics()
			if self.towerButtonClicked:
				self.drawTowerDetails(self.clickedButton)
			self.drawSendWave()
			self.drawInfoBox()
		elif (self.gameOver == False and
		self.startScreen == False and 
		self.pause == True and 
		self.youWon == False):
			self.drawPauseScreen()
		elif (self.gameOver == True and self.startScreen == False and 
		self.youWon == False):
			self.drawGameOver()
		elif (self.gameOver == False and self.startScreen == True and 
		self.youWon == False):
			if self.startScreenHelpMode == False:
				self.drawStartScreen()
			else:
				self.drawInstructions()
		elif self.youWon == True:
			self.drawWin()
	
	def drawGame(self):
		self.drawBoard()

	def drawBoard(self):
		for row in range(self.rows):
			for col in range(self.cols):
				if self.board[row][col] == 0:
					color = '#A37F6F' # Regular cell
				elif self.board[row][col] == 1:
					color = "#FFDC73" # Path cell
				elif self.board[row][col] == 2:
					color = "green"
				elif self.board[row][col] == 3:
					color = "red"
				self.drawCell(row, col, color)
	
	def drawCell(self, row, col, color):
		startx, endx = col*self.cellDim, (col+1)*self.cellDim
		starty, endy = row*self.cellDim, 150+(row+1)*self.cellDim
		self.canvas.create_rectangle(startx, starty, endx, endy, fill=color)
	
	def drawEnemy(self):
		for enemy in self.enemyWave.wave:
			(startx, starty, endx, endy) = (
			enemy.location[0]+self.cellDim/4, 
			enemy.location[1]+self.cellDim/4, 
			enemy.location[2]-self.cellDim/4, 
			enemy.location[3]-self.cellDim/4)
			self.canvas.create_oval(startx, starty, endx, endy, fill = enemy.color)
			self.canvas.create_rectangle(startx, starty-self.cellDim/8, startx + (endx-startx) * enemy.health/self.enemyHealth, starty, fill="#7CFC00")

	def drawTowers(self):
		for tower in self.towers.towerList:
			startx = tower.col*self.cellDim
			starty = tower.row*self.cellDim
			endx = startx + self.cellDim
			endy = starty + self.cellDim
			self.canvas.create_oval(startx, starty,	endx, endy, fill = tower.color.get_html_color())

	def drawShots(self) -> None:
		for tower in self.towers.towerList:
			for shot in tower.shots:
				self.canvas.create_oval(shot.location[0], shot.location[1], shot.location[2], shot.location[3], fill = shot.color)		

	def drawStatistics(self) -> None:
		self.canvas.create_rectangle(self.boardDim, 0, self.width, self.height+10, fill ="#333333", outline="#333333")
		self.drawTowerButtons()
		self.drawTitle()
		self.drawFastForward()
	
	def drawTowerButtons(self) -> None:
		for button in self.towerButtons:
			if self.clickedButton == button and self.towerButtonClicked:
				pressed=True
			else:
				pressed=False
			button.drawButton(pressed)
		numTowerButtons = len(self.towerButtons)-1
		lastButton = self.towerButtons[numTowerButtons]		
		self.canvas.create_rectangle(self.boardDim+10, lastButton.location[3]+10, self.width-210, self.boardDim-10, outline="white")
			
	def drawTowerDetails(self, button) -> None:
		numTowerButtons = len(self.towerButtons)-1
		lastButton = self.towerButtons[numTowerButtons]		
		textx = (self.boardDim + self.width-200)/2
		self.canvas.create_text(textx, lastButton.location[3]+25, text=button.towerName.upper(), fill="white")	
		self.canvas.create_rectangle(self.boardDim+10, self.boardDim-80, self.width-210, self.boardDim-10, outline="white")
		self.drawTowerDesc(button)

	def drawTowerDesc(self, button):
		self.drawTowerIcon(button)
		if button.iconColor == TowerColor.ORANGE:
			tower = self.orangeTower
		elif button.iconColor == TowerColor.RED:
			tower = self.redTower
		elif button.iconColor == TowerColor.GREEN:
			tower = self.greenTower
		elif button.iconColor == TowerColor.PURPLE:
			tower = self.purpleTower
		self.drawTowerChars(tower)
		textx = (self.boardDim + self.width-200)/2
		texty = (self.height-45)
		descText = self.getText(button)
		self.canvas.create_text(textx, texty, text=descText, fill="white", justify="center")

	def drawTowerIcon(self, button):
		numTowerButtons = len(self.towerButtons)-1
		lastButton = self.towerButtons[numTowerButtons]		
		startx = ((self.boardDim + self.width-200)/2) - self.cellDim/2
		starty = lastButton.location[3]+50
		endx = startx + self.cellDim
		endy = starty + self.cellDim
		self.canvas.create_oval(startx, starty, endx, endy, fill=button.iconColor.get_html_color()) 

	def drawTowerChars(self, tower):	
		numTowerButtons = len(self.towerButtons)-1
		lastButton = self.towerButtons[numTowerButtons]		
		textx = ((self.boardDim + self.width-200)/2) - self.cellDim-15
		texty = lastButton.location[3]+110

		self.canvas.create_text(textx+10,  texty,    text=tower.effect.name, fill="white")					
		self.canvas.create_text(textx+105, texty,    text="Cost: " + str(tower.cost), fill="white")
		self.canvas.create_text(textx+10,  texty+35, text="Damage: " + str(tower.shotDamage), fill="white")
		self.canvas.create_text(textx+105, texty+35, text="Range: " + str(tower.radius), fill="white")
		
	def getText(self, button):
		if button.iconColor == TowerColor.ORANGE:
			return "The Orange Tower fires\na small shot that does\nonly minimal damage."
		elif button.iconColor == TowerColor.RED:
			return "The Red Tower fires\na small shot that\ndeals splash damage." 	
		elif button.iconColor == TowerColor.GREEN:
			return "The Green Tower fires\nfaster and damages a\nwider radius of enemies."
		elif button.iconColor == TowerColor.PURPLE:
			return "The Purple Tower slows\ndown enemies around\nit at a set interval."
		
	def drawSendWave(self):
		color = "#2C6700"
		if self.isEnemyWave:
			color = "#587058"
		self.canvas.create_rectangle(self.sendWaveButton[0], self.sendWaveButton[1], self.sendWaveButton[2], self.sendWaveButton[3], fill=color)

		textx = (self.boardDim+self.width)/2
		texty = 40
		self.canvas.create_text(textx, texty, text="SEND WAVE", fill="white")
		
	def drawInfoBox(self):
		self.drawInfoBoxOutline()
		self.drawInfoBoxTitle()
		self.drawInfoBoxText()

	def drawInfoBoxOutline(self):
		self.canvas.create_rectangle(self.infoButton[0], self.infoButton[1], self.infoButton[2], self.infoButton[3], outline="white")
		
	def drawInfoBoxTitle(self):
		pad = 15
		self.canvas.create_text((self.infoButton[0]+self.infoButton[2])/2, self.infoButton[1]+pad, text="INFORMATION BOX", fill="white")		 	
		
	def drawInfoBoxText(self):
		pad = 15
		self.canvas.create_text(self.infoButton[0]+45, self.infoButton[1]+pad+35, 
		text="Lives: " + str(self.lives), fill="white")
		self.canvas.create_text(self.infoButton[0]+45, self.infoButton[1]+pad+75,
		text="Score: " + str(self.score), fill="white")
		self.canvas.create_text(self.infoButton[2]-55, self.infoButton[1]+pad+35,
		text="Wave: " + str(self.waveNum) + "/" + str(self.numWaves), fill="white")
		self.canvas.create_text(self.infoButton[2]-55, self.infoButton[1]+pad+75,
		text="Coins: " + str(self.money), fill="white")
	
	def drawTitle(self) -> None:
		self.canvas.create_image(self.infoButton[0]+85, self.height-235, image=self.towerImage)	

	def drawFastForward(self) -> None:
		self.canvas.create_rectangle(self.fastForwardButton[0], self.fastForwardButton[1], self.fastForwardButton[2], self.fastForwardButton[3], outline="white")
		pad = 30
		fill = 'red' if self.ffdPressed else 'black'
		self.delay = 10 if self.ffdPressed else 50
		self.canvas.create_text(self.fastForwardButton[0]+87, self.fastForwardButton[1]+pad, text="FFD", fill=fill, font=("Helvetica", 24))

	def drawPauseScreen(self):
		self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#003366")
		self.canvas.create_image(self.width/2, 60, image=self.instructionsImage)
		self.canvas.create_text(15, 100, text="1. The goal of tower defense is placing towers on the screen to defeat waves\n    of enemies.\n\n2. Towers have differing characteristics which can be viewed by clicking on\n    their respective buttons.\n\n3. Buy towers with money and place the towers in strategic locations on the\n    map to fire at enemies, stopping them from getting to the end of the path.\n\n4. Send for new enemy waves after defeating enemies in the current wave.\n\n5. Look at the Information Box to track your progress in the game.\n\n6. Pause in game by pressing \'P\' and restart at any time by pressing \'R\'.", font = "Verdana 25", fill="white", anchor="nw")
		self.canvas.create_image(self.width/2, self.height-30, image=self.pauseImage)	

	def drawGameOver(self):
		self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#003366")
		self.canvas.create_image(self.width/2, self.height/2-100, image=self.gameOverImage)
		self.canvas.create_text(self.width/2, self.height/2+10, text="YOUR SCORE IS: "+str(self.score), font="Verdana 50", fill="white")
		self.canvas.create_image(self.width/2, self.height-100, image=self.gameOverHelpImage)
		
	def drawStartScreen(self):
		self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#003366")
		self.canvas.create_image(self.width/2, self.height/2-100, image=self.startImage) 
		self.canvas.create_image(self.width/2, self.height/2+200, image=self.startHelpImage)

	def drawInstructions(self):
		self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#003366")
		self.canvas.create_image(self.width/2, 60, image=self.instructionsImage)
		self.canvas.create_text(15, 100, text="1. The goal of tower defense is placing towers on the screen to defeat waves\n    of enemies.\n\n2. Towers have differing characteristics which can be viewed by clicking on\n    their respective buttons.\n\n3. Buy towers with money and place the towers in strategic locations on the\n    map to fire at enemies, stopping them from getting to the end of the path.\n\n4. Send for new enemy waves after defeating enemies in the current wave.\n\n5. Look at the Information Box to track your progress in the game.\n\n6. Pause in game by pressing \'P\' and restart at any time by pressing \'R\'.", font = "Verdana 25", fill="white", anchor="nw")
		self.canvas.create_image(self.width/2, self.height-40, image=self.instructionsHelpImage)

	def drawWin(self):
		self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#003366")
		self.canvas.create_image(self.width/2, self.height/2-100, image=self.youWinImage)
		self.canvas.create_text(self.width/2, self.height/2+10, text="YOUR SCORE IS: "+str(self.score), font="Verdana 50", fill="white")
		self.canvas.create_image(self.width/2, self.height-100, image=self.youWinHelpImage)

def main():
	app = towerDefense(title='Tower Defence')
	app.run()

if __name__ == "__main__":
	main()