import heapq  # This module provides a priority queue implementation (called "heap").
              # It allows us to always get the item with the lowest cost efficiently.

# We define a class to bundle all the pathfinding logic together.
class AStarPathFinding:
    def __init__(self, maze, start_pos, target_pos):
        # This function is called automatically when a new object is created.
        # It initializes (sets up) the maze, start, and target positions.

        self.maze = maze  # The 2D grid where 1 = walkable, 0 = wall
        self.start_pos = start_pos  # A tuple (row, column) where the path starts
        self.target_pos = target_pos  # A tuple (row, column) where the path ends

        self.open_list = []  # A list of positions to explore, stored as a priority queue
        self.closed_list = []  # A list of already explored positions
        self.came_from = {}  # A dictionary to reconstruct the path later. 
                             # It maps each cell to the previous cell that led to it.

    def heuristic(self, a, b):
        # This function estimates the remaining distance from point `a` to point `b`.
        # It uses Manhattan distance, which is good for grid-based maps
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos):
        # This function returns all walkable neighboring cells of a given cell (pos).

        neighbors = []  # A list to store valid neighboring positions

        # These are the four directions we can move in a grid (up, down, left, right)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Check each direction
        for d in directions:
            # Add the direction to the current position to get a new position
            neighbor = (pos[0] + d[0], pos[1] + d[1])

            # Check if the new position is valid (not outside the maze or a wall)
            if self.is_valid(neighbor):
                neighbors.append(neighbor)  # If valid, add to the list

        return neighbors  # Return the list of walkable neighbors

    def is_valid(self, pos):
        # This function checks if a position is within the maze boundaries
        # and not a wall (value must be 1)

        row, col = pos  # Split the position into row and column

        # Check if row and column are inside the maze, and the cell is walkable
        return (0 <= row < len(self.maze) and 
                0 <= col < len(self.maze[0]) and 
                self.maze[row][col] == 1)

    def find_path(self):
        # This function runs the A* algorithm to find the shortest path.

        # Start by adding the start position to the open list with a priority of 0
        heapq.heappush(self.open_list, (0, self.start_pos))

        # g_score stores the cost to reach each node from the start
        g_score = {self.start_pos: 0}

        # f_score = g_score + estimated cost to goal (heuristic)
        f_score = {self.start_pos: self.heuristic(self.start_pos, self.target_pos)}

        # Keep looping while there are positions left to explore
        while self.open_list:
            # Get the position with the lowest f_score from the open list
            _, current = heapq.heappop(self.open_list)

            # If we reached the goal, stop and reconstruct the path
            if current == self.target_pos:
                return self.reconstruct_path(current)

            # Add the current position to the closed list (we're done with it)
            self.closed_list.append(current)

            # Loop through each walkable neighbor of the current cell
            for neighbor in self.get_neighbors(current):
                # Skip this neighbor if we already evaluated it
                if neighbor in self.closed_list:
                    continue

                # Tentative cost from start to this neighbor
                tentative_g_score = g_score[current] + 1  # All moves cost 1 in this maze

                # If the neighbor is not in g_score or we found a better path to it
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Update the best known path to this neighbor
                    self.came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score

                    # Update the estimated total cost to the goal
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.target_pos)

                    # Add neighbor to the open list for future exploration
                    heapq.heappush(self.open_list, (f_score[neighbor], neighbor))

        # If we exit the loop, no path was found
        return None

    def reconstruct_path(self, current):
        # This function builds the path by going backward from the target
        # using the came_from dictionary

        path = [current]  # Start with the target cell

        # Go backwards from current to start using came_from
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)

        path.reverse()  # The path is from target to start, so we reverse it
        return path

# This block runs only if the script is executed directly (not when imported as a module)
if __name__ == "__main__":

    # Define the maze grid using a 2D list.
    # 1 = walkable space, 0 = wall
    maze = [
        [1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 0, 1]
    ]

    # Set the starting point (top-left corner)
    start_pos = (0, 4)

    # Set the target point (bottom-right corner)
    target_pos = (2, 4)

    # Create an instance of the pathfinding class
    path_finder = AStarPathFinding(maze, start_pos, target_pos)
    print(f"start position: {start_pos}")
    print(f"target position: {target_pos}")

    # Run the pathfinding algorithm
    path = path_finder.find_path()

    # Print the result
    if path:
        print("Path found: ", path)
    else:
        print("No path found")
