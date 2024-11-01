import random

ROAD_WEIGHTS = {
    "highway": 1.0,
    "paved": 1.2,
    "gravel": 1.5,
    "dirt": 2.0
}

class Node:
    def __init__(self, x, y, road_type="paved"):
        self.x = x
        self.y = y
        self.h = 0
        self.parent = None
        self.neighbors = []
        self.road_type = road_type

    def add_neighbor(self, neighbor, cost=1):
        self.neighbors.append((neighbor, cost))

    def reset(self):
        self.h = 0
        self.parent = None

def weighted_manhattan_heuristic(node, goal):
    road_type_weight = ROAD_WEIGHTS.get(node.road_type, 1.0)
    base_distance = abs(node.x - goal.x) + abs(node.y - goal.y)
    return base_distance * road_type_weight

def hill_climb(start, goal, heuristic_func=weighted_manhattan_heuristic):
    current = start
    current.h = heuristic_func(current, goal)

    while current != goal:
        # Get all neighbors with their heuristic values
        neighbors = [(neighbor, heuristic_func(neighbor, goal)) for neighbor, cost in current.neighbors]
        neighbors.sort(key=lambda x: x[1])  # Sort neighbors by heuristic value (ascending)

        # Randomly choose from the best neighbors (within the top 3 or fewer)
        best_neighbors = neighbors[:min(3, len(neighbors))]
        best_neighbor, best_h = random.choice(best_neighbors)

        # If no progress can be made, return None
        if best_h >= current.h:
            return None

        best_neighbor.parent = current
        current = best_neighbor
        current.h = best_h

    return reconstruct_path(current)

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y, node.road_type))
        node = node.parent
    return path[::-1]
