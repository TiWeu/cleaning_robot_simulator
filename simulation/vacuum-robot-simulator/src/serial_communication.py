import serial
import time

class SerialCommunication:
    def __init__(self, port, baudrate, timeout=1):
        """
        Initializes the serial communication.

        Args:
            port (str): The serial port to connect to.
            baudrate (int): The baud rate for the serial communication.
            timeout (int): The timeout for the serial communication in seconds.
        """
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.flushInput()
        self.ser.flushOutput()
    
    def send_data(self, data):
        """
        Sends data over the serial connection.

        Args:
            data (bytes): The data to send.
        """
        if self.ser.is_open:
            self.ser.write(data)
        else:
            print("Serial port is not open. Cannot send data.")
    
    def receive_data(self):
        """
        Receives data from the serial connection.

        Returns:
            bytes: The received data.
        """
        if self.ser.is_open and self.ser.in_waiting:
            return self.ser.read(self.ser.in_waiting)
        return None
    
    def close(self):
        """
        Closes the serial connection.
        """
        self.ser.close()

def format_sensor_data_as_bits(sensors):
    """
    Formats the sensor data into a byte format.

    Args:
        sensors (dict): The sensor data.

    Returns:
        bytes: The formatted sensor data as bytes.
    """
    front = 1 if sensors['front'] else 0
    left = 1 if sensors['left'] else 0
    right = 1 if sensors['right'] else 0
    collision = 1 if sensors['collision'] else 0
    # Combine the bits into a single byte
    data_byte = (front << 4) | (left << 3) | (right << 2) | (collision << 1) | 1
    return bytes([data_byte])

def send_sensor_data(serial_comm, sensors):
    """
    Sends the sensor data over the serial connection.

    Args:
        serial_comm (SerialCommunication): The serial communication instance.
        sensors (dict): The sensor data.
    """
    # formatted_data = format_sensor_data_as_bits(sensors)
    formatted_data = sensors
    serial_comm.send_data(formatted_data)
    print(f"Sent data: {formatted_data}")

def wait_for_data(serial_comm):
    """
    Waits for data to be received over the serial connection.

    Args:
        serial_comm (SerialCommunication): The serial communication instance.

    Returns:
        bytes: The received data.
    """
    print("Waiting for data...")
    counter = 0
    while True:
        received_data = serial_comm.receive_data()
        if received_data:
            print(f"Received data: {received_data}")
            return received_data
        time.sleep(0.8)  # Sleep for a short period to avoid busy-waiting
        counter += 1
        if counter >= 10:
            print("No data received.")
            return None

def main():
    sensors = {
        "front": True,
        "left": False,
        "right": True,
        "collision": False
    }

    # Initialize serial communication
    serial_comm = SerialCommunication(port='COM3', baudrate=9600)
    time.sleep(2)  # Wait for the serial connection to be established

    try:
        while True:
            # Check if the serial connection is open
            if not serial_comm.ser.is_open:
                print("Serial connection lost. Attempting to reconnect...")
                serial_comm.ser.open()
                if serial_comm.ser.is_open:
                    print("Reconnected to serial port.")
                else:
                    print("Failed to reconnect to serial port.")
                    break

            # Send sensor data
            send_sensor_data(serial_comm, sensors)

            # Wait for data to be received
            received_data = wait_for_data(serial_comm)

            # If no data was received, send the same sensor data again
            if received_data is None:
                print("Resending the same sensor data...")
                send_sensor_data(serial_comm, sensors)
            else:
                # Simulate sensor data changes
                sensors["front"] = not sensors["front"]
                sensors["left"] = not sensors["left"]
                sensors["right"] = not sensors["right"]
                sensors["collision"] = not sensors["collision"]

            print("Loop iteration complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the serial connection
        serial_comm.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    main()