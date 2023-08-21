from random import *
import numpy as np

POSSIBLE_ACTIONS = ['w','a','s','d']

class State:
    def __init__(self,mat):
        self.mat = np.asarray(mat)

    def apply(self,action):
        assert(action in POSSIBLE_ACTIONS)
        
        # Rotate matrix so we always shift left
        np_mat = self.mat
        if(action=='w'):
            rot_mat = np.rot90(np_mat)
        elif(action=='s'):
            rot_mat = np.rot90(np_mat,3)
        elif(action=='d'):
            rot_mat = np.rot90(np_mat,2)
        else:
            rot_mat = np_mat

        # Shift as if we are shifting left
        new_rot_mat = np.copy(rot_mat)  # We will override new_rot_mat
        for row in range(4):
            cur = rot_mat[row,0]
            i = 0
            for col in range(1,4):
                nxt = rot_mat[row,col]
                if(cur==0):
                    cur = nxt
                elif(nxt==0):
                    continue
                elif(cur==nxt):
                    new_rot_mat[row,i] = cur*2
                    i+=1
                    cur = 0
                else:
                    new_rot_mat[row,i] = cur
                    cur = nxt 
                    i+=1
            while(i<4):
                new_rot_mat[row,i] = cur
                cur = 0
                i+=1


        # Rotate matrix back
        if(action=='w'):
            mat = np.rot90(new_rot_mat,3)
        elif(action=='s'):
            mat = np.rot90(new_rot_mat,1)
        elif(action=='d'):
            mat = np.rot90(new_rot_mat,2)
        else:
            mat = new_rot_mat

        return State(list(mat))
    
    
    def addTwo(self):
        candidatePositions = []
        for row in range(4):
            for col in range(4):
                if(self.mat[row,col] == 0):
                    candidatePositions += [(row,col)]
        
        newMat = np.copy(self.mat)
        row,col = -1,-1
        try:
            row,col = candidatePositions[randint(0,len(candidatePositions)-1)]
            newMat[row,col] = 2
        except IndexError:
            pass
        return (State(list(newMat)), (row,col))
    

    def evaluate(self) -> int:
        mat = self.mat
        val = 0
        for row in range(4):
            for col in range(4):
                cur = mat[row,col] ** 2
                positionFactor = 4*(row+1) + (4-col)
                for higherRow in range(0,row):
                    if(mat[higherRow,col]>cur):
                        val -= mat[higherRow,col] * positionFactor * 2
                    if(mat[higherRow,col]==cur):
                        val -= mat[higherRow,col] * positionFactor
                for righterCol in range(col+1,4):
                    if(mat[row,righterCol]>cur):
                        val -= mat[row,righterCol] * positionFactor * 2
                    if(mat[row,righterCol]==cur):
                        val -= mat[row,righterCol] * positionFactor
                val += cur * positionFactor
        return val
    

    def canMove(self,action):
        return np.any(self.apply(action).mat != self.mat)