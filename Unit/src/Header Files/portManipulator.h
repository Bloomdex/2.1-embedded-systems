#include <avr/io.h>

#ifndef PORTMANIPULATOR_H_
#define PORTMANIPULATOR_H_

int analogRead(int pin);
void digitalWrite(volatile uint8_t *port, uint8_t mask, uint8_t value);

#endif /* PORTMANIPULATOR_H_ */
