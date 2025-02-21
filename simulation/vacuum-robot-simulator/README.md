# Vacuum Robot Simulator

## Overview
The Vacuum Robot Simulator is a graphical application that simulates the behavior of a vacuum robot navigating through a grid representation of a room. The project focuses on providing an interactive GUI that allows users to visualize the robot's movements and the layout of the room.

## Project Structure
```
vacuum-robot-simulator
├── src
│   ├── main.py          # Entry point of the application
│   ├── gui.py           # GUI implementation for the simulator
│   └── utils
│       └── __init__.py  # Placeholder for utility functions
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd vacuum-robot-simulator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the simulator, execute the following command:
```
python src/main.py
```

This will launch the GUI, where you can interact with the vacuum robot simulation.

## Future Work
- Implement serial communication for sensor data.
- Enhance the grid management and obstacle handling in the utility functions.
- Add more features to the GUI for better user interaction.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.