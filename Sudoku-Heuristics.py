import numpy
import csv

'''
	This code will solve all instances of sudoku given in the problems folder 
	in the assignment. To only solve one instance, comment at the places indicated
	in the code, and change the path to the instance that you would like to solve
'''

#Utility function to print out the sudoku board
def printBoard(gameBoard):
	for i in range(0,9):
		vals = []
		for j in range(0,9):
			vals.append(gameBoard[i][j].value)
		print vals

# store the value of the square on the board and the domain
class boardSquare(object):
	def __init__(self, val):
		self.value = val
		self.domain = range(1,10)

# Determines if an assignment is valid
def isValid(board, value, i,j):
	col = i - i % 3
	row = j - j % 3
	# determines if it is in the same 3x3 square
	for k in range(col, col+3):
		for l in range(row, row+3):
			if board[k][l].value == value:
				return False
	# determines if it is in the same column
	for k in range(0,9):
		if board[k][j].value == value:
			return False
	# determines if it is in the same row
	for k in range(0,9):
		if board[i][k].value == value:
			return False
	return True

# builds the new sudoku board from its parent
def buildBoard(board):
	newBoard = []
	for i in range(0,9):
		tmp = []
		for j in range(0,9):
			tmp.append(boardSquare(board[i][j].value))
			tmp[j].domain = board[i][j].domain
		newBoard.append(tmp)
	return newBoard

# updates the domains of all of the remaining unassigned squares on the board
def updateDomains(board):
	for i in range(0,9):
		for j in range(0,9):
			board[i][j].domain = range(1,10)
			for val in range(1,10):
				if board[i][j].value == 0 and not isValid(board, val, i, j):
					board[i][j].domain.remove(val)	

# checks to ensure that all unassigned squares still have feasible values
def checkDomains(board):
	for i in range(0,9):
		for j in range(0,9):
			if len(board[i][j].domain) == 0:
				return False
	return True

# load the instance into a 2d array of board squares
def load_instance(path):
	gameBoard = []
	file = open(path, 'r')
	j = 0
	for line in file:
		rawVals = line.split()
		tmp = []
		squares = []
		for i in rawVals:
			tmp.append(int(i))
		if len(tmp)> 0:
			for i in tmp:
				sq = boardSquare(i)
				squares.append(sq)
		j += 1
		if len(squares) > 0: 
			gameBoard.append(squares)
	# Remove initial values from unassigned domains		
	for i in range(0,9):
		for j in range(0,9):
			for val in range(1,10):
				if gameBoard[i][j].value == 0 and not isValid(gameBoard, val, i, j):
					gameBoard[i][j].domain.remove(val)											

	return gameBoard

# find the next unanssigned value
def findUnassigned(boardState):
	mc = None
	for i in range(0,9):
		for j in range(0,9):
			if boardState[i][j].value == 0:
				if mc == None:
					mc = (i,j)
				# Implements Most Restricted Variable, finds the variable with the fewest remaining feasible values
 				if len(boardState[i][j].domain) < len(boardState[mc[0]][mc[1]].domain):
					mc = (i,j)
				#Breaks ties with most constraining variable
				elif len(boardState[i][j].domain) == len(boardState[mc[0]][mc[1]].domain) and findConstraints(boardState, i, j) > findConstraints(boardState, mc[0], mc[1]):
					mc = (i,j)
	return mc

# finds the most constraining variable by finding the number of unassigned squares
# that are in the same row, column, and 3x3 square of the square at i,j
def findConstraints(board, i, j):
	constraints = 0
	col = i - i % 3
	row = j - j % 3
	checked = []
	for k in range(col, col+3):
		for l in range(row, row+3):
			if board[k][l].value == 0 and k <> i and l <> j:
				constraints += 1
				checked.append(set((k,l)))
	for k in range(0,9):
		if board[k][j].value ==0 and set((k,j)) not in checked and k <> i:
			constraints += 1
			checked.append(set((i,j)))
	for k in range(0,9):
		if board[i][k].value == 0 and set((i,k)) not in checked and k <> j:
			constraints += 1
			checked.append(set((i,j)))
	return constraints

# Finds the least constraining value to assign to a variable by determining how many 
# of the conflicting squares domains have the same value in their domain. It returns whether 
# a value is in the minimum number of domains.
def isLeastConstraining(board , value, i, j):
	# maximum number of values that can be effected by a square + 1
	minDomains = 25
	minValue = 0
	for val in board[i][j].domain:
		if val >= value : 
			numDomains = 0
			col = i - i % 3
			row = j - j % 3
			checked = []
			for k in range(col, col+3):
				for l in range(row, row+3):
					if board[k][l].value == 0 and val in board[k][l].domain and k <> i and l <> j:
						numDomains += 1
						checked.append(set((k,l)))
			for k in range(0,9):
				if board[k][j].value ==0 and set((k,j)) not in checked and val in board[k][j].domain and k <> i:
					numDomains += 1
					checked.append(set((i,j)))
			for k in range(0,9):
				if board[i][k].value == 0 and set((i,k)) not in checked and val in board[i][k].domain and k <> j:
					numDomains += 1
					checked.append(set((i,j)))
			if numDomains < minDomains and val > minValue:
				minDomains = numDomains
				minValue = val
	return value == minValue


# recursive function to solve the sudoku puzzle
def solveSudoku(boardState, assignments):
	# backtrack if an unassigned square does not have any feasible values
	if not checkDomains(boardState):
		return [False, boardState, assignments]
	# backtrack if you reach 10000 assignments
	if assignments >= 10000:
		return [False, boardState, 10000]
	coords = findUnassigned(boardState)
	# if you have no unassigned values, return that it was solved
	if coords == None: 
		return [True, boardState, assignments]
	i = coords[0]
	j = coords[1]
	for val in range(1,10):
		if isValid(boardState, val, i, j):
			if isLeastConstraining(boardState, val, i, j):
				assignments += 1
				newBoard = buildBoard(boardState)
				newBoard[i][j].value = val
				# update domains of all unassigned variables to reflect new assingment
				updateDomains(newBoard)
				solved = solveSudoku(newBoard,assignments)
				if solved[0]:
					return solved
				elif solved[2] >= 10000:
					return solved
				else:
					assignments = solved[2]
	# if no value is feasible, backtrack
	return [False, boardState, assignments]
	

# START HERE

# stores the average number of assignments for each set of instances
# comment out for single instance
avgNumAssignments = []

## COMMENT OUT FOR LOOOPS TO RUN ON ONE INSTANCE
for i in range(71,0,-1):
	data = []
	for j in range(1,11):
		path = 'problems/' + str(i) + '/' + str(j) + '.sd'''
		print path
		#path = 'problems/41/1.sd'
		gameBoard =  load_instance(path)
		solved = solveSudoku(gameBoard,0)
		# comment this line
		data.append(solved[2])
	# comment this line out
	avgNumAssignments.append([i,numpy.mean(data)])

# comment this block out for single instance
# writes out all average assignments to a file
myfile = open('ForwardChecking.csv', 'w') 
with myfile:
	writer = csv.writer(myfile)
	writer.writerows(avgNumAssignments)	




