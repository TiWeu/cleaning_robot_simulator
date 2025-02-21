class RobotController:
    def __init__(self, robot):
        """
        Initializes the robot controller.

        Args:
            robot (Robot): The robot instance to control.
        """
        self.robot = robot

    def process_command(self, command):
        """
        Processes a command and moves the robot accordingly.

        Args:
            command (str): The command to process ('L' for left, 'R' for right, 'F' for forward).
        """
        self.robot.execute_command(command)

    def get_sensor_data(self):
        """
        Gets the sensor data from the robot.

        Returns:
            dict: The sensor data.
        """
        return self.robot.simulate_sensors()