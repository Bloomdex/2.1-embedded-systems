#include <avr/io.h>

#define F_CPU 16E6	// Frequency definition for delay.h
#include <util/delay.h>

#include "UART.h"
#include "sensors.h"
#include "rollerShutter.h"
#include "portManipulator.h"
#include "serial.h"

void setup(void) {
	DDRB = 0xFF;
	
	initUART();
	initPortManipulator();
	
	_delay_ms(1000);
}

void loop() {
	int8_t temperatureReading = (int8_t)getTemperature();
	int8_t lightReading = (int8_t)getLightIntensity();

	if((int8_t)getTempReadingValid())
		addTemperatureToBuffer(temperatureReading);
	
	if((int8_t)getLightReadingValid())
		addLightToBuffer(lightReading);

	handleInstructions();
}

int main (void)
{
	setup();
	setRollerShutterMoving();
	
	while(1) {
		loop();
		rollerShutterAnimate();
	}
	
	return 0;
}
