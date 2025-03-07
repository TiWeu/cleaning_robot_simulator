#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>
#include <stdio.h>

#define BUFFER_SIZE 100

// Define a struct to hold the sensor values
typedef struct {
    int front;
    int left;
    int right;
    int collision;
} SensorValues;

// Function to initialize UART
void uart_init(unsigned int baud) {
    unsigned int ubrr = F_CPU/16/baud-1;
    UBRR0H = (unsigned char)(ubrr>>8);
    UBRR0L = (unsigned char)ubrr;
    UCSR0B = (1<<RXEN0) | (1<<TXEN0); // Enable receiver and transmitter
    UCSR0C = (1<<USBS0) | (3<<UCSZ00); // Set frame format: 8 data bits, 2 stop bits
}

// Function to receive data
unsigned char uart_receive(void) {
    while (!(UCSR0A & (1<<RXC0))); // Wait for data to be received
    return UDR0; // Get and return received data from buffer
}

// Function to transmit data
void uart_transmit(unsigned char data) {
    while (!(UCSR0A & (1<<UDRE0))); // Wait for empty transmit buffer
    UDR0 = data; // Put data into buffer, sends the data
}

// Function to transmit a string
void uart_transmit_string(const char* str) {
    while (*str) {
        uart_transmit(*str++);
    }
}

// Function to parse the received string and update the sensor values
void parse_sensor_values(const char* str, SensorValues* values) {
    sscanf(str, "F:%d,L:%d,R:%d,C:%d", &values->front, &values->left, &values->right, &values->collision);
}

int main(void) {
    uart_init(9600); // Initialize UART with 9600 baud rate
    char buffer[BUFFER_SIZE]; // Buffer to store received string
    unsigned char received_char;
    int index = 0;
    SensorValues sensor_values = {0, 0, 0, 0}; // Initialize sensor values

    while (1) {
        // Step 1: Receive characters until newline is received or buffer is full
        while (1) {
            received_char = uart_receive();
            if (received_char == '\n' || index >= BUFFER_SIZE - 1) {
                buffer[index] = '\0'; // Null-terminate the string
                break;
            }
            buffer[index++] = received_char;
        }

        // Step 2: Parse the received string and update the sensor values
        parse_sensor_values(buffer, &sensor_values);

        // Step 3: Send acknowledgment
        uart_transmit_string("ACK\n");

        // Step 4: Reset index for next string
        index = 0;
    }

    return 0;
}