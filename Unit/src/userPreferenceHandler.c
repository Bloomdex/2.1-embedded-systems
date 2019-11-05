#include "userPreferenceHandler.h"
#include "eeprom.h"

int8_t prefferedTemperature = 20;
int8_t prefferedLightIntensity = 40;


void initUserPreferenceHandler() {
	int8_t savedPrefferedTemperature = (int8_t)eepromRead_byte(0);
	int8_t savedPrefferedLightIntensity = (int8_t)eepromRead_byte(1);
	
	// Check if the saved values are genuine since return -1 when they're not
	if(savedPrefferedTemperature != -1)
		prefferedTemperature = savedPrefferedTemperature;
	
	if(savedPrefferedLightIntensity != -1)
		prefferedLightIntensity = savedPrefferedLightIntensity;
}

void setUserTempPreference(int8_t newPrefferedTemperature) {
	prefferedTemperature = newPrefferedTemperature;
	
	eepromWrite_byte(0, prefferedTemperature);
}
int8_t getUserTempPreference() {
	return prefferedTemperature;
}

void setUserLightPreference(int8_t newPrefferedLightIntensity) {
	prefferedLightIntensity = newPrefferedLightIntensity;
	
	eepromWrite_byte(1, prefferedLightIntensity);
}
int8_t getUserLightPreference() {
	return prefferedLightIntensity;
}
