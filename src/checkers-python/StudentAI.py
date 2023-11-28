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

EXPLORATION = 0.5
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
        '''curr_node = self
        while curr_node.parent != None:
            curr_node.parent.wins += self.wins
            curr_node.parent.totalSimulations += self.totalSimulations
            curr_node = curr_node.parent'''
        
        curr_node = self
        color = 1 
        while curr_node.parent != None:
            #logging.debug("Child Node Wins = " + str(curr_node.wins) + ". Child Node Simulations = " + str(curr_node.totalSimulations))
            
            if color == 1:
                curr_node.parent.wins += self.totalSimulations - self.wins
            elif color == -1:
                curr_node.parent.wins += self.wins
            curr_node.parent.totalSimulations += self.totalSimulations

            #logging.debug("Parent Node Wins = " + str(curr_node.parent.wins) + ". Parent Node Simulations = " + str(curr_node.parent.totalSimulations))

            curr_node = curr_node.parent
            color *= -1

    def expand(self):
        moves = self.board.get_all_possible_moves(self.color)
        logging.debug(moves)
        for piece in moves: 
            #logging.debug(piece)
            for move in piece:
                #logging.debug(move)
                #logging.debug("self.color is ", self.color)
                #logging.debug(move)
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
        
        #logging.debug("Inside simulate function")
        color = 1 if self.color == 1 else 2
        #logging.debug("Color is " + str(self.color))
        simulate_board = deepcopy(self.board)
        self.issimulated = 1
        count = 0
        while True: 
            #logging.debug("Color is " + str(self.color))
            
            win = simulate_board.is_win(color)
            moves = simulate_board.get_all_possible_moves(color)

            empty1 = simulate_board.get_all_possible_moves(self.color) == []
            empty2 = simulate_board.get_all_possible_moves(self.opponent[self.color]) == []



            if win == 0 and (empty1 or empty2): #condition where there is a tie.
                #logging.debug("Node's moves: ")
                #logging.debug(simulate_board.get_all_possible_moves(self.color))
                #logging.debug("Opponent's moves: ")
                #logging.debug(simulate_board.get_all_possible_moves(self.opponent[self.color]))
                self.totalSimulations += 1
                #logging.debug("Color is " + str(color))
                #logging.debug("win is " + str(win))
                #logging.debug("Tie")
                break
            elif win == self.parent.color:
                #logging.debug("Node's moves: ")
                #logging.debug(simulate_board.get_all_possible_moves(self.color))
                #logging.debug("Opponent's moves: ")
                #logging.debug(simulate_board.get_all_possible_moves(self.opponent[self.color]))
                self.totalSimulations += 1
                self.wins += 1
                #logging.debug("Color is " + str(color))
                #logging.debug("win is " + str(win))
                #logging.debug("win")
                break
            elif win == self.opponent[self.parent.color]:  # Condition where enemy wins
                #logging.debug("Node's moves: ")
                #logging.debug(simulate_board.get_all_possible_moves(self.color))
                #logging.debug("Opponent's moves: ")
                #logging.debug(simulate_board.get_all_possible_moves(self.opponent[self.color]))
                #logging.debug("Color is " + str(color))
                #logging.debug("win is " + str(win))
                #logging.debug("lose")
                self.totalSimulations += 1
                break  
            
            
            
            #logging.debug(empty1 or empty2)

            index = randint(0,len(moves)-1)
            inner_index =  randint(0,len(moves[index])-1)
            
            
            move = moves[index][inner_index]
            simulate_board.make_move(move,color)
            #logging.debug("Color is " + str(color) + "and made move: ")
            #logging.debug(move)
            count += 1

            #orig_stdout = sys.stdout
            #f = open('out.txt', 'a')
            #sys.stdout = f

            #simulate_board.show_board()

            #sys.stdout = orig_stdout
            #f.close()
            
            if color == 1:
                color = 2
            else:
                color = 1

        #exit()
        
        
        #for i in range(count): 
        #    self.board.undo()



    def findLargestChild(self):
        '''
        Takes a parent node as a parameter and returns the child Node that has the largest UCT value
        
        '''

        max_child = None
        max_score = -1

        if self.children == list():
            logging.debug("Returning None")
            return None

        # Get the UTC score for all children
        for child in self.children:
            if child.UCT() > max_score:
                max_child = child
                max_score = child.UCT()

        logging.debug("Returning max child")
        return max_child

    def returnBestMove(self):
        max_child = None
        max_score = 0

        if self.children == list():
            return None

        # Get the UTC score for all children
        for child in self.children:
            score = child.totalSimulations
            if score > max_score:
                max_child = child
                max_score = score

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
        

        #logging.debug(self.board.get_all_possible_moves(self.color))
        
        numSimulations = 20
        root_node = Node(None, move, self.board, self.color)

        curr_node = root_node
        curr_node.issimulated = 1
        
        #logging.debug(curr_node.color)
        #curr_node.simulate()
        logging.debug("299 Curr_node is None: " + str(curr_node == None))

        while numSimulations > 0: 
            logging.debug(numSimulations)
            if curr_node.isexpanded == 0: 
                #logging.debug("Inside if statement")
                #logging.debug("curr_node color is: ")
                #logging.debug(curr_node.color)
                curr_node.expand()
                #logging.debug("After expanding")
                for child in curr_node.children: 
                    #logging.debug("child color is: ")
                    #logging.debug(child.color)
                    child.simulate()
                    #logging.debug("After simulate child")
                    child.backpropogate() 
                    #logging.debug("Child is expanded is " + str(child.isexpanded))
                numSimulations -= 1
                curr_node = root_node
                logging.debug("318 Curr_node is None: " + str(curr_node == None))
            else:
                #logging.debug("Inside else statement")
                #logging.debug("curr_node isexpanded: " + str(curr_node.isexpanded))
                #logging.debug("curr_node issimulated: " + str(curr_node.issimulated))
                if curr_node.issimulated == 1 and curr_node.children != []: 
                    #logging.debug("finding the largest child")
                    
                    #if curr_node.children == []:
                    #    logging.debug("Line 326")
                    #    logging.debug(curr_node.wins)
                    #    logging.debug(curr_node.totalSimulations)
                    #    logging.debug(children)
                    
                    logging.debug(curr_node.children)
                    curr_node = curr_node.findLargestChild()
                    logging.debug("336 Curr_node is None: " + str(curr_node == None))
                    #logging.debug(curr_node == None)

                    #logging.debug(curr_node.UCT())


            #logging.debug("end of while loop")
        bestchild = root_node.returnBestMove()
        #self.board.show_board()
        #logging.debug("Best move is: ")
        #logging.debug(bestchild.move)
        #for child in root_node.children:
            #logging.debug("child info is: ")
            #logging.debug(child.totalSimulations)
            #logging.debug(child.move)
        #logging.debug("Best move is: ")
        #logging.debug(bestchild.move)
        #logging.debug(self.board.get_all_possible_moves(self.color))
        #logging.debug("end")
        self.board.make_move(bestchild.move,self.color)
        return bestchild.move
