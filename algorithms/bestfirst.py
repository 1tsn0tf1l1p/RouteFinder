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
        self.h = float('inf')
        self.parent = None
        self.neighbors = []
        self.road_type = road_type

    def add_neighbor(self, neighbor, cost=1):
        self.neighbors.append((neighbor, cost))

    def reset(self):
        self.h = float('inf')
        self.parent = None

    def __lt__(self, other):
        return self.h < other.h

def weighted_manhattan_heuristic(node, goal):
    road_type_weight = ROAD_WEIGHTS.get(node.road_type, 1.0)
    base_distance = abs(node.x - goal.x) + abs(node.y - goal.y)
    return base_distance * road_type_weight

def best_first_search(start, goal, heuristic_func=weighted_manhattan_heuristic):
    open_set = []
    visited = set()
    start.h = heuristic_func(start, goal)
    heapq.heappush(open_set, (start.h, start))

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(current)

        visited.add(current)

        for neighbor, cost in current.neighbors:
            if neighbor in visited:
                continue

            neighbor_h = heuristic_func(neighbor, goal)

            if neighbor.parent is None or neighbor_h < neighbor.h:
                neighbor.h = neighbor_h
                neighbor.parent = current
                heapq.heappush(open_set, (neighbor_h, neighbor))

    return None

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y, node.road_type))
        node = node.parent
    return path[::-1]