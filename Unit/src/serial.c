#include <avr/io.h>
#include <string.h>
#include "UART.h"
#include "serial.h"

int8_t temperatures[TEMPERATURE_STORAGE_SIZE];
int8_t temperature_head_index = 0;

int8_t lights[LIGHT_STORAGE_SIZE];
int8_t lights_head_index = 0;

void addTemperatureToBuffer(int8_t value) {
    temperatures[temperature_head_index] = value;
    temperature_head_index = (temperature_head_index + 1) % TEMPERATURE_STORAGE_SIZE;
}

void addLightToBuffer(int8_t value) {
    lights[lights_head_index] = value;
    lights_head_index = (lights_head_index + 1) % LIGHT_STORAGE_SIZE;
}

void transmitBufferData(char buffercode, int8_t storagebuffer[], unsigned char storageSize, int8_t bufferIndex) {
    transmitData(buffercode);

    for (int i = 0; i < storageSize; i++) {
        int index = (i + bufferIndex) % storageSize;
        
        if(storagebuffer[index] != 0x00)
            transmitData(storagebuffer[index]);
    }

    transmitData(0x00);
    transmitData(buffercode);
    transmitData(0x00);

    memset(storagebuffer, 0, TEMPERATURE_STORAGE_SIZE);
}

void handleInstructions(void) {
    uint8_t receivedData = receiveData();
    switch(receivedData) {
        case TEMPERATURE_CODE:            
            transmitBufferData(TEMPERATURE_CODE, temperatures, TEMPERATURE_STORAGE_SIZE, temperature_head_index);
            break;
        case LIGHT_CODE:
            transmitBufferData(LIGHT_CODE, lights, LIGHT_STORAGE_SIZE, lights_head_index);
            break;
    }
}
