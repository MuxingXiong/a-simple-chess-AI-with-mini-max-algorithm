import numpy as np
import random
import time
import math

infinity = math.inf
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


class state:
    def __init__(self,chessboard,color,search_depth):
        self.chessboard = chessboard
        self.color = color
        self.search_depth = search_depth
    def step(self,nextStep):
        newChessBoard = np.copy(self.chessboard)
        newChessBoard[nextStep[0]][nextStep[1]] = self.color
        return state(newChessBoard,-1*self.color,self.search_depth+1)



class AI(object):
    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #You are white or black
        self.color = color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need to add your decision to your candidate_list. The system will get the end of your candidate_list as your decision. 
        self.candidate_list = []
        self.opponentColor = -1*color
        self.PositionWeight = np.multiply(-1,
            np.array([ [100,-25,1,5,5,1,-25,100],
                            [-25,-45,1,1,1,1,-45,-25],
                            [1,1,1,2,2,1,1,10],
                            [5,1,2,1,1,2,1,5], 
                            [5,1,2,1,1,2,1 ,5],
                            [1,1,3,1,2,1,1,1],
                            [-25,-45,1,1,1,1,-45,-25],
                            [100,-25,1,5,5,1,-25,100]])
                            )

    # The input is the current chessboard. Chessboard is a numpy array.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear() 
        #==================================================================
        #Write your algorithm here
        self.findCandidateList(chessboard)
        _ , move = self.alphabeta_search(chessboard)
        if(move is not None):
            self.candidate_list.append(move)
        #==============Find new pos========================================

    def alphabeta_search(self,chessboard):

        def max_value(state, alpha, beta):
            if self.is_terminal(state):
                return self.utility(state), None
            v, move = -infinity, None
            for a in self.candidate_list:
                v2, _ = min_value(state.step(a), alpha, beta)
                if(v2>v):
                    v = v2
                    move = a
                if(v>=beta):
                    return v,move
                alpha = max(alpha,v)
            return v, move

        def min_value(state, alpha, beta):
            if self.is_terminal(state):
                return self.utility(state), None
            v, move = infinity, None
            for a in self.candidate_list:
                v2, _ = max_value(state.step(a), alpha, beta)
                if(v2<v):
                    v = v2
                    move = a
                if(v<=alpha):
                    return v,move
                beta = min(beta,v)
            return v, move

        state0 = state(chessboard=chessboard,color=self.color,search_depth=0)
        return max_value(state0, -infinity, +infinity)
    
    def is_terminal(self,state):
        if(len(self.candidate_list)==0):
            return True
        elif(state.search_depth>5):
            return True
        else:
            return False

    def map_weight_sum(self,chessboard):
        return sum(sum(np.multiply(chessboard,self.PositionWeight)))*self.color

    def utility(self,state):
        chessboard = state.chessboard
        return self.map_weight_sum(chessboard=chessboard)

    def findPossibleCandidate(self,i,j,chessboard):
        #up
        m = 1
        while(i-m>=0):
            if(m==1 and (chessboard[i-m][j]==0 or chessboard[i-m][j]==self.color)):
                break
            elif(chessboard[i-m][j]==self.opponentColor):
                m = m + 1
                continue
            elif(chessboard[i-m][j]==self.color):
                break
            elif(chessboard[i-m][j]==0):
                self.candidate_list.append((i-m,j))
                break
        #down
        m = 1
        while(i+m<=self.chessboard_size-1):
            if(m==1 and (chessboard[i+m][j]==0 or chessboard[i+m][j]==self.color)):
                break
            elif(chessboard[i+m][j]==self.opponentColor):
                m = m + 1
                continue
            elif(chessboard[i+m][j]==self.color):
                break
            elif(chessboard[i+m][j]==0):
                self.candidate_list.append((i+m,j))
                break
        #left
        m = 1
        while(j-m>=0):
            if(m==1 and (chessboard[i][j-m]==0 or chessboard[i][j-m]==self.color)):
                break
            elif(chessboard[i][j-m]==self.opponentColor):
                m = m + 1
                continue
            elif(chessboard[i][j-m]==self.color):
                break
            elif(chessboard[i][j-m]==0):
                self.candidate_list.append((i,j-m))
                break
        #right
        m = 1
        while(j+m<=self.chessboard_size-1):
            if(m==1 and (chessboard[i][j+m]==0 or chessboard[i][j+m]==self.color)):
                break
            elif(chessboard[i][j+m]==self.opponentColor):
                m = m + 1
                continue
            elif(chessboard[i][j+m]==self.color):
                break
            elif(chessboard[i][j+m]==0):
                self.candidate_list.append((i,j+m))
                break
        #leftup
        m = 1
        while(i-m>=0 and j-m>=0):
            if(m==1 and (chessboard[i-m][j-m]==0 or chessboard[i-m][j-m]==self.color)):
                break
            elif(chessboard[i-m][j-m]==self.opponentColor):
                m = m + 1
                continue
            elif(chessboard[i-m][j-m]==self.color):
                break
            elif(chessboard[i-m][j-m]==0):
                self.candidate_list.append((i-m,j-m))
                break
        #leftdown
        m = 1
        while(i+m<=self.chessboard_size-1 and j-m>=0):
            if(m==1 and (chessboard[i+m][j-m]==0 or chessboard[i+m][j-m]==self.color)):
                break
            elif(chessboard[i+m][j-m]==self.opponentColor):
                m = m + 1
                continue
            elif(chessboard[i+m][j-m]==self.color):
                break
            elif(chessboard[i+m][j-m]==0):
                self.candidate_list.append((i+m,j-m))
                break
        #rightup
        m = 1
        while(i-m>=0 and j+m<=self.chessboard_size-1):
            if(m==1 and (chessboard[i-m][j+m]==0 or chessboard[i-m][j+m]==self.color)):
                break
            elif(chessboard[i-m][j+m]==self.opponentColor):
                m = m + 1
                continue
            elif(chessboard[i-m][j+m]==self.color):
                break
            elif(chessboard[i-m][j+m]==0):
                self.candidate_list.append((i-m,j+m))
                break
        #rightdown
        m = 1
        while(i+m<=self.chessboard_size-1 and j+m<=self.chessboard_size-1):
            if(m==1 and (chessboard[i+m][j+m]==0 or chessboard[i+m][j+m]==self.color)):
                break
            elif(chessboard[i+m][j+m]==self.opponentColor):
                m = m + 1
                continue
            elif(chessboard[i+m][j+m]==self.color):
                break
            elif(chessboard[i+m][j+m]==0):
                self.candidate_list.append((i+m,j+m))
                break

    def findCandidateList(self,chessboard):
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if(chessboard[i][j]==self.color):
                    self.findPossibleCandidate(i,j,chessboard)
        self.candidate_list = list(set(self.candidate_list))

