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
import numpy as np

class PatternDatabase:
    def __init__(self, size=4):
        self.size = size
        self.patterns = {}
        self.initialize_patterns()
    
    def initialize_patterns(self):
        # Create pattern databases for different groups of tiles
        # For 15-puzzle, we'll use 3 groups: 1-5, 6-10, 11-15
        self.patterns['group1'] = self.build_pattern_db(range(1, 6))
        self.patterns['group2'] = self.build_pattern_db(range(6, 11))
        self.patterns['group3'] = self.build_pattern_db(range(11, 16))
    
    def build_pattern_db(self, tile_group):
        # Simplified pattern database implementation
        # In a full implementation, this would precompute and store all possible patterns
        db = {}
        for tile in tile_group:
            goal_pos = (tile - 1) // self.size, (tile - 1) % self.size
            db[tile] = goal_pos
        return db
    
    def get_pattern_cost(self, board):
        cost = 0
        for group, pattern in self.patterns.items():
            for tile, goal_pos in pattern.items():
                if tile in board:
                    idx = board.index(tile)
                    current_pos = (idx // self.size, idx % self.size)
                    cost += abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])
        return cost

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
        self.hash = hash(tuple(self.board))  # Precompute hash for faster comparisons

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

        # Define possible moves in order of preference (up, down, left, right)
        moves = [
            (row > 0, blank_index - size),  # up
            (row < size - 1, blank_index + size),  # down
            (col > 0 and blank_index % size != 0, blank_index - 1),  # left
            (col < size - 1 and blank_index % size != size - 1, blank_index + 1)  # right
        ]

        for can_move, target_idx in moves:
            if can_move:
                # Create a new board by swapping with the blank space
                new_board = self.board[:]
                new_board[blank_index], new_board[target_idx] = new_board[target_idx], new_board[blank_index]
                # Create new Node and add to the frontier
                new_node = Node(new_board, Parent=self)
                frontier.append(new_node)

        return frontier

 
        

    # Name: Check Heuristic
    # Uses manhatan distance to fin
    def check_heuristic(self, board):
        size = int(math.sqrt(len(board)))
        pattern_db = PatternDatabase(size)
        
        # Manhattan distance
        manhattan = 0
        for idx, value in enumerate(board):
            if value == -1:
                continue
            current_row, current_col = idx // size, idx % size
            goal_row, goal_col = (value - 1) // size, (value - 1) % size
            manhattan += abs(current_row - goal_row) + abs(current_col - goal_col)
        
        # Linear conflicts
        linear_conflicts = 0
        for i in range(size):
            row = board[i*size:(i+1)*size]
            col = board[i::size]
            linear_conflicts += self.count_linear_conflicts(row)
            linear_conflicts += self.count_linear_conflicts(col)
        
        # Pattern database cost
        pattern_cost = pattern_db.get_pattern_cost(board)
        
        # Combine heuristics with weights
        return manhattan + 2 * linear_conflicts + pattern_cost

    def count_linear_conflicts(self, line):
        conflicts = 0
        for i, tile1 in enumerate(line):
            if tile1 == -1:
                continue
            for j, tile2 in enumerate(line[i+1:], i+1):
                if tile2 == -1:
                    continue
                if tile1 > tile2 and (tile1 - 1) // len(line) == (tile2 - 1) // len(line):
                    conflicts += 2
        return conflicts
    
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
        self.visited = set()

    def solve(self):
        # Go through the frontier
        while self.frontier:
            # Pop node with the lowest priority
            priority, _, current_node = heapq.heappop(self.frontier)

            # Convert board to tuple to hash it in visited set
            board_tuple = tuple(current_node.board)
            
            #If board is in visted
            if board_tuple in self.visited:
                continue

            # Add board to visted
            self.visited.add(board_tuple)
            
            # Print the current node's board and cost
            #print("Board:", current_node.board, "| Cost:", current_node.cost, "| Heuristic:", current_node.heuristic, "| Priority:", priority)
            
            # Check if the current node is the goal
            if current_node.is_solved():
                #print("Solution found!")
                return current_node
            
            # Generate moves and add them to the frontier
            for neighbor in current_node.generate_moves():
                if neighbor.hash not in self.visited:
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



