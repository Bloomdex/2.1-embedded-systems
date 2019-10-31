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
  if((int8_t)getTempReadingValid()) {
    addTemperatureToBuffer((int8_t)getTemperature());
  }
  
  if((int8_t)getLightReadingValid()) {
    addLightToBuffer((int8_t)getLightIntensity());
  }

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
