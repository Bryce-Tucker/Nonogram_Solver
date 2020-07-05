import numpy as np

def createBoard(size):
    return(np.full([size[1], size[0], 1], 255, dtype=np.uint8))

def printBoard(board):
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if (board[i][j] == 255):
                print (u"\u2327", end = "")
            elif (board[i][j] == 0):
                print (u"\u25A1", end = "")
            else:
                print (u"\u25A0", end = "")
        print()

def fillRow(board, rowIndex, fillInsructions):
    for c in range(board.shape[1]):
        if (fillInsructions[c] != 255):
            board[rowIndex][c] = fillInsructions[c]

def fillCol(board, colIndex, fillInsructions):
    for r in range(board.shape[0]):
        if (fillInsructions[r] != 255):
            board[r][colIndex] = fillInsructions[r]

def addInstructions(instructions):
    sum = 0
    for instruction in instructions:
        sum += instruction
    sum += len(instructions) - 1
    return (sum)

def listTotal(list):
    sum = 0
    for i in list:
        for j in i:
            sum += j
    return(sum)

def _parseInstructions(size, instructions):
    parsed = [[0]]
    spaceBlocks = [0]
    for i in range(len(instructions)):
        parsed.append([instructions[i]])
        parsed.append([1])
        spaceBlocks.append(len(parsed) - 1)

    instructionSize = addInstructions(instructions)
    parsed[-1][0] = size - instructionSize
    return(parsed, spaceBlocks)

def _translateParsedInstruction(parsed, spaces, trueZero = False):
    translation = []
    for i in range(len(parsed)):
        for j in range(parsed[i][0]):
            if (i in spaces):
                if (trueZero):
                    translation.append(0)
                else:
                    translation.append(255)
            else:
                translation.append(1)
    return (translation)

def getPermutations(size, instructions):
    instructionSum = addInstructions(instructions)
    initialState, spaces = _parseInstructions(size, instructions)


    if (instructions == size):
        return(_translateParsedInstruction(initialState, spaces, True))

    permutations = []
    permutations.append(_translateParsedInstruction(initialState, spaces))

    state = initialState.copy()
    index = 1
    while (index >= 0):
        index = len(spaces) - 1
        state[spaces[index]][0] += 1
        while (listTotal(state) > size):
            if (index == 0):
                index -= 1
                break
            if (index == len(spaces) - 1):
                state[spaces[index]][0] = 0
            else:
                state[spaces[index]][0] = 1
            index -= 1
            state[spaces[index]][0] += 1
        if (index >= 0):
            while (listTotal(state) < size):
                state[-1][0] += 1
            permutations.append(_translateParsedInstruction(state, spaces))

    return(permutations)

def removeInvalidPermutations(line, permutations):
    for i in range(len(line)):
        lenPermutations = len(permutations)
        permutationsIndex = 0
        while (permutationsIndex < lenPermutations):
            if (line[i] == 1 and permutations[permutationsIndex][i] != 1):
                permutations.pop(permutationsIndex)
                lenPermutations -= 1
            elif (line[i] == 0 and permutations[permutationsIndex][i] == 1):
                permutations.pop(permutationsIndex)
                lenPermutations -= 1
            else:
                permutationsIndex += 1

def checkForOverlap(size, instruction, board = [], col = -1, row = -1):
    filled = []

    permutations = getPermutations(size, instruction)

    if (len(board) > 0):
        if (col != -1):
            line = board[:,col]
        else:
            line = board[row, :]
        removeInvalidPermutations(line, permutations)

    if (len(permutations) == 1):
        return(permutations[0])

    overlap = []
    for i in range(size):
        overlappingFilled = True
        overlappingUnfilled = True
        trueZero = False
        for permutation in permutations:
            if (permutation[i] != 1):
                overlappingFilled = False
            if (permutation[i] == 1):
                overlappingUnfilled = False
            if (permutation[i] == 0):
                trueZero = True
        if (overlappingFilled):
            overlap.append(1)
        elif(trueZero or overlappingUnfilled):
            overlap.append(0)
        else:
            overlap.append(255)
    return(overlap)

def checkLine(line, instructions):
    filled = []

    for i in range(len(line)):
        if (line[i] == 1):
            if (len(filled) == 0 or line[i - 1] != 1):
                filled.append(1)
            else:
                filled[-1] += 1
    if (len(filled) == 0):
        if (instructions[0] == 0):
            return(True)
        else:
            return(False)

    if (len(filled) != len(instructions)):
        return(False)

    for i in range(len(instructions)):
        if (filled[i] != instructions[i]):
            return(False)
    return(True)

def checkIfSolved(board, colInstructions, rowInstructions):
    for i in range(board.shape[0]):
        solved = checkLine(board[i,:], rowInstructions[i])
        if (solved == False):
            return(False)

    for i in range(board.shape[1]):
        if (not checkLine(board[:,i], colInstructions[i])):
            return(False)
    return(True)

def markZeros(board, colInstructions, rowInstructions):
    for i in range(board.shape[0]):
        solved = checkLine(board[i,:], rowInstructions[i])
        if (solved):
            for j in range(board.shape[1]):
                if (board[i][j] != 1):
                    board[i][j] = 0
    for i in range(board.shape[1]):
        solved = checkLine(board[:,i], colInstructions[i])
        if (solved):
            for j in range(board.shape[0]):
                if (board[j][i] != 1):
                    board[j][i] = 0

def solvePuzzle(colInstructions, rowInstructions):
    solved = False
    board = createBoard((len(rowInstructions), len(colInstructions)))
    while (not solved):
        for i in range(board.shape[0]):
            row = checkForOverlap(board.shape[0], rowInstructions[i], board, row = i)
            fillRow(board, i, row)
        for i in range(board.shape[1]):
            col = checkForOverlap(board.shape[1], colInstructions[i], board, col = i)
            fillCol(board, i, col)
        solved = checkIfSolved(board, colInstructions, rowInstructions)
        if (not solved):
            markZeros(board, colInstructions, rowInstructions)
    return(board)

def main():
    # Left to Right
    instructionsCol = ([3, 1, 4], [3, 1, 1], [3, 3, 2, 4, 6], [4, 3, 2, 7], [9, 4, 7],
                        [3, 1, 2, 6], [3, 6], [1, 1, 7], [1, 1, 1, 9], [1, 3, 4, 5],
                        [2, 1, 1, 1, 4, 1, 1], [2, 3, 1, 5, 1], [5, 3, 6, 2], [8, 1, 4], [8, 2, 7],
                        [5, 6], [5, 6], [6, 8], [11, 4, 2], [11, 2, 3],
                        [6, 4, 1, 2], [1, 6, 2, 4], [7, 1, 2], [2, 4, 3], [2, 4, 2])
    # Top to Bottom
    instructionsRow = ([3, 2, 3, 1], [3, 3], [3, 1, 3], [4, 5, 2, 3], [5, 15],
                        [5, 3, 10], [5, 12], [2, 15], [1, 2, 9], [2, 4, 7],
                        [3, 2, 2], [2, 3, 3, 1], [4], [4, 2, 4], [1, 4, 2, 1, 2],
                        [3, 1, 4, 3], [1, 1, 1, 5, 1], [1, 1, 9], [2, 3, 10], [7, 8, 1],
                        [17, 1], [8, 4, 1], [9, 6, 1, 1], [8, 1, 1, 7], [4, 1, 1, 2, 5])

    import time
    time1 = time.time()
    board = solvePuzzle(instructionsCol, instructionsRow)
    print("Solved Board")
    printBoard(board)
    time2 = time.time()
    print(time2 - time1)

if __name__ == '__main__':
    main()
