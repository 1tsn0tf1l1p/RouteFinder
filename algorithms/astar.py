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
    visited = set()
    start.g = 0
    start.h = heuristic_func(start, goal)
    start.f = start.g + start.h
    heapq.heappush(open_set, (start.f, start))
    print(f"Starting A* from ({start.x}, {start.y}) to ({goal.x}, {goal.y})")

    while open_set:
        _, current = heapq.heappop(open_set)
        print(f"Processing node: ({current.x}, {current.y}), g={current.g}, h={current.h}, f={current.f}")

        if current == goal:
            print("Goal reached!")
            return reconstruct_path(current)

        visited.add(current)

        for neighbor, cost in current.neighbors:
            if neighbor in visited:
                continue

            tentative_g = current.g + cost * ROAD_WEIGHTS.get(neighbor.road_type, 1.0)

            if tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.h = heuristic_func(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current
                heapq.heappush(open_set, (neighbor.f, neighbor))
                print(f"Updated neighbor: ({neighbor.x}, {neighbor.y}), g={neighbor.g}, h={neighbor.h}, f={neighbor.f}")

    print("No path found.")
    return None

def reconstruct_path(node):
    path = []
    print("Reconstructing path:")
    while node:
        print(f"Node: ({node.x}, {node.y}), road_type={node.road_type}")
        path.append((node.x, node.y, node.road_type))
        node = node.parent
    return path[::-1]