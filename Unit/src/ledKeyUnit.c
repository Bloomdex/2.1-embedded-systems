#include <avr/io.h>
#include <stdint.h>
#define F_CPU 16E6
#include <util/delay.h>

#include "ledKeyUnit.h"
#include "userPreferenceHandler.h"

#define HIGH 0x1
#define LOW  0x0
#define LEDKEYLOCKTICKS 5

const uint8_t data = 5;
const uint8_t clock = 6;
const uint8_t strobe = 7;

uint8_t currentButtonReadings = 0;
uint8_t lockDisplayUpdate = 0;
uint8_t lockTickCount = 0;

enum updateState {displayValues, changeValuesTemp, changeValuesLight};
enum updateState currentUpdateState = displayValues;


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


void updateButtonReadings(uint8_t buttonReadings) {
	// Check if reading is equal to one of the valid readings
	uint8_t validReadings[4] = {1, 2, 16, 32};
	uint8_t readingValid = 0;	
	
	for (uint8_t i = 0; i < 4; i++) {
		if(buttonReadings == validReadings[i])
			currentButtonReadings = buttonReadings;
	}
}

void updateLedKeyUnit(int8_t tempVal, uint8_t lightVal) {
	transmitData(lockDisplayUpdate);
	transmitData(lockTickCount);
	
	if(currentButtonReadings != 0) {	// If a button is pressed or it was locked previously
		if(currentButtonReadings == 1 || currentButtonReadings == 2)
			currentUpdateState = changeValuesTemp;
		else if(currentButtonReadings == 16 || currentButtonReadings == 32)
			currentUpdateState = changeValuesLight;
		
		// Make sure the display stays locked for x ticks
		lockTickCount = 0;
		lockDisplayUpdate = 1;
	}
	else if(lockDisplayUpdate == 0)
		currentUpdateState = displayValues;
		
	if(currentUpdateState == changeValuesTemp || currentUpdateState == changeValuesLight) {
		// Update the changeValues state
		lockTickCount += 1;	
		
		if(lockTickCount >= LEDKEYLOCKTICKS)
			lockDisplayUpdate = 0;
		
		// Actions for changeValues state
		if(currentUpdateState == changeValuesTemp) {
			if(currentButtonReadings == 1)
				updateChangingValues(-1);
			else if(currentButtonReadings == 2)
				updateChangingValues(1);
		}
		else if(currentUpdateState == changeValuesLight) {
			if(currentButtonReadings == 16)
			updateChangingValues(-1);
			else if(currentButtonReadings == 32)
			updateChangingValues(1);
		}
		
		currentButtonReadings = 0;	// Reset out buttons so this doesn't fire again without pressing
	}
	else if(currentUpdateState == displayValues)
		updateDisplayingValues(tempVal, lightVal);
}


void updateChangingValues(int8_t valueToAdd) {
	uint8_t finalDigitArray[8];
	
	if(currentUpdateState == changeValuesTemp) {
		// Compose indicator digit array
		uint8_t indicatorDigitArray[4] = { 0x78, 0x79, 0x37, 0x73 };	// Temp
			
		// Update value by applying changes
		int8_t newTempPreference = getUserTempPreference() + valueToAdd;
		if(newTempPreference >= 0 && newTempPreference <= 100)
			setUserTempPreference(newTempPreference);
		
		// Compose lightPreference digit array
		uint8_t changedValueDigitArray[4];
		valToDigitsInArray(changedValueDigitArray, 4, getUserTempPreference());
		
		// Compose array for display
		appendTwoLedKeyUnitArrays(finalDigitArray, indicatorDigitArray, 4, changedValueDigitArray, 4);
	}
	else if(currentUpdateState == changeValuesLight) {
		// Compose indicator digit array
		uint8_t indicatorDigitArray[5] = { 0x38, 0x10, 0x3D, 0x74, 0x78 }; // Light
			
		// Update value by applying changes
		int8_t newLightPreference = getUserLightPreference() + valueToAdd;
		setUserLightPreference(newLightPreference);
		
		// Compose lightPreference digit array
		uint8_t changedValueDigitArray[3];
		if(newLightPreference >= 0 && newLightPreference <= 100)
			valToDigitsInArray(changedValueDigitArray, 3, getUserLightPreference());
		
		// Compose array for display
		appendTwoLedKeyUnitArrays(finalDigitArray, indicatorDigitArray, 5, changedValueDigitArray, 3);
	}
	
	sendArrayToLedKeyUnit(finalDigitArray);
}

void updateDisplayingValues(int8_t tempVal, uint8_t lightVal) {
	uint8_t temperatureDigitArray[4];
	uint8_t lightIntensityDigitArray[4];
	uint8_t finalDigitArray[8];
	
	// Compose temperature digit array
	valToDigitsInArray(temperatureDigitArray, 4, tempVal);

	// Compose lightIntensity digit array
	valToDigitsInArray(lightIntensityDigitArray, 4, lightVal);
	
	// Compose array for display
	appendTwoLedKeyUnitArrays(finalDigitArray, temperatureDigitArray, 4, lightIntensityDigitArray, 4);

	sendArrayToLedKeyUnit(finalDigitArray);
}


void sendArrayToLedKeyUnit(uint8_t array[]) {
	// Setup
	sendCommand(0x40);	// auto-increment address
	write(strobe, LOW);
	shiftOut(0xc0);		// set starting address = 0
	
	// Send the values to the unit's display
	for(uint8_t position = 0; position < 8; position++) {
		shiftOut(array[position]);
		shiftOut(0x00);
	}
	
	write(strobe, HIGH);
}
