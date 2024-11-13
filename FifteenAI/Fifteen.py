import sys
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from random import shuffle, randint
from A_Star import Node, Environment

# NOTES:
# Random.Shuffle() is a function that shuffles the elements of a list in place.
# Constants
CELL_SPACING = 10 
CELL_COUNT = 3
CELL_SIZE = 100
GRID_ORIGINX = 350
GRID_ORIGINY = 350
W_WIDTH = 600
W_HEIGHT = 600

###############################
# Name: Grid Widget
# Desc: Widget for the grid
###############################
class GridWidget(QWidget):

    # Name: Constructosr
    # Desc: Initalizes all the boards valurs
    def __init__(self, turns_label):
        super().__init__()
        self.setGeometry(500, 500, W_WIDTH, W_HEIGHT)
        self.turns = 0 # User moves
        self.rows, self.cols = 4, 4  # Grid Size
        self.initalize_board() # Create the board
        self.turns_label = turns_label # Set turns label
        self.game_over = False # Determins if game is over
        self.setStyleSheet("background-color: #1a1a1a; border: 5px solid #FFD700;")
        self.show()
    
    # Name: Initalize Board
    # Desc: Initalizes the values in each spot of the board
    def initalize_board(self):
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1]
        shuffle(self.board)
        while not self.isSolvable():
            shuffle(self.board)
    
    # Name: Get Inversion Count
    # Desc: Gets the total numbe of inversions in the boards layour
    def getInvCount(self):
        inv_count = 0# Initialize count of inversions

        # Count inversions in the grid
        for i in range((len(self.board))- 1):
            for j in range(i+1, self.rows * self.cols):
                # If current number is greater than the next number then wn know there is an inversion
                if (self.board[j] != -1 and self.board[i] != -1 and self.board[i] > self.board[j]):
                    inv_count += 1
        return inv_count
    
    # Name: Find Empty Position
    # Desc: FInds the empty position in the board list
    def findEmptyPosition(self):
        # find X position of empty tile
        for i in range(len(self.board)):
            if self.board[i] == -1:
                return self.rows - (i // self.rows)
    
    # Name: Flash Colors
    # Desc: Makes grid glash
    def flash_colors(self):
        # Set each cell to a random color
        self.cell_colors = [QColor(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(self.rows * self.cols)]
        self.update()  # Trigger a repaint with new colors
          
    # Name: Is Solvable
    # Desc: Returns True if the board is solbable 
    def isSolvable(self):
        # Count inversions in the grid
        invCount = self.getInvCount()
        # If grid is odd, return true
        if self.rows % 2 == 1:
            return invCount % 2 == 0
        else:
            pos = self.findEmptyPosition()#find the row position of the empty tile

            # If position is even if the inversion count is odd return true elsse false
            if pos % 2 == 0:
                return invCount % 2 == 1
            # If is odd if the inversion count is even return true else false
            else:
                return invCount % 2 == 0

    # Name: Paint Event 
    # Desc: Paints the board
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setFont(QFont("Courier", 20, QFont.Bold))


        index = 0 # Index 

        #Draw Grid in 2d matrix
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculate position for each cell
                x = col * (CELL_SIZE + CELL_SPACING)
                y = row * (CELL_SIZE + CELL_SPACING)

                # Check if this is the blank (-1) square
                if self.board[index] == -1:
                    # Fill the blank square with red
                    qp.fillRect(x, y, CELL_SIZE, CELL_SIZE, QColor(255, 0, 0))  # Red color
                else:
                    qp.setPen(QColor(255, 255, 0))
                    # Draw the grid cell normally
                    qp.drawRect(x, y, CELL_SIZE, CELL_SIZE)
                    # Draw the number
                    qp.drawText(x, y, CELL_SIZE, CELL_SIZE, Qt.AlignCenter, str(self.board[index]))

                # If In correct
                if self.board[index] == index+1:
                    qp.fillRect(x, y, CELL_SIZE, CELL_SIZE, QColor(0, 255, 0))  # Red color
                    qp.setPen(QColor(0, 0, 0))
                    qp.drawText(x, y, CELL_SIZE, CELL_SIZE, Qt.AlignCenter, str(self.board[index]))

                index += 1

        qp.end()

    # Name: Mouse Pressed Event
    # Desc: Runs when a click on the board
    def mousePressEvent(self, event):
        self.is_solved()

         # Check if the game is over
        if self.game_over:
            print("Game Over")
            self.turns_label.setText(f'Game over with {self.turns} turns')
            return
        
        # Get the row and column of the cell that was clicked
        x, y = event.x(), event.y()

        row_len = self.cols * CELL_SIZE 
        col_len = self.rows * CELL_SIZE

        # Check if the click is outside the grid
        if x < 0 or x >= row_len or y < 0 or y >= col_len:
            print("Invalid move: Clicked outside the grid")
            return

        col = x // CELL_SIZE
        row = y // CELL_SIZE
        clicked_num = row * self.cols + col #Cool trick to find index
        print(f"Clicked on cell {row}, {col}, value: {self.board[clicked_num]}")

        # Check if the cell is next to the empty cell
        #self.board[clicked_num] = 0 Just a test
        #self.turns += 1

        # Update the turns label
        self.turns_label.setText(f'Turns: {self.turns}')

        self.move(clicked_num)


        #Update the grid
        self.update() 

    # Name: Move
    # Desc: Move's pieces
    def move(self, index):
        # Move the cell at index to the empty cell
        #Check Up Cell
        if index - self.cols >= 0 and self.board[index - self.cols] == -1:
            print("Move Up Available")
            temp = self.board[index]
            self.board[index] = self.board[index - self.cols]
            self.board[index - self.cols] = temp
            self.turns += 1
            self.turns_label.setText(f'Turns: {self.turns}')
            return

        #Check Down Cell
        elif index + self.cols < len(self.board) and self.board[index + self.cols] == -1:
            print("Move Down Available")
            temp = self.board[index]
            self.board[index] = self.board[index + self.cols]
            self.board[index + self.cols] = temp
            self.turns += 1
            self.turns_label.setText(f'Turns: {self.turns}')
            return

        #Check Left Cell
        elif index % self.cols != 0 and self.board[index - 1] == -1:
            print("Move Left Available")
            temp = self.board[index]
            self.board[index] = self.board[index - 1]
            self.board[index - 1] = temp
            self.turns += 1
            self.turns_label.setText(f'Turns: {self.turns}')
            return


        #Check Right Cell
        elif index % self.cols != self.cols - 1 and self.board[index + 1] == -1:
            print("Move Right Available")
            temp = self.board[index]
            self.board[index] = self.board[index + 1]
            self.board[index + 1] = temp
            self.turns += 1
            self.turns_label.setText(f'Turns: {self.turns}')
            return
        
        check = self.check_lanes(index)
        if check != -1:
            self.turns += check
            self.turns_label.setText(f'Turns: {self.turns}')
            
        else:
            print("No Moves Available")

    # Name: Is Solved
    # Desc: Check if game is over
    def is_solved(self):
        for i in range(len(self.board) - 1):
            if self.board[i] != i + 1:
                self.game_over = False
                return
        self.game_over = True
    
    # Name: Check Lanes
    # Desc: Check if lanes can be moved
    def check_lanes(self, index):
        # Find the row of the blank space 
        index_of_blank = self.board.index(-1)
        blank_row = index_of_blank // self.cols
        clicked_row = index // self.cols

        # Check if the clicked tile is in the same row as the blank space
        if clicked_row == blank_row:
            # Index is less than the blank
            if index < index_of_blank:
                # Move elements from index to the blank position (right shift)
                for i in range(index_of_blank, index, -1):
                    self.board[i] = self.board[i - 1]
                self.board[index] = -1  
                return index_of_blank - index  

            # Index is greater than the blank
            elif index > index_of_blank:
                for i in range(index_of_blank, index):
                    self.board[i] = self.board[i + 1]
                self.board[index] = -1  
                return index - index_of_blank  
        
        # Find the column of the blank space
        blank_col = index_of_blank % self.cols
        clicked_col = index % self.cols

        # Check if the clicked tile is in the same column as the blank space
        if clicked_col == blank_col:
        # Index is less than the blank (shift up)
            if index < index_of_blank:
                for i in range(index_of_blank, index, -self.cols):
                    self.board[i] = self.board[i - self.cols]
                self.board[index] = -1
                return (index_of_blank - index) // self.cols

            # Index is greater than the blank (shift down)
            elif index > index_of_blank:
                for i in range(index_of_blank, index, self.cols):
                    self.board[i] = self.board[i + self.cols]
                self.board[index] = -1
                return (index - index_of_blank) // self.cols

        return -1
        
        
        

    
###############################
# Name: Main Window
# Desc: Main Window that holds Everything
###############################
class MainWindow(QWidget):

    # Name: Constructor
    # Desc: Constructor Function
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        layout = QVBoxLayout()  # Vertical Layout
        self.setLayout(layout)
        self.setGeometry(500, 500, W_WIDTH, W_HEIGHT)

        self.button = QPushButton("Start")
        self.button.setStyleSheet("background-color: #FF00FF; color: #000000; font-weight: bold; font-size: 16px;")
        layout.addWidget(self.button)
        
        #Add an automate button
        self.autoButton = QPushButton("Auto")
        self.autoButton.setStyleSheet("background-color: #00FFFF; color: #000000; font-weight: bold; font-size: 16px;")
        layout.addWidget(self.autoButton)

        self.grid = None
        self.turns_label = None

        # Loading label and timer setup
        self.loading_label = QLabel("")
        self.loading_label.setStyleSheet("color: #FFD700; font-size: 18px; font-weight: bold;")
        layout.addWidget(self.loading_label)

        # Flashing timer for color change
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self.flash_grid_colors)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_loading_text)

        self.loading_text = "Loading"
        self.loading_dots = 0
        self.solution_thread = None  

        #Assign Button Functionalitys
        self.button.clicked.connect(self.on_clicked) #Assigns function to button click
        self.autoButton.clicked.connect(self.auto_on_clicked)

        self.setStyleSheet("background-color: #2b2b2b; color: #FFD700; font-family: 'Courier New';")

    def update_loading_text(self):
        # Cycles through adding dots to simulate loading
        self.loading_dots = (self.loading_dots + 1) % 4
        self.loading_label.setText(self.loading_text + "." * self.loading_dots)


    # Name: Auto On Clicked
    # Desc: Start or stop automation Process
    def auto_on_clicked(self):
        if self.autoButton.text() == "Auto":

            # Set up the A* environment with the current board state
            if self.grid:
                self.autoButton.setText("Stop Auto")
                self.loading_label.setText("Loading")

                # Start timers
                self.timer.start(500) 
                self.flash_timer.start(300)

                # Start solution thread
                env = Environment(self.grid.board)
                self.solution_thread = SolutionThread(env)
                self.solution_thread.solution_found.connect(self.display_solution)
                self.solution_thread.start()

        else:
            self.autoButton.setText("Auto")
            self.timer.stop()
            self.flash_timer.stop()
            self.loading_label.setText("")
            # Stop the solution thread if running
            if self.solution_thread and self.solution_thread.isRunning():
                self.solution_thread.stop()
                self.solution_thread = None

    #Name: Display Solution
    # Desc: Display solution steps
    def display_solution(self, solution_path):
        # Iterate through each step in the solution path
        for step, node in enumerate(solution_path):
            # Update the grid's board to reflect each step
            self.grid.board = node.board
            self.grid.update()
            self.grid.turns = step + 1
            self.turns_label.setText(f'Turns: {self.grid.turns}')
            QApplication.processEvents()  # Refresh the GUI at each step
            # Delay the move
            QThread.msleep(500)


    # Name: On Clicked
    # Desc: If the main window is clicked this function executes
    def on_clicked(self):
        # If start/stop button is clicked
        if self.button.text() == "Start":
            self.button.setText("Stop")

            # Create Grid
            self.turns_label = QLabel("Turns: 0")
            self.turns_label.setStyleSheet("color: #FFD700; font-size: 18px; font-weight: bold;")
            self.grid = GridWidget(self.turns_label)  
            self.grid.setFixedSize(W_WIDTH - 50, W_HEIGHT - 100)

            # Add grid and label to the layout
            self.layout().addWidget(self.turns_label)
            self.layout().addWidget(self.grid)
            
            # Use the center_grid function to center the grid widget
            self.center_grid()
        else:
            # Change the button text back too start
            self.button.setText("Start")

            # Remove the grid and label
            self.grid.setParent(None) # Detatch the giid
            self.grid = None  # Delete the grid
            self.turns_label.setParent(None) # Detatch the label 
            self.turns_label = None # Delete the label
    
    # Name: Center Grid
    # Desc: Centers Grid
    def center_grid(self):
        # Create a horizontal layout to center the grid
        h_layout = QHBoxLayout()
        h_layout.addStretch()  # Add space before the grid to center it
        h_layout.addWidget(self.grid)
        h_layout.addStretch()  # Add space after the grid to center it
        self.layout().addLayout(h_layout)
    
    # Name: Flash Grid
    # Desc: Flashed colors
    def flash_grid_colors(self):
        if self.grid:
            self.grid.flash_colors()

        
# Name: Solution Thread
# Desc: 
class SolutionThread(QThread):
    solution_found = pyqtSignal(object)  # Signal to send the solution path

    def __init__(self, env):
        super().__init__()
        self.env = env
        self._running = True  # Add a flag to control the thread execution

    def run(self):
        # Only run if _running is True
        end_node = None
        if self._running:
            end_node = self.env.solve()

        if end_node and self._running:
            solution_path = self.env.reconstruct_path(end_node)
            self.solution_found.emit(solution_path)

    def stop(self):
        # Set _running to False to halt the run
        self._running = False
        self.quit()
        self.wait()

# Name: Main Function
# Desc: Runs the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

