# 2022 Q2

import math
import random
import numpy
import pylab

I = range(10)

Board = {(0, 0): (3, 4, 4, 2), (0, 1): (4, 3, 2, 3), (0, 2): (1, 3, 1, 4), (0, 3): (4, 3, 2, 2), (0, 4): (2, 3, 3, 3), (0, 5): (2, 1, 3, 4), (0, 6): (1, 1, 2, 3), (0, 7): (3, 4, 4, 2), (0, 8): (1, 1, 1, 2), (0, 9): (3, 3, 2, 4), (1, 0): (1, 1, 2, 4), (1, 1): (1, 1, 2, 1), (1, 2): (3, 2, 4, 4), (1, 3): (3, 1, 1, 2), (1, 4): (3, 2, 3, 1), (1, 5): (4, 2, 1, 2), (1, 6): (4, 3, 3, 1), (1, 7): (1, 1, 1, 2), (1, 8): (3, 2, 2, 1), (1, 9): (1, 2, 4, 4), (2, 0): (3, 3, 2, 3), (2, 1): (2, 4, 4, 2), (2, 2): (1, 3, 4, 3), (2, 3): (1, 3, 1, 3), (2, 4): (3, 4, 2, 2), (2, 5): (3, 3, 2, 3), (2, 6): (2, 2, 3, 2), (2, 7): (3, 2, 2, 2), (2, 8): (3, 3, 2, 3), (2, 9): (4, 4, 1, 3), (3, 0): (3, 2, 2, 3), (3, 1): (4, 2, 4, 2), (3, 2): (2, 1, 1, 4), (3, 3): (4, 2, 2, 2), (3, 4): (1, 3, 1, 1), (3, 5): (2, 2, 4, 3), (3, 6): (3, 4, 1, 1), (3, 7): (1, 4, 3, 1), (3, 8): (2, 4, 1, 1), (3, 9): (4, 1, 4, 1), (4, 0): (4, 4, 4, 3), (4, 1): (2, 4, 1, 3), (4, 2): (1, 4, 2, 1), (4, 3): (4, 1, 3, 4), (4, 4): (4, 2, 2, 1), (4, 5): (3, 4, 1, 1), (4, 6): (2, 2, 3, 1), (4, 7): (2, 1, 1, 4), (4, 8): (2, 4, 4, 4), (4, 9): (2, 2, 3, 4), (5, 0): (3, 3, 4, 3), (5, 1): (4, 1, 3, 4), (5, 2): (1, 2, 3, 4), (5, 3): (2, 1, 4, 1), (5, 4): (2, 1, 4, 2), (5, 5): (4, 1, 1, 1), (5, 6): (3, 4, 2, 1), (5, 7): (2, 3, 2, 3), (5, 8): (4, 2, 3, 4), (5, 9): (1, 1, 3, 1), (6, 0): (4, 3, 4, 2), (6, 1): (1, 4, 4, 3), (6, 2): (3, 4, 2, 2), (6, 3): (3, 2, 2, 2), (6, 4): (4, 1, 3, 4), (6, 5): (3, 2, 3, 4), (6, 6): (1, 1, 3, 4), (6, 7): (1, 1, 3, 1), (6, 8): (4, 4, 4, 3), (6, 9): (1, 2, 3, 2), (7, 0): (1, 4, 2, 3), (7, 1): (4, 3, 3, 2), (7, 2): (2, 2, 4, 1), (7, 3): (2, 1, 4, 1), (7, 4): (2, 3, 3, 4), (7, 5): (4, 2, 2, 4), (7, 6): (3, 2, 3, 2), (7, 7): (3, 1, 3, 1), (7, 8): (2, 3, 4, 2), (7, 9): (3, 3, 3, 1), (8, 0): (4, 1, 1, 3), (8, 1): (4, 4, 2, 4), (8, 2): (2, 2, 4, 4), (8, 3): (3, 2, 3, 3), (8, 4): (3, 2, 3, 1), (8, 5): (2, 4, 2, 3), (8, 6): (3, 3, 3, 1), (8, 7): (1, 4, 4, 4), (8, 8): (3, 3, 1, 2), (8, 9): (4, 2, 1, 1), (9, 0): (4, 4, 3, 4), (9, 1): (4, 4, 2, 3), (9, 2): (3, 4, 2, 4), (9, 3): (2, 4, 3, 3), (9, 4): (1, 2, 1, 3), (9, 5): (4, 1, 3, 2), (9, 6): (1, 1, 1, 2), (9, 7): (4, 1, 4, 1), (9, 8): (2, 1, 4, 4), (9, 9): (4, 4, 3, 1)}

def BoardCost(B):
    # Sum of absolute values of difference
    # Do left and above for every square
    Sum = 0
    for i in I:
        for j in I:
            if j > 0:
                Sum += abs(B[i,j][0]-B[i,j-1][2])
            if i > 0:
                Sum += abs(B[i,j][1]-B[i-1,j][3])
    return Sum

def ChooseNeigh(sol):
    i, j, k, l = numpy.random.randint(0, 10, 4)
    c1 = BoardCost(sol)
    sol[i, k], sol[j, l] = sol[j, l], sol[i, k]
    c2 = BoardCost(sol)
    sol[i, k], sol[j, l] = sol[j, l], sol[i, k]
    return c2 - c1, (i, j, k, l)

def MoveToNeigh(sol, neighbour):
    i, j, k, l = neighbour
    sol[i, k], sol[j, l] = sol[j, l], sol[i, k]
    return

def RunSA(Solution,Cost,ChooseNeigh,MoveToNeigh,T,N,alpha):
    E = Cost(Solution)
    Best = E
    CostArr = [E]
    BestArr = [Best]
    BestSol = dict(Solution)  # since Solution will be a dictionary (board)
    for i in range(N):
        delta,neighbour = ChooseNeigh(Solution)
        if delta < 0 or math.exp(-delta/T) > random.random():
            MoveToNeigh(Solution,neighbour)
            E += delta
            if E < Best:
                Best = E
                BestSol = dict(Solution)
        CostArr.append(E)
        BestArr.append(Best)
        T *= alpha
    print (Best, T)
    pylab.plot(range(N+1),CostArr)
    pylab.plot(range(N+1),BestArr)
    pylab.show()
    return BestSol


cost = BoardCost(Board)

RunSA(Board, BoardCost, ChooseNeigh, MoveToNeigh, 100000, 100000, 0.999)
