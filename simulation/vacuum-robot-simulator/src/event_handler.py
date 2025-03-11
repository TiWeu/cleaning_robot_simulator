import pygame
import time
from serial_utils import SerialCommunication

def handle_events(current_mode, robot_position, robot_direction, map_data, CELL_SIZE, GRID_SIZE, serial_comm, start_time, WIDTH, HEIGHT):
    """
    Handles Pygame events.

    Args:
        current_mode (str): The current mode of the robot.
        robot_position (tuple): The current position of the robot.
        robot_direction (str): The current direction of the robot.
        map_data (list of list of str): The grid data.
        CELL_SIZE (int): The size of each cell in the grid.
        GRID_SIZE (int): The size of the grid.
        serial_comm (SerialCommunication): The serial communication instance.
        start_time (float): The start time in seconds.
        WIDTH (int): The width of the screen.
        HEIGHT (int): The height of the screen.

    Returns:
        tuple: Updated current_mode, robot_position, robot_direction, serial_comm, start_time.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return None, None, None, None, None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
            if grid_y < GRID_SIZE:  # Ensure click is within grid area
                if current_mode == 'R':
                    if robot_position:
                        map_data[robot_position[1]][robot_position[0]] = 'U'  # Reset old robot position
                    robot_position = (grid_x, grid_y)
                    map_data[grid_y][grid_x] = 'R'  # Set cell to robot position
                else:
                    map_data[grid_y][grid_x] = current_mode  # Set cell to current mode
            else:
                # Check if the start button is pressed
                button_rect = pygame.Rect(WIDTH - 110, HEIGHT - 50, 100, 40)
                if button_rect.collidepoint(event.pos) and not serial_comm:
                    # Initialize serial communication
                    serial_comm = SerialCommunication(port='COM3', baudrate=9600)
                    time.sleep(2)  # Wait for the serial connection to be established
                    start_time = time.time()  # Record the start time
                    print("Serial communication initialized.")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                current_mode = 'U'
            elif event.key == pygame.K_v:
                current_mode = 'V'
            elif event.key == pygame.K_o:
                current_mode = 'O'
            elif event.key == pygame.K_i:
                current_mode = 'I'
            elif event.key == pygame.K_r:
                current_mode = 'R'
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if robot_position:
                    robot_direction = 'W'
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if robot_position:
                    robot_direction = 'E'
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if robot_position:
                    robot_direction = 'N'
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if robot_position:
                    robot_direction = 'S'
    return current_mode, robot_position, robot_direction, serial_comm, start_time