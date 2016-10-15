class Player:

	#Constructor
	def __init__(self, board):
		self.board = board
		self.deselect()
		self.clicked = None

	#Deselect the piece
	def deselect(self):
		self.selected = None
		self.movesOfSelectedToKill = []
		self.movesOfSelectedToWalk = []

	#Set the last clicked position
	def setClicked(self, line, collum):
		self.clicked = self.board[line][collum]

	#Set the selected positon on the board. Assume that is a red piece
	def setSelected(self, line, collum):
		killers = self.searchKillers()
		#See if there are killers to select
		if len(killers) > 0:
			if not (line, collum) in killers:
				return False
		
		#get all possible spaces where the piece can walk to		
		self.selected = self.board[line][collum]
		self.movesOfSelectedToKill = self.selected.canKill(self.board)
		self.movesOfSelectedToWalk = []
		if len(self.movesOfSelectedToKill) == 0:
			self.movesOfSelectedToWalk = self.selected.canMove(self.board)
		return True	

	#Return a list of every piece that can eat any enemy's piece
	def searchKillers(self):
		listKillers = []
		for i in range(0, 8):
			for j in range(0, 8):
				if self.board[i][j] != 0 and self.board[i][j].team == "red":
					targets = self.board[i][j].canKill(self.board)
					if len(targets) != 0:
						listKillers.append((i, j))
		return listKillers

	#Return every piece of that team on the board
	def findAllMyPieces(self, team):
		myPiecesPositions = []
		for i in range(0, 8):
			for j in range(0, 8):
				if self.board[i][j] != 0 and self.board[i][j].team == team:
					myPiecesPositions.append((i, j))
		return myPiecesPositions

	#Return if the choosen destiny is valid, so if it's true, then make the move
	def tryPlay(self, line, collum):
		if self.selected == None:
			return False
		#See if the destiny is reached by killing
		if (line, collum) in self.movesOfSelectedToKill:
			self.selected.makeKill((line,collum), self.board)

			#Seeing if the piece can kill another one
			self.movesOfSelectedToKill = self.selected.canKill( self.board )
			if len(self.movesOfSelectedToKill) != 0:
				self.selected.line = line
				self.selected.collum = collum
				return False
			else:
				return True
		#See if the destiny is reached by moving 
		elif (line, collum) in self.movesOfSelectedToWalk:
			self.selected.makeMove((line, collum), self.board)
			return True
		