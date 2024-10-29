import heapq

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
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.neighbors = []
        self.road_type = road_type

    def add_neighbor(self, neighbor, cost=1):
        self.neighbors.append((neighbor, cost))

    def __lt__(self, other):
        return self.f < other.f

    def reset(self):
        """Reset node attributes to initial values for reuse in multiple A* runs."""
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None

def weighted_manhattan_heuristic(node, goal):
    road_type_weight = ROAD_WEIGHTS.get(node.road_type, 1.0)
    base_distance = abs(node.x - goal.x) + abs(node.y - goal.y)
    return base_distance * road_type_weight

def astar(start, goal, heuristic_func=weighted_manhattan_heuristic):
    open_set = []
    heapq.heappush(open_set, (0, start))
    start.g = 0
    start.f = heuristic_func(start, goal)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(current)

        for neighbor, cost in current.neighbors:
            tentative_g = current.g + cost * ROAD_WEIGHTS.get(neighbor.road_type, 1.0)

            if tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.h = heuristic_func(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current

                heapq.heappush(open_set, (neighbor.f, neighbor))

    return None

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y, node.road_type))
        node = node.parent
    return path[::-1]
