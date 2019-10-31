#ifndef SERIAL_H_
#define SERIAL_H_

// Instruction Codes
#define TEMPERATURE_CODE 0xFE
#define LIGHT_CODE 0xFD

// Storage size of measurement buffers
#define TEMPERATURE_STORAGE_SIZE 255
#define LIGHT_STORAGE_SIZE 255

void addTemperatureToBuffer(int8_t value);
void addLightToBuffer(int8_t value);
void handleInstructions();

#endif
