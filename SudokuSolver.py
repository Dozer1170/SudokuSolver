import sys
import re
import copy
import collections
import time
class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

Point = collections.namedtuple('Point', ['x', 'y'])

w, h = 9, 9;
inputBoard = [[0 for x in range(w)] for y in range(h)]

def printboard(board, spotOfInterest = Point(-1,-1)):
    for i in range(0,9):
        print
        if(i % 3 == 0):
            print "-------------------------"
        for j in range(0,9):
            if(j % 3 == 0):
                print "|",
            if(spotOfInterest.x == i and spotOfInterest.y == j):
                sys.stdout.write(bcolors.OKGREEN + " ")
                sys.stdout.write(str(board[i][j]))
                sys.stdout.write(" " + bcolors.ENDC)
                sys.stdout.flush()
            else:
                print board[i][j],
        print "|",
    print
    print "-------------------------"

def sectioncontainsnumber(board, currentRow, currentColumn, number):
    sectionRow = currentRow / 3
    sectionColumn = currentColumn / 3
    for i in range(0,3):
        for j in range(0,3):
            x = sectionRow * 3 + i
            y = sectionColumn * 3 + j
            if(board[x][y] == number):
                return True
    return False

def rowcolumnorsectioncontainsnumber(board, currentRow, currentColumn, number):
    for i in range (0,9):
        if(board[currentRow][i] == number or board[i][currentColumn] == number or sectioncontainsnumber(board, currentRow, currentColumn, number)):
            return True
    return False

def parseline(currentRow, line):
    for i in range(0,9):
        character = line[i]
        if(re.match('[Xx]', character)):
            inputBoard[currentRow][i] = 0;
        else:
            number = int(character)
            if(rowcolumnorsectioncontainsnumber(inputBoard, currentRow, i, number)):
                return False
            inputBoard[currentRow][i] = number
    return True

def parselinesfromstdin():
    row = 0
    while row < 9:
        print "Please enter row", row + 1
        line = sys.stdin.readline()
        if(re.match('^([\d]|[Xx]){9}$', line) and parseline(row, line)):
            row += 1
        else:
            print "Invalid line, please enter a line with only digits and Xs, that is 9 characters, and does not repeat numbers in rows, columns, or sections"

    print "Board:"
    printboard(inputBoard)

def findnextemptyspot(board):
    for i in range(0,9):
        for j in range(0,9):
            if(board[i][j] == 0):
                return Point(i,j)
    return Point(-1,-1)

def solvepuzzle(board, depth):
    testBoard = copy.deepcopy(board)
    nextBlankPoint = findnextemptyspot(testBoard)
    if(nextBlankPoint.x == -1 and nextBlankPoint.y == -1):
        return testBoard
    for k in range(1,10):
        print "Depth Level:", depth, "trying number", k
        testBoard[nextBlankPoint.x][nextBlankPoint.y] = k #For print statement niceness only
        printboard(testBoard, nextBlankPoint)
        testBoard[nextBlankPoint.x][nextBlankPoint.y] = 0 #For print statement niceness only
        if(not rowcolumnorsectioncontainsnumber(testBoard, nextBlankPoint.x, nextBlankPoint.y, k)):
            testBoard[nextBlankPoint.x][nextBlankPoint.y] = k
            potentialSolvedBoard = solvepuzzle(testBoard, depth + 1)
            if(potentialSolvedBoard):
                blankPoint = findnextemptyspot(potentialSolvedBoard)
                if(blankPoint.x == -1 and blankPoint.y == -1):
                    return potentialSolvedBoard;
    #print "Abandoning branch because no number found that satisfies board at", nextBlankPoint.x, nextBlankPoint.y
    #printboard(board)
    #time.sleep(5)
    return False


parselinesfromstdin()

result = solvepuzzle(inputBoard, 0)

if(not result):
    print "Failed to Solve"
else:
    print "Final Result:"
    printboard(result)
