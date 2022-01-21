from abc import ABC
from tkinter import Tk, Canvas, ALL

###########################################
# Animation class
###########################################

class Animation(ABC):
    # Override these methods when creating an animation
	def mousePressed(self, event): pass
	def keyPressed(self, event): pass
	def timerFired(self): pass
	def init(self): pass
	def redrawAll(self): pass
    
	def __init__(self, delay=50, width=1000, height=600, title='') -> None:
		self.title = title
		self.width = width
		self.height = height
		self.delay = delay

	def run(self) -> None:
		root = Tk()
		self.boardDim = self.width-400
		self.canvas = Canvas(root, width=self.width, height=self.height)
		self.canvas.pack()	
		# set up events
		def redrawAllWrapper():
			self.canvas.delete(ALL)
			self.redrawAll()
		def mousePressedWrapper(event):
			self.mousePressed(event)
			redrawAllWrapper()
		def keyPressedWrapper(event):
			self.keyPressed(event)
			redrawAllWrapper()
		root.title(self.title)
		root.bind("<Button-1>", mousePressedWrapper)
		root.bind("<Key>", keyPressedWrapper)
		# set up timerFired events
		def timerFiredWrapper():
			self.timerFired()
			redrawAllWrapper()
			# pause, then call timerFired again
			self.canvas.after(self.delay, timerFiredWrapper)
		# init and get timerFired running
		self.init()
		timerFiredWrapper()
		# launch the app
		root.mainloop() 
