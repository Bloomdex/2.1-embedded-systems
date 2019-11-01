#include <avr/io.h>
#include <string.h>
#include "UART.h"
#include "serial.h"

// Queue for received data.
volatile unsigned char received_data[RECEIVED_DATA_SIZE];
volatile uint8_t received_data_index = 0;

// Buffer for measured temperatures.
int8_t temperatures[TEMPERATURE_STORAGE_SIZE];
uint8_t temperature_head_index = 0;

// Buffer for measured light intensity.
int8_t lights[LIGHT_STORAGE_SIZE];
uint8_t lights_head_index = 0;

//Adds the given temperature value to the temperature buffer.
void addTemperatureToBuffer(int8_t value) {
    temperatures[temperature_head_index] = value;
    temperature_head_index = (temperature_head_index + 1) % TEMPERATURE_STORAGE_SIZE;
}

//Adds the given light value to the light buffer.
void addLightToBuffer(int8_t value) {
    lights[lights_head_index] = value;
    lights_head_index = (lights_head_index + 1) % LIGHT_STORAGE_SIZE;
}

// Transmits data that has been collected in the buffer. (this will not reset the buffer)
void transmitBufferData(char buffercode, int8_t storagebuffer[], unsigned char storageSize, int8_t bufferIndex) {
    transmitData(buffercode);

    for (uint8_t i = 0; i < storageSize; i++) {
        uint8_t index = (i + bufferIndex) % storageSize;
        
        if(storagebuffer[index] != 0x00)
            transmitData(storagebuffer[index]);
    }

    transmitData(0x00);
    transmitData(buffercode);
    transmitData(0x00);
}

// Handles possible instruction in the received_data queue.
void handleInstructions(void) {
    //Loops over every data point in received_data
    for(uint8_t i = 0; i < RECEIVED_DATA_SIZE; i++) {
        uint8_t index = (i + received_data_index) % RECEIVED_DATA_SIZE;

        // Checks if the current data in received_data is an instruction.
        switch(received_data[index]) {
            case TEMPERATURE_CODE:            
                transmitBufferData(TEMPERATURE_CODE, temperatures, TEMPERATURE_STORAGE_SIZE, temperature_head_index);
                memset(temperatures, 0, TEMPERATURE_STORAGE_SIZE);
                temperature_head_index = 0;
                break;
            case LIGHT_CODE:
                transmitBufferData(LIGHT_CODE, lights, LIGHT_STORAGE_SIZE, lights_head_index);
                memset(lights, 0, LIGHT_STORAGE_SIZE);
                lights_head_index = 0;
                break;
        }

        // Resets the index of the previous value to 0. 
        received_data[index] = 0;
    }

    // Resets the index of the queue back to the front of queue
    received_data_index = 0;
}
