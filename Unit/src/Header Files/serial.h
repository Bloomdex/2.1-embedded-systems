#ifndef SERIAL_H_
#define SERIAL_H_

#include <avr/io.h>

// Total received data to keep queued.
#define RECEIVED_DATA_SIZE 8
extern volatile unsigned char received_data[];
extern volatile uint8_t received_data_index;

// Instruction Codes
#define TEMPERATURE_CODE 0xFE
#define LIGHT_CODE 0xFD

// Storage size of measurement buffers
#define TEMPERATURE_STORAGE_SIZE 255
#define LIGHT_STORAGE_SIZE 255

void addTemperatureToBuffer(int8_t value);
void addLightToBuffer(int8_t value);
void transmitBufferData(char buffercode, int8_t storagebuffer[], unsigned char storageSize, int8_t bufferIndex);
void handleInstructions();

#endif
