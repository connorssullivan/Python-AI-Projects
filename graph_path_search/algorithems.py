from collections import deque
from queue import PriorityQueue

# BFS Algorithm with Distance Calculation
def bfs(graph, start_city, target_city=None):
    # Queue to hold city, distance (List of tuples)
    queue = deque([(start_city, 0, 0)])  # Start with the start_city and a distance of 0

    # Set to hold visited cities seen so fat
    seen = []
    seen.append(start_city)

    # Dict to track the path
    parent = {start_city: None}

    # Dict to track distances from the start_city
    distance_from_start = {start_city: 0}

    # Hold cities visted
    visted = []


    #Total distance visted
    total_distance = 0
    
    # BFS Loop
    while queue:
        # Get the current city and distance traveled from the queue
        current_city, current_distance, dist = queue.popleft()
        total_distance += dist
        visted.append(current_city)
        
        
        # Check if we found the target city
        if current_city == target_city:

            # Reconstruct the path from start city to target city
            path = []
            while current_city:
                path.append(current_city)
                current_city = parent[current_city]

            # Return the path in correct order and the total distance
            return path[::-1], current_distance, visted,total_distance
        
        # Explore all neighboring cities
        for neighbor, distance in graph[current_city].items():

            # If not a duplicate add it in
            if neighbor not in seen:
                # Add the neighbor to the queue with updated distance
                queue.append((neighbor, current_distance + distance, distance))
                seen.append(neighbor)
                parent[neighbor] = current_city

                # Update distance from start_city
                distance_from_start[neighbor] = current_distance + distance
    


# DFS Algorithm with Distance Calculation
def dfs(graph, start_city, target_city=None):
    # Stack to hold (city, distance traveled so far)
    stack = deque([(start_city, 0, 0)])  # Start with start_city and a distance of 0

    # Set to hold seen cities
    seen = []
    seen.append(start_city)

    # Dictionary to track the path
    parent = {start_city: None}

    # Dictionary to track distances from start_city
    distance_from_start = {start_city: 0}

    # Set to hold visted cities
    visted = []

    # Total Distance Traveled
    total_distance = 0

    # DFS Loop
    while stack:
        # Get the current city and distance traveled from the stack
        current_city, distance_traveled, dist= stack.pop()
        total_distance += dist
        visted.append(current_city)

        # If you found the desired city, return the path and distance
        if current_city == target_city:
            # Rebuild the path from start_city to target_city
            path = []
            while current_city:
                path.append(current_city)
                current_city = parent[current_city]
            
            # Return path and total distance
            return path[::-1], distance_traveled,visted,total_distance

        # Explore all neighboring cities
        for neighbor, distance in graph[current_city].items():
            if neighbor not in seen:
                # Add the neighbor to the stack with updated distance
                stack.append((neighbor, distance_traveled + distance, distance))
                seen.append(neighbor)
                parent[neighbor] = current_city

                # Update distance from start_city
                distance_from_start[neighbor] = distance_traveled + distance

    

def ucs(graph, start_city, end_city):
    # Define the Priority Queue
    pq = PriorityQueue()
    pq.put((0,start_city, []))

    # Disctionary to keep track of min cost
    min_cost = {start_city: 0}

    # Dict to track the parent of each city
    parent = {start_city: None}

    # Set to hold visted cities
    visted = []

    total_distance = 0

    # Main Loop
    while pq:
        # Get the city with the lowest cost from the priority
        curr_cost, curr_city, curr_path = pq.get()

        # Append visited city to the current path
        curr_path.append(curr_city)

        # Append the current city to visited
        visted.append(curr_city)

        # If you found the right city return the path and cost
        if curr_city == end_city:
            # Rebuild the path to get the desired path
            path = []
            while curr_city:
                path.append(curr_city)
                curr_city = parent[curr_city]
            return path[::-1], curr_cost, visted, total_distance
        
        #Update the current distance traveled
        total_distance += curr_cost
        
        #Explore the neighbors
        for neighbor, distance in graph[curr_city].items():
            new_cost = curr_cost + distance

            # If the neighbor hasn't been visited, or we found a cheaper path to it
            if neighbor not in min_cost or new_cost < min_cost[neighbor]:
                min_cost[neighbor] = new_cost  # Update the minimum cost to reach the neighbor

                # Set the current city as the parent of the neighbor
                parent[neighbor] = curr_city

                # Add neighbor to the queue with updated cost
                pq.put((new_cost, neighbor, curr_path))  
            
        
        


    



