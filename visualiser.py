import time
import pygame

# Import each algorithm and its respective Node class
from algorithms.astar import Node as AStarNode, astar
from algorithms.hillclimb import Node as HillClimbNode, hill_climb
from algorithms.bestfirst import Node as BestFirstSearchNode, best_first_search

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1400, 1400
ROWS, COLS = 100, 100
CELL_SIZE = WIDTH // COLS

ROAD_COLORS = {
    "highway": (200, 200, 255),
    "paved": (170, 170, 170),
    "gravel": (140, 100, 80),
    "dirt": (100, 70, 50)
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRUCK_COLORS = {
    "hill_climb": (255, 0, 0),  # Red for Hill Climb
    "best_first": (0, 255, 0),  # Green for Best-First Search
    "a_star": (0, 0, 255)       # Blue for A*
}

# Function to draw the grid
def draw_grid(screen, nodes):
    for row in nodes:
        for node in row:
            color = ROAD_COLORS[node.road_type]
            pygame.draw.rect(screen, color, (node.x * CELL_SIZE, node.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (node.x * CELL_SIZE, node.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Function to animate the path
def animate_path(screen, path, color):
    for x, y, road_type in path:
        pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        time.sleep(0.05)
    time.sleep(3)

def add_neighbors_to_grid(nodes):
    for y in range(ROWS):
        for x in range(COLS):
            current_node = nodes[y][x]
            if x > 0:  # Left neighbor
                current_node.add_neighbor(nodes[y][x - 1])
            if x < COLS - 1:  # Right neighbor
                current_node.add_neighbor(nodes[y][x + 1])
            if y > 0:  # Top neighbor
                current_node.add_neighbor(nodes[y - 1][x])
            if y < ROWS - 1:  # Bottom neighbor
                current_node.add_neighbor(nodes[y + 1][x])

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RouteFinder")
    clock = pygame.time.Clock()

    # Create grids for each algorithm
    hill_climb_nodes = [[HillClimbNode(x, y, road_type="paved") for x in range(COLS)] for y in range(ROWS)]
    best_first_search_nodes = [[BestFirstSearchNode(x, y, road_type="paved") for x in range(COLS)] for y in range(ROWS)]
    a_star_nodes = [[AStarNode(x, y, road_type="paved") for x in range(COLS)] for y in range(ROWS)]

    # Add neighbors to each grid
    add_neighbors_to_grid(hill_climb_nodes)
    add_neighbors_to_grid(best_first_search_nodes)
    add_neighbors_to_grid(a_star_nodes)

    # Example of setting some road types
    hill_climb_nodes[20][20].road_type = "highway"
    hill_climb_nodes[40][40].road_type = "dirt"
    hill_climb_nodes[60][60].road_type = "gravel"

    best_first_search_nodes[20][20].road_type = "highway"
    best_first_search_nodes[40][40].road_type = "dirt"
    best_first_search_nodes[60][60].road_type = "gravel"

    a_star_nodes[20][20].road_type = "highway"
    a_star_nodes[40][40].road_type = "dirt"
    a_star_nodes[60][60].road_type = "gravel"

    # Main loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(screen, hill_climb_nodes)  # Draw the grid for the first algorithm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Press 'S' to start the algorithms
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
