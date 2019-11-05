#ifndef EEPROM_H_
#define EEPROM_H_

#include <avr/io.h>

void eepromWrite_byte (uint8_t address, uint8_t data);
uint8_t eepromRead_byte (uint8_t address);

#endif /* EEPROM_H_ */