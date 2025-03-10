import pygame
from robot import Robot
from robot_controller import RobotController
from serial_communication import SerialCommunication, send_sensor_data, wait_for_data  # Import necessary functions
import time

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 10
CELL_SIZE = 50
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + 160  # Extra space for the legend

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load robot image with transparency
robot_image = pygame.image.load('./simulation/vacuum-robot-simulator/src/img/cleaning-robot.png').convert_alpha()
robot_image = pygame.transform.scale(robot_image, (CELL_SIZE, CELL_SIZE))

# Set the background color of the robot image to (200, 200, 200)
background_color = (200, 200, 200)
robot_image.fill(background_color, special_flags=pygame.BLEND_RGBA_MIN)

# Global variables
current_mode = 'U'  # Start with 'Unvisited' mode
robot_position = None  # Track the current robot position
robot_direction = 'N'  # Track the current robot direction
map_data = [['U' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Initialize grid with 'U' for unvisited
serial_initialized = False  # Flag to track if serial communication is initialized

def draw_grid(map_data):
    """
    Draws the grid based on the map data.

    Args:
        map_data (list of list of str): The grid data where each cell can be 'U', 'V', 'O', 'I', or 'R'.
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

def draw_legend():
    """
    Draws the legend explaining the colors and their meanings.
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

def draw_start_button():
    """
    Draws the start button.
    """
    font = pygame.font.SysFont(None, 36)
    button_text = font.render("Start", True, (255, 255, 255))
    button_rect = pygame.Rect(WIDTH - 110, HEIGHT - 50, 100, 40)
    pygame.draw.rect(screen, (0, 128, 0), button_rect)
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 5))
    return button_rect

def test_robot_sensors_in_gui():
    """
    Test function to run the GUI and print sensor data based on the robot's position and obstacles.
    """
    global robot_position, robot_direction, map_data, screen, current_mode, serial_initialized
    clock = pygame.time.Clock()
    
    robot = Robot(initial_position=(0, 0), initial_direction='N', grid=map_data)
    controller = RobotController(robot)
    serial_comm = None  # Initialize serial communication variable
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if grid_y < GRID_SIZE:  # Ensure click is within grid area
                    if current_mode == 'R':
                        if robot_position:
                            map_data[robot_position[1]][robot_position[0]] = 'U'  # Reset old robot position
                        robot_position = (grid_x, grid_y)
                        robot.position = robot_position
                    map_data[grid_y][grid_x] = current_mode  # Set cell to current mode
                else:
                    # Check if the start button is pressed
                    button_rect = draw_start_button()
                    if button_rect.collidepoint(event.pos) and not serial_initialized:
                        # Initialize serial communication
                        serial_comm = SerialCommunication(port='COM3', baudrate=9600)
                        time.sleep(2)  # Wait for the serial connection to be established
                        serial_initialized = True
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
                        robot.direction = robot_direction
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if robot_position:
                        robot_direction = 'E'
                        robot.direction = robot_direction
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if robot_position:
                        robot_direction = 'N'
                        robot.direction = robot_direction
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if robot_position:
                        robot_direction = 'S'
                        robot.direction = robot_direction

        draw_grid(map_data)
        draw_legend()
        button_rect = draw_start_button()  # Draw the start button
        pygame.display.flip()
        
        if robot_position:
            sensors = controller.get_sensor_data()
            print(f"Robot position: {robot.position}, direction: {robot.direction}")
            print(f"Sensors: {sensors}")

            # Send sensor data
            if serial_comm:
                send_sensor_data(serial_comm, sensors)

                # Wait for motor movement command
                received_data = wait_for_data(serial_comm)
                if received_data:
                    command = received_data.decode('utf-8').strip()
                    print(f"Received command: {command}")
                    if command == '1':
                        # Update map_data to reflect the robot's movement
                        map_data[robot_position[1]][robot_position[0]] = 'V'  # Mark the old position as visited
                        robot.move_forward()
                        robot_position = robot.position
                        map_data[robot_position[1]][robot_position[0]] = 'R'  # Mark the new position as robot
                    elif command == '2':
                        robot.turn_left()
                    elif command == '3':
                        robot.turn_right()

                    # Update robot direction
                    robot_direction = robot.direction

                    # Redraw the grid to update the robot's position
                    draw_grid(map_data)
                    draw_legend()
                    pygame.display.flip()

        clock.tick(10)

if __name__ == "__main__":
    test_robot_sensors_in_gui()