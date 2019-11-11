#include "sensors.h"
#include "portManipulator.h"
#include "ultrasonic.h"


float getTemperature() {
	// Get reading from temperature sensor, ADC PIN 0
	int temperatureSensorInput = analogRead(0);
	
	// Set tempReadingValid to tell third parties if the reading is usable
	if (temperatureSensorInput == 0)
		return INVALID_READING_VALUE;
	
	float temperature = (float)temperatureSensorInput / 1024;	// Find percentage of input reading: ranging from 0 to 1023
	
	temperature = temperature * 5;		// Multiply by 5V to get voltage
	temperature = temperature - 0.5;	// Subtract the offset which is 0.5V
	temperature = temperature * 100;	// Convert to degrees
	
	return temperature;
}

float getLightIntensity() {
	// Get reading from light sensor, ADC PIN 1
	int lightSensorInput = analogRead(1);
	
	// Set lightReadingValid to tell third parties if the reading is usable
	if (lightSensorInput == 0)
		return INVALID_READING_VALUE;

	float lightIntensity = (float)lightSensorInput / 10;	// Divide intensity value by 10 to stay inside 127 range of int8
	
	return lightIntensity;
}

float getDistance(void)
{
	float distance = measure_distance();
	
	// if distance is -1 return invalid, else return distance
	return distance >= 0 ? distance : INVALID_READING_VALUE;
}
