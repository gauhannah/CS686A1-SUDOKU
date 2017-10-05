import numpy
import BoardState
import csv

'''
	This code will solve all instances of sudoku given in the problems folder 
	in the assignment. To only solve one instance, comment at the places indicated
	in the code, and change the path to the instance that you would like to solve
'''


# Loads the instance into a BoardState Object
def load_instance(path):
	numAssigned = 0
	board = []
	file = open(path, 'r')
	for line in file:
		rawVals = line.split()
		tmp = []
		for i in rawVals:
			tmp.append(int(i))
		if len(tmp)> 0:
			board.append(tmp)
	board = numpy.matrix(board)
	return BoardState.BoardState(board)

# Determines if an assignment is valid
def isValid(board, value, i,j):
	col = i - i % 3
	row = j - j % 3
	# determines if it is in the same 3x3 square
	for k in range(col, col+3):
		for l in range(row, row+3):
			if board.item(k,l) == value:
				return False
	# determines if it is in the same column
	for k in range(0,9):
		if board.item(k,j) == value:
			return False
	# determines if it is in the same row
	for k in range(0,9):
		if board.item(i,k) == value:
			return False
	return True

# recursive function that solves the sudoku puzzle
def solveSudoku(boardState, assignments):
	# backtrack if you reach 10000 assignments
	if assignments >= 10000:
		return [False, boardState, 10000]
	coords = boardState.findUnassigned()
	# if you have no unassigned values, return that it was solved
	if coords == None: 
		return [True, boardState, assignments]
	i = coords[0]
	j = coords[1]
	# check all values in domain
	for val in range(1,10):
		if isValid(boardState.board,val, i, j):
			assignments += 1
			# make the next state in the tree
			newBoard = BoardState.BoardState(boardState.board)
			newBoard.board[i,j] = val
			solved = solveSudoku(newBoard,assignments)
			if solved[0]:
				return solved
			elif solved[2] >= 10000:
				return solved
			else: 
				boardState.board[i,j] = 0
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
		# uncomment this path, and comment the path on line 86 for 1 instance
		#path = 'problems/3/1,.sd'
		path = 'problems/' + str(i) + '/' + str(j) + '.sd'
		initialState = load_instance(path)
		solved = solveSudoku(initialState,0)
		data.append(solved[2])
	# comment this line out
	avgNumAssignments.append([i,numpy.mean(data)])

# comment this block out for single instance
# writes out all average assignments to a file
myfile = open(str(i) + 'Backtracking.csv', 'w') 
with myfile:
	writer = csv.writer(myfile)
	writer.writerows(avgNumAssignments)	

