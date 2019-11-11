#include "userPreferenceHandler.h"
#include "eeprom.h"

#define PREFERRED_TEMPERATURE_ADDRESS 0
#define PREFERRED_LIGHT_ADDRESS 1
#define PREFERED_MAX_SHUTTER_ADDRESS 2
#define PREFERED_MIN_SHUTTER_ADDRESS 3

int8_t prefferedTemperature = 20;
int8_t prefferedLightIntensity = 40;
int8_t preferedMaxShutter = 160;
int8_t preferedMinShutter = 20;


void initUserPreferenceHandler() {
	int8_t savedPrefferedTemperature = (int8_t)eepromRead_byte(PREFERRED_TEMPERATURE_ADDRESS);
	int8_t savedPrefferedLightIntensity = (int8_t)eepromRead_byte(PREFERRED_LIGHT_ADDRESS);
	int8_t savedPreferedMaxShutter = (int8_t)eepromRead_byte(PREFERED_MAX_SHUTTER_ADDRESS);
	int8_t savedPreferedMinShutter = (int8_t)eepromRead_byte(PREFERED_MIN_SHUTTER_ADDRESS);
	
	// Check if the saved values are genuine since eeprom returns -1 when they're not
	if(savedPrefferedTemperature != -1)
		prefferedTemperature = savedPrefferedTemperature;
	
	if(savedPrefferedLightIntensity != -1)
		prefferedLightIntensity = savedPrefferedLightIntensity;

	if (savedPreferedMaxShutter != -1)
		preferedMaxShutter = savedPreferedMaxShutter;
	
	if (savedPreferedMinShutter != -1)
		preferedMinShutter = savedPreferedMinShutter;
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

void setUserShutterMaxPreference(int8_t newPreferedMaxShutter)
{
	preferedMaxShutter = newPreferedMaxShutter;
	
	eepromWrite_byte(PREFERED_MAX_SHUTTER_ADDRESS, preferedMaxShutter);
}

void setUserShutterMinPreference(int8_t newPreferedMinShutter)
{
	preferedMinShutter = newPreferedMinShutter;

	eepromWrite_byte(PREFERED_MIN_SHUTTER_ADDRESS, preferedMinShutter);
}

int8_t getUserMaxShutterPreference()
{
	return preferedMaxShutter;
}

int8_t getUserMinShutterPreference()
{
	return preferedMinShutter;
}
