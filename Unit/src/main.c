#include <avr/io.h>

#define F_CPU 16E6	// Frequency definition for delay.h
#include <util/delay.h>

#include "UART.h"
#include "sensors.h"
#include "rollerShutter.h"
#include "portManipulator.h"


void setup(void) {
	DDRB = 0xFF;
	
	initUART();
	initPortManipulator();
	

	_delay_ms(1000);
}

void loop() {
	int8_t temperature = (int8_t)getTemperature();
	int8_t lightIntensity = (int8_t)getLightIntensity();
	
	transmitData(temperature);
	transmitData(lightIntensity);
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
