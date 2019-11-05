#include <avr/io.h>
#include <avr/eeprom.h>

#include "eeprom.h"

#define EEPROM_SIZE 1024


void eepromWrite_byte (uint8_t address, uint8_t data) {
	if(address >= EEPROM_SIZE)
		address = 0;
	
	eeprom_update_byte((uint8_t*)address, data);
}

uint8_t eepromRead_byte (uint8_t address) {
	return eeprom_read_byte((uint8_t*)address);
}
