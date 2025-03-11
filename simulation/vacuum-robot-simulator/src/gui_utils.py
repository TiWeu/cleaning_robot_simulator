import pygame
import time

def draw_grid(screen, map_data, robot_image, robot_direction, CELL_SIZE, GRID_SIZE):
    """
    Draws the grid based on the map data.

    Args:
        screen (pygame.Surface): The Pygame screen to draw on.
        map_data (list of list of str): The grid data where each cell can be 'U', 'V', 'O', 'I', or 'R'.
        robot_image (pygame.Surface): The image of the robot.
        robot_direction (str): The direction the robot is facing ('N', 'E', 'S', 'W').
        CELL_SIZE (int): The size of each cell in the grid.
        GRID_SIZE (int): The size of the grid.
    """
    screen.fill((255, 255, 255))
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if map_data[y][x] == 'U':
                color = (200, 200, 200)  # Unvisited
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif map_data[y][x] == 'V':
                color = (0, 255, 0)  # Visited
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif map_data[y][x] == 'O':
                color = (255, 0, 0)  # Obstacle Unidentified
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif map_data[y][x] == 'I':
                color = (0, 0, 255)  # Obstacle Identified
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif map_data[y][x] == 'R':
                # Draw the robot image with the correct rotation
                if robot_direction == 'N':
                    rotated_image = pygame.transform.rotate(robot_image, 0)
                elif robot_direction == 'E':
                    rotated_image = pygame.transform.rotate(robot_image, -90)
                elif robot_direction == 'S':
                    rotated_image = pygame.transform.rotate(robot_image, 180)
                elif robot_direction == 'W':
                    rotated_image = pygame.transform.rotate(robot_image, 90)
                screen.blit(rotated_image, (x * CELL_SIZE, y * CELL_SIZE))

def draw_legend(screen, GRID_SIZE, CELL_SIZE):
    """
    Draws the legend explaining the colors and their meanings.

    Args:
        screen (pygame.Surface): The Pygame screen to draw on.
        GRID_SIZE (int): The size of the grid.
        CELL_SIZE (int): The size of each cell in the grid.
    """
    font = pygame.font.SysFont(None, 24)
    legend_items = [
        ("Unvisited (U)", (200, 200, 200)),
        ("Visited (V)", (0, 255, 0)),
        ("Obstacle Unidentified (O)", (255, 0, 0)),
        ("Obstacle Identified (I)", (0, 0, 255)),
        ("Robot (R)", (255, 255, 0))
    ]
    y_offset = GRID_SIZE * CELL_SIZE + 10
    for text, color in legend_items:
        pygame.draw.rect(screen, color, (10, y_offset, 20, 20))
        img = font.render(text, True, (0, 0, 0))
        screen.blit(img, (40, y_offset))
        y_offset += 30

def draw_start_button(screen, WIDTH, HEIGHT):
    """
    Draws the start button.

    Args:
        screen (pygame.Surface): The Pygame screen to draw on.
        WIDTH (int): The width of the screen.
        HEIGHT (int): The height of the screen.
    """
    font = pygame.font.SysFont(None, 36)
    button_text = font.render("Start", True, (255, 255, 255))
    button_rect = pygame.Rect(WIDTH - 110, HEIGHT - 50, 100, 40)
    pygame.draw.rect(screen, (0, 128, 0), button_rect)
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 5))
    return button_rect

def draw_elapsed_time(screen, start_time, HEIGHT):
    """
    Draws the elapsed time since the start button was pressed.

    Args:
        screen (pygame.Surface): The Pygame screen to draw on.
        start_time (float): The start time in seconds.
        HEIGHT (int): The height of the screen.
    """
    if start_time is not None:
        elapsed_time = time.time() - start_time
        font = pygame.font.SysFont(None, 36)
        time_text = font.render(f"Time: {int(elapsed_time)}s", True, (0, 0, 0))
        screen.blit(time_text, (10, HEIGHT - 50))