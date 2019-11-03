#ifndef PORTMANIPULATOR_H_
#define PORTMANIPULATOR_H_

#include <avr/io.h>

void initPortManipulator();
int analogRead(uint8_t pin);
void digitalWrite(volatile uint8_t *port, uint8_t mask, uint8_t value);

#endif /* PORTMANIPULATOR_H_ */
