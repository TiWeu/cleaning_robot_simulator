#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include <stdio.h>

#define BUFFER_SIZE 100
#define FORWARD 0x01
#define TURN_LEFT 0x02
#define TURN_RIGHT 0x03
#define STOP 0x04

// Define a struct to hold the sensor values
typedef struct {
    int front;
    int left;
    int right;
    int collision;
} SensorValues;

volatile char buffer[BUFFER_SIZE]; // Buffer to store received string
volatile int index = 0;
volatile int data_ready = 0; // Flag to indicate data is ready to be processed

volatile SensorValues sensor_values = {0, 0, 0, 0}; // Initialize sensor values

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

// Function to parse the received byte and update the sensor values
void parse_sensor_values_byte(unsigned char byte, SensorValues* values) {
    values->front = (byte >> 3) & 0x01;
    values->left = (byte >> 2) & 0x01;
    values->right = (byte >> 1) & 0x01;
    values->collision = byte & 0x01;
}

// Function to decide the robot's movement based on sensor values
uint8_t decide_movement(const SensorValues* values) {
    if (values->collision) {
        // Collision detected, stop the robot
        return STOP;
    }
    if (values->front) {
        // Front is blocked, turn randomly left or right
        if (rand() % 2 == 0) {
            return TURN_LEFT;
        } else {
            return TURN_RIGHT;
        }
    } else {
        // Front is free, move forward
        return FORWARD;
    }
}

// Timer interrupt service routine
ISR(TIMER1_COMPA_vect) {
    static enum {RECEIVE, PROCESS} state = RECEIVE;
    unsigned char received_byte;

    switch (state) {
        case RECEIVE:
            received_byte = uart_receive();
            buffer[index++] = received_byte;
            if (index >= 1) { // We only need one byte
                data_ready = 1; // Set flag to indicate data is ready to be processed
                index = 0; // Reset index for next byte
                state = PROCESS; // Move to the next state
            }
            break;

        case PROCESS:
            if (data_ready) {
                // Step 2: Parse the received byte and update the sensor values
                parse_sensor_values_byte(buffer[0], &sensor_values);

                // Step 3: Decide the movement and send the instruction
                uint8_t movement = decide_movement(&sensor_values);

                // Create a buffer to hold the movement and sensor values
                char output_buffer[BUFFER_SIZE];
                snprintf(output_buffer, BUFFER_SIZE, "%d", movement);

                // Send the combined movement and sensor values
                uart_transmit_string(output_buffer);

                // Reset data_ready flag
                data_ready = 0;
                state = RECEIVE; // Move back to the receive state
            }
            break;
    }
}

// Function to initialize Timer1
void timer1_init(void) {
    TCCR1B |= (1 << WGM12); // Configure timer 1 for CTC mode
    TIMSK1 |= (1 << OCIE1A); // Enable CTC interrupt
    OCR1A = 15624; // Set CTC compare value for 1Hz at 16MHz AVR clock, with a prescaler of 1024
    TCCR1B |= (1 << CS12) | (1 << CS10); // Start timer at Fcpu/1024
}

int main(void) {
    uart_init(9600); // Initialize UART with 9600 baud rate
    timer1_init(); // Initialize Timer1
    sei(); // Enable global interrupts

    while (1) {
        // Main loop can be empty as everything is handled in the ISR
    }

    return 0;
}