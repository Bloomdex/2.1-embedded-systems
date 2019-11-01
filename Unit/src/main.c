#include <avr/io.h>
#include <avr/interrupt.h>

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
	
	// Enables interrupts by setting the global interrupt mask
	sei();

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

//Interrupt Service Routine for when data is received.
ISR(USART_RX_vect)
{
	//Checks if any data has been sent.
	if (UCSR0A & (1<<RXC0)) {
		unsigned char data = UDR0;

		//Stores the data in the received_data queue, so it can handle the received data at a later moment.
    	received_data[received_data_index] = data;
    	received_data_index = (received_data_index + 1) % RECEIVED_DATA_SIZE;
	}
}
