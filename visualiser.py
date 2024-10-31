import time
import pygame
import random
from algorithms.astar import Node as AStarNode, astar
from algorithms.hillclimb import Node as HillClimbNode, hill_climb
from algorithms.bestfirst import Node as BestFirstSearchNode, best_first_search

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 100, 100
CELL_SIZE = WIDTH // COLS

ROAD_COLORS = {
    "highway": (200, 200, 255),
    "paved": (170, 170, 170),
    "gravel": (140, 100, 80),
    "dirt": (100, 70, 50)
}

ROAD_TYPES = ["highway", "paved", "gravel", "dirt"]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRUCK_COLORS = {
    "hill_climb": (255, 0, 0),
    "best_first": (0, 255, 0),
    "a_star": (0, 0, 255)
}

def create_random_road_map(NodeClass):
    nodes = [[NodeClass(x, y, road_type=random.choice(ROAD_TYPES)) for x in range(COLS)] for y in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLS):
            current_node = nodes[y][x]
            if x > 0:
                current_node.add_neighbor(nodes[y][x - 1])
            if x < COLS - 1:
                current_node.add_neighbor(nodes[y][x + 1])
            if y > 0:
                current_node.add_neighbor(nodes[y - 1][x])
            if y < ROWS - 1:
                current_node.add_neighbor(nodes[y + 1][x])
    return nodes

def draw_grid(screen, nodes):
    for row in nodes:
        for node in row:
            color = ROAD_COLORS[node.road_type]
            rect = (node.x * CELL_SIZE, node.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

def animate_path(screen, path, color):
    for x, y, road_type in path:
        rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)
        pygame.display.flip()
    time.sleep(3)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RouteFinder")
    clock = pygame.time.Clock()

    hill_climb_nodes = create_random_road_map(HillClimbNode)
    best_first_search_nodes = create_random_road_map(BestFirstSearchNode)
    a_star_nodes = create_random_road_map(AStarNode)

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(screen, hill_climb_nodes)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    print("Running Hill Climb Algorithm")
                    path = hill_climb(hill_climb_nodes[0][0], hill_climb_nodes[ROWS - 1][COLS - 1])
                    if path:
                        print(f"Hill Climb Path Length: {len(path)}")
                        animate_path(screen, path, TRUCK_COLORS["hill_climb"])
                    else:
                        print("Hill Climb: No path found.")

                    print("Running Best-First Search Algorithm")
                    path = best_first_search(best_first_search_nodes[0][0], best_first_search_nodes[ROWS - 1][COLS - 1])
                    if path:
                        print(f"Best First Search Path Length: {len(path)}")
                        animate_path(screen, path, TRUCK_COLORS["best_first"])
                    else:
                        print("Best-First Search: No path found.")

                    print("Running A* Algorithm")
                    path = astar(a_star_nodes[0][0], a_star_nodes[ROWS - 1][COLS - 1])
                    if path:
                        print(f"A* Path Length: {len(path)}")
                        animate_path(screen, path, TRUCK_COLORS["a_star"])
                    else:
                        print("A*: No path found.")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
