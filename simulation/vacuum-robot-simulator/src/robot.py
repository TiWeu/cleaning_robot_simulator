class Robot:
    def __init__(self, initial_position, initial_direction, grid):
        """
        Initializes the robot.

        Args:
            initial_position (tuple): The initial position of the robot (x, y).
            initial_direction (str): The initial direction of the robot ('N', 'E', 'S', 'W').
            grid (list of list of str): The grid representing the room.
        """
        self.position = initial_position
        self.direction = initial_direction
        self.grid = grid

    def turn_left(self):
        """Turns the robot 90 degrees to the left."""
        directions = ['N', 'W', 'S', 'E']
        self.direction = directions[(directions.index(self.direction) + 1) % 4]

    def turn_right(self):
        """Turns the robot 90 degrees to the right."""
        directions = ['N', 'E', 'S', 'W']
        self.direction = directions[(directions.index(self.direction) + 1) % 4]

    def move_forward(self):
        """Moves the robot one step forward in the current direction."""
        x, y = self.position
        if self.direction == 'N':
            y -= 1
        elif self.direction == 'E':
            x += 1
        elif self.direction == 'S':
            y += 1
        elif self.direction == 'W':
            x -= 1

        # Check if the new position is within the grid and not an obstacle
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid) and self.grid[y][x] != 'O':
            self.position = (x, y)

    def execute_command(self, command):
        """
        Executes a movement command.

        Args:
            command (str): The command to execute ('L' for left, 'R' for right, 'F' for forward).
        """
        if command == 'L':
            self.turn_left()
        elif command == 'R':
            self.turn_right()
        elif command == 'F':
            self.move_forward()

    def simulate_sensors(self):
        """
        Simulates the robot's sensors to check for obstacles.

        Returns:
            dict: A dictionary with sensor readings for 'front', 'left', and 'right'.
        """
        x, y = self.position
        sensors = {'front': False, 'left': False, 'right': False}

        if self.direction == 'N':
            sensors['front'] = y <= 0 or self.grid[y - 1][x] == 'O' or self.grid[y - 1][x] == 'I'
            sensors['left'] = x <= 0 or (y > 0 and (self.grid[y - 1][x - 1] == 'O' or self.grid[y - 1][x - 1] == 'I'))
            sensors['right'] = x >= len(self.grid[0]) - 1 or (y > 0 and (self.grid[y - 1][x + 1] == 'O' or self.grid[y - 1][x + 1] == 'I'))
        elif self.direction == 'E':
            sensors['front'] = x >= len(self.grid[0]) - 1 or self.grid[y][x + 1] == 'O' or self.grid[y][x + 1] == 'I'
            sensors['left'] = y >= len(self.grid) - 1 or (x < len(self.grid[0]) - 1 and (self.grid[y - 1][x + 1] == 'O' or self.grid[y - 1][x + 1] == 'I'))
            sensors['right'] = y <= 0 or (x < len(self.grid[0]) - 1 and (self.grid[y + 1][x + 1] == 'O' or self.grid[y + 1][x + 1] == 'I'))
        elif self.direction == 'S':
            sensors['front'] = y >= len(self.grid) - 1 or self.grid[y + 1][x] == 'O' or self.grid[y + 1][x] == 'I'
            sensors['left'] = x >= len(self.grid[0]) - 1 or (y < len(self.grid) - 1 and (self.grid[y + 1][x + 1] == 'O' or self.grid[y + 1][x + 1] == 'I'))
            sensors['right'] = x <= 0 or (y < len(self.grid) - 1 and (self.grid[y + 1][x - 1] == 'O' or self.grid[y + 1][x - 1] == 'I'))
        elif self.direction == 'W':
            sensors['front'] = x <= 0 or self.grid[y][x - 1] == 'O' or self.grid[y][x - 1] == 'I'
            sensors['left'] = y >= len(self.grid) - 1 or (x > 0 and (self.grid[y + 1][x - 1] == 'O' or self.grid[y + 1][x - 1] == 'I'))
            sensors['right'] = y <= 0 or (x > 0 and (self.grid[y - 1][x - 1] == 'O' or self.grid[y - 1][x - 1] == 'I'))

        #return sensors
        front = 1 if sensors['front'] else 0
        left = 1 if sensors['left'] else 0
        right = 1 if sensors['right'] else 0
        collision = 0  # Placeholder for collision sensor
        # Combine the bits into a single byte
        data_byte = (front << 3) | (left << 2) | (right << 1) | collision
        return bytes([data_byte])