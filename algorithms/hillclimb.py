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
    def backtrack(current, visited, depth=0):
        print(f"Visiting ({current.x}, {current.y}), h={heuristic_func(current, goal)}")

        if current == goal:
            print("Goal reached!")
            return [current]

        visited.add((current.x, current.y))

        neighbors = [(n, heuristic_func(n, goal)) for n, c in current.neighbors if (n.x, n.y) not in visited]
        neighbors.sort(key=lambda x: x[1])

        for neigh, hval in neighbors:
            print(f"-> Trying neighbor ({neigh.x}, {neigh.y}), h={hval}")
            neigh.parent = current
            result = backtrack(neigh, visited, depth + 1)
            if result is not None:
                return [current] + result

        print(f"No progress from ({current.x}, {current.y}), backtracking...")
        visited.remove((current.x, current.y))
        return None

    path_nodes = backtrack(start, set())
    if path_nodes is None:
        print("No path found after exploring all options.")
        return None

    return [(node.x, node.y, node.road_type) for node in path_nodes]


def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y, node.road_type))
        node = node.parent
    return path[::-1]
