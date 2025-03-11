import pygame
from robot import Robot
from robot_controller import RobotController
from serial_utils import SerialCommunication, send_sensor_data, wait_for_data  # Import necessary functions
from gui_utils import draw_grid, draw_legend, draw_start_button, draw_elapsed_time
from event_handler import handle_events
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
start_time = None  # Variable to track the start time

def test_robot_sensors_in_gui():
    """
    Test function to run the GUI and print sensor data based on the robot's position and obstacles.
    """
    global robot_position, robot_direction, map_data, screen, current_mode, serial_initialized, start_time
    clock = pygame.time.Clock()
    
    robot = Robot(initial_position=(0, 0), initial_direction='N', grid=map_data)
    controller = RobotController(robot)
    serial_comm = None  # Initialize serial communication variable
    
    while True:
        current_mode, robot_position, robot_direction, serial_comm, start_time = handle_events(current_mode, robot_position, robot_direction, map_data, CELL_SIZE, GRID_SIZE, serial_comm, start_time, WIDTH, HEIGHT)
        if current_mode is None:
            return

        # Update robot position in the robot object
        if robot_position:
            robot.position = robot_position
            robot.direction = robot_direction

        draw_grid(screen, map_data, robot_image, robot_direction, CELL_SIZE, GRID_SIZE)
        draw_legend(screen, GRID_SIZE, CELL_SIZE)
        button_rect = draw_start_button(screen, WIDTH, HEIGHT)  # Draw the start button
        draw_elapsed_time(screen, start_time, HEIGHT)  # Draw the elapsed time
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
                    draw_grid(screen, map_data, robot_image, robot_direction, CELL_SIZE, GRID_SIZE)
                    draw_legend(screen, GRID_SIZE, CELL_SIZE)
                    draw_elapsed_time(screen, start_time, HEIGHT)  # Draw the elapsed time
                    pygame.display.flip()

        clock.tick(30)

if __name__ == "__main__":
    test_robot_sensors_in_gui()