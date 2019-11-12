#include "serial.h"

#include <avr/io.h>
#include <string.h>
#include "UART.h"
#include "sensors.h"
#include "rollerShutter.h"
#include "userPreferenceHandler.h"

// Queue for received data.
volatile unsigned char received_data[RECEIVED_DATA_SIZE];
volatile uint8_t received_data_index = 0;

// Current real Data reading.
int8_t currentTemperatureReading = INVALID_READING_VALUE;
int8_t currentLightReading = INVALID_READING_VALUE;
int8_t currentDistanceReading = INVALID_READING_VALUE;

// Buffer for measured temperatures.
int8_t temperatures[TEMPERATURE_STORAGE_SIZE];
uint8_t temperature_head_index = 0;

// Buffer for measured light intensity.
int8_t lights[LIGHT_STORAGE_SIZE];
uint8_t lights_head_index = 0;

uint8_t distances[DISTANCE_STORAGE_SIZE];
uint8_t distances_head_index = 0;

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

void addDistanceToBuffer(uint8_t value)
{
    distances[distances_head_index] = value;
    distances_head_index = (distances_head_index + 1) % DISTANCE_STORAGE_SIZE;
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
    transmitData(0x0A);
}

void transmitBufferDataUint(char buffercode, uint8_t storagebuffer[], unsigned char storageSize, int8_t bufferIndex)
{
    transmitData(buffercode);

    for (uint8_t i = 0; i < storageSize; i++)
    {
        uint8_t index = (i + bufferIndex) % storageSize;

        if (storagebuffer[index] != 0x00)
            transmitData(storagebuffer[index]);
    }

    transmitData(0x00);
    transmitData(buffercode);
    transmitData(0x0A);
}

void transmitModuleStatus() {
    transmitData(CODE_MODULE_STATUS);

    transmitData(getShutterForcedState());
    transmitData(getRollerShutterState());
    transmitData(currentTemperatureReading != INVALID_READING_VALUE);
    transmitData(currentLightReading != INVALID_READING_VALUE);
    transmitData(currentDistanceReading != INVALID_READING_VALUE);

    transmitData(0x00);
    transmitData(CODE_MODULE_STATUS);
    transmitData(0x0A);
}

// Handles possible instruction in the received_data queue.
void handleInstructions(void) {
    //Loops over every data point in received_data
    for(uint8_t i = 0; i < RECEIVED_DATA_SIZE; i++) {
        uint8_t index = (i + received_data_index) % RECEIVED_DATA_SIZE;
        uint8_t value_index = (i + 1 + received_data_index) % RECEIVED_DATA_SIZE;

        // Checks if the current data in received_data is an instruction.
        switch(received_data[index]) {
            case CODE_TEMPERATURE:           
                transmitBufferData(CODE_TEMPERATURE, temperatures, TEMPERATURE_STORAGE_SIZE, temperature_head_index);
                memset(temperatures, 0, TEMPERATURE_STORAGE_SIZE);
                temperature_head_index = 0;
                break;
            case CODE_LIGHT:
                transmitBufferData(CODE_LIGHT, lights, LIGHT_STORAGE_SIZE, lights_head_index);
                memset(lights, 0, LIGHT_STORAGE_SIZE);
                lights_head_index = 0;
                break;
            case CODE_DISTANCE:
                transmitBufferDataUint(CODE_DISTANCE, distances, DISTANCE_STORAGE_SIZE, distances_head_index);
                memset(distances, 0, DISTANCE_STORAGE_SIZE);
                distances_head_index = 0;
                break;
            case CODE_ROLLERSHUTTER_FORCE_CLOSE:
                setShutterForceClosed();
                break;
            case CODE_ROLLERSHUTTER_FORCE_OPEN:
                setShutterForceOpened();
                break;
            case CODE_ROLLERSHUTTER_FREE:
                setShutterFreed();
                break;
            case CODE_MODULE_STATUS:
                transmitModuleStatus();
                break;
            case CODE_PREFERRED_TEMPERATURE:
                setUserTempPreference(received_data[value_index]);
                received_data[value_index] = 0;
                break;
            case CODE_PREFERRED_LIGHT:
                setUserLightPreference(received_data[value_index]);
                received_data[value_index] = 0;
                break;
            case CODE_PREFERRED_MIN_SHUTTER:
                setUserShutterMinPreference(received_data[value_index]);
                received_data[value_index] = 0;
                break;
            case CODE_PREFERRED_MAX_SHUTTER:
                setUserShutterMaxPreference(received_data[value_index]);
                received_data[value_index] = 0;
                break;
        }

        // Resets the index of the previous value to 0. 
        received_data[index] = 0;
    }

    // Resets the index of the queue back to the front of queue
    received_data_index = 0;
}
