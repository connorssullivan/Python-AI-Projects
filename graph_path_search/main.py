import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time
from search import *
from algorithems import *
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap

#Name: Search Window
# Description: Creates the main search window dor the program
class SearchWindow(QWidget):

    # Name: Main Constructor
    # Description: Creates the QWidget and sets it's Layout
    def __init__(self):
        super().__init__()

        # Dr. Wangs Map
        self.map = UndirectedGraph({
            "Buffalo": {"Boston": 450, "Pittsburgh": 219},
            "Boston": {"NewYork": 216},
            "NewYork": {"Philadelphia": 94, "Pittsburgh": 370},
            "Philadelphia": {"Baltimore": 101, "Salisbury": 138},
            "Pittsburgh": {"Baltimore": 248,},
            "Baltimore": {"WashingtonDC": 45, "Salisbury": 117},
            "WashingtonDC": {"Richmond": 110, "Salisbury": 116},
            "Richmond": {"Norfolk": 93},
            "Norfolk": {"Salisbury": 132},
        
        })
        

        # List all cities
        self.cities = list(self.map.graph_dict.keys())

        # List of algorithms
        self.algorithms = ["BFS", "DFS", "UCS"]

        # UI elements
        # Create QLabel
        self.image_label = QLabel(self)
        pixmap = QPixmap('usa_map.JPG')  
        resized_pixmap = pixmap.scaled(800, 500)  
        self.image_label.setPixmap(resized_pixmap)

        # Start City box
        self.start_label = QLabel("Select Start City:")
        self.start_combo = QComboBox()
        self.start_combo.addItems(self.cities)

        # Selected city box
        self.end_label = QLabel("Select End City:")
        self.end_combo = QComboBox()
        self.end_combo.addItems(self.cities)

        # Algorithm Box
        self.alg_label = QLabel("Select Search Algorithm:")
        self.alg_combo = QComboBox()
        self.alg_combo.addItems(self.algorithms)

        # Button to start search
        self.result_label = QLabel("")
        self.search_button = QPushButton("Start Search")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.start_label)
        layout.addWidget(self.start_combo)
        layout.addWidget(self.end_label)
        layout.addWidget(self.end_combo)
        layout.addWidget(self.alg_label)
        layout.addWidget(self.alg_combo)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        # Button click event
        self.search_button.clicked.connect(self.start_search)

    # Name: Start Search
    # Description: Starts the search algorithem
    def start_search(self):
        # Get selected cities and algorithm
        start_city = self.start_combo.currentText()
        end_city = self.end_combo.currentText()
        algorithm = self.alg_combo.currentText()

        # Check if start and end cities are same
        if start_city == end_city:
            QMessageBox.warning(self, "Invalid", "Start and end cities must be different!!!!!")
            return

        # Display the selection information
        self.result_label.setText(f"Starting Search: {start_city} to {end_city} using {algorithm}")

        # If user selects BFS
        if algorithm == 'BFS':
            print("You have selected BFS")

            # Time the BFS Search
            start_time = time.time() # Start Time
            result = bfs(self.map.graph_dict, start_city, end_city)
            end_time = time.time()# End time

            # Calculate execution time
            execution_time = end_time - start_time

            

            print(f'\nExecution Time: {execution_time}\nPath To Target: {result[0]}\nDistance Of Path: {result[1]} \
                \nVisted Nodes: {result[2]}\nTotal Distance: {result[3]}')
            
            self.result_label.setText(f'\nExecution Time: {execution_time}\nPath To Target: {result[0]}\nDistance Of Path: {result[1]} \
                \nVisted Nodes: {result[2]}\nTotal Distance: {result[3]}')

        # If the User selects DFS
        if algorithm == 'DFS':
            print('You have selected DFS')

            # Time DFS Search
            start_time = time.time()
            result = dfs(self.map.graph_dict, start_city, end_city)
            end_time = time.time()

            # Calculate Execution Time
            execution_time = end_time - start_time

            print(f'\nExecution Time: {execution_time}\nPath To Target: {result[0]}\nDistance Of Path: {result[1]} \
                \nVisted Nodes: {result[2]}\nTotal Distance: {result[3]}')
            
            self.result_label.setText(f'\nExecution Time: {execution_time}\nPath To Target: {result[0]}\nDistance Of Path: {result[1]} \
                \nVisted Nodes: {result[2]}\nTotal Distance: {result[3]}')
            
        # If the User selects UCS
        if algorithm== 'UCS':
            print('You have selected UCS')

            # Time UCS Search
            start_time = time.time()
            result = ucs(self.map.graph_dict, start_city, end_city)
            end_time = time.time()

            # Calculate Execution Time
            execution_time = end_time - start_time

            print(f'\nExecution Time: {execution_time}\nPath To Target: {result[0]}\nDistance Of Path: {result[1]} \
                \nVisted Nodes: {result[2]}\nTotal Distance: {result[3]}')
            
            self.result_label.setText(f'\nExecution Time: {execution_time}\nPath To Targer: {result[0]}\nDistance Of Path: {result[1]} \
                \nVisted Nodes: {result[2]}\nTotal Distance: {result[3]}')

def main():
    app = QApplication(sys.argv)
    window = SearchWindow()
    window.setWindowTitle("PROJECT 1")
    window.resize(800, 500)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

