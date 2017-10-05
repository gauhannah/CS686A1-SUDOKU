import numpy

# CLass that contains the state of the board for the backtracking solution

class BoardState(object):

	def __init__(self, board):
		self.board = board

	def findUnassigned(self):
		for i in range(0,9):
			for j in range(0,9):
				if self.board[i,j] == 0:
					return (i,j)
		return None


