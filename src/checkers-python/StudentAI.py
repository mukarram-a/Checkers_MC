from random import randint
from BoardClasses import Move
from BoardClasses import Board
import sys, math, logging
from copy import deepcopy

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

logging.basicConfig(level = logging.DEBUG, filename = "log.log", filemode = "w",
                    format = "%(asctime)s - %(levelname)s - %(lineno)d - %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S")

EXPLORATION = 3
root = None

class Node():

    def __init__(self, parent, move, board, color):
        self.isexpanded = 0            # 0 if the node has not been through the simulation, 1 if it has been through the simulation
        self.issimulated = 0
        self.wins = 0               # Tracks the number of wins from the simulation
        self.totalSimulations = 0   # Tracks the total simulations run on a node
        self.exploration = EXPLORATION
        self.move = move            # Board position that the piece moves to
        self.parent = parent        # Node object that references the parent node
        self.children = list()       # Contains Node objects for child nodes
        self.color = color 
        self.board = board
        self.opponent = {1:2,2:1}



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
            # If the current node should not be removed, skip it.
            return

        if parent.children == set():
            # If node has no children, delete it
            del parent
            return

        for nodes in self.children:
            # else, recursively check all nodes to see if they can be deleted
            self.removeSubTree(nodes, do_not_remove)
        
        return
            
    
    def findMove(self):
        global root
        '''
        Checks the highest value child to determine the next move
        
        '''

        #TODO

        # If the root node has children, get the highest-value 
        # child to determine the next move
        if root.children != set():
            future_move = max(root.children)


    def UCT(self):
        '''
        Calculates and returns the UCT value for a node
        
        '''
        if self.totalSimulations == 0: 
            return sys.maxsize
        
        return (self.wins/self.totalSimulations) + self.exploration * math.sqrt((math.log(self.parent.totalSimulations)/ self.totalSimulations))

    def backpropogate(self):
        '''
        Starts at a child node and updates "wins" and "totalSimulations" 
        values for all parent nodes as it reaches the root.
        
        '''
        curr_node = self
        while curr_node.parent != None:
            curr_node.parent.wins += self.wins
            curr_node.parent.totalSimulations += self.totalSimulations
            curr_node = self.parent


    def expand(self):
        moves = self.board.get_all_possible_moves(self.color)
        logging.debug(moves)
        for piece in moves: 
            #logging.debug(piece)
            for move in piece:
                #logging.debug("self.color is ", self.color)
                logging.debug(move)
                self.board.make_move(move, self.color)
                child = Node(self, move, self.board, self.opponent[self.color])
                self.children.append(child)
                self.board.undo()
        self.isexpanded = 1
    

    
    def simulate(self):
        '''
        Simulates a game to an end-state (win, lose, or tie) based on random probability

        Returns 0 for Loss and Tie
        Returns 1 for Win 
        
        '''
        
        color = deepcopy(self.color)
        self.issimulated = 1
        count = 0
        while True: 
            win = self.board.is_win(color)
            moves = self.board.get_all_possible_moves(color)

            if win == 0 and moves == []: #condition where there is a tie.
                self.totalSimulations += 1
                self.wins += 1
                return
            elif win == self.color:
                self.totalSimulations += 1
                self.wins += 1
                return
            elif win == self.opponent[self.color]:  # Condition where enemy wins
                self.totalSimulations += 1
                return 
            
            
            index = randint(0,len(moves)-1)
            inner_index =  randint(0,len(moves[index])-1)
            move = moves[index][inner_index]
            self.board.make_move(move,color)
            count += 1
            
            if color == 1:
                color = 2
            else:
                color = 1
        
        for i in count: 
            self.board.undo()



    def findLargestChild(self):
        '''
        Takes a parent node as a parameter and returns the child Node that has the largest UCT value
        
        '''

        max_child = None
        max_score = 0

        if self.children == list():
            return None

        # Get the UTC score for all children
        for child in self.children:
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
        

        numSimulations = 5
        root_node = Node(None, move, self.board, self.color)

        curr_node = root_node
        
        logging.debug(curr_node.color)
        curr_node.simulate()
        logging.debug(curr_node.color)

        while numSimulations > 0: 
            logging.debug(numSimulations)
            if curr_node.isexpanded == 0: 
                logging.debug("Inside if statement")
                curr_node.expand()
                for child in curr_node.children: 
                    child.simulate()
                    child.backpropogate() 
                    logging.debug("Child is expanded is " + str(child.isexpanded))
                numSimulations -= 1
                curr_node = root_node
            else:
                logging.debug("Inside else statement")
                logging.debug("curr_node isexpanded: " + str(curr_node.isexpanded))
                logging.debug("curr_node issimulated: " + str(curr_node.issimulated))
                if curr_node.issimulated == 1 and curr_node.children != []: 
                    logging.debug("finding the largest child")
                    curr_node = curr_node.findLargestChild()

        bestchild = root_node.findLargestChild()
        self.board.make_move(move,self.color)
        return bestchild.move
