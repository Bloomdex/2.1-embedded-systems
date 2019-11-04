#include <avr/io.h>
#include <stdint.h>
#define F_CPU 16E6
#include <util/delay.h>

#include "ledKeyUnit.h"

#define HIGH 0x1
#define LOW  0x0

const uint8_t data = 7;
const uint8_t clock = 6;
const uint8_t strobe = 5;


void initLedKeyUnit() {
	sendCommand(0x89);  // activate and set brightness to medium
}


// read value from pin
int read(uint8_t pin) {
	// if pin set in port
	return PIND & _BV(pin) ? HIGH : LOW;
}

// write value to pin
void write(uint8_t pin, uint8_t val) {
	if (val == LOW)
		PORTD &= ~(_BV(pin)); // clear bit
	else
		PORTD |= _BV(pin); // set bit
}

// shift out value to data
void shiftOut (uint8_t val) {
	uint8_t i;
	for (i = 0; i < 8; i++)  {
		write(clock, LOW);   // bit valid on rising edge
		write(data, val & 1 ? HIGH : LOW); // lsb first
		val = val >> 1;
		write(clock, HIGH);
	}
}

uint8_t shiftIn() {
	uint8_t value = 0;
	uint8_t i;

	DDRD &= ~(_BV(data)); // clear bit, direction = input
	
	for (i = 0; i < 8; ++i) {
		write(clock, LOW);   // bit valid on rising edge
		value = value | (read(data) << i); // lsb first
		write(clock, HIGH);
	}
	
	DDRD |= _BV(data); // set bit, direction = output
	
	return value;
}

void sendCommand(uint8_t value) {
	write(strobe, LOW);
	shiftOut(value);
	write(strobe, HIGH);
}


// Get the length of any int up to 32 bits
int getIntLength (int value) {
	// Source: https://stackoverflow.com/questions/3068397/finding-the-length-of-an-integer-in-c
	int l = !value;
	
	while (value) {
		l++; value/=10;
	}
	
	return l;
}

// Fills an array with a given integer until the desired size has been reached
// (We can't return arrays in C so treat this as a function with return)
void fillArrayWithGiven(uint8_t result[], int sizeCurrent, int sizeToFill, int given) {
	if(sizeToFill - sizeCurrent > 0) {
		for (int i = sizeCurrent; i < sizeToFill; i++) {
			result[i] = given;
		}
	}
}

// Takes an array, size and value and fills the array with digits based on the value
// (We can't return arrays in C so treat this as a function with return)
void valToDigitsInArray(uint8_t result[], uint8_t maxArraySize, int val) {
	uint8_t digits[] = { 0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f };	// Digits 0 to 9
	uint8_t digitNegative = 0x40;
	uint8_t digitEmpty = 0x00;
	
	uint8_t negativeNumber = 0;
	
	int currentArraySize = getIntLength(val);	// Get the size the array should be
	
	// Check if given value is negative and do actions based on this
	if(val < 0) {
		negativeNumber = 1;		// Set the negativeNumber bool to true
		currentArraySize += 1;	// Add one to the size of the array for the negative sign
		val = -val;				// Convert the value to positive
	}
	
	// Fill the array with the integer digits and negative digit if needed
	uint8_t val_copy = val;
	for (uint8_t position = currentArraySize - 1; position < currentArraySize; position--) {
		if(negativeNumber == 1 && position == 0)
			result[position] = digitNegative;	// Add negative digit to array
		else {
			// Add digit to array
			uint8_t val_part = val_copy % 10;		// Get the last value of the integer
			result[position] = digits[val_part];	// Convert the last value to a digit for the led key unit
			val_copy = val_copy / 10;				// Update the integer so the last value is now gone
		}
	}
	
	// Fill the rest of the array with the empty digit
	fillArrayWithGiven(result, currentArraySize, maxArraySize, digitEmpty);
}

// Append two arrays that have a fixed size of 8 digits for the led key unit
// (We can't return arrays in C so treat this as a function with return)
void appendTwoLedKeyUnitArrays(uint8_t result[], uint8_t array1[], uint8_t arraySize1, uint8_t array2[], uint8_t arraySize2) {
	for (uint8_t i = 0; i < arraySize1; i++)
		result[i] = array1[i];
		
	for (uint8_t i = 0; i < arraySize2; i++)
		result[i + arraySize1] = array2[i];
}


uint8_t readButtons() {
	uint8_t buttons = 0;
	write(strobe, LOW);
	shiftOut(0x42); // key scan (read buttons)

	DDRD &= ~(_BV(data)); // clear bit, direction = input

	for (uint8_t i = 0; i < 4; i++) {
		uint8_t v = shiftIn() << i;
		buttons |= v;
	}

	DDRD |= _BV(data); // set bit, direction = output
	write(strobe, HIGH);
	return buttons;
}


enum state {displayingValues, changingValues};
enum state ledKeyUnitState = displayingValues;

#include "UART.h"

void updateLedKeyUnit(int8_t tempVal, uint8_t lightVal) {
	//if(readButtons() != 0)
	//	ledKeyUnitState = changingValues;
	//else
	//	ledKeyUnitState = displayingValues;
	
	
	//uint8_t testArr[8] = { 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40 };
		
	if (ledKeyUnitState == displayingValues)
		updateDisplayingValues(tempVal, lightVal);
	//else if (ledKeyUnitState == changingValues)
	//	sendArrayToLedKeyUnit(testArr);
}

uint8_t temperatureDigitArray[4];
uint8_t lightIntensityDigitArray[4];
uint8_t finalDigitArray[8];

void updateDisplayingValues(int8_t tempVal, uint8_t lightVal) {
	// Setup
	sendCommand(0x40);	// auto-increment address
	write(strobe, LOW);
	shiftOut(0xc0);		// set starting address = 0
	
	// Compose temperature digit array
	valToDigitsInArray(temperatureDigitArray, 4, tempVal);

	// Compose lightIntensity digit array
	valToDigitsInArray(lightIntensityDigitArray, 4, lightVal);
	
	// Compose array for display
	appendTwoLedKeyUnitArrays(finalDigitArray, temperatureDigitArray, 4, lightIntensityDigitArray, 4);

	sendArrayToLedKeyUnit(finalDigitArray);
}

void sendArrayToLedKeyUnit(uint8_t array[]) {
	// Send the values to the unit's display
	for(uint8_t position = 0; position < 8; position++) {
		shiftOut(array[position]);
		shiftOut(0x00);
	}
}
