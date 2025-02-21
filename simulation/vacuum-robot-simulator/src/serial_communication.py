import serial

class SerialCommunication:
    def __init__(self, port, baudrate):
        """
        Initializes the serial communication.

        Args:
            port (str): The serial port to connect to.
            baudrate (int): The baud rate for the serial communication.
        """
        self.ser = serial.Serial(port, baudrate)
    
    def send_data(self, data):
        """
        Sends data over the serial connection.

        Args:
            data (str): The data to send.
        """
        self.ser.write(data.encode())
    
    def receive_data(self):
        """
        Receives data from the serial connection.

        Returns:
            str: The received data.
        """
        if self.ser.in_waiting:
            return self.ser.readline().decode().strip()
        return None
    
    def close(self):
        """
        Closes the serial connection.
        """
        self.ser.close()