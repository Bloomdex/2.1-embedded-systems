#include "userPreferenceHandler.h"
#include "eeprom.h"

#define PREFERRED_TEMPERATURE_ADDRESS 0
#define PREFERRED_LIGHT_ADDRESS 1

int8_t prefferedTemperature = 20;
int8_t prefferedLightIntensity = 40;


void initUserPreferenceHandler() {
	int8_t savedPrefferedTemperature = (int8_t)eepromRead_byte(PREFERRED_TEMPERATURE_ADDRESS);
	int8_t savedPrefferedLightIntensity = (int8_t)eepromRead_byte(PREFERRED_LIGHT_ADDRESS);
	
	// Check if the saved values are genuine since return -1 when they're not
	if(savedPrefferedTemperature != -1)
		prefferedTemperature = savedPrefferedTemperature;
	
	if(savedPrefferedLightIntensity != -1)
		prefferedLightIntensity = savedPrefferedLightIntensity;
}

void setUserTempPreference(int8_t newPrefferedTemperature) {
	prefferedTemperature = newPrefferedTemperature;
	
	eepromWrite_byte(PREFERRED_TEMPERATURE_ADDRESS, prefferedTemperature);
}
int8_t getUserTempPreference() {
	return prefferedTemperature;
}

void setUserLightPreference(int8_t newPrefferedLightIntensity) {
	prefferedLightIntensity = newPrefferedLightIntensity;
	
	eepromWrite_byte(PREFERRED_LIGHT_ADDRESS, prefferedLightIntensity);
}
int8_t getUserLightPreference() {
	return prefferedLightIntensity;
}
