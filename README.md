# COSC411 - Artificial Intelligence Projects
## Salisbury University

This repository contains projects developed for COSC411 (Artificial Intelligence) at Salisbury University. These projects demonstrate various AI algorithms and problem-solving techniques.

## Projects

### 1. Fifteen Puzzle Solver (A* Search)
A sophisticated implementation of the classic 15-puzzle game with an AI solver using the A* search algorithm. The solver employs multiple heuristic techniques to find optimal solutions efficiently:

<img src="https://github.com/user-attachments/assets/df1e23a9-798b-4db8-b1ce-f737545df8e9" width="450"/>



- **Advanced Heuristics**:
  - Manhattan Distance
  - Linear Conflicts Detection
  - Pattern Database
  - Combined Weighted Heuristics

**Key Features:**
- Interactive GUI built with PyQt5
- Automatic puzzle solver using A* search
- Multiple heuristic functions for optimal pathfinding
- Solution animation and step tracking
- Performance optimizations for faster solving



### 2. Graph Path Search
An implementation of various graph search algorithms to find optimal paths between cities in the United States. The project visualizes and compares different search strategies.

Example:
<img width="840" alt="Screenshot 2025-04-15 at 9 29 56 PM" src="https://github.com/user-attachments/assets/8b53947d-d56c-4293-b592-d8371abcbfee" />

**Features:**
- Multiple search algorithms:
  - Depth-First Search (DFS)
  - Breadth-First Search (BFS)
  - A* Search
- Real distance calculations between cities
- Path visualization
- Performance metrics:
  - Execution time
  - Path length
  - Visited nodes

Example output from DFS search (Buffalo to Richmond):
```
Execution Time: 0.00037932395935058594
Path To Target: ['Buffalo', 'Pittsburgh', 'NewYork', 'Philadelphia', 'Salisbury', 'Norfolk', 'Richmond']
Distance Of Path: 1046
Visted Nodes: ['Buffalo', 'Pittsburgh', 'NewYork', 'Philadelphia', 'Salisbury', 'Norfolk', 'Richmond']
Total Distance: 1046
```

![Graph Path Search Example](Insert path to your graph image here)

## Technologies Used
- Python 3.x
- PyQt5
- NumPy
- Heapq (Priority Queue implementation)

## Course Information
- **Course**: COSC411 - Artificial Intelligence
- **Institution**: Salisbury University
- **Semester**: Spring 2024

## Author
Connor Sullivan

## Acknowledgments
Special thanks to the course instructor and teaching assistants for their guidance throughout these projects. 
