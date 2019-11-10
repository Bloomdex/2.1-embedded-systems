#include "dataHandler.h"

#include <avr/io.h>

#include "sensors.h"

int8_t temperature_pool[TEMPERATURE_POOL_STORAGE_SIZE];
uint8_t temperature_pool_head_index = 0;
int8_t lightIntensity_pool[LIGHTINTENSITY_POOL_STORAGE_SIZE];
uint8_t lightIntensity_pool_head_index = 0;


void updateSensorData(int8_t currentTemperature, int8_t currentLightIntensity) {
	// Check for invalid values
	if(currentTemperature == INVALID_READING_VALUE)
		currentTemperature = 0;
	if(currentLightIntensity == INVALID_READING_VALUE)
		currentLightIntensity = 0;
	
	// Update our pools
	temperature_pool[temperature_pool_head_index] = currentTemperature;
	temperature_pool_head_index = (temperature_pool_head_index + 1) % TEMPERATURE_POOL_STORAGE_SIZE;
	
	lightIntensity_pool[lightIntensity_pool_head_index] = currentLightIntensity;
	lightIntensity_pool_head_index = (lightIntensity_pool_head_index + 1) % LIGHTINTENSITY_POOL_STORAGE_SIZE;
}

int8_t getTemperatureMod() {
	return getMode(temperature_pool, TEMPERATURE_POOL_STORAGE_SIZE);
}

int8_t getLightIntensityMod() {
	return getMode(lightIntensity_pool, LIGHTINTENSITY_POOL_STORAGE_SIZE);
}

int8_t getMode(int8_t array[], uint8_t size) {
	int8_t mode = 0;
	uint8_t maxCount = 0;

	for (uint8_t i = 0; i < size; ++i) {
		uint8_t count = 0;
		
		for (uint8_t j = 0; j < size; ++j) {
			if (array[j] == array[i])
				count += 1;
		}
		
		if (count > maxCount) {
			maxCount = count;
			mode = array[i];
		}
	}

	return mode;
}
