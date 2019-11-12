#ifndef SERIAL_H_
#define SERIAL_H_

#include <avr/io.h>

// Total received data to keep queued.
#define RECEIVED_DATA_SIZE 16
extern volatile unsigned char received_data[];
extern volatile uint8_t received_data_index;

extern int8_t currentTemperatureReading;
extern int8_t currentLightReading;
extern int8_t currentDistanceReading;

// Instruction Codes - Sensor data
#define CODE_TEMPERATURE 0xFE
#define CODE_LIGHT 0xFD
#define CODE_DISTANCE 0xF6

//Instruction Codes - RollerShutter
#define CODE_ROLLERSHUTTER_FORCE_CLOSE 0xFC
#define CODE_ROLLERSHUTTER_FORCE_OPEN 0xFB
#define CODE_ROLLERSHUTTER_FREE 0xFA

//Instruction Codes - Module Status
#define CODE_MODULE_STATUS 0xF9

//Instruction Codes - Set Preferred Settings
#define CODE_PREFERRED_TEMPERATURE 0xF8
#define CODE_PREFERRED_LIGHT 0xF7
#define CODE_PREFERRED_MAX_SHUTTER 0xF5
#define CODE_PREFERRED_MIN_SHUTTER 0xF4

// Storage size of measurement buffers
#define TEMPERATURE_STORAGE_SIZE 255
#define LIGHT_STORAGE_SIZE 255
#define DISTANCE_STORAGE_SIZE 255

void addTemperatureToBuffer(int8_t value);
void addLightToBuffer(int8_t value);
void addDistanceToBuffer(uint8_t value);
void transmitBufferData(char buffercode, int8_t storagebuffer[], unsigned char storageSize, int8_t bufferIndex);
void transmitBufferDataUint(char buffercode, uint8_t storagebuffer[], unsigned char storageSize, int8_t bufferIndex);
void transmitModuleStatus();
void handleInstructions();

#endif
