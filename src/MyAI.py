# ==============================CS-199==================================
# FILE:         MyAI.py
#
# AUTHOR:       Justin Chung
#
# DESCRIPTION:  This file contains the MyAI class. You will implement your
#               agent in this file. You will write the 'getAction' function,
#               the constructor, and any additional helper functions.
#
# NOTES:        - MyAI inherits from the abstract AI class in AI.py.
#
#               - DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
from collections import deque
import math, random
from time import time

class MyAI( AI ):
    
    board = []
    cov = []
    q =  deque()
    flag = set()        # flag = set of all tiles that are flagged
    flagged = deque()   # flagged = queue of tiles that we pop and call Action.FLAG from
    visited = set()
    onTheQ = set()
    orderedCoords = []
    xVal = 0
    yVal = 0

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        ########################################################################
        #                           YOUR CODE BEGINS                           #
        ########################################################################
        self.r = rowDimension
        self.c = colDimension
        self.t = totalMines
        self.x = startX
        self.y = startY
        self.uncovered = 0
        self.timeElapsed = 0
        self.initialTime = time()

        global board, q, visited, xVal, yVal, cov, onTheQ, flagged, orderedCoords, flag
        board = []
        cov = []
        q = deque()
        flag = set()
        flagged = deque()
        visited = set()
        onTheQ = set()
        orderedCoords = []

        for m in range(self.getC()):
            inner = []
            for n in range(self.getR()):
                inner.append(-1)
                cov.append((m,n))
            board.append(inner)

        xVal = self.getX()
        yVal = self.getY()

        ########################################################################
        #                           YOUR CODE ENDS                             #
        ########################################################################
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getT(self):
        return self.t

    def getC(self):
        return self.c

    def getU(self):
        return self.uncovered

    def getR(self):
        return self.r

    def getValidNeighbors(self, x, y):
        ''' returns list of all neighbors of (x,y)  '''
        validN = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (i < 0 or i >= self.c or j < 0 or j >= self.r or (i == x and j == y)):
                    continue
                else:
                    validN.append((i,j))
        return validN
        
    def numUnmarkedNeighbors(self, x, y):
        num = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (i < 0 or i >= self.c or j < 0 or j >= self.r or (i == x and j == y)):
                    continue
                else:
                    if board[i][j] == -1:
                        num += 1
        return num

    def numMarkedNeighbors(self, x, y):
        num = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (i < 0 or i >= self.c or j < 0 or j >= self.r or (i == x and j == y)):
                    continue
                else:
                    if board[i][j] == -2:
                        num += 1
        return num

    def effectiveLabel(self, number, x, y):
        return number - self.numMarkedNeighbors(x,y)

    def removeElement(self, x, y):
        global q
        tempQ = deque()
        while not (not q):
            if q.pop() != (x,y):
                tempQ.append((x,y))
        q = tempQ

    def printBoard(self):
        counter = 0
        for r in range(self.c):
            print(counter, end=" |")
            for c in range(self.r):
                txt = str(board[r][c]).rjust(5)
                print(txt, end=" ")
            print("\n")
            counter += 1
        print("\n")

    def calcAvgProb(self, x, y):
        
        currentNeighbors = self.getValidNeighbors(x,y)
        numValidNeighbors = 0
        total = 0
        
        for cX, cY in currentNeighbors:
            if (cX, cY) not in cov and board[cX][cY] != -2:
                if self.numUnmarkedNeighbors(cX, cY) <= 0:
                    continue        # dont count it if all neighbors are marked already
                else:
                    numValidNeighbors += 1
                    total += (self.effectiveLabel(board[cX][cY], cX, cY) / self.numUnmarkedNeighbors(cX,cY))
        if numValidNeighbors == 0:
            return -1
        return total / numValidNeighbors
    
    def neighborInCov(self, x, y):
        currentNeighbors = self.getValidNeighbors(x,y)
        covNeighbors = []
        for cX,cY in currentNeighbors:
            if (cX, cY) in cov:
                covNeighbors.append((cX, cY))
        return covNeighbors

    def getAction(self, number: int) -> "Action Object":

        ########################################################################
        #                           YOUR CODE BEGINS                           #
        ########################################################################
    
        time_remaining = 300 - self.timeElapsed    
        if (((self.r * self.c) - self.t) == self.uncovered):
            return Action(AI.Action.LEAVE)
        elif time_remaining >= 5:
            startTime = time()
            global xVal, yVal
    
            if number != -1:
                board[xVal][yVal] = number
                visited.add((xVal, yVal))
                onTheQ.add((xVal, yVal))

                self.uncovered += 1
                cov.remove((xVal, yVal))
            
                currentNeighbors = self.getValidNeighbors(xVal, yVal)

                mine = (self.effectiveLabel(number, xVal, yVal) == self.numUnmarkedNeighbors(xVal, yVal))
                safe = (self.effectiveLabel(number, xVal, yVal) == 0)
                
                for c in currentNeighbors:
                    (cX, cY) = c
                    if (board[cX][cY] == -1):
                        if mine:
                            flagged.append(c)
                            flag.add(c)
                            if c in onTheQ:
                                onTheQ.remove(c)
                                self.removeElement(cX, cY)
                        elif (c not in onTheQ and safe):
                            q.append(c)
                            onTheQ.add(c)
            
            if len(flagged) != 0:
                xVal, yVal = flagged.pop()
                board[xVal][yVal] = -2

                if ((xVal, yVal) in cov):
                    cov.remove((xVal, yVal))
        
                self.timeElapsed += time() - startTime
                return Action(AI.Action.FLAG, xVal, yVal)
            
            elif len(q) != 0:
                xVal, yVal = q.pop()
                
                endTime = time()
                self.timeElapsed += (endTime - startTime)
                return Action(AI.Action.UNCOVER, xVal, yVal)

            else:
                for cX, cY in cov:
                    for nX, nY in self.getValidNeighbors(cX, cY):
                        n_neighbors = self.getValidNeighbors(nX, nY)
                        if (nX, nY) not in cov and board[nX][nY] != -2:
                            if self.effectiveLabel(board[nX][nY], nX, nY) == self.numUnmarkedNeighbors(nX, nY):
                                # get unmarked neighbors of v
                                for kX, kY in n_neighbors:
                                    if (kX, kY) in cov and (kX, kY) not in onTheQ:
                                        flag.add((kX, kY))
                                        flagged.append((kX, kY))
                                        cov.remove((kX, kY))
                            elif self.effectiveLabel(board[nX][nY], nX, nY) == 0:
                                # iterate through neighbors of (nX, nY) and add each one to q
                                for kX, kY in n_neighbors:
                                    if (kX, kY) in cov and (kX, kY) not in onTheQ:
                                        q.append((kX, kY))
                                        onTheQ.add((kX, kY))
                                        
                if len(flag) == self.t:
                    for c in cov:
                        q.append(c)
                        onTheQ.add(c)

                if len(flagged) > 0:
                    xVal, yVal = flagged.pop()
                    board[xVal][yVal] = -2

                    self.timeElapsed += (time() - startTime)
                    return Action(AI.Action.FLAG, xVal, yVal)
                
                elif len(q) != 0:
                    xVal, yVal = q.pop()
                    
                    self.timeElapsed += (time() - startTime)
                    return Action(AI.Action.UNCOVER, xVal, yVal)
                
                else:
                    
                    if (((self.r * self.c) - self.t) == self.uncovered):
                        return Action(AI.Action.LEAVE)

                    tempMin = 1000
                    minX, minY = -1, -1
                
                    for (cX, cY) in cov:
                        c_prob = self.calcAvgProb(cX, cY)
                    
                        if c_prob == -1:
                            continue        # dont count this tile if it has no uncovered neighbors
                        elif c_prob < tempMin:
                            tempMin = c_prob
                            minX = cX
                            minY = cY

                    xVal, yVal = minX, minY

                    endTime = time()
                    self.timeElapsed += (endTime - startTime)
                    return Action(AI.Action.UNCOVER, xVal, yVal)

        else:
            rand_index = random.randint(0, len(cov)-1)
            rand_x, rand_y = cov[rand_index]
            xVal, yVal = rand_x, rand_y
            return Action(AI.Action.UNCOVER, xVal, yVal)
        
        
        ########################################################################
        #                           YOUR CODE ENDS                             #
        ####################################################################
