#include <avr/io.h>

#define F_CPU 16E6	// Frequency definition for delay.h
#include <util/delay.h>

#include "UART.h"
#include "sensors.h"
#include "rollerShutter.h"


void setup(void) {
	DDRB = 0xFF;
	
	initUART();
	
	
	// Source: https://medium.com/@jrejaud/arduino-to-avr-c-reference-guide-7d113b4309f7
	// 16Mhz / 128 = 125kHz ADC reference clock
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));
	
	// Voltage reference from AVcc (5V on ATMega328p)
	ADMUX |= (1<<REFS0);
	
	ADCSRA |= (1<<ADEN);	// Turn on ADC
	ADCSRA |= (1<<ADSC);	// Do a preliminary conversion
	

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
