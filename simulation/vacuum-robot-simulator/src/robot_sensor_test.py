from robot import Robot

def test_robot_sensors():
    # Define a sample grid
    grid = [
        ['U', 'U', 'U', 'U', 'U'],
        ['U', 'O', 'U', 'O', 'U'],
        ['U', 'U', 'R', 'U', 'U'],
        ['U', 'O', 'U', 'O', 'U'],
        ['U', 'U', 'U', 'U', 'U']
    ]

    # Initialize the robot at position (2, 2) facing North
    robot = Robot(initial_position=(2, 2), initial_direction='N', grid=grid)

    # Simulate sensors and print the results
    sensors = robot.simulate_sensors()
    print(f"Robot position: {robot.position}, direction: {robot.direction}")
    print(f"Sensors: {sensors}")

    # Change direction and position to test different scenarios
    robot.turn_right()
    robot.move_forward()
    sensors = robot.simulate_sensors()
    print(f"Robot position: {robot.position}, direction: {robot.direction}")
    print(f"Sensors: {sensors}")

    robot.turn_right()
    robot.move_forward()
    sensors = robot.simulate_sensors()
    print(f"Robot position: {robot.position}, direction: {robot.direction}")
    print(f"Sensors: {sensors}")

if __name__ == "__main__":
    test_robot_sensors()