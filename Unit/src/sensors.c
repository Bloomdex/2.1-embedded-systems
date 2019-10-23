#include "portManipulator.h"


float getTemperature() {
	// Get reading from temperature sensor, ADC PIN 0
	int temperatureInput = analogRead(0);
	
	float temperature = (float)temperatureInput / 1024;	// Find percentage of input reading: ranging from 0 to 1023
	temperature = temperature * 5;						// Multiply by 5V to get voltage
	temperature = temperature - 0.5;					// Subtract the offset which is 0.5V
	temperature = temperature * 100;					// Convert to degrees
	
	return temperature;
}
