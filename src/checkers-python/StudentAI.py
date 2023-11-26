from random import randint
from BoardClasses import Move
from BoardClasses import Board
import sys, math

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

EXPLORATION = 3
root = None

class Node():

    def __init__(self, parent, move):
        self.score = 0              # (number of black pieces) - (number of white pieces)
        
        self.wins = 0 
        self.totalSimulations = 0 
        self.exploration = EXPLORATION
        
        self.move = move            # Board position that the piece moves to
        self.parent = parent        # Node object that references the parent node
        self.children = set()       # Contains Node objects for child nodes


    def removeSubTree(self, parent, do_not_remove):
        '''
        Recursively removes sub trees from Python memory to prevent MemoryError
        
        do_not_remove is the node of the subtree that we don't want to delete 

        Ex.

                Root
               /   \
           left     right   

           left is the next move we decided on, so "left" == "do_not_remove"
           The right subtree will be deleted to clear memory
        
        '''

        if parent is do_not_remove:
            return


        if parent.children == set():
            # If node has no children, delete it
            del parent
            return

        for nodes in self.children:
            # else, recursively check all nodes to see if they can be deleted
            self.removeSubTree(nodes)
        
        return
            
    
    def findMove(self):
        global root
        '''
        Checks the highest value child to determine the next move
        
        '''

        # If the root node has children, get the highest-value 
        # child to determine the next move
        if root.children != set():
            future_move = max(root.children)


    def UCT(self):
        return (self.wins/self.totalSimulations) + self.exploration * math.sqrt((math.log(self.parent.totalSimulations)/ self.totalSimulations))


    def findLargestChild(self, parent):
        '''
        Takes a parent node as a parameter and returns the child Node that has the largest UCT value
        
        '''

        max_child = None
        max_score = 0

        # Get the UTC score for all children
        for child in parent.children:
            if child.UCT() > max_score:
                max_child = child
                max_score = child.UCT()

        return max_child




class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        
        '''if self.color == 1:
            self.turn = 'B'
            self.enemy_turn = 'W'
        elif self.color == 2:
            self.turn = 'W'
            self.enemy_turn = "B"'''


    def score(self):
        b_count, w_count = self.board.count_score()
        if self.color == 1:
            return b_count - w_count
        return w_count - b_count

    
    def Max_Value(self,depth):
        #print("Inside Max_value and depth is : ", depth)
        win = self.board.is_win(self.color)
        moves = self.board.get_all_possible_moves(self.color)
        
        v = -sys.maxsize - 1  # Negative Infinity
        move = None

        # Terminal conditions
        if depth == 0:
            #print("returning None")
            return self.score(), None
        elif win == 0 and moves == []: #condition where there is a tie.
            return [0,None]
        elif win == self.color:
            return [7,None] #returning [None for Move obj, 1 for win]
        elif win == self.opponent[self.color]:
            return [-7,None] #returning [None for Move obj, -1 for loss]

        #self.board.show_board()
        #print(moves)
        for pieces in moves: 
            for move_ in pieces: 
                self.board.make_move(move_,self.color)
                v2, move2 = self.Min_Value(depth-1)
                move2 = move_
                self.board.undo()

                if v2 > v: 
                    # If v2 is the largest value found so far, replace v and move
                    v, move = v2, move2

        return v, move



    def Min_Value(self, depth):
        #print("Inside Min_value and depth is : ", depth)
        win = self.board.is_win(self.color)
        moves = self.board.get_all_possible_moves(self.opponent[self.color])
      
        v = sys.maxsize  # Positive Infinity
        move = None
        
        # Terminal Conditions
        if depth == 0: 
            #print("returning None")
            return self.score(), None
        elif win == 0 and moves == []: #condition where there is a tie.
            return [0,None]
        elif win == self.color:
            return [7,None] #returning [None for Move obj, 1 for win]
        elif win == self.opponent[self.color]:  # Condition where enemy wins
            return [-7,None] #returning [None for Move obj, -1 for loss]
        

        # Get all possible moves for the enemy AI & find the best move for the enemy
        #self.board.show_board()
        #print(moves)
        for pieces in moves:
            for enemy_move in pieces:
                #print("Enemy move is: ", enemy_move, ".")
                self.board.make_move(enemy_move, self.opponent[self.color])
                v2, move2 = self.Max_Value(depth - 1)
                move2 = enemy_move
                self.board.undo()

                if v2 < v:
                    # If v2 is the smallest value found so far, replace v and move
                    v, move = v2, move2

        return v, move

    
    def mm_search(self):
        # Mini-Max search

        # Compute all possible moves for our AI
        #moves = self.board.get_all_possible_moves(self.color)

        # Run every possible move through the Max_Value algorithm
        # Find the move that has the largest score value (this is the most optimal move)
        depth = 4
        v, move = self.Max_Value(depth)
        return move 


        #best_move = max([self.Max_Value(i) for i in moves])
    

        # return: Move
        #return best_move

      

    def recursion(self):

        if self.color == 1:
            turn = 'B'
        elif self.color == 2:
            turn = 'W'
        win = self.board.is_win(turn) #we need to pass whose turn it it to check winning condition
        moves = self.board.get_all_possible_moves(self.color)
        if win == 0 and moves != []: # condition where no one won yet
            #print("No one won.")
            #print("moves: ",moves)
            scores = []
            for row in moves: #trying to go through all the moves avaliable and check if they lead to winning conditions
                for move in row:
                    self.board.make_move(move,self.color)
                    score = self.recursion()[1] # index 1 gives the score(win/loss) of making a move
                    scores.append([move,score])
                    self.board.undo() #we have to undo the move just made to test other moves
            scores.sort(key = lambda x: x[1], reverse = True)
            #self.board.show_board()
            #print("Scores: ",scores)
            return [scores[0][0],sum([score[1] for score in scores])] #returning [Move obj, sum of all the wins of all possible moves]
        elif win == 0: #condition where there is a tie.
            return [None,0]
        elif win == self.color:
            return [None,1] #returning [None for Move obj, 1 for win]
        else:
            return [None,-1] #returning [None for Move obj, -1 for loss]
        
    
    def get_move(self,move):
        #print("get_move")
        
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        #moves = self.board.get_all_possible_moves(self.color)
        #index = randint(0,len(moves)-1)
        #inner_index =  randint(0,len(moves[index])-1)
        #move = moves[index][inner_index]
        #move = self.recursion()[0]
        

        
        
        move = self.mm_search()
        #self.board.show_board()
        #print("Resulting move is : ", move)
        #print("COLOR", self.color)
        self.board.make_move(move, self.color)
        return move
