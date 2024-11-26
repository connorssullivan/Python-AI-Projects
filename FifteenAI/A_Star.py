# Psedo Code:
# Correct Configuration
# Class Node:
#   Current State
#   Cost To Here (How Many Steps)
#   Heuristic (Manhatan Distance of all pieces summed)
# 
#   void GenerateMoves():
#       Build the Frontier
#       Create new Nodes   
#           Get Cost
#           Get Heuristic
#       Insert these Node into PQ
#       (EXTRA CREDIT: Generate multiple move turns)
#
#   int CheckHeuristic():
#       Get the heuristic
#
#   Void CheckSolved():
#       Check if the puzzle is solved    
#
#   void Make Move():
#       Expand off of frontier
#       Pop from priority queue
#       Check if solved
#       Generate new Moves


import heapq
import math

class Node:
    # Name: Constructor
    # Desc: Creates a Node
    def __init__(self, boardState, Parent= None):
        self.board = boardState # Set Nodes board
        self.parent = Parent # Set the parent

        # Set Nodes Cost
        if Parent == None:
            self.cost = 0
        else:
            self.cost = Parent.cost + 1
        
        # Set Nodes heuristic
        self.heuristic = self.check_heuristic(self.board)

    #Name Generate Moves
    # Desc: Gene
    def generate_moves(self):
        # Get size of board
        size = int(math.sqrt(len(self.board)))

        # Find blank space
        blank_index = self.board.index(-1)
        row, col = blank_index // size, blank_index % size

        # List to hold possible moves as new nodes
        frontier = []

        # Go through the board
        # Loop through each tile in the board
        for idx, num in enumerate(self.board):
            # If it is blank (-1), skip it
            if num == -1:
                continue

            # If you can move up
            if row > 0 and idx == blank_index - size:
                # Create a new board by swapping with the blank space
                new_board = self.board[:]
                new_board[blank_index], new_board[idx] = new_board[idx], new_board[blank_index]
                # Create new Node and add to the frontier
                new_node = Node(new_board, Parent=self)
                frontier.append(new_node)

            # If you can move down
            if row < size - 1 and idx == blank_index + size:
                # Create a new board by swapping with the blank space
                new_board = self.board[:]
                new_board[blank_index], new_board[idx] = new_board[idx], new_board[blank_index]
                # Create new Node and add to the frontier
                new_node = Node(new_board, Parent=self)
                frontier.append(new_node)

            # If you can move left
            if col > 0 and idx == blank_index - 1 and blank_index % size != 0:
                # Create a new board by swapping with the blank space
                new_board = self.board[:]
                new_board[blank_index], new_board[idx] = new_board[idx], new_board[blank_index]
                # Create new Node and add to the frontier
                new_node = Node(new_board, Parent=self)
                frontier.append(new_node)

            # If you can move right
            if col < size - 1 and idx == blank_index + 1 and blank_index % size != size - 1:
                # Create a new board by swapping with the blank space
                new_board = self.board[:]
                new_board[blank_index], new_board[idx] = new_board[idx], new_board[blank_index]
                # Create new Node and add to the frontier
                new_node = Node(new_board, Parent=self)
                frontier.append(new_node)

        return frontier

 
        

    # Name: Check Heuristic
    # Uses manhatan distance to fin
    def check_heuristic(self, board):
        size = int(math.sqrt(len(board)))

        # Target position for each tile in the solved board
        goal = {(i+1): (i // size, i % size) for i in range(size * size - 1)}
        goal[-1] = (size - 1, size - 1)

        distance = 0

        # Go throgh the board
        for idx, value in enumerate(board):
            if value == -1:
                continue  # Ignore blank 
            
            # Current Row and Column
            current_row, current_col = idx // size, idx % size
            
            # Goal row and column
            goal_row, goal_col = goal[value]
            
            # Add the Manhattan distance for this tile
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        
        return distance
    
    # Name: Is Solved
    # Desc: Checks if the puzzle is soved
    def is_solved(self):
        return self.board == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1]


class Environment:
    def __init__(self, initial_board):
        self.initial_node = Node(initial_board)
        self.frontier = []  # List that will serve as a heap
        self.counter = 0  # Counter for tie-breaking
        # Add initial node to the heap with (priority, counter, node)
        heapq.heappush(self.frontier, (self.initial_node.heuristic + self.initial_node.cost, self.counter, self.initial_node))
        self.counter += 1

    def solve(self):
        visited = set()  # Set to track visited board states

        # Go through the frontier
        while self.frontier:
            # Pop node with the lowest priority
            priority, _, current_node = heapq.heappop(self.frontier)

            # Convert board to tuple to hash it in visited set
            board_tuple = tuple(current_node.board)
            
            #If board is in visted
            if board_tuple in visited:
                continue

            # Add board to visted
            visited.add(board_tuple)
            
            # Print the current node's board and cost
            #print("Board:", current_node.board, "| Cost:", current_node.cost, "| Heuristic:", current_node.heuristic, "| Priority:", priority)
            
            # Check if the current node is the goal
            if current_node.is_solved():
                #print("Solution found!")
                return current_node
            
            # Generate moves and add them to the frontier
            for neighbor in current_node.generate_moves():
                # Calculate priority for the neighbor
                neighbor_priority = neighbor.heuristic + neighbor.cost
                # Add the neighbor to the heap
                heapq.heappush(self.frontier, (neighbor_priority, self.counter, neighbor))
                self.counter += 1
                
        #print("No solution found.")
        return None 
    
    def reconstruct_path(self, final_node):
        path = []
        current_node = final_node

        # Traverse back from the solution to the start node
        while current_node is not None:
            path.append(current_node)
            current_node = current_node.parent  # Move to the parent node

        # Reverse the list to show the path from start to solution
        path.reverse()

        # Display the steps
        #for step, node in enumerate(path):
            #print(f"Step {step}:")
            #print(node.board)  # Assuming each node has a 'state' attribute representing the board
            #print()  # Blank line for readability

        return path
    


# Example usage For testing

# Define the initial board for the 15-puzzle (mixed state)
#initial_board = [14, 7, 13, 10, 2, 15, 1, 11, 9, 8, 4, -1, 3, 6, 5, 12]

# Create the environment with the initial board
#env = Environment(initial_board)

# Solve the puzzle
#end_node = env.solve()

# Print the solution steps
#final = env.reconstruct_path(end_node)



