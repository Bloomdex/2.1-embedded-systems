#ifndef LEDKEYUNIT_H_
#define LEDKEYUNIT_H_

void initLedKeyUnit();

int read(uint8_t pin);
void write(uint8_t pin, uint8_t val);
void shiftOut (uint8_t val);
uint8_t shiftIn();
void sendCommand(uint8_t value);

int getIntLength (int value);
void fillArrayWithGiven(uint8_t result[], int sizeCurrent, int sizeToFill, int given);
void valToDigitsInArray(uint8_t result[], uint8_t maxArraySize, int val);
void appendTwoLedKeyUnitArrays(uint8_t result[], uint8_t array1[], uint8_t arraySize1, uint8_t array2[], uint8_t arraySize2);

uint8_t checkIfPresent();

uint8_t readButtons();

void updateButtonReadings(uint8_t buttonReadings);
void updateLedKeyUnit(int8_t tempVal, uint8_t lightVal);

void updateChangingValues(int8_t valueToAdd, int8_t tempVal, uint8_t lightVal);
void updateDisplayingValues(int8_t tempVal, uint8_t lightVal);

void sendArrayToLedKeyUnit(uint8_t array[]);

#endif /* LEDKEYUNIT_H_ */
