#include <avr/io.h>

#define UBBRVAL 51


void initUART(void) {
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	
	// disable U2X mode
	UCSR0A = 0;
	
	// enable transmitter and receiver
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}

// Transmit data (to Realterm)
void transmitData(int data) {
	// Wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	
	// send the data
	UDR0 = data;
}

// Receive data (from Realterm)
unsigned char receiveData(void) {
	// Wait for data to be received
	while( !( UCSR0A & (1<<RXC0) ) );
	
	// Get and return received data from buffer
	return UDR0;
}
