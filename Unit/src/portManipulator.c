#include <avr/io.h>


// Read analog pins
int analogRead(uint8_t pin) {
	// Source: https://medium.com/@jrejaud/arduino-to-avr-c-reference-guide-7d113b4309f7
	ADMUX &= 0xF0;    // Clear previously read channel
	ADMUX |= pin;    // Define new ADC Channel to read, analog pins 0 to 5 on ATMega328p
	
	ADCSRA |= (1<<ADSC);    // New Conversion
	ADCSRA |= (1<<ADSC);    // Do a preliminary conversion
	
	// Wait until conversion is finished
	while(ADCSRA & (1<<ADSC));
	
	// Return ADC value
	return ADCW;
}

// Write to a set of masked pins
void digitalWrite(char port, uint8_t mask, uint8_t value) {
	if (port == 'B') {
		PORTB = (PORTB & ~mask) | (value & mask);
	}
	else if (port == 'D') {
		PORTD = (PORTD & ~mask) | (value & mask);
	}
}
