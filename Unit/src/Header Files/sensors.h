#ifndef SENSORS_H_
#define SENSORS_H_

#include <avr/io.h>

#define INVALID_READING_VALUE -128

float getTemperature();
float getLightIntensity();
uint8_t getDistance(void);

#endif /* SENSORS_H_ */
